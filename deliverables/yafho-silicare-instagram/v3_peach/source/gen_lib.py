# Shared helpers for building HyperFrames still/slide compositions
TOP = lambda idx, color='inherit': f'<div class="top" style="color:{color}"><div class="brand">Yafho <i>· Silicare</i></div><div class="lab" style="opacity:.6">{idx}</div></div>'

def dress(x, y, s, extra=''):
    return f'<div class="dress" style="left:{x}px;top:{y}px;width:{s}px;height:{s}px;{extra}"><div class="core"></div><div class="gloss"></div></div>'

def layers(cx, cy, active=None, gap=78, scale=1.0):
    # 4 layers bottom->top in DOM order: silicone contact (bottom), foam, SAP pad, film (top)
    spec = [
        ('sil', 'linear-gradient(135deg,rgba(205,235,226,.95),rgba(150,205,190,.9))', 'repeating-linear-gradient(45deg,rgba(255,255,255,.35) 0 2px,transparent 2px 22px)'),
        ('foam', '#F3ECE1', 'radial-gradient(circle,rgba(150,125,95,.35) 2px,transparent 2.6px)'),
        ('sap', 'linear-gradient(135deg,#FFFFFF,#E9F1EF)', 'repeating-linear-gradient(0deg,rgba(18,58,64,.10) 0 3px,transparent 3px 12px)'),
        ('film', 'rgba(255,255,255,.28)', 'linear-gradient(135deg,rgba(255,255,255,.55),rgba(255,255,255,0) 60%)'),
    ]
    out = [f'<div class="iso" style="left:{cx}px;top:{cy}px;transform:scale({scale})">']
    n = len(spec)
    for i, (k, bg, pat) in enumerate(spec):
        off = (n - 1 - i) * gap - (n - 1) * gap / 2  # bottom layer lowest
        op = 1 if (active is None or active == i) else .22
        border = '3px solid #E2573B' if active == i else '2px solid rgba(255,255,255,.55)'
        sz = 420 if k != 'sap' else 300
        o = (420 - sz) // 2
        out.append(f'<div style="position:absolute;left:0;top:{off:.0f}px;opacity:{op}"><div class="layer" style="left:{-210+o}px;top:{-210+o}px;width:{sz}px;height:{sz}px;background:{pat},{bg};background-size:{"18px 18px," if k=="foam" else ""}auto;border:{border};box-shadow:0 30px 60px -20px rgba(0,0,0,.45)"></div></div>')
    out.append('</div>')
    return ''.join(out)

def page(slides, w, h, title, extra_head='', timeline_js=''):
    clips = []
    for i, s in enumerate(slides):
        clips.append(f'<section id="s{i}" class="clip" data-start="{i}" data-duration="1" data-track-index="1">{s}</section>')
    return f'''<!doctype html><html lang="ru"><head><meta charset="UTF-8"><title>{title}</title>
<script src="gsap.min.js"></script><link rel="stylesheet" href="shared.css">{extra_head}
<style>#root{{position:relative;width:{w}px;height:{h}px;overflow:hidden}}</style></head>
<body><div id="root" data-composition-id="main" data-width="{w}" data-height="{h}" data-duration="{len(slides)}">
{''.join(clips)}
</div><script>window.__timelines={{}};const tl=gsap.timeline({{paused:true}});tl.to({{}},{{duration:{len(slides)}}});window.__timelines["main"]=tl;</script></body></html>'''
