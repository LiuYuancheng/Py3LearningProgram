import wx
import knob
import time
import random


class Frame(wx.Frame):

    def __init__(self):

        wx.Frame.__init__(self, None, -1, "Speedometer Demo", size=(400, 650))

        sizer = wx.BoxSizer(wx.VERTICAL)
        self.ctrl = knob.KnobCtrl(self, value=60.0, minValue=-10.0, maxValue=220.0, increment=1.0, size=(150, 150))
        self.ctrl.ShowToolTip = False
        self.ctrl.ShowPointer = True
        self.ctrl.ShowValue = True
        self.ctrl.ShowScale = False
        self.ctrl.GaugeText = 'Mph'
        self.ctrl.OdometerToolTip = 'Distance covered'

        #self.ctrl.OdometerPeriod = "H"                 # calculate distance travelled in Hours, Mins or Secs
        #self.ctrl.PointerColour = "#0000cda0"

        self.ctrl.SetThumbSize(10)                      # Size of knob's indicator
        self.ctrl.SetTickFrequency(1.0)
        # neon blue for negative values, green, amber and red
        self.ctrl.SetTickColours([(77, 77, 255), (0, 255, 0), (255, 153, 51), (255, 42, 0)])
        # ColourRanges treated as <= percentage, unless SetTickRangePercentage(False)
        self.ctrl.SetTickColourRanges([4.4, 70, 80, 100]) # must match in number the tick colours

        self.ctrl.SetBackgroundColour(wx.Colour(80, 80, 80))
        #self.ctrl.SetPrimaryColour((33, 36, 112, 255))
        self.ctrl.SetSecondaryColour((225, 225, 225, 255))

        self.ctrl.SetOdometerUpdate(1000)               # milliseconds between odometer updates
        #self.ctrl.OdometerColour = '#0000ff40'
        #self.ctrl.OdometerBackgroundColour = '#ffffffa0'

        self.ctrl.SetDefaultTickColour('#ffffff') # White

        help = wx.TextCtrl(self, -1, value="", size=(-1, 70),
                           style=wx.TE_MULTILINE|wx.TE_READONLY|wx.TE_CENTRE)
        help.SetValue("Adjust Speedometer with Mouse or Keyboard\nClick & Drag - Right Click - Mouse Scroll\nKeyboard Up / Down / Page Up / Page Down\nHome / End / Plus & Minus / numbers as a %")
        rand_button = wx.CheckBox(self, -1, 'Generate randomish Speed values')
        rand_button.Bind(wx.EVT_CHECKBOX, self.OnRand)
        pointer_button = wx.CheckBox(self, -1, 'Pointer On')
        pointer_button.SetValue(True)
        pointer_button.Bind(wx.EVT_CHECKBOX, self.OnPointer)
        odometer_button = wx.CheckBox(self, -1, 'Show Odometer')
        odometer_button.SetValue(True)
        odometer_button.Bind(wx.EVT_CHECKBOX, self.OnOdometer)
        value_button = wx.CheckBox(self, -1, 'Show Value')
        value_button.SetValue(True)
        value_button.Bind(wx.EVT_CHECKBOX, self.OnValue)
        scale_button = wx.CheckBox(self, -1, 'Show Scale')
        scale_button.SetValue(False)
        scale_button.Bind(wx.EVT_CHECKBOX, self.OnScale)
        hotspot_button = wx.CheckBox(self, -1, 'Show Hotspot Tooltips (Thumb && Odometer)')
        hotspot_button.SetValue(False)
        hotspot_button.Bind(wx.EVT_CHECKBOX, self.OnHotSpot)

        self.ctrl.Bind(wx.EVT_SCROLL, self.on_event)
        help.Bind(wx.EVT_SET_FOCUS, self.on_focus_event)
        self.Bind(wx.EVT_CLOSE, self.OnQuit)

        sizer.Add(self.ctrl, 1, wx.EXPAND, 0)
        sizer.Add(help, 0, wx.EXPAND)
        sizer.Add(rand_button, 0, wx.EXPAND)
        sizer.Add(pointer_button, 0, wx.EXPAND)
        sizer.Add(odometer_button, 0, wx.EXPAND)
        sizer.Add(value_button, 0, wx.EXPAND)
        sizer.Add(scale_button, 0, wx.EXPAND)
        sizer.Add(hotspot_button, 0, wx.EXPAND)

        self.SetSizer(sizer)
        self.Show()

        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.OnTimer, self.timer)

    def OnRand(self, event):
        if self.timer.IsRunning():
            self.timer.Stop()
        else:
            self.timer.Start(1000)

    def OnPointer(self, event):
        obj = event.GetEventObject()
        if obj.GetValue():
            self.ctrl.ShowPointer = True
        else:
            self.ctrl.ShowPointer = False
        self.ctrl.Refresh()

    def OnOdometer(self, event):
        obj = event.GetEventObject()
        if obj.GetValue():
            self.ctrl.ShowOdometer = True
            self.ctrl.SetOdometerUpdate(1000)
        else:
            self.ctrl.ShowOdometer = False
            self.ctrl.SetOdometerUpdate(0)
        self.ctrl.Refresh()

    def OnValue(self, event):
        obj = event.GetEventObject()
        if obj.GetValue():
            self.ctrl.ShowValue = True
            self.ctrl.GaugeText = 'Mph'
        else:
            self.ctrl.ShowValue = False
            self.ctrl.GaugeText = ''
        self.ctrl.Refresh()

    def OnScale(self, event):
        obj = event.GetEventObject()
        if obj.GetValue():
            self.ctrl.ShowScale = True
        else:
            self.ctrl.ShowScale = False
        self.ctrl.Refresh()

    def OnHotSpot(self, event):
        self.ctrl.SetHotSpots()

    def OnTimer(self, event):
        # calculate a value based on a % range of current value so it doesn't jump all over the place
        x = self.ctrl.GetValue()
        y = x + 5
        x = x - int(x/10)
        y = y + int(y/10)
        if x < self.ctrl._handler.min_value:
            x = self.ctrl._handler.min_value
        if y > self.ctrl._handler.max_value:
            y = self.ctrl._handler.max_value
        try:
            #self.ctrl.SetValue(float(random.randint(x, y)))
            self.ctrl.SetValue(round(random.uniform(x,y), 1))
        except Exception as e: # probably empty range error
            self.ctrl.SetValue(x)

    def on_event(self, event):
        print (event.EventType,"Position:", event.Position)
        #print ("Average speed / Running time:", self.ctrl.GetAverageSpeed())
        event.Skip()

    # Prevent keyboard event taking focus from ctrl
    def on_focus_event(self, event):
        self.ctrl.SetFocus()
        event.Skip()

    def OnQuit(self, event):
        if self.timer.IsRunning():
            self.timer.Stop()
        self.Destroy()


app = wx.App()
frame = Frame()
app.MainLoop()
