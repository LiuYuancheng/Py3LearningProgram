import wx
import knob
import time
import os

'''
In a homage to Spinal Tap, the volume knob goes to 11 :)
'''
styles = {'KNOB_GLOW':1, 'KNOB_DEPRESSION':2, 'KNOB_HANDLE_GLOW':4, 'KNOB_TICKS':8, 'KNOB_SHADOW':16, 'KNOB_RIM':32}
StyleList = list(styles.keys())
Options = ['Scale','Inside','MinMax','Value','Pointer']
class Frame(wx.Frame):

    def __init__(self):

        wx.Frame.__init__(self, None, -1, "Styles", size=(500, 500))
        path = os.path.dirname(os.path.realpath(__file__))
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizerh = wx.BoxSizer(wx.HORIZONTAL)
        self.ctrl = knob.KnobCtrl(self, value=7.0, minValue=0.0, maxValue=220.0, increment=0.5, size=(150, 150))
        self.ctrl.ShowToolTip = False
        self.ctrl.ShowPointer = False
        self.ctrl.ShowValue = False
        self.ctrl.PointerColour = "#ffffffa0"
        self.ctrl.SetThumbSize(10)
        self.ctrl.SetTickFrequency(.5)
        self.ctrl.SetTickColours([(0, 255, 0, 255), (255, 187, 0, 255), (255, 61, 0, 255)])
        self.ctrl.SetTickColourRanges([70, 90, 100])
        self.ctrl.SetBackgroundColour(wx.Colour(120, 120, 120))
        self.ctrl.SetSecondaryColour((225, 225, 225, 255))
        self.ctrl.SetDefaultTickColour('#ffffff') # White
        self.ctrl.ShowScale = True
        self.ctrl.ShowMinMax = False

        #self.ctrl.SetFont(wx.Font(wx.FontInfo(10).FaceName("Helvetica").Italic())) # Alter font for the gauge

        self.lb = wx.CheckListBox(self, -1, choices=StyleList, size=(-1, 140))
        self.lb.SetCheckedStrings(['KNOB_GLOW', 'KNOB_DEPRESSION', 'KNOB_HANDLE_GLOW', 'KNOB_TICKS', 'KNOB_SHADOW'])

        self.lb2 = wx.CheckListBox(self, -1, choices=Options, size=(-1, 140))
        self.lb2.SetCheckedStrings(['Scale'])

        self.ctrl.Bind(wx.EVT_SCROLL, self.on_event)
        self.lb.Bind(wx.EVT_CHECKLISTBOX, self.OnCheck)
        self.lb2.Bind(wx.EVT_CHECKLISTBOX, self.OnOptions)
        self.Bind(wx.EVT_CLOSE, self.OnQuit)
        self.Bind(wx.EVT_CHILD_FOCUS, self.on_focus_event)

        sizer.Add(self.ctrl, 1, wx.EXPAND, 0)
        sizerh.Add(self.lb, 1, wx.EXPAND, 0)
        sizerh.Add(self.lb2, 1, wx.EXPAND, 0)
        sizer.Add(sizerh, 0, wx.EXPAND, 0)
        self.SetSizer(sizer)
        self.Show()
        self.Refresh()
        self.Update()

    def on_event(self, event):
        print (event, "Position:", event.Position)

    # Prevent keyboard event taking focus from ctrl
    def on_focus_event(self, event):
        self.ctrl.SetFocus()
        event.Skip()

    def OnCheck(self, event):
        cs = self.lb.GetCheckedStrings()
        style = 0
        for i in cs:
            if i in styles:
                style = style | styles[i]
        self.ctrl.SetKnobStyle(style)

    def OnOptions(self, event):
        cs = self.lb2.GetCheckedStrings()
        if 'Scale' in cs:
            self.ctrl.ShowScale = True
        else:
            self.ctrl.ShowScale = False
        if 'Inside' in cs:
            self.ctrl.InsideScale = True
        else:
            self.ctrl.InsideScale = False
        if 'MinMax' in cs:
            self.ctrl.ShowMinMax = True
        else:
            self.ctrl.ShowMinMax = False
        if 'Value' in cs:
            self.ctrl.ShowValue = True
        else:
            self.ctrl.ShowValue = False
        if 'Pointer' in cs:
            self.ctrl.ShowPointer = True
        else:
            self.ctrl.ShowPointer = False

        self.ctrl.SendSizeEvent()   # something to force the repaint

    def OnQuit(self, event):
        self.Destroy()


app = wx.App()
frame = Frame()
app.MainLoop()
