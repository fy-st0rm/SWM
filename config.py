# Donot mess with the imports unless you know what you are doing

import sys
import os
import Xlib.rdb, Xlib.X, Xlib.XK, Xlib.display
import subprocess
import traceback


# Your mod key
MOD = Xlib.X.Mod4Mask	# Win key

# Apps 
terminal = ["/usr/bin/alacritty"]
search = ["/usr/bin/dmenu_run"]

# Border
border_width = 1
active_border = "#ffffff"
inactive_border = "#000000"

# Gaps
gap_x = 5
gap_y = 5

# Key binding for the window manager
# NOTE: Only two keys is supported by the key binds
key_binds = {
	(MOD, Xlib.XK.XK_Return): terminal,
	(MOD, Xlib.XK.XK_d): search,

	(MOD, Xlib.XK.XK_q): ["close"],
	(MOD, Xlib.XK.XK_Left): ["focus_left"],
	(MOD, Xlib.XK.XK_Right): ["focus_right"]
}

# Auto start commands
auto_start = [
	["/usr/bin/nitrogen", "--restore"]
]
