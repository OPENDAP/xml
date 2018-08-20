<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
    <xd:doc xmlns:xd="http://www.oxygenxml.com/ns/doc/xsl" scope="stylesheet">
        <xd:desc>
            <xd:p><xd:b>Created on:</xd:b> Nov 8, 2009</xd:p>
            <xd:p><xd:b>Author:</xd:b> jimg</xd:p>
            <xd:p></xd:p>
        </xd:desc>
    </xd:doc>
    
    <xsl:output method="html"/>
    
    <xsl:template match="/">
        <html>
        <head>
        <title>All the provider names</title>
        </head>
        <body>
        <h1>All the provider names</h1>
        <ul>
             <xsl:apply-templates select="datasets/provider"/>
        </ul>
        </body>
        </html>
    </xsl:template>
    
    <xsl:template match="provider">
        <li>
            <h3>Datasets from <xsl:value-of select="@name"/></h3>
            <ul>
                <xsl:apply-templates select="dataset"/>
            </ul>
        </li>
    </xsl:template>

    <xsl:template match="dataset">
        <li>
            <xsl:value-of select="@name"/>
        </li>
    </xsl:template>
</xsl:stylesheet>
