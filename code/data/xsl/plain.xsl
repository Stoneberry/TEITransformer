<?xml version = "1.0" encoding = "UTF-8"?> 
<xsl:stylesheet version = "1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
        xmlns:tei_ns="http://www.tei-c.org/ns/1.0">
        
  <xsl:template match = "/"> 
        <html> 
          <head> 
            <meta charset="utf-8"/>
            <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no"/>
          <title></title>
        </head>
        <body> 
          <main>
            <div class="tei-document wrapper">
              <div id="col1" class="column"></div>
              <div id="col2" class="column"><xsl:apply-templates/></div>
              <div id="col3" class="column"></div>
            </div>
          </main>
      </body>
    </html> 
  </xsl:template> 

    <xsl:template match="*">
        <div class="{local-name()}">
            <xsl:apply-templates select="node()|@*"/>
        </div>
    </xsl:template>
    
    <xsl:template match="*[not(*)]">
      <xsl:if test="string-length(translate(., ' ', '')) &gt; 1">
        <p class="{local-name()}" id="{generate-id(.)}">
          <xsl:apply-templates select="node()|@*"/>
        </p>
      </xsl:if>
  </xsl:template>
  
    
  <!--   Text level  -->
    
  <xsl:template match="@*">
    <xsl:if test="name() != 'class'">
      <xsl:copy-of select="."/>            
    </xsl:if>
  </xsl:template>

</xsl:stylesheet>