# HackClubMicropad

---

## Table of Contents

- [Overview](#overview)
- [Photos](#photos)
- [Bill of Materials](#bill-of-materials)

---

## Overview

The HackClub Micropad is a compact, USB-HID macropad intended for programmable shortcut input.
It was designed from scratch in KiCad and manufactured via JLCPCB. Firmware runs on CircuitPython.
It is a keybord with a programmable OLED screen, 6 keys, and a rotary encoder.
It is a fun, memorable, and beginner friendly productivity tool.

**Key features:**

- Seeed Studio XIAO RP2040 microcontroller
- Mechanical key switches (MX-compatible footprints)
- Rotary encoder with push-button
- Onboard NeoPixel (WS2812B) RGB indicator
- USB-C connectivity via the XIAO module
- 3D-printed enclosure (FDM, PLA)

---

## Photos

**PCB Top View**

<img width="730" height="721" alt="Screenshot From 2026-03-31 19-39-57" src="https://github.com/user-attachments/assets/fd13e33d-039b-49c9-9115-e39eb24e3b55" />


**Assembled Board**

<img width="1167" height="1304" alt="snapshot_assembly" src="https://github.com/user-attachments/assets/11aedb4f-9b7b-4105-a592-af1b7facb1cd" />



**Case**

<img width="1263" height="1206" alt="snapshot_case_only_back" src="https://github.com/user-attachments/assets/de758e59-299c-42b5-977e-5ff287965a88" />

<img width="1189" height="1285" alt="snapshot_case_only_front" src="https://github.com/user-attachments/assets/7e2ddc50-dd56-4372-939a-72a66af384ac" />


---

### Bill of Materials


| Part Number | Description | Quantity | Ordering Location |
| :--- | :--- | :--- | :--- |
| 2648-SC0917-ND | Raspberry Pi Pico H 40 pin DIP | 1 | [DigiKey](https://www.digikey.com/en/products/detail/seeed-technology-co-ltd/102010428/14672129?s=N4IgTCBcDaIIwFYCcB2AtHADGTWAsYAHGgHIAiIAugL5A) |
| 688-EC1110120201 | 11mm Metal Shaft Type Rotary Encoder | 1 | [DigiKey](https://www.digikey.com/en/products/detail/alps-alpine/EC1110120201/21721621?s=N4IgTCBcDaIGwA4EFoCiBhAjNgDJsOBmIAugL5A) |
| 3086-MDOB128064V2V-YI-ND | SSD1306 OLED Screen | 1 | [DigiKey](https://www.digikey.com/en/products/detail/midas-displays/MDOB128064V2V-YI/20842029?s=N4IgTCBcDaIMwAYAcA2AtAWQCIHkBCAjGEgigCwBqYFaAmgJJoByWIAugL5A) |
| 1528-1541-ND | RGB LED with integrated controller | 3 | [DigiKey](https://www.digikey.com/en/products/detail/adafruit-industries-llc/2686/5804107?s=N4IgTCBcDaIIwFYwA4C0iAsdUDkAiIAugL5A) |
| 1644-MX2A-E1NW-ND | Push button switch, normally open, 45° tilted | 6 | [DigiKey](https://www.digikey.com/en/products/detail/cherry-americas-llc/MX2A-E1NW/21738396?s=N4IgTCBcDaIIwDYAsSC0BZAGmAgqgonAHIDqqRAIiALoC%2BQA) |
| 1N4148FS-ND | 100V 0.15A standard switching diode, DO-35 | 6 | [DigiKey](https://www.digikey.com/en/products/detail/onsemi/1N4148/458603?s=N4IgTCBcDaIIwDkAsckA4BiBlAtAgIiALoC%2BQA) |
| 490-8808-ND | Unpolarized capacitor, 0.1uF | 2 | [DigiKey](https://www.digikey.com/en/products/detail/murata-electronics/RDER71E104K0K1H03B/4770963?s=N4IgTCBcDaICwE4AMBaAHGpaUDkAiIAugL5A) |
| 399-C324C106K3R5TA7301CT-ND | Unpolarized capacitor, 10uF | 2 | [DigiKey](https://www.digikey.com/en/products/detail/kemet/C324C106K3R5TA7301/12699356?s=N4IgTCBcDaIMwE4EFoDCcwBZUEYAMAbANJwBKArACoCCA7HHjqpcgHIAiIAugL5A) |
| 732-8825-1-ND | Polarized capacitor, 100uF | 2 | [DigiKey](https://www.digikey.com/en/products/detail/kemet/C324C106K3R5TA7301/12699356?s=N4IgTCBcDaIMwE4EFoDCcwBZUEYAMAbANJwBKArACoCCA7HHjqpcgHIAiIAugL5A) |
| 56-CCF554K70FKE36CT-ND | Resistor, 4.7k | 2 | [DigiKey](https://www.digikey.com/en/products/detail/vishay-beyschlag-draloric-bc-components/CCF554K70FKE36/28262019?s=N4IgTCBcDaIKwDYC0BhFAxOcAsBpA7AAzq4CiAzAigCpIByAIiALoC%2BQA) |


