#!/opt/bin/python

import pdbxml
import struct
import sys

class DatebookEntry:
  def __init__( self, record ):
    # Make a temp copy for us...
    data = record.raw

    self.type = 0
    self.id = record.id
    self.alarm = ""
    self.repeat = ""
    self.exceptions = []
    self.description = ""
    self.note = ""

    # Grab the first stuff...
    format = "!BBBBHH"
    (startHour, startMin,
     endHour, endMin,
     rawDate, palmFlags) = struct.unpack( format, data[:8] )
    data = data[8:]

    self.makeTimes( startHour, startMin, endHour, endMin )
    self.makeDate( rawDate )
    data = self.parseFlags( palmFlags, data )
  
  def makeTimes( self, startHour, startMin, endHour, endMin ):
    # make the start and end dates...
    self.start = "%2d:%02d" % ( startHour, startMin )
    self.end = "%2d:%02d" % ( endHour, endMin )
    if( startHour == startMin == endHour == endMin == 255 ):
      self.start = self.end = "Undef"
  
  def makeDate( self, rawDate ):
    (self.day, self.month, self.year,
     self.date) = self.parseDate( rawDate )
  
  def parseFlags( self, flags, data ):
    hasAlarm       = flags & 0x4000
    hasRepeat      = flags & 0x2000
    hasNote        = flags & 0x1000
    hasExceptions  = flags & 0x800
    hasDescription = flags & 0x400
    
    if( hasAlarm ):
      data = self.makeAlarm( data )
    if( hasRepeat ):
      data = self.makeRepeat( data )
    if( hasExceptions ):
      data = self.makeExceptions( data )
    if( hasDescription ):
      data = self.makeDescription( data )
    if( hasNote ):
      data = self.makeNote( data )

    return data

  def makeAlarm( self, data ):
    format = "!BB"
    (advance, advanceUnit) = struct.unpack( format, data[:2] )
    data = data[2:]
    if( advanceUnit == 0 ):
      self.alarm = "%2d minutes" % (advance,)
    elif( advanceUnit == 1 ):
      self.alarm = "%2d hours" % (advance,)
    elif( advanceUnit == 2 ):
      self.alarm = "%2d days" % (advance,)
    else:
      self.alarm = "%2d %2d" % (advance, advanceUnit)
    return data
  
  def makeRepeat( self, data ):
    format = "!BxHBBBB"
    (type, end, freq, repOn, repStart,
     unknown) = struct.unpack( format, data[:8] )
    data = data[8:]
    
    if( type == 1 ):
      self.repeat = "%d days" % (freq,)
    elif( type == 2 ):
      self.repeat = "%d weeks" % (freq,)
    elif( type == 3 ):
      self.repeat = "%d months" % (freq,)
    elif( type == 5 ):
      self.repeat = "%d years" % (freq,)
    else:
      self.repeat = "%d %d's" % (freq, type)
    
    if( end == 0xffff ):
      self.repeat += " forever!"
    else:
      self.repeat += " " + self.parseDate( end )[3]
    
    return data

  def parseDate( self, rawDate ):
    day = rawDate & 0x1f   # The day is the first 5 bits.
    rawDate >>= 5

    month = rawDate & 0xf  # The month is the next 4 bits.
    rawDate >>= 4

    year = rawDate & 0x7f
    year += 1904           # Oh, but it starts from 1904.

    # Add a convienience date.
    date = "%(day)02d/%(month)02d/%(year)4d" % vars()
    return (day, month, year, date)

  def makeExceptions( self, data ):
    format = "!H"
    (count,) = struct.unpack( format, data[:2] )
    data = data[2:]
    while( count > 0 ):
      (exception,) = struct.unpack( format, data[:2] )
      data = data[2:]
      count -= 1
      self.exceptions.append( self.parseDate(exception)[3] )
    return data

  def makeDescription( self, data ):
    lastChar = data.find( "\0" )
    if( lastChar == -1 ):
      self.description = data
      data = ""
    else:
      self.description = data[:lastChar]
      data = data[lastChar+1:]
    return data

  def makeNote( self, data ):
    lastChar = data.find( "\0" )
    if( lastChar == -1 ):
      self.note = data
      data = ""
    else:
      self.note = data[:lastChar]
      data = data[lastChar+1:]
    return data


def main( args ):
  f = pdbxml.prc.File( "DatebookDB.pdb" )
  for record in f.data:
    entry = DatebookEntry( record )
    format  = "%(id)d %(date)s %(start)s %(end)s %(alarm)s %(repeat)s\n"
    format += "  desc: %(description)s\n"
    format += "  note: %(note)s\n"
    sys.stdout.write( format % vars(entry) )

if __name__ == "__main__":
  main( sys.argv )

