from pathlib import Path
from lxml import etree

XML_PATH = Path(__file__).resolve().parents[1] / "data" / "commerce.xml"

try:
    etree.parse(str(XML_PATH))
    print("El XML está bien formado.")
except etree.XMLSyntaxError as error:
    print("El XML NO está bien formado.")
    print(error)
