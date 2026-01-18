import wx
import knob
import time

class Frame(wx.Frame):

    def __init__(self):

        wx.Frame.__init__(self, None, -1, "PSI meter", size=(500, 500))

        sizer = wx.BoxSizer(wx.VERTICAL)
        self.ctrl = knob.KnobCtrl(self, value=14.5, minValue=0.0, maxValue=145.0, increment=0.1, size=(150, 150))
        self.ctrl.ShowToolTip = False
        self.ctrl.ShowPointer = True
        self.ctrl.ShowValue = True
        self.ctrl.GaugeText = 'PSI'
        self.ctrl.ShowScale = True
        self.ctrl.InsideScale = False
        self.ctrl.SetThumbSize(10)
        self.ctrl.SetStartEndDegrees(135.0, 405.0)
        self.ctrl.SetTickFrequency(0.25)
        self.ctrl.SetTickColours(['#ff00ff',wx.BLUE,'#cae1ff', (255, 187, 51, 255), (210, 21, 0, 255)])
        self.ctrl.SetTickColourRanges([5, 10, 20, 80, 100])
        self.ctrl.SetBackgroundColour(wx.Colour(180, 180, 180))
        #self.ctrl.SetPrimaryColour((33, 36, 33, 255))
        self.ctrl.SetSecondaryColour('#1e90ff')
        self.ctrl.SetDefaultTickColour('#ffffff') # White
        self.ctrl.Caption = "Simple one line optional caption"
        self.ctrl.SetHotSpots()
        #self.ctrl.SetAlwaysTickColours(True)
        help = wx.TextCtrl(self, -1, value="", size=(-1, 110),
                           style=wx.TE_MULTILINE|wx.TE_READONLY|wx.TE_CENTRE)
        self.ctrl.Bind(wx.EVT_SCROLL, self.on_event)
        help.Bind(wx.EVT_SET_FOCUS, self.on_focus_event)
        self.Bind(wx.EVT_CLOSE, self.OnQuit)
        sizer.Add(self.ctrl, 1, wx.EXPAND, 0)
        sizer.Add(help, 0, wx.EXPAND)
        self.SetSizer(sizer)
        self.Show()
        self.Refresh()
        self.Update()

        help.SetValue("Adjust p.s.i. with Mouse or Keyboard\nLeft Click & Drag - Right Click\nMouse Scroll Up / Down\nKeyboard Up / Down / Page Up / Page Down\nKeyboard Home / End / Plus & Minus\nKeyboard numbers as a %")

    def on_event(self, event):
        print (event, "Position:", event.Position)

    # Prevent keyboard event taking focus from ctrl
    def on_focus_event(self, event):
        self.ctrl.SetFocus()
        event.Skip()

    def OnQuit(self, event):
        self.Destroy()


app = wx.App()
frame = Frame()
app.MainLoop()
