#!/usr/bin/python
#-----------------------------------------------------------------------------
# Name:        ClosureInstance.py
#
# Purpose:     This module is used to test how to switch(show/hide) differetn 
#              wx panel in a frame window.  I follow the example in this link:  
#              https://www.blog.pythonlibrary.org/2010/06/16/wxpython-how-to-switch-between-panels/               
#
# Author:      Yuancheng Liu
#
# Created:     2021/01/16
# Copyright:
# License:
#-----------------------------------------------------------------------------
import wx
import wx.grid as gridlib

class PanelOne(wx.Panel):
    
    def __init__(self, parent):
        """Constructor"""
        wx.Panel.__init__(self, parent=parent)
        txt = wx.TextCtrl(self)

class PanelTwo(wx.Panel):
    def __init__(self, parent):
        """Constructor"""
        wx.Panel.__init__(self, parent=parent)
        sizer = wx.BoxSizer(wx.VERTICAL)
        grid = gridlib.Grid(self)
        grid.CreateGrid(12,12)
        sizer.Add(grid, 0, wx.EXPAND)
        self.SetSizer(sizer)

class MainFrame(wx.Frame):
    def __init__(self, parent, id ,title):
        wx.Frame.__init__(self, parent, id, title, size=(640, 480))
        # Add the control menu bar
        menuBar = wx.MenuBar()
        pageMenu = wx.Menu()
        pageItem = pageMenu.Append(wx.ID_ANY, "Switch Panels")
        pageMenu.Bind(wx.EVT_MENU, self.onSwitchPanels)
        menuBar.Append(pageMenu, '&Page')
        self.SetMenuBar(menuBar)
        # Init the panels.
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.pnl1 = PanelOne(self)
        self.sizer.Add(self.pnl1, 1, wx.EXPAND)
        self.pnl2 = PanelTwo(self)
        self.sizer.Add(self.pnl2, 1, wx.EXPAND)
        self.pnl2.Hide()
        self.SetSizer(self.sizer)

    def onSwitchPanels(self, event):
        if self.pnl1.IsShown():
            self.SetTitle("Show Panel 2")
            self.pnl1.Hide()
            self.pnl2.Show()
        else:
            self.SetTitle("Show Panel 1")
            self.pnl2.Hide()
            self.pnl1.Show()
        self.Layout()


#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class MyApp(wx.App):
    def OnInit(self):
        mainFrame = MainFrame(None, -1, "Switch panel test.")
        mainFrame.Show(True)
        return True

#-----------------------------------------------------------------------------
if __name__ == '__main__':
    app = MyApp(0)
    app.MainLoop()