"""Parse a subset of .r files to create .bin resources for pilrc."""

"""File formats:
----------------
type 'Skin' {
	integer;					/* Skin version - must be 1 for this skin structure */
	cstring[24];			/* Skin name - can be 23 chars + zero at the end */
	integer NONE=1, SONY=2, HANDERA=4, HIGHDENSITY=8;/* High resolution mode */
	unsigned longint;		/* Minimal supported color depth */

	integer;					/* Title height */
	integer	NO=0, YES=1;/* Standard Palm OS title with time */
	integer;					/* Title bar bitmap ID */
	rect;						/* Title bar rectangle */

	integer;					/* Refresh button bitmap ID */
	integer;					/* Refresh button selected bitmap ID */
	rect;						/* Refresh button rectangle */

	integer;					/* Memory bitmap ID */
	rect;						/* Memory - the full size rectangle */
	rect;						/* Memory - bar display rectangle */
	integer;					/* Memory - delimiting vertical line color color */
	integer;					/* Memory - delimiting vertical line color gray */

	integer;					/* Battery bitmap ID */
	integer;					/* Battery charging bitmap ID */
	rect;						/* Battery - the full size rectangle */
	rect;						/* Battery - bar display rectangle */
	integer;					/* Battery - delimiting vertical line color color */
	integer;					/* Battery - delimiting vertical line color gray */
	
	integer;					/* Homer bitmap ID */
	integer;					/* Homer selected bitmap ID */
	rect;						/* Homer bitmap rectangle */
	rect;						/* Homer hot-spot rectangle */

	integer;					/* Gadget toggle bitmap ID */
	integer;					/* Gadget toggle selected bitmap ID */
	rect;						/* Gadget toggle bitmap rectangle */
	rect;						/* Gadget toggle hot-spot rectangle */

	integer;					/* Gadget bar background bitmap ID */
	rect;						/* Gadget bar background rectangle */

	integer;					/* Number of visible gadgets (max is 16) */
	integer	NO=0, YES=1;/* Gadgets vertical */
	point;					/* starting point for drawing gadgets */
	integer;					/* gadget horizontal padding */
	integer;					/* gadget width */
	integer;					/* gadget height */
	
	integer;					/* Number of gadgets */
	integer;					/* First gadget bitmap ID */
	integer;					/* First gadget selected bitmap ID */
	
	Integer;					/* GadgetLockUnlock bitmapID */
	Integer;					/* GadgetLockUnlock selected bitmapID */
	
	rect;						/* App area - gadgets hidden*/
	rect;						/* App area - gadgets drawn*/
	
	integer DEFAULT=0, RIGHT=1, LEFT=2;	/* Scrollbar position */
	integer;					/* Scrollbar width */
	integer;					/* Scrollbar background color color */
	integer;					/* Scrollbar background color gray */
	integer;					/* Scrollbar foreground color color */
	integer;					/* Scrollbar foreground color gray */
	integer;					/* Scrollbar vertical size correction */
	
	integer;					/* Number of category icons */
	integer;					/* First category icon bitmap ID */
	integer;					/* Category icon width */
	integer;					/* Category icon height */
	
	integer NONE=0, UP=1, LEFT=2, RIGHT=3;	/* Tabs position */
	integer NO=0, YES=1;	/* Two rows of tabs */
	integer;					/* Bitmap ID of the slice: left */
	integer;					/* Bitmap ID of the slice: selected left */
	integer;					/* Bitmap ID of the slice: selected right */
	integer;					/* Bitmap ID of the slice: right - last tab*/	
	integer;					/* Bitmap ID of the slice: left after selected */
	integer;					/* Bitmap ID of the slice: right - non-last tab */

	integer;					/* Slice height */
	integer;					/* Slice width */
	integer;					/* Upper line thickness */
	integer;					/* Non-selected real height */
	
	integer;					/* Bitmap ID of the "Previous tab" scroll arrow */
	integer;					/* Bitmap ID of the "Next tab" scroll arrow */
	integer;					/* Tab scroll arrow height */
	integer;					/* Tab scroll arrow width */
	
	integer;					/* horizontal offset from the left side of the left slice */
	integer;					/* horizontal offset from the left side of the "afer selected" slice */
	integer;					/* horizontal offset from the right side of the right slice */
	integer;					/* horizontal offset from the right side of the "before selected" slice */
	integer;					/* vertical offset from the top of the slice */
	integer;					/* vertical offset from the top of the selected slice */

	rect;						/* App area to be painted with the background color */

	};
----------------
#include "SkinDefs.r"

resource 'Skin' (1) {
	1,							/* Skin version - must be 1 for this skin structure */
	"Basique HR",				/* Skin name - can be 23 chars + zero at the end */
	SONY,						/* High resolution mode */
	4,							/* Minimal supported color depth */
	

	16,						/* Title height */
	YES,						/* Standard Palm OS title with time */
	0,							/* Title bar bitmap ID */
	{0, 0, 0, 0},			/* Title bar rectangle */

	8002,						/* Refresh button bitmap ID */
	8010,						/* Refresh button selected bitmap ID */
	{40, 2, 10, 10},		/* Refresh button rectangle */

	8003,						/* Memory bitmap ID */
	{53, 1, 31, 12},		/* Memory - the full size rectangle */
	{54, 3, 27, 7},		/* Memory - bar display rectangle */
	220,						/* Memory - delimiting vertical line color color */
	6,							/* Memory - delimiting vertical line color gray */

	8004,						/* Battery bitmap ID */
	8025,						/* Battery charging bitmap ID */
	{85, 1, 31, 12},		/* Battery - the full size rectangle */
	{86, 2, 25, 8},		/* Battery - bar display rectangle */
	64,						/* Battery - delimiting vertical line color color */
	10,						/* Battery - delimiting vertical line color gray */
	
	8014,						/* Homer bitmap ID */
	8021,						/* Homer selected bitmap ID */
	{0, 150, 10, 10},		/* Homer bitmap rectangle */
	{0, 150, 10, 10},		/* Homer hot-spot rectangle */

	8013,						/* Gadget toggle bitmap ID */
	8020,						/* Gadget toggle selected bitmap ID */
	{150, 150, 10, 10},	/* Gadget toggle bitmap rectangle */
	{150, 150, 10, 10},	/* Gadget toggle hot-spot rectangle */

	8012,						/* Gadget bar background bitmap ID */
	{0, 141, 160, 19},	/* Gadget bar background rectangle */

	8,							/* Number of visible gadgets (max is 16) */
	NO,						/* Gadgets vertical */
	{14, 143},				/* starting point for drawing gadgets */
	3,							/* gadget horizontal padding */
	14,						/* gadget width */
	16,						/* gadget height */
	
	13,						/* Number of gadgets */
	8100,						/* First gadget bitmap ID */
	8200,						/* First gadget selected bitmap ID */
	
	8151,						/* GadgetLockUnlock bitmapID */
	8152,						/* GadgetLockUnlock selected bitmapID */
	
	{3, 16, 150, 137},	/* App area - gadgets hidden*/
	{1, 16, 152, 125},	/* App area - gadgets drawn*/
	
	DEFAULT,					/* Scrollbar position */
	7,							/* Scrollbar width */
	0,							/* Scrollbar background color color */
	0,							/* Scrollbar background color gray */
	89,						/* Scrollbar foreground color color */
	15,						/* Scrollbar foreground color gray */
	3,							/* Scrollbar vertical size correction */

	14,						/* Number of category icons */
	4400,						/* First category icon bitmap ID */
	11,						/* Category icon width */
	10,						/* Category icon height */

	NONE,						/* Tabs position */
	NO,						/* Two rows of tabs */
	0,							/* Bitmap ID of the slice: left */
	0,							/* Bitmap ID of the slice: selected left */
	0,							/* Bitmap ID of the slice: selected right */
	0,							/* Bitmap ID of the slice: right */	
	0,							/* Bitmap ID of the slice: left after selected */
	0,							/* Bitmap ID of the slice: right - non-last tab */
	0,							/* Slice height */
	0,							/* Left slice width */
	0,							/* Upper line thickness */
	0,							/* Non-selected real height */
	
	0,							/* Bitmap ID of the "Previous tab" scroll arrow */
	0,							/* Bitmap ID of the "Next tab" scroll arrow */
	0,							/* Tab scroll arrow height */
	0,							/* Tab scroll arrow width */

	0,							/* horizontal offset from the left side of the left slice */
	0,							/* horizontal offset from the left side of the "afer selected" slice */
	0,							/* horizontal offset from the right side of the right slice */
	0,							/* horizontal offset from the right side of the "before selected" slice */
	0,							/* vertical offset from the top of the slice */
	0,							/* vertical offset from the top of the selected slice */

	{0, 15, 160, 145}		/* App area to be painted with the background color */
	};

resource 'Skin' (2) {
	1,							/* Skin version - must be 1 for this skin structure */
	"Classique-Top HR",		/* Skin name - can be 23 chars + zero at the end */
	SONY,						/* High resolution mode */
	4,							/* Minimal supported color depth */
	

	14,						/* Title height */
	NO,						/* Standard Palm OS title with time */
	8001,						/* Title bar bitmap ID */
	{0, 0, 78, 12},		/* Title bar rectangle */

	8002,						/* Refresh button bitmap ID */
	8010,						/* Refresh button selected bitmap ID */
	{81, 1, 10, 10},		/* Refresh button rectangle */

	8003,						/* Memory bitmap ID */
	{96, 0, 31, 12},		/* Memory - the full size rectangle */
	{97, 2, 27, 7},		/* Memory - bar display rectangle */
	220,						/* Memory - delimiting vertical line color color */
	6,							/* Memory - delimiting vertical line color gray */

	8004,						/* Battery bitmap ID */
	8025,						/* Battery charging bitmap ID */
	{128, 0, 31, 12},		/* Battery - the full size rectangle */
	{129, 1, 25, 8},		/* Battery - bar display rectangle */
	64,						/* Battery - delimiting vertical line color color */
	10,						/* Battery - delimiting vertical line color gray */
	
	8014,						/* Homer bitmap ID */
	8021,						/* Homer selected bitmap ID */
	{0, 150, 10, 10},		/* Homer bitmap rectangle */
	{0, 150, 10, 10},		/* Homer hot-spot rectangle */

	8013,						/* Gadget toggle bitmap ID */
	8020,						/* Gadget toggle selected bitmap ID */
	{150, 150, 10, 10},	/* Gadget toggle bitmap rectangle */
	{150, 150, 10, 10},	/* Gadget toggle hot-spot rectangle */

	8012,						/* Gadget bar background bitmap ID */
	{0, 141, 160, 19},	/* Gadget bar background rectangle */

	8,							/* Number of visible gadgets (max is 16) */
	NO,						/* Gadgets vertical */
	{14, 143},				/* starting point for drawing gadgets */
	3,							/* gadget horizontal padding */
	14,						/* gadget width */
	16,						/* gadget height */
	
	13,						/* Number of gadgets */
	8100,						/* First gadget bitmap ID */
	8200,						/* First gadget selected bitmap ID */
	
	8151,						/* GadgetLockUnlock bitmapID */
	8152,						/* GadgetLockUnlock selected bitmapID */
	
	{3, 30, 150, 123},	/* App area - gadgets hidden*/
	{3, 30, 150, 111},	/* App area - gadgets drawn*/
	
	DEFAULT,					/* Scrollbar position */
	7,							/* Scrollbar width */
	0,							/* Scrollbar background color color */
	0,							/* Scrollbar background color gray */
	89,						/* Scrollbar foreground color color */
	15,						/* Scrollbar foreground color gray */
	3,							/* Scrollbar vertical size correction */

	14,						/* Number of category icons */
	4400,						/* First category icon bitmap ID */
	11,						/* Category icon width */
	10,						/* Category icon height */
/***********/
	UP,						/* Tabs position */
	NO,						/* Two rows of tabs */
	4200,						/* Bitmap ID of the slice: left */
	4201,						/* Bitmap ID of the slice: selected left */
	4202,						/* Bitmap ID of the slice: selected right */
	4203,						/* Bitmap ID of the slice: right */	
	4214,						/* Bitmap ID of the slice: left after selected */
	4214,						/* Bitmap ID of the slice: right - non-last tab */
	16,						/* Slice height */
	6,							/* Left slice width */
	1,							/* Upper line thickness */
	14,						/* Non-selected real height */
	
	4204,						/* Bitmap ID of the "Previous tab" scroll arrow */
	4205,						/* Bitmap ID of the "Next tab" scroll arrow */
	10,						/* Tab scroll arrow height */
	7,							/* Tab scroll arrow width */

	4,							/* horizontal offset from the left side of the left slice */
	1,							/* horizontal offset from the left side of the "afer selected" slice */
	2,							/* horizontal offset from the right side of the right slice */
	1,							/* horizontal offset from the right side of the "before selected" slice */
	2,							/* vertical offset from the top of the slice */
	3,							/* vertical offset from the top of the selected slice */

	{0, 29, 160, 131}		/* App area to be painted with the background color */
	};
----------------
"""


