import wx
import knob
import time

class Frame(wx.Frame):

    def __init__(self):

        wx.Frame.__init__(self, None, -1, "Ampere meter Demo", size=(500, 500))

        sizer = wx.BoxSizer(wx.VERTICAL)
        self.ctrl = knob.KnobCtrl(self, value=0.0, minValue=0.0, maxValue=22.0, increment=0.05, size=(150, 150))
        self.ctrl.ShowToolTip = False
        self.ctrl.ShowPointer = True
        self.ctrl.ShowValue = True
        self.ctrl.ShowScale = True
        self.ctrl.GaugeText = 'AMP'
        self.ctrl.ShowMinMax = True
        self.ctrl.SetThumbSize(10)
        self.ctrl.SetTickFrequency(0.1)
        self.ctrl.SetTickColours([(0, 0, 0), (0, 255, 0, 255), (255, 187, 0, 255), (255, 61, 0, 255)])
        self.ctrl.SetTickColourRanges([0.1, 75, 90, 100])
        self.ctrl.SetBackgroundColour(wx.Colour(80, 80, 80))
        self.ctrl.SetPrimaryColour((33, 36, 112, 255))
        self.ctrl.SetSecondaryColour((225, 225, 225, 255))
        self.ctrl.OdometerPeriod = "H"
        self.ctrl.SetOdometerUpdate(1000)
        self.ctrl.SetDefaultTickColour('#ffffff') # White
        self.ctrl.Caption = "Simple one line optional caption"
        self.ctrl.SetHotSpots()
        self.ctrl.OdometerToolTip = "Counter is accumulated Amp Hours"
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

        help.SetValue("Adjust Amperes with Mouse or Keyboard\nLeft Click & Drag - Right Click\nMouse Scroll Up / Down\nKeyboard Up / Down / Page Up / Page Down\nKeyboard Home / End / Plus & Minus\nKeyboard numbers as a %")

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
