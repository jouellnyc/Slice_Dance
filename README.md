# K10 Slice Dance

Multi-style image slicing and animation for the **UNIHIKER K10** (ESP32-S3, MicroPython + LVGL).

Splits an image into horizontal slices and animates them into place using a handful of eased transition styles — slide, cascade, zoom, bounce, and explode — all rendered live on the K10's onboard 2.8" screen.

<img width="321" height="518" alt="image" src="https://github.com/user-attachments/assets/fe37eeb3-a67c-4428-aa66-ddb313350110" />

## Demo

Tested with a 225x220 RGB565 image (`cg_225x220_map_data.py`, ~400KB as a Python source file). Runs smoothly at both 10 and 20 slices on the K10's ESP32-S3 @ 240MHz.

## Compatibility

Originally written for the **Waveshare RP2350-Touch-LCD-2.8**, this version has been adapted to run on the **UNIHIKER K10** using its built-in `unihiker_k10.screen` module to access the underlying LVGL screen object — no separate display or touch driver setup required.

The core animation logic (slicing, easing, per-style transitions) is unchanged from the original Waveshare script and should be portable to any MicroPython + LVGL board with minimal changes — swap out the screen/driver init at the top for your target hardware.

| Board | Status |
|---|---|
| UNIHIKER K10 (ESP32-S3) | ✅ Tested, fast |
| Waveshare RP2350-Touch-LCD-2.8 | ✅ Original target, works (slower) |
| Other MicroPython + LVGL boards | 🤷 Should work, untested |

## Requirements

- UNIHIKER K10 flashed with MicroPython firmware (V0.9.8 or later)
- Thonny (or similar) for uploading files
- An RGB565 image data module (see below)

## Setup

1. Flash MicroPython onto the K10 following the [official guide](https://www.unihiker.com/wiki/K10/GettingStarted/gettingstarted_mpy/).
2. Convert your image to raw RGB565 bytes and generate a Python data module exposing:
   - `<name>_width`
   - `<name>_height`
   - `<name>_data` (raw RGB565 bytes)
3. Upload both your image data module and `k10_slice_dance.py` to the K10 via Thonny.
4. Set `DESIRED_MAP_FILE` in `k10_slice_dance.py` to your image module's base name.
5. Run:
   ```python
   import k10_slice_dance
   ```

## Animation Styles

- **slide** — all slices glide in from alternating left/right
- **cascade** — slices animate in one after another
- **zoom** — slices scale in from the center
- **bounce** — slices drop from above with an elastic settle
- **explode** — slices burst outward from center, then reassemble

## Tuning

- `NUM_SLICES` — more slices = finer-grained motion, more LVGL draw calls per frame. 10–20 runs smoothly on the K10.
- `ANIMATION_SPEED` — milliseconds per animation frame; lower is faster.
- `SLIDE_DISTANCE` — how far off-screen slices start before entering.

## Notes

- Image data is loaded fully into memory before animating — the K10's 8MB PSRAM comfortably handles images in the hundreds-of-KB range as raw RGB565 `.py` modules.
- Each slice is rendered as its own `lv.image` object attached to the K10's existing LVGL screen (`screen.__dict__['screen']`), so no custom display driver is needed.

## License

MIT — adapt freely for your own board.

