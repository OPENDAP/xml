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
        <xsl:apply-templates select="greeting"/>
    </xsl:template>
    
    <xsl:template match="greeting">
        <html>
            <body>
                <h1>
                    <xsl:value-of select="."/>
                </h1>
            </body>
        </html>
    </xsl:template>
</xsl:stylesheet>
