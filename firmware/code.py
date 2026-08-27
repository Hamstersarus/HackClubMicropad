## HackClub Macropad — KMK firmware with on-demand video playback
## Board: Seeed XIAO RP2350 (U1)
##
## Matrix (2 rows x 3 cols), diodes anode->switch->COL, cathode->ROW:
##   physical layout is 2 cols x 3 rows; see keymap comments for the mapping.
## Encoder (SW7): A=D6  B=D7  C=GND  (rotation = volume; turn-only)
## OLED (SSD1306, U2) I2C: SDA=D4  SCL=D5  addr=0x3C  (raw driver, 400kHz)
##
## Video: the top-left key sends "PLAY" over the USB *data* serial (enabled in
## boot.py). The host companion (host/play_companion.py) then streams 1024-byte
## OLED frames back over that channel while playing the audio on the computer.
## This module blits incoming frames to the OLED between matrix scans.

import board
import busio
import usb_cdc

from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC, make_key
from kmk.scanners import DiodeOrientation
from kmk.modules import Module
from kmk.modules.encoder import EncoderHandler
from kmk.extensions.media_keys import MediaKeys

W, H = 128, 64
FRAME = W * H // 8  # 1024
ADDR = 0x3C
INIT = bytes([0xAE, 0xD5, 0x80, 0xA8, 0x3F, 0xD3, 0x00, 0x40, 0x8D, 0x14,
              0x20, 0x00, 0xA1, 0xC8, 0xDA, 0x12, 0x81, 0x7F, 0xD9, 0xF1,
              0xDB, 0x40, 0xA4, 0xA6, 0x2E, 0xAF])


class OLED:
    """Minimal raw SSD1306 128x64 driver — fast full-frame blits."""
    def __init__(self, scl, sda):
        self.i2c = busio.I2C(scl, sda, frequency=400_000)  # SSD1306 max
        while not self.i2c.try_lock():
            pass
        self.i2c.writeto(ADDR, b"\x00" + INIT)
        self._win = bytes([0x00, 0x21, 0, 127, 0x22, 0, 7])
        self._out = bytearray(1 + FRAME)
        self._out[0] = 0x40

    def show(self, buf):
        self.i2c.writeto(ADDR, self._win)
        self._out[1:] = buf
        self.i2c.writeto(ADDR, self._out)


def _load(path, default=b"\x00" * FRAME):
    try:
        with open(path, "rb") as f:
            d = f.read(FRAME)
        return d if len(d) == FRAME else default
    except OSError:
        return default


class VideoModule(Module):
    """Streams OLED frames from the USB data serial, between KMK scans."""
    def __init__(self):
        self.oled = OLED(board.D5, board.D4)
        self.splash = _load("/splash.bin")
        self.ser = usb_cdc.data
        self.frame = bytearray(FRAME)
        self.view = memoryview(self.frame)
        self.fill = 0

    def during_bootup(self, keyboard):
        self.oled.show(self.splash)

    def before_matrix_scan(self, keyboard):
        ser = self.ser
        if ser is not None and ser.in_waiting:
            self.fill += ser.readinto(self.view[self.fill:])
            if self.fill >= FRAME:
                self.oled.show(self.frame)
                self.fill = 0

    def after_matrix_scan(self, keyboard):
        pass

    def before_hid_send(self, keyboard):
        pass

    def after_hid_send(self, keyboard):
        pass

    def on_powersave_enable(self, keyboard):
        pass

    def on_powersave_disable(self, keyboard):
        pass


keyboard = KMKKeyboard()
keyboard.extensions.append(MediaKeys())

video = VideoModule()
keyboard.modules.append(video)

# Video control keys: signal the host companion over the USB data serial.
def _play(*args):
    if usb_cdc.data is not None:
        usb_cdc.data.write(b"PLAY\n")

def _stop(*args):
    if usb_cdc.data is not None:
        usb_cdc.data.write(b"STOP\n")

make_key(names=("VPLAY",), on_press=_play)
make_key(names=("VSTOP",), on_press=_stop)

# --- Key matrix ---
keyboard.col_pins = (board.D3, board.D2, board.D1)   # COL0, COL1, COL2
keyboard.row_pins = (board.D9, board.D10)            # ROW0, ROW1
keyboard.diode_orientation = DiodeOrientation.COL2ROW

# --- Encoder (volume) ---
encoder = EncoderHandler()
keyboard.modules.append(encoder)
encoder.pins = ((board.D6, board.D7, None),)
encoder.map = [((KC.VOLD, KC.VOLU),)]

# --- Keymap ---
# Physical 2 cols x 3 rows. Electrical scan order is row0 then row1, col0..col2.
#   top-left = PLAY video       top-right = STOP video
#   mid-left = c                mid-right = d
#   bot-left = e                bot-right = f
keyboard.keymap = [
    [
        # ROW0:  SW3(top-right)   SW2(bot-left)   SW1(top-left)
        KC.VSTOP,        KC.E,           KC.VPLAY,
        # ROW1:  SW4(bot-right)   SW5(mid-left)   SW6(mid-right)
        KC.F,            KC.C,           KC.D,
    ],
]

if __name__ == '__main__':
    keyboard.go()