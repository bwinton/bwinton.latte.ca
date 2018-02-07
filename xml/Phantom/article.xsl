<?xml version="1.0"?>

<xsl:stylesheet xmlns:xsl="http://www.w3.org/XSL/Transform/1.0">

    <xsl:strip-space elements="*"/>
    <xsl:template match="/">
        <xsl:processing-instruction name="cocoon-format">type="text/html"</xsl:processing-instruction>
        <html>
            <head>
                <title><xsl:value-of select="article/articleinfo/title"/></title>
                <link rel="stylesheet" type="text/css" href="article.css"/>
            </head>
            <body>
                <xsl:apply-templates select="article"/>
            </body>
        </html>
    </xsl:template>

    <xsl:template match="article">

        <xsl:apply-templates select="articleinfo"/>

        <div class="toc">
            <h3>Contents</h3>
            <ol>
                <xsl:apply-templates mode="toc"/>
            </ol>
        </div>

        <xsl:apply-templates select="section"/>
    </xsl:template>

    <xsl:template match="articleinfo">
        <div class="header">
            <h1><xsl:value-of select="title"/></h1>
            <h2><xsl:value-of select="author"/></h2>
            <small><xsl:apply-templates select="copyright"/></small>
        </div>
        <xsl:apply-templates select="revhistory"/>

        <h3>Copyright</h3>
        <xsl:apply-templates select="legalnotice"/>
    </xsl:template>

    <xsl:template match="br">
        <br/>
    </xsl:template>

    <xsl:template match="copyright">
        <xsl:text>&#169; </xsl:text>
        <xsl:apply-templates select="holder"/>,
        <xsl:apply-templates select="year"/>.
    </xsl:template>

    <xsl:template match="articleinfo" mode="toc"/>

    <xsl:template match="author">
        <xsl:value-of select="concat( firstname, ' ', surname )"/>
    </xsl:template>

    <xsl:template match="revhistory">
        <h3>Revision History</h3>
        <table width="100%" border="1">
            <xsl:apply-templates/>
        </table>
    </xsl:template>

    <xsl:template match="revision">
        <tr>
            <td><xsl:value-of select="revnumber"/></td>
            <td><xsl:value-of select="date"/></td>
            <td><xsl:value-of select="authorinitials"/></td>
        </tr>
        <tr>
            <td colspan="3"><xsl:value-of select="revremark"/></td>
        </tr>
    </xsl:template>

    <xsl:template match="section" mode="toc">
        <li><a href="#{generate-id()}"><xsl:value-of select="title"/></a></li>
        <xsl:choose>
            <xsl:when test="section/title">
                <ol>
                    <xsl:apply-templates select="section" mode="toc"/>
                </ol>
            </xsl:when>
        </xsl:choose>
    </xsl:template>

    <xsl:template match="section">
        <div class="section">
        <h3><a name="{generate-id()}"><xsl:value-of select="title"/></a></h3> 
        <xsl:apply-templates/>
        </div>
    </xsl:template>

    <xsl:template match="title"/>

    <xsl:template match="para">
        <p><xsl:apply-templates/></p>
    </xsl:template>

    <xsl:template match="programlisting">
        <div class="code">
            <pre><code><xsl:value-of select="."/></code></pre>
        </div>
    </xsl:template>

    <xsl:template match="literal">
        <tt><xsl:value-of select="."/></tt>
    </xsl:template>

    <xsl:template match="ulink">
        <a>
            <xsl:attribute name="href">
                <xsl:value-of select="@url"/>
            </xsl:attribute>
            <xsl:value-of select="."/>
        </a>
    </xsl:template>

    <xsl:template match="filename">
        <code><xsl:value-of select="."/></code>
    </xsl:template>

    <xsl:template match="itemizedlist">
        <h4><xsl:value-of select="title"/></h4> 
        <ul><xsl:apply-templates/></ul>
    </xsl:template>
    
    <xsl:template match="listitem">
        <li><xsl:apply-templates/></li>
    </xsl:template>

    <xsl:template match="table">
        <table>
            <xsl:if test="@frame">
                <xsl:attribute name="border">1</xsl:attribute>
            </xsl:if>
            <xsl:apply-templates/>
        </table>
    </xsl:template>

    <xsl:template match="table/title">
        <caption><xsl:value-of select="."/></caption>
    </xsl:template>

    <xsl:template match="thead">
        <thead><xsl:apply-templates/></thead>
    </xsl:template>

    <xsl:template match="row">
        <tr><xsl:apply-templates/></tr>
    </xsl:template>

    <xsl:template match="entry">
        <xsl:choose>
            <xsl:when test="ancestor::thead">
                <th><xsl:apply-templates/></th>
            </xsl:when>
            <xsl:otherwise>
                <td>
                    <xsl:if test="@morerows">
                        <xsl:attribute name="rowspan">
                            <xsl:value-of select="@morerows + 1"/>
                        </xsl:attribute>
                    </xsl:if>
                    <xsl:apply-templates/>
                </td>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>

</xsl:stylesheet>
