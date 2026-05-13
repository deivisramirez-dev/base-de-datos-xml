# Guía práctica para estudiantes  
## Bases de Datos XML: diseño, validación, consulta, transformación e integración

**Asignatura:** Bases de Datos Avanzada  
**Actividad:** Construcción de una base de datos XML para un sistema de comercio electrónico  
**Modalidad sugerida:** Trabajo individual o en parejas  
**Duración sugerida en clase:** 2 a 3 horas  
**Producto final:** Proyecto funcional con archivos XML, XSD, XPath, XQuery, XSLT y una aplicación web básica

---

## 1. Propósito de la actividad

En esta actividad construirás una pequeña base de datos XML a partir de un modelo de datos de comercio electrónico. El objetivo no es solamente crear un archivo XML, sino aplicar el flujo completo de trabajo que se utiliza cuando XML se emplea como tecnología de almacenamiento, intercambio, validación, consulta y presentación de datos.

Al finalizar, deberás ser capaz de:

1. Representar información estructurada usando XML.
2. Verificar si un documento XML está bien formado.
3. Diseñar un esquema de validación mediante XSD.
4. Asociar un documento XML con su esquema XSD.
5. Validar un XML contra reglas estructurales y de tipos de datos.
6. Consultar datos XML mediante XPath.
7. Procesar consultas más complejas mediante XQuery.
8. Transformar información XML a HTML usando XSLT.
9. Integrar datos XML en una aplicación web básica.

---

## 2. Contexto del caso de estudio

El caso de estudio corresponde a un sistema simplificado de comercio electrónico. El sistema gestiona información sobre clientes, productos, tiendas, órdenes de compra, ítems de órdenes, envíos e inventario.

El modelo de datos de referencia contiene las siguientes entidades:

| Entidad | Descripción general |
|---|---|
| `CUSTOMERS` | Información de los clientes. |
| `ORDERS` | Órdenes o pedidos realizados por los clientes. |
| `ORDER_ITEMS` | Detalle de productos incluidos en cada orden. |
| `PRODUCTS` | Catálogo de productos disponibles. |
| `SHIPMENTS` | Información de envíos asociados a clientes y tiendas. |
| `STORES` | Tiendas físicas o virtuales. |
| `INVENTORY` | Existencias de productos por tienda. |

En un modelo relacional estas entidades se representan mediante tablas. En esta actividad las representarás en XML, considerando una estructura jerárquica que mantenga las relaciones principales del sistema.

---

## 3. Herramientas recomendadas

Puedes trabajar con una de las siguientes combinaciones:

### Opción recomendada para la clase

- Visual Studio Code.
- Extensión XML para VS Code.
- Python 3.10 o superior.
- Librería `lxml`.
- Navegador web.

### Opción complementaria para XQuery

- BaseX.
- Saxon.
- eXist-db.
- Cualquier entorno que permita ejecutar consultas XQuery.

---

## 4. Estructura esperada del proyecto

Tu proyecto debe organizarse de la siguiente manera:

```text
xml-commerce-project/
│
├── data/
│   ├── commerce.xml
│   └── commerce.xsd
│
├── queries/
│   ├── xpath/
│   │   ├── 01_all_products.xpath
│   │   ├── 02_customers_names.xpath
│   │   ├── 03_shipped_orders.xpath
│   │   ├── 04_products_price_gt_40.xpath
│   │   └── 05_order_items_by_order.xpath
│   │
│   └── xquery/
│       ├── 01_orders_with_customers.xq
│       ├── 02_order_totals.xq
│       └── 03_inventory_by_store.xq
│
├── transforms/
│   └── products_to_html.xsl
│
├── templates/
│   ├── index.html
│   ├── products.html
│   ├── orders.html
│   └── inventory.html
│
├── scripts/
│   ├── check_well_formed.py
│   ├── validate_xml.py
│   ├── run_xpath_examples.py
│   └── transform_products.py
│
├── app.py
├── requirements.txt
└── README.md
```

---

# 5. Flujo de trabajo de la actividad

La actividad seguirá nueve pasos. Cada paso tiene una finalidad técnica y una evidencia que deberás producir.

---

## Paso 1. Verificar que el XML esté bien formado

### ¿Qué debes hacer?

Crea el archivo `data/commerce.xml`. Este archivo debe tener un único elemento raíz, por ejemplo:

```xml
<commerce>
    ...
</commerce>
```

Dentro del elemento raíz debes representar las principales colecciones de datos:

```xml
<customers>...</customers>
<stores>...</stores>
<products>...</products>
<orders>...</orders>
<shipments>...</shipments>
<inventory>...</inventory>
```

### Reglas mínimas de XML bien formado

Tu documento debe cumplir las siguientes condiciones:

