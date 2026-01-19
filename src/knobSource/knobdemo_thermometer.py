import wx
import knob
import time
import os
class Frame(wx.Frame):

    def __init__(self):

        wx.Frame.__init__(self, None, -1, "Thermometer", size=(550, 500))
        path = os.path.dirname(os.path.realpath(__file__))
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.ctrl = knob.KnobCtrl(self, value=32, minValue=-10, maxValue=180, increment=.5, size=(150, 150))
        self.ctrl.ShowToolTip = False
        self.ctrl.ShowPointer = True
        self.ctrl.ShowValue = True
        self.ctrl.GaugeText = '°F\n\n'
        self.ctrl.GaugeImage = wx.Image(path+'/images/thermometer.png')
        self.ctrl.GaugeImagePos = 0
        self.ctrl.ShowScale = True
        self.ctrl.SetThumbSize(5)
        self.ctrl.SetTickFrequency(.5)
        self.ctrl.SetTickColours(['#ffffff', '#ADD8E6FF', '#03C03CFF', '#FF6347FF', '#ff00ffff', '#000000'])
        self.ctrl.SetTickColourRanges([15, 30, 65, 75, 95, 100])
        self.ctrl.SetBackgroundColour(wx.Colour(80, 80, 80))
        #self.ctrl.SetPrimaryColour((33, 36, 112, 255))
        self.ctrl.SetSecondaryColour('#1e90ff')
        self.ctrl.SetDefaultTickColour('#ffffff') # White
        self.ctrl.SetHotSpots()
        self.ctrl.SetAlwaysTickColours(True)
        self.ctrl.InsideScale = False
        self.ctrl.Bind(wx.EVT_SCROLL, self.on_event)
        self.ctrl.Bind(wx.EVT_LEFT_UP, self.on_focus_event)
        self.Bind(wx.EVT_CLOSE, self.OnQuit)
        sizer.Add(self.ctrl, 1, wx.EXPAND, 0)
        self.SetSizer(sizer)
        self.Show()
        self.Refresh()
        self.Update()

    def on_event(self, event):
        print (event, "Position:", event.Position)

    # Prevent keyboard event taking focus from ctrl
    def on_focus_event(self, event):
        self.ctrl.SetFocus()
        print(event, "send control request", event.Position)
        event.Skip()

    def OnQuit(self, event):
        self.Destroy()


app = wx.App()
frame = Frame()
app.MainLoop()
