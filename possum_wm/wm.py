import Xlib
import Xlib.display

import time

# QUESTIONABLE ASSUMPTIONS:
# - only the first screen is used/cared about.
class PossumWM:
    def start(self):
        # Display name is inferred from $DISPLAY environment variable.
        self.display = Xlib.display.Display()
        self.screen = self.display.get_default_screen()
        self.root = self.display.screen().root

    def info(self):
        g = self.root.get_geometry()
        return [
            "root window dimensions = {}x{}".format(g.width, g.height),
        ]

    def stop(self):
        self.display.close()
        self.display = None

    def handle(self, event):
        print("[PossumWM.handle] Got event!")
        print("  ", event)

    def loop(self):
        while True:
            self.handle(self.display.next_event())
