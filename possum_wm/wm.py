import Xlib
import Xlib.display
import Xlib.X as X
import Xlib.XK as XK

import time

# QUESTIONABLE ASSUMPTIONS:
# - only the first screen is used/cared about.
class PossumWM:
    def start(self):
        # Display name is inferred from $DISPLAY environment variable.
        self.display = Xlib.display.Display()
        self.screen = self.display.get_default_screen()
        self.root = self.display.screen().root

        #self.root.change_attributes(event_mask = X.KeyPressMask | X.KeyReleaseMask)
        #self.root.change_attributes(event_mask=X.KeyPressMask)
        self.grab_keys()

    def stop(self):
        self.display.close()
        self.display = None

    def info(self):
        g = self.root.get_geometry()
        return [
            "root window dimensions = {}x{}".format(g.width, g.height),
        ]

    def grab_keys(self):
        # FIXME: WHY THE FUCK IS THIS NOT WORKING
        self._grab_key('Tab', X.Mod1Mask)
        self._grab_key('a', X.ControlMask)

    def _grab_key(self, key, modifiers):
        # Possible options for modifiers:
        #   ShiftMask
        #   LockMask = ???
        #   ControlMask
        #   Mod1Mask = Alt
        #   Mod2Mask = ???
        #   Mod3Mask = ???
        #   Mod4Mask = ???
        #   Mod5Mask = ???

        if not isinstance(key, str):
            print("_grab_key(): key was not a string?")
            exit(1)

        keysym = XK.string_to_keysym(key)
        keycode = self.display.keysym_to_keycode(keysym)
        print("keycode = ", keycode)

        self.root.grab_key(keycode, modifiers, True,
                           X.GrabModeAsync, X.GrabModeAsync)

    def handle(self, event):
        print("[PossumWM.handle] Got event!")
        print("  ", event)

    def loop(self):
        while True:
            self.handle(self.display.next_event())
