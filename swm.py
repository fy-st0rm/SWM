from swm_config import *


def error_handler(tag, err):
	print(tag, err)


class SWM:
	def __init__(self):
		self.display = Xlib.display.Display()

		# Color map
		self.color_map = self.display.screen().default_colormap

		# Getting root window and redirecting event
		self.root = self.display.screen().root
		self.root.change_attributes(event_mask = Xlib.X.SubstructureRedirectMask)

		# Screen dimension
		self.width = self.root.get_geometry().width
		self.height = self.root.get_geometry().height

		# Windows
		self.active_window = None
		self.window_list = []

		# Special key commands
		self.key_cmds = [["close"], ["focus_left"], ["focus_right"], ["ws1"], ["ws2"]]

		self.__grab_keys()

	#---------------#
	# Event grabers #
	#---------------#

	def __grab_keys(self):
		self.root.grab_key(Xlib.X.AnyKey, MOD, 1, Xlib.X.GrabModeAsync, Xlib.X.GrabModeAsync)

	#----------------#
	# Event Handlers #
	#----------------#

	def __handle_map(self, event):
		# Maps the open window
		self.window_list.append(event.window)
		event.window.map()

		self.__update_focus(event.window)
		self.__configure_window(event)

	def __handle_key_press(self, event):
		keysym = self.display.keycode_to_keysym(event.detail, 0)

		# handling key bindings
		for key in key_binds:
			if keysym == key[1]:
				cmd = key_binds[key]
				
				if cmd not in self.key_cmds:
					self.system(cmd)
				else:

					# Closes the focused window
					if cmd[0] == "close":
						self.__destroy_window()
						self.__configure_window(event)

					# To change the focus in the windows
					elif cmd[0] == "focus_left":
						if self.active_window is not None:
							next_focus = self.window_list.index(self.active_window) - 1
							if next_focus < 0:
								next_focus = 0

							self.__update_focus(self.window_list[next_focus])

					elif cmd[0] == "focus_right":
						if self.active_window is not None:
							next_focus = self.window_list.index(self.active_window) + 1
							if next_focus >= len(self.window_list):
								next_focus = len(self.window_list) - 1

							self.__update_focus(self.window_list[next_focus])

	#-----------------#
	# Window Handlers #
	#-----------------#

	def __destroy_window(self):
		try:
			self.active_window.destroy()
			self.window_list.remove(self.active_window)
			self.__update_focus(self.window_list[-1])

		except:
			print("No active window")

	def __configure_window(self, event):
		# Setting up tiling 
		x = border_width + gap_x 
		y = 0
		for win in self.window_list:
			args = {"border_width": border_width}
			args["x"] = x
			args["y"] = (y + gap_y)
			args["width"] = int(self.width / len(self.window_list)) - (border_width + border_width) - (gap_x + gap_x)
			args["height"] = self.height - (border_width + border_width) - (gap_y + gap_y)
			x += int(self.width / len(self.window_list))

			win.configure(**args)


	def __update_focus(self, window):
		self.active_window = window
		self.active_window.set_input_focus(Xlib.X.RevertToParent, Xlib.X.CurrentTime)
		self.active_window.configure(stack_mode = Xlib.X.Above)
		self.display.sync()


	def __update_border(self):
		# Changes the color of the border to indicate which window is active

		# Screen dimension
		self.width = self.root.get_geometry().width
		self.height = self.root.get_geometry().height

		for win in self.window_list:
			if win != self.active_window:
				border_color = inactive_border
			else:
				border_color = active_border

			border_color = self.color_map.alloc_named_color(border_color).pixel #borderColour).pixel
			win.configure(border_width = border_width)
			win.change_attributes(None,border_pixel=border_color)
			
			self.display.sync()

	#--------------#
	# System Stuff #
	#--------------#

	def system(self, command):
		try:
			subprocess.Popen(command)
		except BaseException as e:
			error_handler("[System]", e)


	#------------#
	# Main stuff #
	#------------#

	def event(self):
		if self.display.pending_events() > 0:	# Only waits for event when there is one pending
			try:
				event = self.display.next_event()

			except Xlib.error.ConnectionClosedError as e:
				error_handler("[Event]", e)
				raise KeyboardInterrupt
		else:
			return

		if event.type == Xlib.X.MapRequest: 
			self.__handle_map(event)
		elif event.type == Xlib.X.KeyPress: 
			self.__handle_key_press(event)

	def __auto_start(self):
		for i in auto_start:
			self.system(i)

	def main_loop(self):
		self.__auto_start()

		while True:
			try:
				self.__update_border()
				self.event()
			except (KeyboardInterrupt, SystemExit):
				raise


def main():
	swm = SWM()
	swm.main_loop()


if __name__ == "__main__":
	main()
