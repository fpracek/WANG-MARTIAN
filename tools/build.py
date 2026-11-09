import pathlib
r=pathlib.Path(__file__).resolve().parent.parent
t=(r/'template.html').read_text(encoding='utf-8')
d=(r/'data.js').read_text(encoding='utf-8')
(r/'index.html').write_text(t.replace('/*DATA*/',d),encoding='utf-8')
print('index.html', (r/'index.html').stat().st_size, 'bytes')
