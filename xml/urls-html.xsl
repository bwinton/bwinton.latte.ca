<?xml version="1.0"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <xsl:template match="xbel">
   <html>
    <head>
     <link>
       <xsl:attribute name="rel">stylesheet</xsl:attribute>
       <xsl:attribute name="href">/%7Ebwinton/urls.css</xsl:attribute>
       <xsl:attribute name="type">text/css</xsl:attribute>
     </link>
     <title><xsl:value-of select="title"/></title>
    </head>
    <body>
     <h1>
      <xsl:value-of select="title"/>
     </h1>
     <xsl:if test="desc">
       <xsl:value-of select="desc"/>
     </xsl:if>
     <xsl:apply-templates select="folder | bookmark | alias | separator"/>
     Owned by
     <xsl:for-each select="info/metadata">
      <a>
       <xsl:attribute name="href">
        mailto:<xsl:value-of select="@owner"/>
       </xsl:attribute>
       <xsl:value-of select="@owner"/>
      </a>
    </xsl:for-each>
    </body>
   </html>
  </xsl:template>


  <xsl:template match="folder">
   <h2>
    <a>
      <xsl:attribute name="name"><xsl:value-of select="title"/></xsl:attribute>
      <xsl:value-of select="title"/>
    </a>
   </h2>
   <table border="0" width="100%">
    <xsl:apply-templates select="folder | bookmark | alias | separator"/>
   </table>
   <p/>
  </xsl:template>

  <xsl:template match="bookmark">
   <tr>
     <td colspan="2">
      <a>
        <xsl:attribute name="href"><xsl:value-of select="@href"/></xsl:attribute>
        <xsl:value-of select="@href"/>
      </a>
     </td>
   </tr>
   <tr>
     <td width="100"></td>
     <td>
      <xsl:choose>
       <xsl:when test="title">
        <xsl:value-of select="title"/>
       </xsl:when>  
       <xsl:otherwise>unknown</xsl:otherwise>
      </xsl:choose>
     </td>
   </tr>
  </xsl:template>
</xsl:stylesheet>