import getopt
import re
import struct
import sys

class Parser( object ):
    def __init__( self ):
        self.commentRe = re.compile( "/\*(?P<comment>([^*]|\*(?!/))*)\*/" )

    def processLine( self, line ):
        # Strip comments and whitespace.
        temp = re.search( self.commentRe, line )
        comment = ""
        if ( temp != None ):
            comment = temp.group( 'comment' )
        newLine = re.sub( self.commentRe, "", line )
        newLine = newLine.strip()
        return newLine, comment

class PrintParser( Parser ):
    def process( self, line, data ):
        if line != "":
            print line
    
class IncludeParser( Parser ):
    def __init__( self, superParser ):
        super(IncludeParser, self).__init__()
        self.superParser = superParser

    def process( self, line, data ):
        filename = line.split()[1][1:-1]
        parser = DotRParser()
        parser.parse( file(filename) )
        self.superParser.copyFrom( parser )

class ResourceParser( Parser ):
    def __init__( self, superParser ):
        super(ResourceParser, self).__init__()
        self.superParser = superParser

    def process( self, line, data ):
        resource = line.split()
        resource = (resource[1][1:-1],int(resource[2][1:-1]))
        type = self.superParser.getType( resource[0] )
        resourceData = []
        index = 0
        done = 0
        try:
            while not done:
                line, comment = self.processLine( data.next() )
                if line.startswith( "};" ):
                    done = 1
                elif line != "":
                    parsedLine = self.parseLine( type[index], line )
                    index = index + 1
                    resourceData.append( parsedLine )
        except StopIteration:
            if not done:
                raise Usage( "Ran out of file in the middle of resource %s!" %(resource,) )
        if done:
            self.superParser.addResource( resource, resourceData )

    def parseLine( self, type, line ):
        if line.endswith(","):
            data = line[:-1]
        else:
            data = line
        data = type.parse( data )
        return (type, data)

