from pathlib import Path
from lxml import etree

PROJECT_ROOT = Path(__file__).resolve().parents[1]
XML_PATH = PROJECT_ROOT / "data" / "commerce.xml"
XSL_PATH = PROJECT_ROOT / "transforms" / "products_to_html.xsl"
OUTPUT_PATH = PROJECT_ROOT / "output" / "products.html"

OUTPUT_PATH.parent.mkdir(exist_ok=True)

xml_doc = etree.parse(str(XML_PATH))
xsl_doc = etree.parse(str(XSL_PATH))
transform = etree.XSLT(xsl_doc)
html_result = transform(xml_doc)

OUTPUT_PATH.write_text(str(html_result), encoding="utf-8")
print(f"Transformación generada en: {OUTPUT_PATH}")
