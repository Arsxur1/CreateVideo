# Каркас кампании «Кожа помнит»: сборка, проверка, рендер, выгрузка
import os, shutil, subprocess, glob
from gen_lib import page
from brand import logo, header, wave, ORANGE, MAGENTA, BLUE, INK, GREY, RED, STAGE, YELLOW, sili
from lineart import svg
ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.abspath(os.path.join(ROOT, '../../deliverables/yafho-silicare-instagram/v6_campaign'))
HF = ['npx', '-y', 'hyperframes@0.8.139']
FOOT = 'Медицинское изделие. Применение — по назначению специалиста.'

def _dir(name):
    d = os.path.join(ROOT, 'kp', name); os.makedirs(d, exist_ok=True)
    shutil.copy(os.path.join(ROOT, 'node_modules/gsap/dist/gsap.min.js'), d)
    shutil.copy(os.path.join(ROOT, 'shared.css'), d)
    return d

def _snap(d, times):
    shutil.rmtree(os.path.join(d, 'snapshots'), ignore_errors=True)
    subprocess.run(HF + ['snapshot', '--at', ','.join(str(t) for t in times)], cwd=d, capture_output=True, timeout=600)
    return sorted(glob.glob(os.path.join(d, 'snapshots', 'frame-*.png')))

def carousel(name, slides, title):
    d = _dir(name)
    open(os.path.join(d, 'index.html'), 'w').write(page(slides, 1080, 1350, title))
    shots = _snap(d, [i + .5 for i in range(len(slides))])[:len(slides)]
    od = os.path.join(OUT, name); os.makedirs(od, exist_ok=True)
    for f in glob.glob(os.path.join(od, 'slide*.png')): os.remove(f)
    for i, s in enumerate(shots): shutil.copy(s, os.path.join(od, f'slide{i+1}.png'))
    return od

CSS = '''#root{position:relative;width:1080px;height:1920px;overflow:hidden}
.cap{position:absolute;left:70px;right:70px;text-align:center;font-family:'Inter Display';font-weight:800;letter-spacing:-0.03em;line-height:1.08;color:#2B2B2B}
.sub{position:absolute;left:90px;right:90px;text-align:center;font-family:Inter;font-weight:500;color:#555;line-height:1.4}
#pbar{position:absolute;left:0;top:0;height:10px;width:1080px;background:#F38221;transform-origin:left;z-index:50}'''

def reel(name, dur, body, js, title, check=(), render=True):
    d = _dir(name)
    html = f'''<!doctype html><html lang="ru"><head><meta charset="UTF-8"><title>{title}</title><script src="gsap.min.js"></script><link rel="stylesheet" href="shared.css"><style>{CSS}</style></head><body>
<div id="root" data-composition-id="main" data-width="1080" data-height="1920" data-duration="{dur}">
<div class="fill" style="background:#fff;z-index:0"></div>{body}
<div id="pbar" class="clip" data-start="0" data-duration="{dur}" data-track-index="9" style="inset:auto;height:10px"></div></div>
<script>window.__timelines={{}};const tl=gsap.timeline({{paused:true}});tl.fromTo("#pbar",{{scaleX:0}},{{scaleX:1,duration:{dur},ease:"none"}},0);
{js}
tl.to({{}},{{duration:.01}},{dur-0.01});window.__timelines["main"]=tl;</script></body></html>'''
    open(os.path.join(d, 'index.html'), 'w').write(html)
    shots = _snap(d, check) if check else []
    od = os.path.join(OUT, name); os.makedirs(od, exist_ok=True)
    if render:
        out = os.path.join(od, f'{name}.mp4')
        r = subprocess.run(HF + ['render', '--quality', 'high', '--output', out], cwd=d, capture_output=True, text=True, timeout=1200)
        if r.returncode != 0: print(r.stdout[-2000:], r.stderr[-2000:])
        cover_t = check[0] if check else 1
        subprocess.run(['ffmpeg','-loglevel','error','-y','-ss',str(cover_t),'-i',out,'-frames:v','1',os.path.join(od,'cover.png')])
    return shots

def strip(files, out, width=2000):
    files = [f for f in files if f]
    args = []
    for f in files: args += ['-i', f]
    subprocess.run(['ffmpeg','-loglevel','error','-y',*args,'-filter_complex',f'hstack={len(files)},scale={width}:-1',out]) if len(files)>1 else shutil.copy(files[0], out)
    return out

def clip(id, s, d, inner, track=1, bg='#fff'):
    return f'<section id="{id}" class="clip" data-start="{s}" data-duration="{d}" data-track-index="{track}"><div class="fill" style="background:{bg}"></div>{inner}</section>'

def slide_frame(label, idx, inner, footer=True, bg='#fff'):
    f = f'<div style="position:absolute;right:80px;bottom:78px;font-size:18px;color:#999;max-width:440px;text-align:right">{FOOT}</div>' if footer else ''
    return f'<div class="fill" style="background:{bg};color:{INK}"></div>{header(label, idx)}{inner}<div style="position:absolute;left:80px;bottom:64px">{logo(46)}</div>{f}'
