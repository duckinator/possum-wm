import Xlib
import Xlib.display
import Xlib.X as X
import Xlib.XK as XK

import time

# QUESTIONABLE ASSUMPTIONS:
# - only the first screen is used/cared about.
# - you won't press <key> then alt for an alt+<key> shortcut.
#   (this usually results in weird things anyway?)
class PossumWM:
    def start(self):
        # Display name is inferred from $DISPLAY environment variable.
        self.display = Xlib.display.Display()
        if self.display is None:
            print("Couldn't open display!")
            exit(1)

        self.screen = self.display.get_default_screen()
        self.root = self.display.screen().root

        #self.root.change_attributes(event_mask = X.KeyPressMask | X.KeyReleaseMask)
        #self.root.change_attributes(event_mask=X.KeyPressMask)
        self.grab_keys()

        self.alt_l_keycode = self.keycode('Alt_L')
        self.alt_r_keycode = self.keycode('Alt_R')
        self.tab_keycode = self.keycode('Tab')
        self.left_keycode = self.keycode('Left')
        self.right_keycode = self.keycode('Right')

        self.alt_pressed = False
        self.alt_l_pressed_last = False

    def stop(self):
        self.display.close()
        self.display = None

    def keycode(self, keyname):
        return self.display.keysym_to_keycode(
            XK.string_to_keysym(keyname)
        )

    def info(self):
        g = self.root.get_geometry()
        return [
            "root window dimensions = {}x{}".format(g.width, g.height),
        ]

    def grab_keys(self):
        self._grab_key('Tab', X.Mod1Mask)
        self._grab_key('Alt_L', X.NONE)
        self._grab_key('Left', X.Mod1Mask)
        self._grab_key('Right', X.Mod1Mask)

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

        self.root.grab_key(keycode, modifiers, True,
                           X.GrabModeAsync, X.GrabModeAsync)

    def handle_keypress(self, event):
        #print("[PossumWM.handle_keypress]", event)
        keycode = event.detail

        if keycode == self.alt_l_keycode or keycode == self.alt_r_keycode:
            self.alt_pressed = True

        if keycode == self.alt_l_keycode:
            self.alt_l_pressed_last = True
        else:
            self.alt_l_pressed_last = False

    def handle_keyrelease(self, event):
        #print("[PossumWM.handle_keyrelease]", event)
        keycode = event.detail

        if self.alt_pressed:
            if keycode == self.left_keycode:
                self.root.circulate(X.LowerHighest)
            elif keycode == self.right_keycode:
                self.root.circulate(X.RaiseLowest)

        if keycode == self.alt_l_keycode and self.alt_l_pressed_last:
            print("~~~ Alt_L was pressed on its own.")
        self.alt_l_pressed_last = False

        if keycode == self.alt_l_keycode or keycode == self.alt_r_keycode:
            self.alt_pressed = False

    def handle(self, event):
        if isinstance(event, Xlib.protocol.event.KeyPress):
            self.handle_keypress(event)
        elif isinstance(event, Xlib.protocol.event.KeyRelease):
            self.handle_keyrelease(event)
        else:
            print("[PossumWM.handle] Got unhandled event!")

    def loop(self):
        while True:
            self.handle(self.display.next_event())
