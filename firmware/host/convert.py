#!/usr/bin/env python3
"""Convert a video into packed 1-bit SSD1306 frames for the macropad OLED.

Pipeline: ffmpeg scales/letterboxes the video to 128x64 grayscale and pipes raw
frames here; we threshold to 1-bit and pack into the SSD1306 "MVLSB" page format
(1024 bytes/frame). Output is a flat concatenation of frames -> frames.bin, which
the companion player streams to the board over USB serial.

Usage: python3 convert.py INPUT.mp4 [--fps 30] [--out frames.bin] [--threshold 128]
"""
import argparse
import subprocess
import sys
import numpy as np

W, H = 128, 64
FRAME_BYTES = W * H // 8  # 1024


def build_ffmpeg(path, fps):
    # Fit to height 64 preserving aspect (Bad Apple is ~4:3 -> 86x64), center on 128.
    vf = f"fps={fps},scale=-1:64:flags=area,pad={W}:{H}:(ow-iw)/2:0:color=black,format=gray"
    return [
        "ffmpeg", "-v", "error", "-i", path,
        "-vf", vf, "-f", "rawvideo", "-pix_fmt", "gray", "-",
    ]


def pack_mvlsb(gray, threshold):
    """gray: (64,128) uint8 -> 1024 bytes, page-major (SSD1306 horizontal mode)."""
    on = gray >= threshold                     # (64,128) bool, True = pixel lit
    pages = on.reshape(H // 8, 8, W)           # (8 pages, 8 bits, 128 cols)
    weights = (1 << np.arange(8)).reshape(1, 8, 1)
    packed = (pages * weights).sum(axis=1).astype(np.uint8)  # (8,128)
    return packed.tobytes()                    # page0 col0..127, page1 ...


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("--fps", type=int, default=30)
    ap.add_argument("--out", default="frames.bin")
    ap.add_argument("--threshold", type=int, default=128)
    args = ap.parse_args()

    proc = subprocess.Popen(build_ffmpeg(args.input, args.fps), stdout=subprocess.PIPE)
    n = 0
    raw_size = W * H  # 8192 bytes per gray frame
    with open(args.out, "wb") as out:
        while True:
            buf = proc.stdout.read(raw_size)
            if len(buf) < raw_size:
                break
            gray = np.frombuffer(buf, dtype=np.uint8).reshape(H, W)
            out.write(pack_mvlsb(gray, args.threshold))
            n += 1
            if n % 300 == 0:
                print(f"  {n} frames...", file=sys.stderr)
    proc.wait()
    print(f"wrote {args.out}: {n} frames, {n*FRAME_BYTES} bytes, "
          f"{n/args.fps:.1f}s at {args.fps} fps")


if __name__ == "__main__":
    main()