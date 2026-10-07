import os, subprocess
from kp import _dir, _snap, OUT, HF, strip
import sfx
SOUT = OUT.replace('v6_campaign','v8_styles')
def style_reel(name, dur, body, js, title, events, pad=None, pad_amp=.05, check=(), bg='#fff', extra_css='', grain='', outdir=None):
    d=_dir(name)
    css='#root{position:relative;width:1080px;height:1920px;overflow:hidden;background:%s} #pbar{position:absolute;left:0;top:0;height:8px;width:1080px;background:#F38221;transform-origin:left;z-index:50}'%bg + extra_css
    g = f'<div class="clip" data-start="0" data-duration="{dur}" data-track-index="8" style="z-index:40;pointer-events:none">{grain}</div>' if grain else ''
    html=f'''<!doctype html><html lang="ru"><head><meta charset="UTF-8"><title>{title}</title><script src="gsap.min.js"></script><link rel="stylesheet" href="shared.css"><style>{css}</style></head><body>
<div id="root" data-composition-id="main" data-width="1080" data-height="1920" data-duration="{dur}"><div class="fill" style="background:{bg};z-index:0"></div>{body}{g}
<div id="pbar" class="clip" data-start="0" data-duration="{dur}" data-track-index="9" style="inset:auto;height:8px"></div></div>
<script>window.__timelines={{}};const tl=gsap.timeline({{paused:true}});tl.fromTo("#pbar",{{scaleX:0}},{{scaleX:1,duration:{dur},ease:"none"}},0);
{js}
tl.to({{}},{{duration:.01}},{dur-0.01});window.__timelines["main"]=tl;</script></body></html>'''
    open(os.path.join(d,'index.html'),'w').write(html)
    shots=_snap(d,check) if check else []
    od=os.path.join(outdir or SOUT,name); os.makedirs(od,exist_ok=True)
    silent=os.path.join(d,'silent.mp4'); wav=os.path.join(d,'sound.wav'); out=os.path.join(od,f'{name}.mp4')
    r=subprocess.run(HF+['render','--quality','high','--output',silent],cwd=d,capture_output=True,text=True,timeout=1500)
    if r.returncode: print(r.stdout[-1500:],r.stderr[-1500:])
    sfx.mix(dur,events,wav,pad,pad_amp)
    subprocess.run(['ffmpeg','-loglevel','error','-y','-i',silent,'-i',wav,'-c:v','copy','-c:a','aac','-b:a','192k','-shortest',out])
    if check: subprocess.run(['ffmpeg','-loglevel','error','-y','-ss',str(check[0]),'-i',out,'-frames:v','1',os.path.join(od,'cover.png')])
    return shots
def kick(a=.8):
    import numpy as np
    t=np.arange(int(.35*sfx.SR))/sfx.SR
    return a*(np.sin(2*np.pi*(55+120*np.exp(-t*30))*t)*np.exp(-t*9)+.25*sfx.hp(sfx.rng.standard_normal(len(t)),3000)*np.exp(-t*80))