class Type:
    def __init__( self ):
        self.typedef = []
    def append( self, valueParser ):
        self.typedef.append( valueParser )
    def __len__( self ):
        return self.typedef.__len__()
    def __getitem__( self, index ):
        return self.typedef[index]
    def getPackStr( self ):
        retval = "<"
        for parser in self.typedef:
            retval += parser.getPackStr()
        return retval        

class TypeParser( Parser ):
    def __init__( self, superParser ):
        super(TypeParser, self).__init__()
        self.superParser = superParser

    def process( self, line, data ):
        type = line.split()[1][1:-1]
        typedef = Type()
        done = 0
        try:
            while not done:
                line, comment = self.processLine( data.next() )
                if line.startswith( "};" ):
                    done = 1
                elif line != "":
                    if line.endswith( ";" ):
                        line = line[:-1]
                    typedef.append( self.getParser(line, comment) )
        except StopIteration:
            if not done:
                raise Usage( "Ran out of file in the middle of type %s!" %(type,) )
        if done:
            self.superParser.addType( type, typedef )

    def getParser( self, line, comment ):
        line = line.split()
        type, extra = line[0],line[1:]
        type = type.lower()
        retval = None
        unsigned = 0
        if type == "unsigned":
            type = extra[0]
            extra = extra[1:]
            unsigned = 1

        if type == "integer":
            retval = IntegerParser( unsigned, extra, comment )
        elif type == "longint":
            retval = LongIntParser( unsigned, extra, comment )
        elif type.startswith( "cstring" ):
            extra = [ type[7:] ]
            retval = StringParser( extra, comment )
        elif type == "rect":
            retval = RectParser( extra, comment )
        elif type == "point":
            retval = PointParser( extra, comment )
        else:
            raise Usage( "Unknown base type %s for %d!" %(type, comment) )
        return retval

