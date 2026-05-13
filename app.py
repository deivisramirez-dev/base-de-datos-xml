import os
from decimal import Decimal, InvalidOperation
from pathlib import Path

from flask import Flask, Response, render_template
from lxml import etree

app = Flask(__name__)

PROJECT_ROOT = Path(__file__).resolve().parent
XML_PATH = PROJECT_ROOT / "data" / "commerce.xml"
XSD_PATH = PROJECT_ROOT / "data" / "commerce.xsd"
XSL_PATH = PROJECT_ROOT / "transforms" / "products_to_html.xsl"

_xml_doc: etree._ElementTree | None = None
_xsd_schema: etree.XMLSchema | None = None
_xslt_transform: etree.XSLT | None = None


def get_xml_doc() -> etree._ElementTree:
    global _xml_doc
    if _xml_doc is None:
        _xml_doc = etree.parse(str(XML_PATH))
    return _xml_doc


def get_xsd_schema() -> etree.XMLSchema:
    global _xsd_schema
    if _xsd_schema is None:
        xsd_doc = etree.parse(str(XSD_PATH))
        _xsd_schema = etree.XMLSchema(xsd_doc)
    return _xsd_schema


def get_xslt() -> etree.XSLT:
    global _xslt_transform
    if _xslt_transform is None:
        xsl_doc = etree.parse(str(XSL_PATH))
        _xslt_transform = etree.XSLT(xsl_doc)
    return _xslt_transform


def _text(elem: etree._Element, tag: str, default: str = "") -> str:
    node = elem.find(tag)
    if node is None or node.text is None:
        return default
    return node.text.strip()


def customer_by_id(tree: etree._ElementTree, customer_id: str) -> str:
    cid = str(customer_id).strip()
    if not cid:
        return "—"
    for node in tree.xpath(f"/commerce/customers/customer[@customer_id='{cid}']"):
        return _text(node, "full_name", "—")
    return "—"


def store_by_id(tree: etree._ElementTree, store_id: str) -> str:
    sid = str(store_id).strip()
    if not sid:
        return "—"
    for node in tree.xpath(f"/commerce/stores/store[@store_id='{sid}']"):
        return _text(node, "store_name", "—")
    return "—"


def product_name_by_id(tree: etree._ElementTree, product_id: str) -> str:
    pid = str(product_id).strip()
    if not pid:
        return "—"
    for node in tree.xpath(f"/commerce/products/product[@product_id='{pid}']"):
        return _text(node, "product_name", "—")
    return "—"


def order_total(order_el: etree._Element) -> str:
    total = Decimal("0")
    container = order_el.find("items")
    if container is None:
        return f"{total:.2f}"
    for item in container.findall("item"):
        try:
            price = Decimal(_text(item, "unit_price", "0"))
            qty = int(_text(item, "quantity", "0") or "0")
        except (InvalidOperation, ValueError):
            continue
        total += price * qty
    return f"{total:.2f}"


def order_dict(tree: etree._ElementTree, order_el: etree._Element) -> dict:
    customer_id = _text(order_el, "customer_id")
    store_id = _text(order_el, "store_id")
    return {
        "id": order_el.get("order_id") or "",
        "datetime": _text(order_el, "order_datetime"),
        "customer": customer_by_id(tree, customer_id),
        "store": store_by_id(tree, store_id),
        "status": _text(order_el, "order_status"),
        "total": order_total(order_el),
    }


def order_detail_dict(tree: etree._ElementTree, order_el: etree._Element) -> dict:
    base = order_dict(tree, order_el)
    items: list[dict] = []
    container = order_el.find("items")
    if container is not None:
        for item in container.findall("item"):
            try:
                price = Decimal(_text(item, "unit_price", "0"))
                qty = int(_text(item, "quantity", "0") or "0")
            except (InvalidOperation, ValueError):
                price = Decimal("0")
                qty = 0
            subtotal = price * qty
            pid = _text(item, "product_id")
            items.append(
                {
                    "line_item_id": item.get("line_item_id") or "",
                    "product": product_name_by_id(tree, pid),
                    "unit_price": _text(item, "unit_price"),
                    "quantity": str(qty),
                    "subtotal": f"{subtotal:.2f}",
                    "shipment_id": _text(item, "shipment_id"),
                }
            )
    base["items"] = items
    return base


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/validate")
def validate():
    tree = get_xml_doc()
    schema = get_xsd_schema()
    is_valid = schema.validate(tree)
    errors = [f"Línea {err.line}: {err.message}" for err in schema.error_log]
    return render_template("validate.html", is_valid=is_valid, errors=errors)


@app.route("/products")
def products():
    tree = get_xml_doc()
    products_data = []
    for p in tree.xpath("/commerce/products/product"):
        products_data.append(
            {
                "id": p.get("product_id") or "",
                "name": _text(p, "product_name"),
                "unit_price": _text(p, "unit_price"),
                "details": _text(p, "product_details"),
            }
        )
    return render_template("products.html", products=products_data)


@app.route("/customers")
def customers():
    tree = get_xml_doc()
    customers_data = []
    for c in tree.xpath("/commerce/customers/customer"):
        customers_data.append(
            {
                "id": c.get("customer_id") or "",
                "full_name": _text(c, "full_name"),
                "email": _text(c, "email_address"),
            }
        )
    return render_template("customers.html", customers=customers_data)


@app.route("/orders")
def orders():
    tree = get_xml_doc()
    orders_data = [order_dict(tree, o) for o in tree.xpath("/commerce/orders/order")]
    return render_template("orders.html", orders=orders_data)


@app.route("/orders/<order_id>")
def order_detail(order_id: str):
    try:
        oid = str(int(order_id))
    except ValueError:
        return (
            render_template(
                "not_found.html",
                message="El identificador de la orden no es válido.",
            ),
            404,
        )
    tree = get_xml_doc()
    matches = tree.xpath(f"/commerce/orders/order[@order_id='{oid}']")
    if not matches:
        return (
            render_template(
                "not_found.html",
                message="No existe una orden con ese identificador.",
            ),
            404,
        )
    order = order_detail_dict(tree, matches[0])
    return render_template("order_detail.html", order=order)


@app.route("/inventory")
def inventory():
    tree = get_xml_doc()
    rows = []
    for inv in tree.xpath("/commerce/inventory/inventory_item"):
        sid = _text(inv, "store_id")
        pid = _text(inv, "product_id")
        rows.append(
            {
                "id": inv.get("inventory_id") or "",
                "store": store_by_id(tree, sid),
                "product": product_name_by_id(tree, pid),
                "available_units": _text(inv, "product_inventory"),
            }
        )
    return render_template("inventory.html", inventory=rows)


@app.route("/transform/products")
def transform_products():
    tree = get_xml_doc()
    transform = get_xslt()
    html_result = transform(tree)
    return Response(str(html_result), mimetype="text/html; charset=utf-8")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5000"))
    host = os.environ.get("HOST", "127.0.0.1")
    debug = os.environ.get("FLASK_DEBUG", "1").lower() in ("1", "true", "yes")
    app.run(host=host, port=port, debug=debug)
