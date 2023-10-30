import wx

# Create the application object
app = wx.App()

# Create the frame object
frame = wx.Frame(None)

# Set the taskbar icon
icon = wx.Icon("calendar.ico", wx.BITMAP_TYPE_ICO)
frame.SetIcon(icon)

# Add widgets and code to the GUI here

# Show the frame
frame.Show()

# Run the event loop
app.MainLoop()