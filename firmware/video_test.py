## Stage-A standalone test: receive 1024-byte OLED frames on the USB data serial
## and blit them straight to the SSD1306 via raw I2C (bypassing displayio for speed).
## Not KMK — this temporarily replaces code.py just to prove the video path.
import board
import busio
import usb_cdc

ADDR = 0x3C
W, H = 128, 64
FRAME = W * H // 8  # 1024

# SSD1306 128x64 init sequence (A1/C8 = rotated 180; swap to A0/C0 if upside-down)
INIT = bytes([
    0xAE, 0xD5, 0x80, 0xA8, 0x3F, 0xD3, 0x00, 0x40,
    0x8D, 0x14, 0x20, 0x00, 0xA1, 0xC8, 0xDA, 0x12,
    0x81, 0x7F, 0xD9, 0xF1, 0xDB, 0x40, 0xA4, 0xA6,
    0x2E, 0xAF,
])


class OLED:
    def __init__(self, scl, sda, addr=ADDR, freq=400_000):  # SSD1306 max is 400kHz
        self.addr = addr
        self.i2c = busio.I2C(scl, sda, frequency=freq)
        while not self.i2c.try_lock():
            pass
        self.i2c.writeto(addr, b"\x00" + INIT)
        self._win = bytes([0x00, 0x21, 0, 127, 0x22, 0, 7])
        self._out = bytearray(1 + FRAME)
        self._out[0] = 0x40

    def show(self, buf):
        self.i2c.writeto(self.addr, self._win)   # reset column/page window
        self._out[1:] = buf
        self.i2c.writeto(self.addr, self._out)   # 0x40 + 1024 data bytes


oled = OLED(board.D5, board.D4)
oled.show(bytes(FRAME))  # clear

ser = usb_cdc.data
ser.timeout = 0.02
# Read straight into one fixed frame buffer (no per-frame allocation).
frame = bytearray(FRAME)
view = memoryview(frame)
fill = 0
while True:
    if ser.in_waiting:
        fill += ser.readinto(view[fill:])   # tops up the current frame only
        if fill >= FRAME:
            oled.show(frame)
            fill = 0