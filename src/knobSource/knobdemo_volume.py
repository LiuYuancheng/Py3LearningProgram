import wx
import knob
import time
import os

'''
In a homage to Spinal Tap, the volume knob goes to 11 :)
'''


class Frame(wx.Frame):

    def __init__(self):

        wx.Frame.__init__(self, None, -1, "Volume knob that goes to 11", size=(500, 500))
        path = os.path.dirname(os.path.realpath(__file__))
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.ctrl = knob.KnobCtrl(self, value=0.0, minValue=0.0, maxValue=11.0, increment=0.1, size=(150, 150))
        knobstyle = self.ctrl.GetKnobStyle()
        self.ctrl.SetKnobStyle(knobstyle | knob.KNOB_RIM)
        self.ctrl.ShowToolTip = False
        self.ctrl.ShowPointer = False
        self.ctrl.ShowValue = False
        self.ctrl.DisableMinMaxMouseDrag = True
        #self.ctrl.GaugeText = u"\U0001F508"
        #self.ctrl.GaugeText = u"\U0001F50A"
        #self.ctrl.GaugeText = "Vol\n\n"
        self.ctrl.GaugeImage = wx.Image(path+'/images/woofer.png')
        self.ctrl.PointerColour = "#ffffffa0"
        self.ctrl.SetThumbSize(10)
        self.ctrl.SetTickFrequency(0.1)
        self.ctrl.SetTickColours([(0, 255, 0, 255), (255, 187, 0, 255), (255, 61, 0, 255)])
        self.ctrl.SetTickColourRanges([70, 90, 100])
        self.ctrl.SetBackgroundColour(wx.Colour(120, 120, 120))
        #self.ctrl.SetPrimaryColour((33, 36, 112, 255))
        self.ctrl.SetSecondaryColour((225, 225, 225, 255))
        self.ctrl.SetDefaultTickColour('#ffffff') # White
        #self.ctrl.ShowScale = True
        self.ctrl.ShowMinMax = True
        #self.ctrl.DefinedScaleValues = [1.5, 4.5, 5.5, 6.5, 7.55, 10.0, 11.0, 12.0] # 7.55 and 12.0 are illegal and will be excluded
        help = wx.TextCtrl(self, -1, value="\nQuick Demonstration - Please wait!", size=(-1, 110),
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

        # Further restrict maximum mouse move to 50° - Only active if DisableMinMaxMouseDrag = True
        #self.ctrl.mouse_max_move = 50


        x = 0
        for i in [0.0, 1.0, 1.8, 3.3, 4.8, 7.3, 9.1, 0.0]:
            self.ctrl.SetValue(i)
            self.Refresh()
            self.Update()
            wx.GetApp().Yield()
            time.sleep(2)

        help.SetValue("Adjust Volume with Mouse or Keyboard\nLeft Click & Drag - Right Click\nMouse Scroll Up / Down\nKeyboard Up / Down / Page Up / Page Down\nKeyboard Home / End / Plus & Minus\nKeyboard numbers as a %")

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
