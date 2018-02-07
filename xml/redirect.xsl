<?xml version="1.0"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
    <xsl:output method="html"/>

    <xsl:param name="style"/>

    <xsl:template match="/">
    
        <xsl:choose>

            <xsl:when test="$style='tree-view'">
                <xsl:processing-instruction name="xml-stylesheet">
                    href="tree-view.xsl" type="text/xsl"
                </xsl:processing-instruction>
                <xsl:processing-instruction name="cocoon-process">
                    type="xinclude"
                </xsl:processing-instruction>
                <xsl:processing-instruction name="cocoon-process">
                    type="xslt"
                </xsl:processing-instruction>
            </xsl:when>

            <xsl:when test="$style='tree-two'">
                <xsl:processing-instruction name="xml-stylesheet">
                    href="xbel-1.0.xsl" type="text/xsl"
                </xsl:processing-instruction>
                <xsl:processing-instruction name="cocoon-process">
                    type="xinclude"
                </xsl:processing-instruction>
                <xsl:processing-instruction name="cocoon-process">
                    type="xslt"
                </xsl:processing-instruction>
            </xsl:when>

            <xsl:otherwise>
                <xsl:processing-instruction name="xml-stylesheet">
                    href="urls-html.xsl" type="text/xsl"
                </xsl:processing-instruction>
                <xsl:processing-instruction name="cocoon-process">
                    type="xinclude"
                </xsl:processing-instruction>
                <xsl:processing-instruction name="cocoon-process">
                    type="xslt"
                </xsl:processing-instruction>
            </xsl:otherwise>

        </xsl:choose>

        <xsl:apply-templates/>
    </xsl:template>

    <xsl:template match="@*|*|text">
        <xsl:copy-of select="."/>
    </xsl:template>
</xsl:stylesheet>

