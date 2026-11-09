#!/usr/bin/env python3
"""Genera WangFont.cs (font reale del terminale 2236) e GameData.cs (sprite/stringhe HEX)
dal listato pulito di @MRTIAN e dal sorgente di WangEmu. Niente trascrizione a mano."""
import re, sys, pathlib, json

LIST = pathlib.Path(r"E:\TEMP\Claude\MartianNiakwa\mrtian_orig_list.txt")
CHARSET = pathlib.Path(r"E:\Dropbox\FAUSTO\WangEmu3.0\src\UiCrt_Charset.cpp")
OUT = pathlib.Path(__file__).resolve().parent.parent

# ---------- font ----------
tables, cur = {}, None
for l in CHARSET.read_text(encoding="latin-1").splitlines():
    m = re.search(r'uint8 (\w+)\[\]', l)
    if m:
        cur = m.group(1); tables[cur] = []; continue
    m = re.search(r'/\*[0-9A-F]{3}:.*\*/\s+0x([0-9A-Fa-f]{2})', l)
    if m and cur: tables[cur].append(int(m.group(1), 16))
assert len(tables['chargen']) == 1024 and len(tables['chargen_2236_alt']) == 1024

# ---------- listato ----------
prog = {}
for l in LIST.read_text(encoding="latin-1").splitlines():
    if l.startswith('#') or not l.strip(): continue
    m = re.match(r'(\d+)(.*)$', l)
    prog[int(m.group(1))] = m.group(2)

# tutti i letterali HEX( ) per riga, in ordine
hx = {}
for ln, txt in prog.items():
    h = re.findall(r'HEX\(([0-9A-Fa-f]+)\)', txt)
    if h: hx[ln] = h

# sprite DEFFN: PRINT AT(riga,Y[+k][,n]);[HEX(..)]
opre = re.compile(r"PRINT AT\((\d+),(Y1|Y|Z)(?:\+(\d+))?(?:,(\d+))?\);?(?:HEX\(([0-9A-Fa-f]+)\);?)?")
def ops(txt):
    out = []
    for m in opre.finditer(txt):
        out.append((int(m.group(1)), int(m.group(3) or 0), int(m.group(4) or 0), m.group(5) or ""))
    return out

spr = {}
lns = sorted(prog)
i = 0
while i < len(lns):
    m = re.match(r"DEFFN '(\d+)", prog[lns[i]])
    if m and m.group(1) not in ('126', '127'):
        name = m.group(1); body = []
        i += 1
        while i < len(lns) and not prog[lns[i]].startswith('RETURN'):
            body += ops(prog[lns[i]]); i += 1
        spr[name] = body
    i += 1
# esplosione del cannone: righe 4210..4300 (stesso formato, colonna Y1)
for ln in range(4210, 4311, 10):
    spr[f"L{ln}"] = ops(prog[ln])


js = "// generato da tools/gen_data.py" + chr(10)
js += "const FONT_N=" + json.dumps(tables['chargen']) + ";" + chr(10)
js += "const FONT_A=" + json.dumps(tables['chargen_2236_alt']) + ";" + chr(10)
js += "const SPR=" + json.dumps({k:[list(o) for o in v] for k,v in spr.items()}) + ";" + chr(10)
js += "const HX=" + json.dumps({str(k):v for k,v in hx.items()}) + ";" + chr(10)
(OUT/"data.js").write_text(js, encoding="utf-8")
print("ok", len(js))
