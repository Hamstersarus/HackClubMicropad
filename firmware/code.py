## HackClub Macropad — KMK firmware
## Board: Seeed XIAO RP2350 (U1)
## Pinout traced from KiCAD/Macropad/Macropad.kicad_pcb
##
## Matrix (2 rows x 3 cols), diodes 1N4148 anode->switch->COL, cathode->ROW:
##          COL0(D3)   COL1(D2)   COL2(D1)
##   ROW0    SW3        SW2        SW1
##   ROW1    SW4        SW5        SW6
##
## Encoder (SW7): A=D6(GPIO0)  B=D7(GPIO1)  C=GND   (rotation only for now)
## OLED (SSD1306, U2) on I2C: SDA=D4(GPIO6)  SCL=D5(GPIO7)  addr=0x3C
## NeoPixels (SK6812 x3) on D8 are NOT wired up yet in this file.

import board

from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.scanners import DiodeOrientation
from kmk.modules.encoder import EncoderHandler
from kmk.extensions.media_keys import MediaKeys
from kmk.extensions.display import Display, TextEntry
from kmk.extensions.display.ssd1306 import SSD1306

keyboard = KMKKeyboard()

# MediaKeys extension: required for volume/mute/media keycodes (KC.VOLU, etc.)
keyboard.extensions.append(MediaKeys())

# --- OLED display (SSD1306) --------------------------------------------
# Change OLED_HEIGHT to 32 if your panel is the short 128x32 variant.
OLED_WIDTH = 128
OLED_HEIGHT = 64
oled_driver = SSD1306(sda=board.D4, scl=board.D5, device_address=0x3C)
keyboard.extensions.append(
    Display(
        display=oled_driver,
        width=OLED_WIDTH,
        height=OLED_HEIGHT,
        entries=[
            TextEntry(text="Macropad", x=0, y=0),
            TextEntry(text="Hamstersaurus", x=0, y=22),
            TextEntry(text="ready :)", x=0, y=44),
        ],
        brightness=0.8,
    )
)

# --- Key matrix ---------------------------------------------------------
# Order matters: it defines the index of each key in the keymap below.
keyboard.col_pins = (board.D3, board.D2, board.D1)   # COL0, COL1, COL2
keyboard.row_pins = (board.D9, board.D10)            # ROW0, ROW1
keyboard.diode_orientation = DiodeOrientation.COL2ROW

# --- Encoder ------------------------------------------------------------
encoder = EncoderHandler()
keyboard.modules.append(encoder)
# (pin_a, pin_b, pin_button)  -> button is None because the knob is turn-only
encoder.pins = ((board.D6, board.D7, None),)

# --- Keymap -------------------------------------------------------------
# Flat list, row-major, matching the physical table above.
# These are placeholder keycodes — change them to whatever you want each
# key to do (KC.A, KC.MUTE, macros, layer switches, etc.).
# Physical board is 2 columns x 3 rows; desired letters top -> bottom:
#     top-left = a      top-right = b
#     mid-left = c      mid-right = d
#     bot-left = e      bot-right = f
#
# The list below is in ELECTRICAL scan order (row0 then row1, col0..col2),
# which does not match the physical grid, so each slot is labelled with its
# switch designator and physical position.
keyboard.keymap = [
    [
        # ROW0:  SW3(top-right)     SW2(bot-left)      SW1(top-left)
        KC.B,              KC.E,              KC.A,
        # ROW1:  SW4(bot-right)     SW5(mid-left)      SW6(mid-right)
        KC.F,              KC.C,              KC.D,
    ],
]

# Encoder map: one (counter-clockwise, clockwise) tuple per layer.
# Turning the knob changes the volume.
encoder.map = [
    ((KC.VOLD, KC.VOLU),),
]

if __name__ == '__main__':
    keyboard.go()
