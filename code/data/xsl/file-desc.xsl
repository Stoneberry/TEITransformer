<?xml version = "1.0" encoding = "UTF-8"?> 
<xsl:stylesheet version = "1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
        xmlns:tei_ns="http://www.tei-c.org/ns/1.0">
        
  <xsl:template match = "/"> 
    <div class="file-desc">
      <xsl:apply-templates/>
    </div>
  </xsl:template> 

    <xsl:template match="*">
        <h3 class="fileinfo-head"><xsl:value-of select="name(.)"/></h3>
        <div class="fileinfo-block">
          <xsl:apply-templates select="node()"/>
        </div>
    </xsl:template>
    
    <xsl:template match="*[not(*)]">
      <xsl:if test="string-length(translate(., ' ', '')) &gt; 1">
        <p class="fileinfo-text">
        <span class="fileinfo-node"><xsl:value-of select="name(.)"/>: </span>
        <span>
          <xsl:apply-templates select="node()"/>
        </span>
      </p>
      </xsl:if>
  </xsl:template>
  
    
  <!--   Text level  -->
    
  <!-- <xsl:template match="@*">
    <xsl:if test="name() != 'class'">
      <xsl:copy-of select="."/>         
    </xsl:if>
  </xsl:template> -->

</xsl:stylesheet>