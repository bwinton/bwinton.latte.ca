f = open( "PalmOS.act", 'wb' )
hexValues = [0xff, 0xcc, 0x99, 0x66, 0x33, 0x00 ]

bhexValues = [0xff, 0xcc, 0x99 ]

colours = [(r,g,b)
           for r in hexValues
           for b in bhexValues
           for g in hexValues
           ]

bhexValues = [0x66, 0x33, 0x00 ]

colours += [(r,g,b)
            for r in hexValues
            for b in bhexValues
            for g in hexValues
            ]

colours = colours[:-1]

greyValues = [0x11, 0x22, 0x44, 0x55, 0x77, 0x88, 0xaa, 0xbb, 0xdd, 0xee, 0xc0 ]
colours += [(x,x,x) for x in greyValues ]

cValues = [0x80, 0x00]
colours += [(r,0x80-r,0x80-b)
            for r in cValues
            for b in cValues
            ]

print "256 -", len(colours), "=", 256 - len(colours)
print [(0x00,0x00,0x00) for x in xrange( len(colours), 256 ) ]
colours += [(0x00,0x00,0x00) for x in xrange( len(colours), 256 ) ]

for colour in colours:
    for byte in colour:
        f.write( chr( byte ) )

f.write( chr( 0x00 ) )
f.write( chr( 0xe9 ) )
f.write( chr( 0x00 ) )
f.write( chr( 0xe8 ) )

f.flush();
f.close();
