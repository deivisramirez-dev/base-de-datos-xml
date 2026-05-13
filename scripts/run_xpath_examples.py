from pathlib import Path
from lxml import etree

PROJECT_ROOT = Path(__file__).resolve().parents[1]
XML_PATH = PROJECT_ROOT / "data" / "commerce.xml"

def as_text(node):
    if isinstance(node, etree._Element):
        return etree.tostring(node, encoding="unicode", pretty_print=True).strip()
    return str(node)

queries = {
    "Todos los productos": "/commerce/products/product",
    "Nombres de clientes": "/commerce/customers/customer/full_name/text()",
    "Órdenes enviadas": "/commerce/orders/order[order_status='SHIPPED']",
    "Productos con precio mayor a 40": "/commerce/products/product[unit_price > 40]",
    "Ítems de la orden 5001": "/commerce/orders/order[@order_id='5001']/items/item",
}

xml_doc = etree.parse(str(XML_PATH))

for title, expression in queries.items():
    print("\n" + "=" * 80)
    print(title)
    print("XPath:", expression)
    results = xml_doc.xpath(expression)
    if not results:
        print("Sin resultados.")
    for result in results:
        print(as_text(result))