- Tener un único elemento raíz.
- Cerrar correctamente todas las etiquetas.
- Escribir los atributos entre comillas.
- Anidar los elementos correctamente.
- Respetar mayúsculas y minúsculas en nombres de etiquetas.
- No cruzar etiquetas de apertura y cierre.

### Ejemplo de error

```xml
<product product_id=101>
    <product_name>Teclado mecánico</product_name>
</products>
```

Este fragmento es incorrecto porque:

- El atributo `product_id` no está entre comillas.
- Se abre la etiqueta `<product>` pero se cierra con `</products>`.

### Evidencia requerida

Incluye en tu informe una captura o salida de consola que demuestre que el archivo XML está bien formado.

Puedes usar:

```bash
python scripts/check_well_formed.py
```

---

## Paso 2. Definir el mecanismo de validación

### ¿Qué debes hacer?

Define un archivo `data/commerce.xsd` para validar la estructura del XML. En esta actividad se usará **XSD** porque permite controlar tipos de datos, atributos obligatorios, cardinalidades y relaciones entre identificadores.

### Reglas mínimas que debe controlar el XSD

Tu XSD debe validar al menos lo siguiente:

| Elemento o atributo | Tipo esperado |
|---|---|
| `customer_id` | Entero positivo |
| `order_id` | Entero positivo |
| `product_id` | Entero positivo |
| `store_id` | Entero positivo |
| `shipment_id` | Entero positivo |
| `order_datetime` | Fecha y hora |
| `unit_price` | Decimal |
| `quantity` | Entero positivo |
| `product_inventory` | Entero no negativo |
| `order_status` | Valor controlado |
| `shipment_status` | Valor controlado |

### Evidencia requerida

Incluye una breve explicación de por qué se decidió usar XSD y no DTD.

---

## Paso 3. Asociar el XML con su XSD

### ¿Qué debes hacer?

Modifica la raíz del archivo XML para asociarla con el esquema XSD:

```xml
<commerce xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
          xsi:noNamespaceSchemaLocation="commerce.xsd">
```

### Evidencia requerida

Muestra el fragmento inicial de tu archivo XML donde se observe la asociación con `commerce.xsd`.

---

## Paso 4. Validar el documento XML

### ¿Qué debes hacer?

Ejecuta la validación del XML contra el XSD.

Comando sugerido:

```bash
python scripts/validate_xml.py
```

### Resultado esperado

Si el documento cumple con las reglas del esquema, deberías obtener un mensaje similar a:

```text
El XML es válido según el XSD.
```

### Evidencia requerida

Incluye la salida de consola o una captura del proceso de validación.

---

## Paso 5. Consultar con XPath

### ¿Qué debes hacer?

Crea y ejecuta consultas XPath para localizar datos específicos dentro del árbol XML.

Ejemplos de consultas requeridas:

### Consulta 1. Obtener todos los productos

```xpath
/commerce/products/product
```

### Consulta 2. Obtener los nombres de todos los clientes

```xpath
/commerce/customers/customer/full_name/text()
```

### Consulta 3. Obtener las órdenes enviadas

```xpath
/commerce/orders/order[order_status='SHIPPED']
```

### Consulta 4. Obtener productos con precio mayor a 40

```xpath
/commerce/products/product[unit_price > 40]
```

### Consulta 5. Obtener los ítems de una orden específica

```xpath
/commerce/orders/order[@order_id='5001']/items/item
```

### Evidencia requerida

Debes entregar al menos cinco consultas XPath con sus resultados.

Puedes ejecutar ejemplos con:

```bash
python scripts/run_xpath_examples.py
```

---

## Paso 6. Procesar consultas complejas con XQuery

### ¿Qué debes hacer?

Crea consultas XQuery que combinen información de varias partes del documento XML.

### Consulta XQuery 1. Órdenes con nombre del cliente

```xquery
for $order in /commerce/orders/order
let $customer := /commerce/customers/customer[@customer_id = $order/customer_id]
return
<order_summary>
    <order_id>{data($order/@order_id)}</order_id>
    <customer>{data($customer/full_name)}</customer>
    <status>{data($order/order_status)}</status>
</order_summary>
```

### Consulta XQuery 2. Total de cada orden

```xquery
for $order in /commerce/orders/order
return
<order_total>
    <order_id>{data($order/@order_id)}</order_id>
    <total>{
        sum(
            for $item in $order/items/item
            return xs:decimal($item/unit_price) * xs:integer($item/quantity)
        )
    }</total>
</order_total>
```

### Consulta XQuery 3. Inventario por tienda

```xquery
for $inv in /commerce/inventory/inventory_item
let $store := /commerce/stores/store[@store_id = $inv/store_id]
let $product := /commerce/products/product[@product_id = $inv/product_id]
return
<inventory_report>
    <store>{data($store/store_name)}</store>
    <product>{data($product/product_name)}</product>
    <available_units>{data($inv/product_inventory)}</available_units>
</inventory_report>
```

### Evidencia requerida

