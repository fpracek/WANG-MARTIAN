# WANG-MARTIAN

**Martian War** — the classic Wang 2200 BASIC game by Ralf Berger (1980/81), ported to a single-file web page.
Open [`index.html`](index.html) in any browser (desktop, phone, tablet; touch controls are shown automatically).

## Controls
| Key | Action |
|---|---|
| ← / `4` | move left |
| → / `6` | move right |
| ↓ / `5` | stop |
| Space / ↑ / `8` | fire |
| Enter | confirm / play again |
| Esc | restart |

Any key skips the opening "humans running in" animation.

## How it works
The page contains a small emulation of the Wang 2236 terminal (80x24, alternate character set with block graphics,
bright/blink/underline/inverse attributes, `BOX` overlays) and a line-by-line port of the original `@MRTIAN` program,
keeping the Wang BASIC-2 semantics that matter (an `IF..THEN` governs only one statement; `KEYIN` never blocks).

## Files
- `index.html` – the game (built file, self-contained)
- `template.html` – page, terminal emulation and game logic
- `data.js` – generated: terminal font and sprite/HEX data
- `tools/gen_data.py` – regenerates `data.js` from the original BASIC listing and the WangEmu character generator dump
- `tools/build.py` – injects `data.js` into `template.html` -> `index.html`

Rebuild: `python tools/gen_data.py && python tools/build.py` (the paths inside `gen_data.py` point to the author's machine; adjust them).

## Credits
- Game: Ralf Berger, Wang Laboratories (1980/81). This repository only contains a port for preservation and study.
- Terminal character generator tables: [WangEmu](https://github.com/jimbattle/wangemu) by Jim Battle (MIT, see `NOTICE`).
