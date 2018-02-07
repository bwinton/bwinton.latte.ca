import DotRParser
import getopt
import re
import struct
import sys
import time
import wx
from wxPython.lib.maskednumctrl import wxMaskedNumCtrl

class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg

class DotRCreatorFrame( wx.Frame ):
    def __init__(self, types, parent=None, ID=-1, title="Dot R Creator",
                 pos=wx.DefaultPosition, size=wx.DefaultSize,
                 style=wx.DEFAULT_FRAME_STYLE):
        wx.Frame.__init__(self, parent, ID, title, pos, size, style)
        self.scroll = wx.ScrolledWindow( self,-1 )
        panel = wx.Panel( self.scroll, -1 )

        foo = types['Skin']

        self.addMenu()
        self.sizer = wx.FlexGridSizer( 0, 2, 2, 2 )

        for parser in foo:
            label = self.getLabel( panel, parser )
            self.sizer.Add( label, 0, wx.EXPAND )
            entry = self.getEntry( panel, parser )
            self.sizer.Add( entry, 1, wx.EXPAND )
        
        panel.SetSizer( self.sizer )
        panel.SetAutoLayout( 1 )
        panel.Layout()
        panel.Fit()
        
        self.unit = 20
        width,height = panel.GetSizeTuple()
        self.scroll.SetScrollbars( self.unit, self.unit, width/self.unit, height/self.unit+1 )
        if ( width > 400 ):
            width = 400
        if ( height > 400 ):
            height = 400
        self.SetSize( (width, height) )

        wx.EVT_CLOSE(self, self.OnCloseWindow)

    def getEntry( self, parent, parser ):
        retval = None
        if ( type(parser) == DotRParser.IntegerParser ):
            retval = wxMaskedNumCtrl( parent, integerWidth=5, allowNegative=False)
        elif ( type(parser) == DotRParser.StringParser ):
            retval = wx.TextCtrl( parent, -1, str(parser) )
            retval.SetMaxLength( parser.getLength() )
        else:
            retval = wx.Button( parent, -1, str(parser) )
        return retval
        
    def getLabel( self, parent, parser ):
        retval = wx.StaticText( parent, -1, parser.comment )
        return retval

    def addMenu( self ):
        self.status = StatusBar( self, "Welcome to the DotRCreator!" )
        # Setting up the menu.
        filemenu= wx.Menu()
        filemenu.Append(wx.ID_ABOUT, "&About"," Information about this program")
        filemenu.AppendSeparator()
        filemenu.Append(wx.ID_EXIT,"E&xit"," Terminate the program")
        # Creating the menubar.
        menuBar = wx.MenuBar()
        menuBar.Append(filemenu,"&File") # Adding the "filemenu" to the MenuBar
        self.SetMenuBar(menuBar)  # Adding the MenuBar to the Frame content.
        wx.EVT_MENU(self, wx.ID_EXIT, self.OnCloseMe)

    def OnCloseMe(self, event):
        self.Close(True)

    def OnCloseWindow(self, event):
        self.Destroy()

class StatusBar: 
    def __init__( self, _parent, _text="This is the statusbar" ):
        self.parent = _parent 
        sb = _parent.CreateStatusBar(2) 
        _parent.SetStatusText(_text,0) 
        sb.SetStatusWidths([-1, 150]) 
        self.timer = wx.PyTimer( self.Notify ) 
        self.timer.Start(1000) 
        self.Notify() 
 
    def Notify(self): 
        t = time.localtime(time.time()) 
        st = time.strftime(" %d-%b-%Y   %I:%M:%S", t) 
        self.parent.SetStatusText(st, 1) 
 
    def __del__(self): 
        self.timer.Stop() 
        del self.timer 
 
class DotRCreatorApp( wx.App ):
    def setTypes( self, types ):
        self.types = types

    def OnInit(self):
        self.frame = DotRCreatorFrame( self.types )
        self.SetTopWindow(self.frame)
        self.frame.Show( 1 )
        return True

def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        try:
            opts, args = getopt.getopt(argv[1:], "h", ["help"])
        except getopt.error, msg:
             raise Usage(msg)
        for filename in args:
            parser = DotRParser.DotRParser()
            parser.parse( file(filename) )
#            app = DotRCreatorApp()
#            app.setTypes( parser.types )
            app = wx.PySimpleApp()
            frame = DotRCreatorFrame( parser.types )
            frame.Show(1)
            app.MainLoop()
            print

    except Usage, err:
        print >>sys.stderr, err.msg
        print >>sys.stderr, "for help use --help"
        return 2

if __name__ == "__main__":
    #sys.exit(main())
    print main( ["DotRCreator.py", "SkinDefs.r"] )

