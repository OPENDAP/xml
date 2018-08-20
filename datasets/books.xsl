<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" 
    version="1.0">

<xsl:output method="text"/>

<xsl:template match="books">
    My books:
    <xsl:apply-templates/>
</xsl:template>

<xsl:template match="book">
    <xsl:value-of select="text()"/>
</xsl:template>

</xsl:stylesheet>