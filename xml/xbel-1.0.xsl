<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
<!--  version 1.01-->
<!-- last update: 18-4-2001 changes <h4 onclick=""> to <a href="javascript:"><h4> -->
<xsl:output method="html" />
<xsl:template match="/">
<html>
<head>
	<title><xsl:value-of select="xbel/title" />
	</title>
<link rel="stylesheet" href="bookmark.css" />
<script>
function dl(val)
	{
	// val is de id die hoort bij de titel van een dl. de id is gelijik aan die
	// van een dl met de prefix t. Om de bijbehorende dl te krijgen moet dus de t (is het eerste)
	// teken van de id) eruit gefilterd worden. Dit gebeurt hier:
	var dl_id = val.substring(1, val.length);
	
	//Kijken hoeveel childnodes de betreffende dl heeft:
	var aantal_dls = document.getElementById(dl_id).childNodes.length;
	
	//for loop. Eerste child van een dl is altijd een kop. Deze moet altijd worden getoond
	for (var i = 1; i &lt; aantal_dls ; i++)
	{
	var test = document.getElementById(dl_id).childNodes[i].nodeName;
	if (test == "DIV")
		{
		var div = document.getElementById(dl_id).childNodes[i];
		var testdisplay = div.style.display;
		if (testdisplay == "none")
			{
				div.style.display="block"
			}
		if (testdisplay == "block")
			{
				div.style.display="none"
			}
		}
	if (test == "DL")
		{
		var dl = document.getElementById(dl_id).childNodes[i];
		var testdisplay = dl.style.display;
		if (testdisplay == "none")
			{
				dl.style.display="block"
			}
		if (testdisplay == "block")
			{
				dl.style.display="none"
			}
		}
	}
	}
</script>
</head>
<body>
<xsl:for-each select="xbel/folder">
	<xsl:sort select="title" order="ascending"/><xsl:call-template name="xbel-folder"/>
</xsl:for-each>
</body>
</html>
</xsl:template>

<xsl:template name="xbel-folder" >
	<xsl:variable name="pos">
	<xsl:value-of select="position()" />
	</xsl:variable> 
	<dl>
	<xsl:attribute name="id">
	<xsl:value-of select="$pos" />
	</xsl:attribute>
	<a>
	<xsl:attribute name="href">javascript:dl('t<xsl:value-of select="$pos" />')</xsl:attribute>
	<xsl:attribute name="id">t<xsl:value-of select="$pos" /></xsl:attribute>
	<h3>
	<xsl:value-of select="title"/>
	</h3>
	</a>
	<xsl:if test="folder">
	<xsl:for-each select = "folder">
		<xsl:sort select="title"  />
		<xsl:call-template name="folder">
			<xsl:with-param name="pos" select="$pos" />
		</xsl:call-template>
	</xsl:for-each> 
	</xsl:if>
	<xsl:if test="bookmark">
	<xsl:for-each select = "bookmark">
		<xsl:sort select="title"  /> 
		<xsl:call-template name="bookmark"/>
	</xsl:for-each> 
	</xsl:if>
	</dl>
</xsl:template>

<xsl:template name="folder">
	<xsl:param name="pos" />
	<dl>
	<xsl:attribute name="id">
	<xsl:value-of select="$pos" />
	<xsl:value-of select="-position()" />
	</xsl:attribute>
	<xsl:attribute name="style">display:none;</xsl:attribute>
	<a>
	<xsl:attribute name="id">t<xsl:value-of select="$pos" /><xsl:value-of select="-position()" />
	</xsl:attribute>
	<xsl:attribute name="href">javascript:dl('t<xsl:value-of select="$pos" /><xsl:value-of select="-position()" />')</xsl:attribute>
	<h4>
	<xsl:value-of select="title"/>
	</h4>
	</a>
	<xsl:if test="folder">
	<xsl:variable name="position">
	<xsl:value-of select="$pos" />
	<xsl:value-of select="-position()" />
	</xsl:variable>
	<xsl:for-each select = "folder">
		<xsl:sort select="title"  /> 
		<xsl:call-template name="folder">
		<xsl:with-param name="pos" select="$position" />
		</xsl:call-template>
	</xsl:for-each> 
	</xsl:if>
	<xsl:if test="bookmark">
	<xsl:for-each select = "bookmark">
		<xsl:sort select="title"  /> 
		<xsl:call-template name="bookmark"/>
	</xsl:for-each> 
	</xsl:if>
	</dl>
</xsl:template>


<xsl:template name="bookmark">
	<div>
	<xsl:attribute name="style">display:none;</xsl:attribute>
	<a>
	<xsl:attribute name="href">
	<xsl:value-of select="@href" />
	</xsl:attribute>
	<xsl:attribute name="visited">
	<xsl:value-of select="@visited" />
	</xsl:attribute>
	<xsl:attribute name="modified">
	<xsl:value-of select="@modified" />
	</xsl:attribute>
	<xsl:value-of select="title" />
	</a>
	<xsl:call-template name="desc"/>
	</div>
</xsl:template>

<xsl:template name="desc"><br /><xsl:value-of select="desc" />
</xsl:template>

</xsl:stylesheet>