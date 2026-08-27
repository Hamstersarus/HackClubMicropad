#!/usr/bin/env python3
"""Companion player: streams packed OLED frames to the macropad over the USB data
serial while playing the audio on this computer, kept in sync by pacing both from
one clock here.

Modes:
  --now         stream immediately, once (Stage-A test)
  (default)     wait for the board to send 'PLAY' (Stage-B: play on keypress),
                then stream + play audio; loops so you can trigger it repeatedly.
"""
import argparse
import glob
import subprocess
import sys
import time

import serial  # pyserial

FRAME = 128 * 64 // 8  # 1024


def find_data_port():
    # The data channel enumerates as the if02 interface; console is if00.
    for p in sorted(glob.glob("/dev/serial/by-id/*XIAO*")):
        if "if02" in p:
            return p
    # Fallback: second ACM device
    acms = sorted(glob.glob("/dev/ttyACM*"))
    return acms[1] if len(acms) > 1 else (acms[0] if acms else None)


def load_frames(path):
    with open(path, "rb") as f:
        data = f.read()
    return [data[i:i + FRAME] for i in range(0, len(data) - FRAME + 1, FRAME)]


def load_splash(path):
    try:
        with open(path, "rb") as f:
            d = f.read(FRAME)
        return d if len(d) == FRAME else None
    except OSError:
        return None


def stream(ser, frames, fps, audio, splash=None):
    proc = None
    if audio:
        proc = subprocess.Popen(
            ["ffplay", "-nodisp", "-autoexit", "-loglevel", "quiet", audio]
        )
    ser.reset_input_buffer()  # drop the PLAY token / stale bytes
    t0 = time.monotonic()
    grace = 1.0               # ignore STOP for the first second (play-press residue)
    rx = b""
    stopped = False
    try:
        for i, fr in enumerate(frames):
            if ser.in_waiting:
                rx += ser.read(ser.in_waiting)
            elapsed = time.monotonic() - t0
            if elapsed < grace:
                rx = b""            # discard any residue during the grace window
            elif b"STOP" in rx:     # a real stop press after playback is underway
                stopped = True
                break
            if b"PLAY" in rx:       # ignore repeated play presses
                rx = b""
            if proc and proc.poll() is not None:
                break
            target = t0 + i / fps
            dt = target - time.monotonic()
            if dt > 0:
                time.sleep(dt)
            ser.write(fr)
    finally:
        if proc and proc.poll() is None:
            proc.terminate()          # stop audio immediately on STOP
        if proc:
            proc.wait()
        if splash:
            ser.write(splash)         # return the OLED to the title card
    print("STOPPED" if stopped else f"finished ({len(frames)/fps:.1f}s)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--frames", default="frames.bin")
    ap.add_argument("--audio", default="badapple.mp3")
    ap.add_argument("--fps", type=int, default=30)
    ap.add_argument("--port", default=None)
    ap.add_argument("--splash", default="splash.bin")
    ap.add_argument("--now", action="store_true", help="stream once immediately")
    args = ap.parse_args()

    frames = load_frames(args.frames)
    print(f"loaded {len(frames)} frames from {args.frames}")
    splash = load_splash(args.splash)

    if args.now:
        port = args.port or find_data_port()
        if not port:
            sys.exit("No data serial port found. Is boot.py enabling usb_cdc.data?")
        stream(serial.Serial(port, 115200, timeout=0.1),
               frames, args.fps, args.audio, splash)
        return

    # Resilient loop: wait for the board, serve PLAY presses, recover from unplugs.
    print("companion running — waiting for the board / play key...  Ctrl-C to quit")
    while True:
        port = args.port or find_data_port()
        if not port:
            time.sleep(2)          # board not plugged in yet; keep waiting
            continue
        try:
            ser = serial.Serial(port, 115200, timeout=0.1)
            print(f"connected: {port}")
            pending = b""
            while True:
                pending += ser.read(64)
                if b"PLAY" in pending:
                    pending = b""
                    print("PLAY received -> starting")
                    stream(ser, frames, args.fps, args.audio, splash)
                    print("waiting for next PLAY...")
        except (serial.SerialException, OSError):
            print("board disconnected — waiting for it to come back...")
            time.sleep(2)          # unplugged mid-run; retry the connection


if __name__ == "__main__":
    main()