import os, shutil, subprocess, glob
from kp import _dir, _snap, OUT, HF, strip
from cine import GRAIN, DARK
import lineart
def art_paths(key):
    a = lineart.ART[key]()
    if a.get('twin'):
        return [(d,acc,'translate(-75,0)') for d,acc in a['paths']] + [(d,acc,'translate(675,25) scale(-1,1)') for d,acc in a['paths'] if not acc]
    return a['paths']
CSS = '#root{position:relative;width:1080px;height:1920px;overflow:hidden;background:%s} .lab2{position:absolute;left:64px;top:90px;font-size:24px;font-weight:700;color:#F38221;letter-spacing:.12em;text-transform:uppercase} #pbar{position:absolute;left:0;top:0;height:8px;width:1080px;background:#F38221;transform-origin:left;z-index:50;box-shadow:0 0 18px #F38221}' % DARK
def cine_reel(name, dur, body, js, title, audio_events, pad=(110,164.8,220,261.6), check=(), pad_amp=.06):
    d = _dir(name)
    html = f'''<!doctype html><html lang="ru"><head><meta charset="UTF-8"><title>{title}</title><script src="gsap.min.js"></script><link rel="stylesheet" href="shared.css"><style>{CSS}</style></head><body>
<div id="root" data-composition-id="main" data-width="1080" data-height="1920" data-duration="{dur}">
<div class="fill" style="background:{DARK};z-index:0"></div>{body}
<div class="clip" id="grainc" data-start="0" data-duration="{dur}" data-track-index="8" style="z-index:40;pointer-events:none">{GRAIN}</div>
<div id="pbar" class="clip" data-start="0" data-duration="{dur}" data-track-index="9" style="inset:auto;height:8px"></div></div>
<script>window.__timelines={{}};const tl=gsap.timeline({{paused:true}});tl.fromTo("#pbar",{{scaleX:0}},{{scaleX:1,duration:{dur},ease:"none"}},0);
{js}
tl.to({{}},{{duration:.01}},{dur-0.01});window.__timelines["main"]=tl;</script></body></html>'''
    open(os.path.join(d,'index.html'),'w').write(html)
    shots = _snap(d, check) if check else []
    od = os.path.join(OUT.replace('v6_campaign','v7_cinematic'), name); os.makedirs(od, exist_ok=True)
    silent = os.path.join(d,'silent.mp4'); wav = os.path.join(d,'sound.wav'); out = os.path.join(od, f'{name}.mp4')
    r = subprocess.run(HF+['render','--quality','high','--output',silent], cwd=d, capture_output=True, text=True, timeout=1500)
    if r.returncode: print(r.stdout[-1500:], r.stderr[-1500:])
    import sfx; sfx.mix(dur, audio_events, wav, pad, pad_amp)
    subprocess.run(['ffmpeg','-loglevel','error','-y','-i',silent,'-i',wav,'-c:v','copy','-c:a','aac','-b:a','192k','-shortest',out])
    if check: subprocess.run(['ffmpeg','-loglevel','error','-y','-ss',str(check[0]),'-i',out,'-frames:v','1',os.path.join(od,'cover.png')])
    return shots
