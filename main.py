import wx

class MainWindow(wx.Frame):
    window_width = 640
    window_height = 480
    
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(self.window_width,self.window_height))
        self.lua_code = wx.TextCtrl(self, style=wx.TE_MULTILINE,pos=(0,0),size=(310,350))
        
        self.serial_output = wx.TextCtrl(self, style=wx.TE_MULTILINE,pos=(320,0),size=(300,350))
        self.serial_output.SetBackgroundColour((0,0,0))
        self.serial_output.SetForegroundColour((255,255,255))
        self.serial_output.SetEditable(False)
        
        self.upload =wx.Button(self, label="Upload", pos=(self.window_width-70, self.window_height-120),size=(50,30))        
        self.Bind(wx.EVT_BUTTON,self.uploadLuaCode,self.upload)
        
        self.CreateStatusBar() # A Statusbar in the bottom of the window

        # Setting up the menu.
        filemenu= wx.Menu()

        # wx.ID_ABOUT and wx.ID_EXIT are standard IDs provided by wxWidgets.
        filemenu.Append(wx.ID_ABOUT, "&About"," Information about this program")
        filemenu.AppendSeparator()
        menuExit = filemenu.Append(wx.ID_EXIT,"E&xit"," Terminate the program")
        self.Bind(wx.EVT_MENU, self.OnExit, menuExit)
        # Creating the menubar.
        menuBar = wx.MenuBar()
        menuBar.Append(filemenu,"&File") # Adding the "filemenu" to the MenuBar
        self.SetMenuBar(menuBar)  # Adding the MenuBar to the Frame content.
        self.Show(True)

    def OnExit(self, event):
        self.Close(True)

    def uploadLuaCode(self,event):
        print self.lua_code.GetValue()
        
app = wx.App(False)
frame = MainWindow(None, "Sample editor")
app.MainLoop()