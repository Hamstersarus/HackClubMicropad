## boot.py — runs once at power-on / hard reset (NOT on soft reload).
## Enables a second USB serial channel (data) alongside the REPL console, so the
## host can stream binary video frames without colliding with KMK's console logs.
import usb_cdc

usb_cdc.enable(console=True, data=True)