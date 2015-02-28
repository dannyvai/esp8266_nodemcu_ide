import wx
import serial
import thread
import time

class MainWindow(wx.Frame):
    window_width = 640
    window_height = 480
    
    upload_queue = []    
    
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(self.window_width,self.window_height))
        self.lua_code = wx.TextCtrl(self, style=wx.TE_MULTILINE,pos=(0,0),size=(310,350))
        
        self.serial_output = wx.TextCtrl(self, style=wx.TE_MULTILINE,pos=(320,0),size=(300,350))
        self.serial_output.SetBackgroundColour((0,0,0))
        self.serial_output.SetForegroundColour((255,255,255))
        self.serial_output.SetEditable(False)
        
        self.serial_com =  wx.TextCtrl(self, pos=(0, self.window_height-120),size=(50,30))
        self.start_serial_com = wx.Button(self, label="connect", pos=(55, self.window_height-120),size=(50,30))        
        self.Bind(wx.EVT_BUTTON,self.connectSerial,self.start_serial_com)
        
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
        code =  self.lua_code.GetValue()
        for line in code:
            self.upload_queue.append(line)

    def connectSerial(self,event):
         thread.start_new_thread(self.handleSerialConn,(self.serial_com.GetValue(),))

    def handleSerialConn(self,com):
        ser = serial.Serial(com,baudrate=9600)
        ser.timeout = 0.5
        while True:
            if len(self.upload_queue) > 0:
                line = self.upload_queue[0]
                ser.write(line)
                self.upload_queue.remove(line)
                res = ser.read(1024)
                if res and len(res) > 0:
                    self.serial_output.AppendText(res)
                    
            time.sleep(0.1)

def main():
    app = wx.App(False)
    frame = MainWindow(None, "Sample editor")
    app.MainLoop()

if __name__ == "__main__":
    main()

