from pathlib import Path
from lxml import etree

PROJECT_ROOT = Path(__file__).resolve().parents[1]
XML_PATH = PROJECT_ROOT / "data" / "commerce.xml"
XSD_PATH = PROJECT_ROOT / "data" / "commerce.xsd"

try:
    xml_doc = etree.parse(str(XML_PATH))
    xsd_doc = etree.parse(str(XSD_PATH))
    schema = etree.XMLSchema(xsd_doc)

    if schema.validate(xml_doc):
        print("El XML es válido según el XSD.")
    else:
        print("El XML NO es válido según el XSD.")
        for error in schema.error_log:
            print(f"Línea {error.line}: {error.message}")
except Exception as error:
    print("No se pudo ejecutar la validación.")
    print(error)
