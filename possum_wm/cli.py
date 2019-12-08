import sys

from . import __author__, __version__

from .wm import PossumWM

def version():
    print("PossumWM v{} by {}.".format(__version__, __author__))

def main():
    if "--version" in sys.argv:
        version()
        exit()

    wm = PossumWM()
    try:
        print("*** PossumWM Starting.")
        print("* Version {}.".format(__version__))
        wm.start()
        for line in wm.info():
            print("* {}.".format(line))
        wm.loop()
    except KeyboardInterrupt:
        pass
    finally:
        print()
        print("*** PossumWM Stopping.")
        wm.stop()

