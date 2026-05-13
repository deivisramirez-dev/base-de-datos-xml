<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:output method="html" encoding="UTF-8" indent="yes"/>

    <xsl:template match="/">
        <html>
            <head>
                <meta charset="UTF-8"/>
                <title>Productos desde XML</title>
                <style>
                    body { font-family: Arial, sans-serif; margin: 32px; }
                    table { border-collapse: collapse; width: 100%; }
                    th, td { border: 1px solid #cccccc; padding: 8px; text-align: left; }
                    th { background: #eeeeee; }
                </style>
            </head>
            <body>
                <h1>Listado de productos</h1>
                <table>
                    <tr>
                        <th>ID</th>
                        <th>Producto</th>
                        <th>Precio unitario</th>
                        <th>Detalles</th>
                    </tr>
                    <xsl:for-each select="/commerce/products/product">
                        <tr>
                            <td><xsl:value-of select="@product_id"/></td>
                            <td><xsl:value-of select="product_name"/></td>
                            <td><xsl:value-of select="unit_price"/></td>
                            <td><xsl:value-of select="product_details"/></td>
                        </tr>
                    </xsl:for-each>
                </table>
            </body>
        </html>
    </xsl:template>
</xsl:stylesheet>
