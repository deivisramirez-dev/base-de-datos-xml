# Proyecto base: Bases de Datos XML para comercio electrónico

Este proyecto contiene una plantilla inicial para desarrollar una actividad práctica sobre bases de datos XML.

## Objetivo

Completar una solución que permita:

1. Crear un documento XML bien formado.
2. Definir un XSD para validar el XML.
3. Ejecutar consultas XPath.
4. Crear consultas XQuery.
5. Transformar XML a HTML mediante XSLT.
6. Integrar los datos XML en una aplicación Flask.

## Instalación (entorno local)

Necesitas **Python 3.10 o superior**. Las dependencias usan **`lxml` 6.x**, que incluye ruedas precompiladas para versiones recientes (por ejemplo **3.14 en Windows**). Si en Windows el comando `python` no existe, prueba `py -3`.

```bash
python -m venv .venv
```

**Windows (PowerShell)**

```powershell
.\.venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
```

**macOS / Linux**

```bash
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## Validación (local)

```bash
python scripts/check_well_formed.py
python scripts/validate_xml.py
```

## Aplicación web (local)

```bash
python app.py
```

Por defecto el servidor de desarrollo escucha en **127.0.0.1:5000**. Variables opcionales:

| Variable      | Ejemplo   | Uso |
|---------------|-----------|-----|
| `HOST`        | `0.0.0.0` | Escuchar en todas las interfaces (útil en contenedores o red local). |
| `PORT`        | `8000`    | Puerto distinto al 5000. |
| `FLASK_DEBUG` | `0`       | Desactiva el modo debug (`1` o `true` lo activa). |

Abre en el navegador:

```text
http://127.0.0.1:5000
```

### Probar como en Render (Gunicorn)

Gunicorn solo funciona bien en **Linux o macOS**. En Windows suele bastar `python app.py`. En Linux/macOS, con el venv activado:

```bash
export PORT=8000
gunicorn app:app --bind 0.0.0.0:$PORT --workers 1
```

## Despliegue en Render

1. Sube el proyecto a **GitHub** (o GitLab/Bitbucket conectado a Render).
2. En [Render](https://render.com): **New** → **Web Service** (o **Blueprint** si quieres usar el `render.yaml` del repo).
3. Conecta el repositorio, deja **Runtime** en **Python 3**.
4. **Build command:** `pip install --upgrade pip && pip install -r requirements.txt`
5. **Start command:** `gunicorn app:app --bind 0.0.0.0:$PORT --workers 1`  
   Si usas **Blueprint**, al elegir el archivo `render.yaml` Render aplicará estos comandos automáticamente. Si creas el servicio a mano, puedes copiar el mismo comando; Render define la variable **`$PORT`**.
6. **Plan:** Free es válido para pruebas; el servicio puede “dormir” tras inactividad.
7. Tras el despliegue, abre la URL `https://<tu-servicio>.onrender.com`.

Archivos relevantes:

- `Procfile`: comando `web` que Render detecta en despliegues Python.
- `render.yaml`: definición opcional de infraestructura (Blueprint).
- `runtime.txt`: versión de Python en Render (cámbiala solo si el build indica que esa `python-3.12.x` no está disponible en tu cuenta).

No hace falta base de datos: la app lee `data/commerce.xml` desde el disco del contenedor (cada despliegue incluye los archivos del repositorio).

## Tareas pendientes

- Revisar las restricciones opcionales de `data/commerce.xsd` (por ejemplo `xs:keyref` adicionales).
- Ejecutar y documentar las consultas XPath (`python scripts/run_xpath_examples.py`).
- Ejecutar y documentar las consultas XQuery (archivos en `queries/xquery/`).
- Generar evidencias para el informe final (capturas de validación, XSLT y aplicación web).

## Estado del repositorio

- `data/commerce.xml` incluye varios clientes, tiendas, productos, órdenes, envíos e inventario, coherente con el XSD.
- La aplicación Flask en `app.py` expone las rutas indicadas en la guía (`/`, `/validate`, `/products`, `/customers`, `/orders`, `/inventory`, `/transform/products`) y el detalle por id, por ejemplo `/orders/5001`.
