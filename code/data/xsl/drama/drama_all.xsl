<?xml version = "1.0" encoding = "UTF-8"?> 
<xsl:stylesheet version = "1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
 				xmlns:tei_ns="http://www.tei-c.org/ns/1.0">
 				
<!-- 	<xsl:template match = "/"> -->
<!--      	<html> -->
<!--         	<head> -->
<!--         		<meta charset="utf-8"/>-->
<!--         		<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no"/>-->
<!--            <link rel="stylesheet" type="text/css" href="drama.css" />-->
<!--    			<title></title>-->
<!--  			</head>-->
<!--  			<body> -->
<!--  				<main>-->
<!--  					<div class="wrapper">-->
<!--  		 				<div id="col1"></div>-->
<!--  		 				<div id="col2"><xsl:apply-templates/></div>-->
<!--  		 				<div id="col3"></div>-->
<!--  		 			</div>-->
<!--    			</main>-->
<!--  		</body>-->
<!--    </html> -->
<!--  </xsl:template> -->


    <!-- Basic behavior -->

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


  <!-- Core elements  -->

    <!-- Cast -->

    <xsl:template match="//tei_ns:castList">
      <div class="castList">
         <xsl:apply-templates select="node()|@*"/>
      </div>
    </xsl:template>

    <xsl:template match="//tei_ns:castGroup">
      <div class="castGroup">
         <xsl:apply-templates select="node()|@*"/>
      </div>
    </xsl:template>

    <xsl:template match="//tei_ns:castItem">
      <p class="castItem" id="{generate-id(.)}">
         <xsl:apply-templates select="node()|@*"/>
      </p>
    </xsl:template>

    <!-- Cast elems -->

    <xsl:template match="tei_ns:castItem/tei_ns:roleDesc">
      <span class="roleDesc">
         <xsl:apply-templates select="node()|@*"/>
      </span>
    </xsl:template>

    <xsl:template match="tei_ns:castGroup/tei_ns:roleDesc">
      <p class="castGroup-head roleDesc" id="{generate-id(.)}">
         <xsl:apply-templates select="node()|@*"/>
      </p>
    </xsl:template>

    <xsl:template match="//tei_ns:role">
      <span class="role">
         <xsl:apply-templates select="node()|@*"/>
      </span>
    </xsl:template>


    <!-- Movie elements-->

    <xsl:template match="//tei_ns:actor">
      <span class="actor">
         <xsl:apply-templates select="node()|@*"/>
      </span>
    </xsl:template>

    <xsl:template match="//tei_ns:camera">
      <p class="camera" id="{generate-id(.)}">
         <xsl:apply-templates select="node()|@*"/>
      </p>
    </xsl:template>

    <xsl:template match="//tei_ns:sound">
      <p class="sound" id="{generate-id(.)}">
         <xsl:apply-templates select="node()|@*"/>
      </p>
    </xsl:template>

    <xsl:template match="//tei_ns:caption">
      <p class="caption" id="{generate-id(.)}">
         <xsl:apply-templates select="node()|@*"/>
      </p>
    </xsl:template>

    <xsl:template match="//tei_ns:tech">
      <p class="tech" id="{generate-id(.)}">
         <xsl:apply-templates select="node()|@*"/>
      </p>
    </xsl:template>

    <xsl:template match="//tei_ns:view">
      <p class="view" id="{generate-id(.)}">
        <xsl:apply-templates select="node()|@*"/>
      </p>
    </xsl:template>


    <!-- Common -->

    <xsl:template match="//tei_ns:performance">
      <div class="performance">
        <xsl:apply-templates select="node()|@*"/>
      </div>
    </xsl:template>

    <xsl:template match="//tei_ns:prologue">
      <div class="prologue">
        <xsl:apply-templates select="node()|@*"/>
      </div>
    </xsl:template>

    <xsl:template match="//tei_ns:epilogue">
      <div class="epilogue">
        <xsl:apply-templates select="node()|@*"/>
      </div>
    </xsl:template>

    <xsl:template match="//tei_ns:set">
      <p class="set" id="{generate-id(.)}">
        <xsl:apply-templates select="node()|@*"/>
      </p>
    </xsl:template>

    <xsl:template match="tei_ns:set/tei_ns:p">
      <p class="author-remark set" id="{generate-id(.)}">
        <xsl:apply-templates select="node()|@*"/>
      </p>
    </xsl:template>

    <xsl:template match="//tei_ns:pb">
      <p class="pb" id="{generate-id(.)}">
         <xsl:apply-templates select="node()|@*"/>
      </p>
    </xsl:template>


    <!-- SP -->


    <xsl:template match="//tei_ns:sp">
      <p class="sp" id="{generate-id(.)}">
         <xsl:apply-templates select="node()|@*"/>
      </p>
    </xsl:template>

    <xsl:template match="tei_ns:sp/tei_ns:p">
      <span class="p-text p">
        <xsl:apply-templates select="node()|@*"/>
      </span>
    </xsl:template>

    <xsl:template match="//tei_ns:speaker">
      <span class="speaker">
         <xsl:apply-templates select="node()|@*"/>
      </span>
    </xsl:template>

    <xsl:template match="tei_ns:sp/tei_ns:p/text()">
      <span class="p-text p">
        <xsl:value-of select="."/>
      </span>
    </xsl:template>


    <!--   Heads  -->

    <xsl:template match="//tei_ns:head">
      <p class="general-title head" id="{generate-id(.)}">
        <xsl:apply-templates select="node()|@*"/>
      </p>
    </xsl:template>

    <xsl:template match="tei_ns:div[@type='act']/tei_ns:head">
      <p class="act-title {local-name()}" id="{generate-id(.)}">
        <xsl:apply-templates select="node()|@*"/>
      </p>
    </xsl:template>
    
    <xsl:template match="tei_ns:div[@type='scene']/tei_ns:head">
      <p class="scene-title {local-name()}" id="{generate-id(.)}">
        <xsl:apply-templates select="node()|@*"/>
      </p>
    </xsl:template>

    <xsl:template match="tei_ns:castGroup/tei_ns:head">
      <p class="castGroup-head head" id="{generate-id(.)}">
         <xsl:apply-templates select="node()|@*"/>
      </p>
    </xsl:template>

    <xsl:template match="tei_ns:castList/tei_ns:head">
      <p class="castList-head head" id="{generate-id(.)}">
         <xsl:apply-templates select="node()|@*"/>
      </p>
    </xsl:template>

    <!-- SP elements -->

    <xsl:template match="//tei_ns:speaker">
      <span class="speaker">
         <xsl:apply-templates select="node()|@*"/>
      </span>
    </xsl:template>

      <!-- Stage -->

    <xsl:template match="//tei_ns:stage">
      <p class="stage" id="{generate-id(.)}">
            <xsl:apply-templates select="node()|@*"/>
      </p>
    </xsl:template>

    <xsl:template match="tei_ns:div[@type='scene']/tei_ns:stage">
      <p class="author-remark stage" id="{generate-id(.)}">
        <xsl:apply-templates select="node()|@*"/>
      </p>
    </xsl:template>

    <xsl:template match="tei_ns:sp/tei_ns:p/tei_ns:stage">
      <span class="speaker-remark stage">
        <xsl:apply-templates select="node()|@*"/>
      </span>
    </xsl:template>

    <xsl:template match="tei_ns:sp/tei_ns:stage">
      <xsl:choose>
        <xsl:when test="starts-with(., '(')">
          <span class="speaker-remark {local-name()}">
            <xsl:apply-templates select="node()|@*"/>
          </span>
        </xsl:when>
        <xsl:otherwise>
          <span class="author-remark-block display-block {local-name()}">
            <xsl:apply-templates select="node()|@*"/>
          </span>
        </xsl:otherwise>
      </xsl:choose>
    </xsl:template> 

    <xsl:template match="tei_ns:sp/tei_ns:stage[@type='delivery']">
      <span class="speaker-remark stage">
        <xsl:apply-templates select="node()|@*"/>
      </span>
    </xsl:template>

    <xsl:template match="tei_ns:sp/tei_ns:stage[@type='action']">
      <span class="author-remark-block display-block stage">
        <xsl:apply-templates select="node()|@*"/>
      </span>
    </xsl:template> 
    

  <!--   Text level  -->
    
    <xsl:template match="tei_ns:titleStmt/tei_ns:title[1]">
      <p class="doc-title title" id='doc-title'>
        <xsl:value-of select="."/> 
      </p>
    </xsl:template>
    
    <xsl:template match="@*">
        <xsl:if test="name() != 'class'">
            <xsl:copy-of select="."/>            
        </xsl:if>
    </xsl:template>


</xsl:stylesheet>