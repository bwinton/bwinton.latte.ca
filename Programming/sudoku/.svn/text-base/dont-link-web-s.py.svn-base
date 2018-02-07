import random
import re
import sys
import urllib

NUM_PUZZLES = 20
START_PUZZLE = 3

# 1 = Easy, 2 = Difficult, 3 = Hard...
PUZZLE_LEVEL = 1 

cellRe = re.compile( r'<TD CLASS=.\d ID="?c(\d\d)"?><INPUT CLASS=.\d NAME=[^ ]* (READONLY VALUE="\d"|MAXLENGTH=1)? ID="?.\d\d"?></TD>' )

def getPuzzle( num ):
    p = urllib.urlopen( 'http://play.websudoku.com/?level=%d&set_id=%d' % (PUZZLE_LEVEL, num) )
    s = p.read()
    p.close()
    m = cellRe.findall( s )
    return m

def printPuzzle( num, puzzle ):
    sys.stdout.write( "Web Sudoku Easy %d\n" % num )
    row = '0'
    for i in puzzle:
        if i[0][1] != row:
            sys.stdout.write( '\n' )
            row = i[0][1]
        if i[1] == 'MAXLENGTH=1':
            sys.stdout.write( "." )
        else:
            sys.stdout.write( i[1][-2] )
    sys.stdout.write( '\n\n' )

if __name__ == "__main__":
    for i in range( NUM_PUZZLES ):
        puzzle = getPuzzle( i+1+START_PUZZLE )
        printPuzzle( i+1+START_PUZZLE, puzzle )
