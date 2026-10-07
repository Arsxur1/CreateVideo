# Кинематографичный визуальный набор: тьма, свет, зерно, частицы, кинетика
import random
from brand import ORANGE, logo
DARK = '#0B0C10'
def backdrop(seed=1, n=46):
    r = random.Random(seed)
    parts = ''.join(f'<div class="pt" style="position:absolute;left:{r.randint(0,1080)}px;top:{r.randint(0,1920)}px;width:{(s:=r.choice([2,3,3,4,6]))}px;height:{s}px;border-radius:50%;background:rgba(255,{r.randint(150,210)},{r.randint(90,150)},{r.uniform(.25,.8):.2f});filter:blur({0 if s<5 else 1}px)"></div>' for _ in range(n))
    return f'''<div class="fill" style="background:radial-gradient(120% 80% at 50% 45%,#1A1410 0%,{DARK} 60%,#050506 100%)"></div>
<div class="fill pfield">{parts}</div>
<div class="fill" style="pointer-events:none;background:radial-gradient(ellipse at center,transparent 55%,rgba(0,0,0,.75) 100%)"></div>'''
GRAIN = '<div class="fill" style="z-index:40;pointer-events:none;opacity:.10;mix-blend-mode:overlay;background-image:repeating-radial-gradient(circle at 13% 27%,#fff 0 1px,transparent 1px 3px),repeating-radial-gradient(circle at 71% 63%,#000 0 1px,transparent 1px 4px)"></div>'
def glow_svg(paths, size, idp, stroke=5, accent=ORANGE, base='#F5E6D8'):
    """paths: list of (d, accent). Каждая линия рисуется трижды: широкое свечение + ореол + яркое ядро."""
    out=['<defs><filter id="gb'+idp+'" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="9"/></filter><filter id="gs'+idp+'" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="3"/></filter></defs>']
    for item in paths:
        d,acc = item[0],item[1]; tr = f' transform="{item[2]}"' if len(item)>2 else ''
        c = accent if acc else base; w = stroke*(2 if acc else 1)
        cls = 'ga' if acc else 'gi'
        out.append(f'<path class="{cls}" pathLength="1" d="{d}" fill="none" stroke="{accent if acc else "#FFB070"}" stroke-opacity="{.9 if acc else .35}" stroke-width="{w*5}" stroke-linecap="round" stroke-linejoin="round" filter="url(#gb{idp})"{tr}/>')
        out.append(f'<path class="{cls}" pathLength="1" d="{d}" fill="none" stroke="{c}" stroke-opacity=".8" stroke-width="{w*2}" stroke-linecap="round" stroke-linejoin="round" filter="url(#gs{idp})"{tr}/>')
        out.append(f'<path class="{cls}" pathLength="1" d="{d}" fill="none" stroke="{"#FFE3C6" if acc else "#FFFFFF"}" stroke-width="{w*.8}" stroke-linecap="round" stroke-linejoin="round"{tr}/>')
    return f'<svg id="{idp}" viewBox="0 0 600 600" width="{size}" height="{size}" style="overflow:visible">{"".join(out)}</svg>'
def kin(id, words, top, size=110, color='#fff', accent_idx=(), extra=''):
    """Кинетический заголовок: каждое слово — отдельный блок для «удара»."""
    ws = ''.join(f'<span class="kw" style="display:inline-block;margin:0 .14em;{"color:"+ORANGE+";text-shadow:0 0 30px rgba(243,130,33,.65)" if i in accent_idx else ""}">{w}</span>' for i,w in enumerate(words))
    return f'<div id="{id}" style="position:absolute;left:60px;right:60px;top:{top}px;text-align:center;font-family:\'Inter Display\';font-weight:800;letter-spacing:-0.03em;line-height:1.05;font-size:{size}px;color:{color};text-shadow:0 4px 30px rgba(0,0,0,.6);{extra}">{ws}</div>'
def slam_js(id, t, stagger=.12):
    return f'tl.from("#{id} .kw",{{opacity:0,scale:1.8,filter:"blur(12px)",duration:.35,stagger:{stagger},ease:"power3.out"}},{t});'
def draw_js(idp, t, dur=1.6, acc_t=None, acc_dur=.8):
    s = f'tl.fromTo("#{idp} .gi",{{strokeDasharray:1,strokeDashoffset:1}},{{strokeDashoffset:0,duration:{dur},ease:"power2.inOut"}},{t});'
    if acc_t is not None:
        s += f'tl.fromTo("#{idp} .ga",{{strokeDasharray:1,strokeDashoffset:1,opacity:0}},{{strokeDashoffset:0,opacity:1,duration:{acc_dur},ease:"power2.out"}},{acc_t});'
    return s
def flash(id, t, color='#FFE3C6'):
    return (f'<div id="{id}" class="fill" style="z-index:45;background:{color};opacity:0;pointer-events:none"></div>',
            f'tl.fromTo("#{id}",{{opacity:.85}},{{opacity:0,duration:.35,ease:"power2.out"}},{t});')
def drift_js(t0, dur):
    return f'tl.to(".pfield",{{y:-120,duration:{dur},ease:"none"}},{t0});'
def end_card(id, line1, line2, cta, seed=9):
    fs = 104 if max(len(line1),len(line2))<=19 else 80
    return f'''{backdrop(seed)}
{kin(id+"a", line1.split(), 470, fs, extra='white-space:nowrap')}{kin(id+"b", line2.split(), 470+int(fs*1.25), fs, extra='white-space:nowrap', accent_idx=tuple(range(len(line2.split()))))}
<div id="{id}l" style="position:absolute;left:0;right:0;top:1000px;text-align:center;filter:drop-shadow(0 0 24px rgba(243,130,33,.45))">{logo(120,ORANGE)}</div>
<div id="{id}c" style="position:absolute;left:90px;right:90px;top:1250px;text-align:center;font-size:36px;color:#F2E6DA;font-weight:500;line-height:1.45">{cta}</div>
<div style="position:absolute;left:90px;right:90px;bottom:120px;text-align:center;font-size:22px;color:rgba(255,255,255,.45)">Медицинское изделие. Применение — по назначению специалиста.</div>'''