class ValueParser( object ):
    def __init__( self, extra, comment ):
        self.extra = extra
        self.comment = comment

class IntegerParser( ValueParser ):
    def __init__( self, unsigned, extra, comment ):
        super(IntegerParser, self).__init__( extra, comment )
        self.unsigned = unsigned
        if len( self.extra ) > 0:
            temp = self.extra
            self.extra = {}
            for value in temp:
                key,value = value.split("=")
                key = key.strip()
                value = value.strip()
                self.extra[ key ] = value
    def parse( self, data ):
        retval = None
        if len(self.extra) == 0:
            retval = int( data )
        elif self.extra.has_key( data ):
            retval = self.extra[ data ]
        else:
            raise Usage( "Unknown enum %s! (enums %s)" %(data,self.extra) )
        return retval
    def __repr__( self ):
        retval = ""
        if self.unsigned:
            retval = "Unsigned "
        if len(self.extra) > 0:
            retval += "Enum " # + str( self.extra )
        else:
            retval += "Integer"
        return retval
    def getPackStr( self ):
        if self.unsigned:
            retval = "H"
        else:
            retval = 'h'
        return retval

class LongIntParser( ValueParser ):
    def __init__( self, unsigned, extra, comment ):
        super(LongIntParser, self).__init__( extra, comment )
        self.unsigned = unsigned
    def parse( self, data ):
        return long( data )
    def __repr__( self ):
        if self.unsigned:
            return "Unsigned LongInt"
        else:
            return "LongInt"
    def getPackStr( self ):
        if self.unsigned:
            retval = "L"
        else:
            retval = 'l'
        return retval

