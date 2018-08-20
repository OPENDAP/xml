<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
    <xd:doc xmlns:xd="http://www.oxygenxml.com/ns/doc/xsl" scope="stylesheet">
        <xd:desc>
            <xd:p><xd:b>Created on:</xd:b> Nov 8, 2009</xd:p>
            <xd:p><xd:b>Author:</xd:b> jimg</xd:p>
            <xd:p></xd:p>
        </xd:desc>
    </xd:doc>
    
    <!-- This odd variable definition is how you get a newline in the output
        which goes a long way toward making the result readable -->
    <xsl:variable name="newline">
<xsl:text>
</xsl:text>
    </xsl:variable>
    
    <xsl:variable name="newline-space">
<xsl:text>

</xsl:text>
    </xsl:variable>

    <xsl:output method="text"/>
    
    <!-- TODO
        Add ':' onto the front of attributes under === headings
        Add newline after those attribtues 
        Use mode for attributes -->
    
    <xsl:template match="/">
        <!-- Not starting out with a = ... = heading makes for smaller headings
        and for better contents numbering -->
        <!-- xsl:text>= Datasets =</xsl:text>
        <xsl:value-of select="$newline-space"/ -->
        
        <!-- Simply calling apply-templates produces different whitespace 
            than calling it with the node-set from select="dataset/provider" -->
        <!-- xsl:apply-templates/ -->
        <xsl:apply-templates select="datasets/provider"/>

    </xsl:template>
    
    <xsl:template match="provider">
        <xsl:text>== </xsl:text>
        <xsl:value-of select="@name"/>
        <xsl:text> ==</xsl:text>
        <xsl:value-of select="$newline-space"/>
        <xsl:apply-templates select="dataset"/>
    </xsl:template>

    <xsl:template match="dataset">
        <xsl:call-template name="dataset-entry"/>
        <xsl:value-of select="$newline"/>
    </xsl:template>
    
    <xsl:template match="dataset[last()]">
        <xsl:call-template name="dataset-entry"/>
        <xsl:value-of select="$newline-space"/>
    </xsl:template>
    
    <xsl:template name="dataset-entry">
        <xsl:text>=== </xsl:text>
        <xsl:value-of select="@name"/>
        <xsl:text> === </xsl:text>
        <xsl:value-of select="$newline"/>
        
        <!-- a dataset node always has a 'name' attribute; if it has subdataset
            nodes it always has an 'expandable' attrubute -->
        <xsl:choose>
        <xsl:when test="count(subdataset)>0">
            <!-- 'if' is used here because the ': ' text has to be output before
                any of the attribute processing templates are run but it should
                only be present if there are attributes besides 'name' and
                'expandable' -->
            <xsl:if test="count(./@*)>2">
                <xsl:text>: </xsl:text>
                <!-- select all attributes of the current element. '@*' works too. -->
                <xsl:apply-templates select="./@*"/>
                <xsl:value-of select="$newline"/>
            </xsl:if>
            <xsl:apply-templates select="subdataset"/>    
        </xsl:when>
            
        <xsl:otherwise>
            <!-- no subdatasets means 'expandable' won't be present -->
            <xsl:if test="count(./@*)>1">
                <xsl:text>: </xsl:text>
                <!-- select all attributes of the current element. '@*' works too. -->
                <xsl:apply-templates select="./@*"/>
            </xsl:if>
            <!-- no subdatasets to process -->
        </xsl:otherwise>
            
        </xsl:choose>
    </xsl:template>
        
    <xsl:template match="subdataset">
        <xsl:text>* </xsl:text>
        <xsl:value-of select="@name"/>
        <xsl:text>: </xsl:text>
        <xsl:apply-templates select="./@*"/>
        <xsl:value-of select="$newline"/>
    </xsl:template>
      
    <!-- Don't write out these attributes; uses template matching precedence 
        to override the more general below. Because a rule with a predicate
        gets a +0.5 added to its priority, I set these to 1.0 so they will
        fire in all cases. I'm leaving this as is, along with the "@*[last()]"
        template below because it's a good example, even though it's not
        used anymore. -->
    
    <xsl:template match="@name" priority="1.0">
    </xsl:template>

    <xsl:template match="@expandable" priority="1.0">
    </xsl:template>
   
    <!-- Attributes to write: info, dir, gcmd, las, dds, baseUrl, ...,  -->
    
    <xsl:template match="@*">
        <xsl:call-template name="dataset-attributes"/>
    </xsl:template>
    
    <!--xsl:template match="@*[last()]">
        <xsl:call-template name="dataset-attributes"/>
        <xsl:value-of select="$newline"/>
    </xsl:template-->
        
    <xsl:template name="dataset-attributes">
        <xsl:text>[</xsl:text>
        <xsl:value-of select="."/>
        <xsl:text> </xsl:text>
        <xsl:value-of select="name()"/>
        <xsl:text>] </xsl:text>
    </xsl:template>
    
</xsl:stylesheet>