Entrega tres consultas XQuery y explica qué información obtiene cada una.

---

## Paso 7. Almacenar el XML

### ¿Qué debes hacer?

Conserva el archivo `commerce.xml` como fuente principal de datos del proyecto. Adicionalmente, puedes cargarlo en una base de datos XML nativa, como BaseX, para ejecutar XQuery.

### Alternativas de almacenamiento

| Alternativa | Uso en esta actividad |
|---|---|
| Archivo XML | Fuente principal del proyecto. |
| BaseX | Ejecución de consultas XQuery. |
| Aplicación web | Lectura y presentación de datos XML. |

### Evidencia requerida

Describe dónde está almacenado el XML y cómo lo consulta tu aplicación o herramienta.

---

## Paso 8. Transformar o presentar la información

### ¿Qué debes hacer?

Usa XSLT para transformar el XML a HTML. El archivo de transformación debe llamarse:

```text
transforms/products_to_html.xsl
```

El objetivo es generar una tabla HTML con los productos.

Puedes ejecutar la transformación con:

```bash
python scripts/transform_products.py
```

### Evidencia requerida

Entrega el archivo XSLT y el archivo HTML generado o una captura de la visualización.

---

## Paso 9. Integrar el XML en una aplicación

### ¿Qué debes hacer?

Crea una aplicación web básica usando Flask que consulte el archivo XML y muestre información del sistema.

La aplicación debe tener al menos las siguientes rutas:

| Ruta | Descripción |
|---|---|
| `/` | Página principal. |
| `/validate` | Muestra si el XML es válido contra el XSD. |
| `/products` | Lista los productos. |
| `/customers` | Lista los clientes. |
| `/orders` | Lista las órdenes con su cliente y total. |
| `/inventory` | Lista inventario por tienda y producto. |
| `/transform/products` | Muestra la transformación XSLT de productos. |

### Ejecución sugerida

```bash
pip install -r requirements.txt
python app.py
```

Luego abre en el navegador:

```text
http://127.0.0.1:5000
```

### Evidencia requerida

Incluye capturas de la aplicación funcionando.

---

# 6. Entregables de la actividad

Debes entregar un archivo comprimido `.zip` o un repositorio en GitHub con la siguiente estructura:

```text
xml-commerce-project/
│
├── data/
│   ├── commerce.xml
│   └── commerce.xsd
│
├── queries/
│   ├── xpath/
│   └── xquery/
│
├── transforms/
│   └── products_to_html.xsl
│
├── templates/
│
├── scripts/
│
├── app.py
├── requirements.txt
├── README.md
└── informe.md o informe.pdf
```

El informe debe incluir:

1. Portada.
2. Breve descripción del caso de estudio.
3. Explicación de la estructura XML diseñada.
4. Evidencia de XML bien formado.
5. Evidencia de validación con XSD.
6. Consultas XPath con resultados.
7. Consultas XQuery con resultados o explicación.
8. Evidencia de transformación XSLT.
9. Evidencia de la aplicación funcionando.
10. Conclusiones sobre el uso de XML en bases de datos avanzadas.

---

# 7. Criterios de evaluación sugeridos

| Criterio | Puntaje |
|---|---:|
| Estructura XML coherente con el modelo propuesto | 1.5 |
| XML bien formado | 1.0 |
| XSD correctamente diseñado y asociado | 1.5 |
| Validación funcional del XML | 1.0 |
| Consultas XPath correctas | 1.0 |
| Consultas XQuery correctas | 1.0 |
| Transformación XSLT a HTML | 1.0 |
| Aplicación web funcional | 1.5 |
| Organización del proyecto e informe | 0.5 |
| **Total** | **10.0** |

---

# 8. Lista de verificación final

Antes de entregar, verifica lo siguiente:

- [ ] El archivo `commerce.xml` abre correctamente.
- [ ] El XML tiene un único elemento raíz.
- [ ] Todos los identificadores principales están definidos.
- [ ] El archivo `commerce.xsd` valida la estructura esperada.
- [ ] El XML está asociado con el XSD.
- [ ] La validación con Python o VS Code es exitosa.
- [ ] Se entregan al menos cinco consultas XPath.
- [ ] Se entregan al menos tres consultas XQuery.
- [ ] Existe una transformación XSLT funcional.
- [ ] La aplicación Flask ejecuta correctamente.
- [ ] El proyecto tiene README con instrucciones de uso.
- [ ] El informe incluye evidencias del proceso.

---

# 9. Conclusión esperada

Esta actividad permite comprender que XML no es únicamente un formato de almacenamiento. XML puede actuar como una tecnología estructurada para representar información, validarla, consultarla, transformarla e integrarla dentro de aplicaciones. En bases de datos avanzadas, este flujo resulta importante porque conecta conceptos de modelado de datos, lenguajes de consulta, validación estructural e interoperabilidad entre sistemas.