class StringParser( ValueParser ):
    def __init__( self, extra, comment ):
        super(StringParser, self).__init__( extra, comment )
    def parse( self, data ):
        if len(data) > self.getLength():
            raise Usage( "String %s longer than %s!" %(data,self.extra[0][1:-1]) )
        return data
    def __repr__( self ):
        return "String [" + str(self.getLength()) + "]"
    def getLength( self ):
        return int(self.extra[0][1:-1])
    def getPackStr( self ):
        retval = self.extra[0][1:-1] + 's'
        return retval

class RectParser( ValueParser ):
    def __init__( self, extra, comment ):
        super(RectParser, self).__init__( extra, comment )
    def parse( self, data ):
        return data
    def __repr__( self ):
        return "Rect"
    def getPackStr( self ):
        retval = '4H'
        return retval

class PointParser( ValueParser ):
    def __init__( self, extra, comment ):
        super(PointParser, self).__init__( extra, comment )
    def parse( self, data ):
        return data
    def __repr__( self ):
        return "Point"
    def getPackStr( self ):
        retval = '2H'
        return retval

class DotRParser( Parser ):
    def __init__( self ):
        super(DotRParser, self).__init__()
        self.types = {}
        self.resources = {}

    def parse( self, data ):
        try:
            while 1:
                line, comment = self.processLine( data.next() )
                if line.startswith( "#include " ):
                    parser = IncludeParser( self )
                elif line.startswith( "type " ):
                    parser = TypeParser( self )
                elif line.startswith( "resource " ):
                    parser = ResourceParser( self )
                else:
                    parser = PrintParser()
                parser.process( line, data )
        except StopIteration:
            pass
        self.writeResources()

    def addType( self, type, typedef ):
        self.types[ type ] = typedef

    def getType( self, type ):
        return self.types[ type ]

    def addResource( self, resource, resourceData ):
        self.resources[ resource ] = resourceData

    def copyFrom( self, other ):
        self.types.update( other.types )
        self.resources.update( other.resources )

    def writeResources( self ):
        keys = self.resources.keys()
        keys.sort()
        for resource in keys:
            # print resource #, self.resources[resource]
            filename = "%s%04d.bin" % (resource[0], resource[1])
            print 'DATA "%s" ID %d "%s"' % (resource[0], resource[1], filename)
            output = file( filename, 'wb' )
            #output.


class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg

def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        try:
            opts, args = getopt.getopt(argv[1:], "h", ["help"])
        except getopt.error, msg:
             raise Usage(msg)
        print "Add the following to your skins.rcp:"
        for filename in args:
            parser = DotRParser()
            parser.parse( file(filename) )
            print "Types:",
            for type in parser.types:
                fmt = parser.types[type].getPackStr()
                print type, fmt, struct.calcsize( fmt )
            # print "Resources:", parser.resources
            print

    except Usage, err:
        print >>sys.stderr, err.msg
        print >>sys.stderr, "for help use --help"
        return 2

if __name__ == "__main__":
    sys.exit(main())


