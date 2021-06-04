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

</xsl:stylesheet>