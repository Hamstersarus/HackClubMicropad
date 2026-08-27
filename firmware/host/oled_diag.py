## Diagnostic: init SSD1306 and show test patterns directly (no serial).
## Prints any exception so we can see it on the console.
import board, busio, time

ADDR=0x3C; W=128; H=64; FRAME=W*H//8
INIT=bytes([0xAE,0xD5,0x80,0xA8,0x3F,0xD3,0x00,0x40,0x8D,0x14,0x20,0x00,
            0xA1,0xC8,0xDA,0x12,0x81,0x7F,0xD9,0xF1,0xDB,0x40,0xA4,0xA6,0x2E,0xAF])

def run(freq):
    print("=== trying I2C @", freq, "Hz ===")
    i2c=busio.I2C(board.D5, board.D4, frequency=freq)
    while not i2c.try_lock(): pass
    i2c.writeto(ADDR, b"\x00"+INIT)
    print("init OK")
    win=bytes([0x00,0x21,0,127,0x22,0,7])
    out=bytearray(1+FRAME); out[0]=0x40
    def show(buf):
        i2c.writeto(ADDR, win)
        out[1:]=buf
        i2c.writeto(ADDR, out)
    checker=bytes(([0xAA]* W)+([0x55]*W))*4   # alternating pattern, 1024 bytes
    show(checker); print("checker SHOWN OK")
    n=0
    while True:
        show(checker if n%2 else bytes(FRAME))
        n+=1
        if n%20==0: print("frames:", n)
        time.sleep(0.1)

try:
    run(400_000)
except Exception as e:
    print("ERROR @400k:", repr(e))
    import sys; sys.print_exception(e)