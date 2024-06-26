import curses
import os

import vargo

VARGO_CONF_PATH = os.path.join(vargo.__file__[:-11], 'VARGO_conf.json')

# VARGO_VERSION = vargo.__version__
VARGO_VERSION = "0.1"

VARGO_TABLE_STATUS_APPLICATIONS = 0

TEXTPAD_OFF = 0
TEXTPAD_CMD = 1
TEXTPAD_FILTER = 2
TEXTPAD_EDIT = 3

APPLICATIONS_INDEX_BAR = [
    "NAMESPACE",
    "NAME",
    "SYNC",
    "HEALTH"
]

VARGO_APPLICATIONS_KEYBIND_HELP = [
    ("r", "refresh page"),
    ("shift+r", "refresh application")
]

VARGO_LOGO = """____   _________ __________ 
\\   \\ /   /  _  \\\\______   \\
 \\   Y   /  /_\\  \\|       _/
  \\     /    |    \\    |   \\
   \\___/\\____|__  /____|_  /
                \\/       \\/ 
"""

QWERTY_KEY_0 = 48           # 0
QWERTY_KEY_1 = 49           # 1
QWERTY_KEY_2 = 50           # 2
QWERTY_KEY_3 = 51           # 3
QWERTY_KEY_4 = 52           # 4
QWERTY_KEY_5 = 53           # 5
QWERTY_KEY_6 = 54           # 6

AZERTY_KEY_0 = 224          #
AZERTY_KEY_1 = 38           # &
AZERTY_KEY_2 = 234          #
AZERTY_KEY_2_ALT = 169      #
AZERTY_KEY_3 = 34           # "
AZERTY_KEY_4 = 39           # '
AZERTY_KEY_5 = 40           # (
AZERTY_KEY_6 = 45           # -

KEY_UP = 259                # up
KEY_DOWN = 258              # down
KEY_LEFT = 260              # left
KEY_RIGHT = 261             # right

KEY_SHIFT_G = 71            # G
KEY_SHIFT_P = 80            # P (shift+p)
KEY_SHIFT_R = 82            # R (shift+r)

KEY_A = 97                  # a
KEY_E = 101                 # e
KEY_F = 102                 # f
KEY_G = 103                 # g
KEY_H = 104                 # h
KEY_P = 112                 # p
KEY_Q = 113                 # q
KEY_R = 114                 # r

KEY_BACKSLASH = 47          # /
KEY_COLON = 58              # :

KEY_ENTER = 10              # enter
KEY_ESCAPE = 27             # escape
KEY_BACKSPACE = 8           # backspace

KEY_CTRL_D = 4              # ctrl + d

def curses_init_color_pairs():
    # Start colors in curses
    curses.start_color()
    
                                                      ## TITLE COLOR
    curses.init_pair(1, 202, 234)                     # ORANGE    ON BLACK
    
                                                      ## STANDARD COLORS
    curses.init_pair(2, curses.COLOR_WHITE, 234)      # WHITE     ON BLACK
    curses.init_pair(3, 234, curses.COLOR_WHITE)      # BLACK     ON WHITE
    
                                                      ## HEADER & SURROUND COLORS
    curses.init_pair(4, 69, 234)                      # BLUE      ON BLACK
    curses.init_pair(5, curses.COLOR_MAGENTA, 234)    # MAGENTA   ON BLACK
    curses.init_pair(6, 245, 234)                     # GRAY      ON BLACK
    curses.init_pair(7, curses.COLOR_CYAN, 234)       # CYAN      ON BLACK
    curses.init_pair(8, 51, 234)                      # BLACK     ON LIGHT BLUE
    curses.init_pair(9, 234, 51)                      # LIGHT BLUE ON BLACK
    
                                                      ## TABLE (UN)SELECTED COLORS
    curses.init_pair(10, 245, 234)                    # GRAY      ON BLACK    # 404
    curses.init_pair(20, 234, 245)                    # BLACK     ON GRAY     # 404 SELECTED
    
    curses.init_pair(11, 84, 234)                     # GREENISH  ON BLACK    # OK
    curses.init_pair(21, 234, 84)                     # BLACK     ON GREENISH # OK SELECTED
    
    curses.init_pair(12, 226, 234)                    # YELLOW    ON BLACK    # PENDING
    curses.init_pair(22, 234, 226)                    # BLACK     ON YELLOW   # PENDING SELECTED

    curses.init_pair(13, curses.COLOR_RED, 234)       # RED       ON BLACK   # ERROR
    curses.init_pair(23, 234, curses.COLOR_RED)       # BLACK     ON RED     # ERROR SELECTED

    curses.init_pair(14, curses.COLOR_WHITE, 234)     # WHITE     ON BLACK   # MESSAGE
    curses.init_pair(24, 234, curses.COLOR_WHITE)     # BLACK     ON WHITE   # MESSAGE SELECTED