<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:output method="html" encoding="UTF-8" indent="yes"/>

    <xsl:template match="/">
        <section class="xsl-products">
            <h2>Listado de productos (transformación XSLT)</h2>
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
        </section>
    </xsl:template>
</xsl:stylesheet>
