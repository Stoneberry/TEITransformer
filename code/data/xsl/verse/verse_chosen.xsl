<?xml version = "1.0" encoding = "UTF-8"?> 
<xsl:stylesheet version = "1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
        xmlns:tei_ns="http://www.tei-c.org/ns/1.0">


    <xsl:template match="//tei_ns:lg">
      <p class="lg" id="{generate-id(.)}">
        <xsl:apply-templates select="node()|@*"/>
      </p>
    </xsl:template>

    <xsl:template match="//tei_ns:l">
      <p class="l" id="{generate-id(.)}">
        <xsl:apply-templates select="node()|@*"/>
      </p>
    </xsl:template>

    <xsl:template match="tei_ns:l/text()">
      <xsl:value-of select="."/>
    </xsl:template>

    <xsl:template match="tei_ns:l/tei_ns:speaker">
      <span class="l-speaker speaker">
        <xsl:apply-templates select="node()|@*"/>
      </span>
    </xsl:template>

    <xsl:template match="tei_ns:speaker/text()">
      <xsl:value-of select="."/>
    </xsl:template>

    <xsl:template match="tei_ns:l/tei_ns:stage">
      <span class="l-stage stage">
        <xsl:apply-templates select="node()|@*"/>
      </span>
    </xsl:template>

    <xsl:template match="tei_ns:stage/text()">
      <xsl:value-of select="."/>
    </xsl:template>

 </xsl:stylesheet>