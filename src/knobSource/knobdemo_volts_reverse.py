import wx
import knob
import time
import os

class Frame(wx.Frame):

    def __init__(self):

        wx.Frame.__init__(self, None, -1, "Reversible Milli Ṽoltmeter", size=(500, 500))
        path = os.path.dirname(os.path.realpath(__file__))
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.ctrl = knob.KnobCtrl(self, value=0.0, minValue=-10.0, maxValue=2.0, increment=0.01, size=(150, 150))
        knobstyle = self.ctrl.GetKnobStyle()
        self.ctrl.SetKnobStyle(knobstyle | knob.KNOB_RIM)
        self.ctrl.ShowToolTip = False
        self.ctrl.ShowPointer = True
        self.ctrl.ShowValue = True
        self.ctrl.ShowMinMax = False
        self.ctrl.GaugeText = 'mṼ\n\n'
        self.ctrl.ShowMinMax = True
        self.ctrl.GaugeImage = wx.Image(path+'/images/volts.png')
        self.ctrl.GaugeImagePos = 0
        self.ctrl.SetThumbSize(10)
        self.ctrl.SetTickFrequency(0.05)
        self.ctrl.SetStartEndDegrees(405.0, 123.0)
        self.ctrl.SetTickColours(['#ff00ff','#0000bb','#cae1ff', (255, 187, 51, 255), (210, 61, 0, 255)])
        self.ctrl.SetTickColourRanges([5, 15, 83.33, 90, 100])
        self.ctrl.SetBackgroundColour(wx.Colour(180, 180, 180))
        self.ctrl.SetPrimaryColour((33, 36, 33, 255))
        self.ctrl.SetSecondaryColour('#1e90ff')
        self.ctrl.SetDefaultTickColour('#ffffff') # White
        self.ctrl.Caption = "Simple optional text\ncaption"
        self.ctrl.CaptionPos = 1
        self.ctrl.SetHotSpots()
        help = wx.TextCtrl(self, -1, value="", size=(-1, 110),
                           style=wx.TE_MULTILINE|wx.TE_READONLY|wx.TE_CENTRE)
        rev_button = wx.CheckBox(self, -1, 'Reverse the Voltmeter')
        rev_button.Bind(wx.EVT_CHECKBOX, self.OnRev)
        inv_button = wx.CheckBox(self, -1, 'Invert the Voltmeter')
        inv_button.Bind(wx.EVT_CHECKBOX, self.OnInvert)
        ori_button = wx.CheckBox(self, -1, 'Reorient the Voltmeter')
        ori_button.Bind(wx.EVT_CHECKBOX, self.OnReorient)
        self.ctrl.Bind(wx.EVT_SCROLL, self.on_event)
        self.Bind(wx.EVT_CHILD_FOCUS, self.on_focus_event)
        self.Bind(wx.EVT_CLOSE, self.OnQuit)
        sizer.Add(self.ctrl, 1, wx.EXPAND, 0)
        sizer.Add(help, 0, wx.EXPAND)
        sizer.Add(rev_button, 0, wx.EXPAND)
        sizer.Add(inv_button, 0, wx.EXPAND)
        sizer.Add(ori_button, 0, wx.EXPAND)
        self.SetSizer(sizer)
        self.Show()
        self.Refresh()
        self.Update()

        help.SetValue("Adjust milliṼolts with Mouse or Keyboard\nLeft Click & Drag - Right Click\nMouse Scroll Up / Down\nKeyboard Up / Down / Page Up / Page Down\nKeyboard Home / End / Plus & Minus\nKeyboard numbers as a %")

    def OnRev(self, event):
        start, end = self.ctrl.GetStartEndDegrees()
        end, start = start, end                     # swap values
        self.ctrl.SetStartEndDegrees(start, end)

    def OnReorient(self, event):
        start, end = self.ctrl.GetStartEndDegrees()
        start = abs(start) + 45                     # rotate using positive in case it's been inverted
        end = abs(end) + 45                         # or it could have an invalid + and - start and end
        if start > 360 and end > 360:               # keep reasonable if multiple rotations
            start -= 360
            end -= 360
        self.ctrl.SetStartEndDegrees(start, end)

    def OnInvert(self, event):
        start, end = self.ctrl.GetStartEndDegrees()
        start =  -start                             # invert
        end = -end
        self.ctrl.SetStartEndDegrees(start, end)

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
