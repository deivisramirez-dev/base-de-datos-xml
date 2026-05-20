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
fragment = str(html_result)

OUTPUT_PATH.write_text(
    f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8"/>
    <title>Productos desde XML (XSLT)</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 32px; }}
        table {{ border-collapse: collapse; width: 100%; }}
        th, td {{ border: 1px solid #cccccc; padding: 8px; text-align: left; }}
        th {{ background: #eeeeee; }}
    </style>
</head>
<body>
{fragment}
</body>
</html>
""",
    encoding="utf-8",
)
print(f"Transformación generada en: {OUTPUT_PATH}")
