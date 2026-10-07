from stylekit import *
from brand import ORANGE, logo, sili
import sfx, random
r=random.Random(12)
BG='#0E0B09'
LENS='position:absolute;left:90px;top:420px;width:900px;height:900px;border-radius:50%;overflow:hidden;box-shadow:0 0 0 14px #1d1915,0 0 0 18px rgba(243,130,33,.5),0 0 80px rgba(243,130,33,.25)'
def ticks():
    return ''.join(f'<div style="position:absolute;left:{540-2}px;top:{420+450-470}px;width:4px;height:28px;background:rgba(243,130,33,.7);transform-origin:2px 470px;transform:rotate({a}deg)"></div>' for a in range(0,360,30))
def scene(id,s,d,tex,label,sub,extra=''):
    return f'''<section id="{id}" class="clip" data-start="{s}" data-duration="{d}" data-track-index="1"><div class="fill" style="background:{BG}"></div>
<div style="{LENS}"><div id="{id}t" style="position:absolute;inset:-160px">{tex}</div>
<div style="position:absolute;inset:0;border-radius:50%;box-shadow:inset 0 0 120px 40px rgba(0,0,0,.85)"></div>{extra}</div>{ticks()}
<div id="{id}l" style="position:absolute;left:80px;right:80px;top:1400px;text-align:center;font-family:Inter Display,sans-serif;font-weight:800;font-size:66px;color:#fff">{label}</div>
<div id="{id}s" style="position:absolute;left:80px;right:80px;top:1500px;text-align:center;font-family:Inter Display,sans-serif;font-weight:500;font-size:38px;color:{ORANGE}">{sub}</div>
<div style="position:absolute;left:0;right:0;top:150px;text-align:center;font-family:Inter Display,sans-serif;font-weight:700;font-size:28px;letter-spacing:.3em;color:rgba(255,255,255,.5)">ПОД ЛУПОЙ · SILI-CARE</div></section>'''
holes=f'<div style="position:absolute;inset:0;background-color:#EFB98A;background-image:radial-gradient(circle at 48% 45%,#1a0f08 0 26px,#8a5a34 30px,rgba(255,230,200,.9) 36px,transparent 40px);background-size:120px 120px"></div><div class="sheen" style="position:absolute;inset:0;background:linear-gradient(115deg,transparent 35%,rgba(255,255,255,.35) 48%,transparent 60%)"></div>'
cells=''.join(f'<div style="position:absolute;left:{r.randint(-40,1180)}px;top:{r.randint(-40,1180)}px;width:{(s:=r.randint(50,150))}px;height:{s}px;border-radius:50%;background:radial-gradient(circle,rgba(120,80,40,.55) 0 40%,#F6E1C2 62%,#FFF4E2 72%,transparent 74%)"></div>' for _ in range(170))
foam=f'<div style="position:absolute;inset:0;background:#F3DDBD">{cells}</div>'
fib=''.join(f'<path d="M{r.randint(-100,1300)} {r.randint(-100,1300)} q{r.randint(-300,300)} {r.randint(-300,300)} {r.randint(-500,500)} {r.randint(-500,500)}" stroke="rgba({r.choice(["255,255,255","180,205,240","220,230,245"])},.9)" stroke-width="{r.choice([3,4,6])}" fill="none"/>' for _ in range(160))
fibers=f'<div style="position:absolute;inset:0;background:#DCE6F2"><svg viewBox="0 0 1220 1220" style="position:absolute;inset:0;width:100%;height:100%">{fib}</svg></div>'
drop='<div id="dp" style="position:absolute;left:330px;top:300px;width:240px;height:240px;border-radius:50%;background:radial-gradient(circle at 35% 30%,rgba(255,240,200,.95),rgba(226,168,87,.9) 55%,rgba(180,110,40,.85));box-shadow:0 20px 40px rgba(0,0,0,.35)"></div>'
beads=''.join(f'<div class="bd" style="position:absolute;left:{x}px;top:{y}px;width:{s}px;height:{s}px;border-radius:50%;background:radial-gradient(circle at 35% 30%,rgba(255,255,255,.95),rgba(190,215,240,.55) 45%,rgba(120,150,190,.35));box-shadow:0 10px 18px rgba(0,0,0,.25)"></div>' for x,y,s in [(180,220,140),(520,160,90),(640,420,170),(300,520,110),(560,640,80),(200,700,120)])
film=f'<div style="position:absolute;inset:0;background:linear-gradient(135deg,#E9EEF3,#C9D3DE)"></div><div class="sheen" style="position:absolute;inset:0;background:linear-gradient(115deg,transparent 30%,rgba(255,255,255,.6) 45%,transparent 60%)"></div>'
D=3.3; T=[2.2+i*D for i in range(4)]
body=f'''<section id="h0" class="clip" data-start="0" data-duration="2.2" data-track-index="1"><div class="fill" style="background:{BG}"></div>
<div id="lz" style="{LENS};background:radial-gradient(circle,#2a221b,#0E0B09)"></div>{ticks()}
<div id="hk" style="position:absolute;left:60px;right:60px;top:760px;text-align:center;font-family:Inter Display,sans-serif;font-weight:800;font-size:90px;line-height:1.05;color:#fff">Что касается<br><span style="color:{ORANGE}">вашей кожи?</span></div></section>
{scene("a",T[0],D,holes,"Перфорированный силикон","касается кожи — и мягко отпускает")}
{scene("b",T[1],D,foam,"Мягкая пена","поддерживает влажную среду у раны")}
{scene("c",T[2],D,fibers,"Суперабсорбент","забирает излишек влаги и держит внутри",drop)}
{scene("d",T[3],D,film,"Защитный верхний слой","барьер снаружи",beads)}
<section id="z" class="clip" data-start="{T[3]+D}" data-duration="4.4" data-track-index="1"><div class="fill" style="background:{BG}"></div>
<div id="zp" style="position:absolute;left:330px;top:430px">{sili(0,0,420,"transform:rotate(-6deg)")}</div>
<div id="z1" style="position:absolute;left:60px;right:60px;top:980px;text-align:center;font-family:Inter Display,sans-serif;font-weight:800;font-size:84px;line-height:1.1;color:#fff">5 слоёв.<br><span style="color:{ORANGE}">Одна задача —<br>не ранить.</span></div>
<div id="z2" style="position:absolute;left:0;right:0;top:1340px;text-align:center;filter:drop-shadow(0 0 20px rgba(243,130,33,.4))">{logo(96)}</div>
<div style="position:absolute;left:80px;right:80px;bottom:110px;text-align:center;font-size:22px;color:rgba(255,255,255,.4)">Медицинское изделие. Применение — по назначению специалиста. Иллюстрация.</div></section>'''
js='tl.from("#lz",{scale:.3,opacity:0,duration:.6,ease:"back.out(1.4)"},.05).from("#hk",{opacity:0,y:30,duration:.5},.5);'
ev=[(.05,sfx.whoosh(.6,.25)),(.6,sfx.chime(440,.15,2))]
for k,t in zip('abcd',T):
    js+=f'tl.fromTo("#{k}t",{{filter:"blur(18px)",scale:1.25,x:60,y:40}},{{filter:"blur(0px)",scale:1.05,x:-60,y:-40,duration:{D},ease:"power1.out"}},{t});'
    js+=f'tl.fromTo("#{k}t",{{filter:"blur(18px)"}},{{filter:"blur(0px)",duration:.9,ease:"power2.out"}},{t});'
    js+=f'tl.from("#{k}l",{{opacity:0,y:30,duration:.4}},{t+.6}).from("#{k}s",{{opacity:0,duration:.4}},{t+1.0});'
    js+=f'tl.fromTo("#{k} .sheen",{{xPercent:-60}},{{xPercent:60,duration:{D},ease:"none"}},{t});'
    ev+=[(t-.2,sfx.whoosh(.5,.18)),(t+.2,sfx.tear(1.2,.06)),(t+.7,sfx.chime([523,587,659,784][ 'abcd'.index(k)],.12,2))]
js+=f'tl.to("#dp",{{scale:.15,opacity:0,duration:1.5,ease:"power2.in"}},{T[2]+1.3});'
ev+=[(T[2]+1.3,sfx.chime(330,.18,1.0)),(T[2]+2.6,sfx.chime(262,.12,1.0))]
js+=f'tl.from("#d .bd",{{scale:0,duration:.4,stagger:.15,ease:"back.out(2)"}},{T[3]+.4}).to("#d .bd",{{y:120,duration:2.2,ease:"power1.in",stagger:.1}},{T[3]+1.1});'
TZ=T[3]+D
js+=f'tl.from("#zp",{{scale:3,opacity:0,filter:"blur(20px)",duration:.9,ease:"power3.out"}},{TZ}).from("#z1",{{opacity:0,y:30,duration:.5}},{TZ+.8}).from("#z2",{{opacity:0,duration:.5}},{TZ+1.4});'
ev+=[(TZ,sfx.whoosh(.9,.3)),(TZ+.8,sfx.boom(.6)),(TZ+1.0,sfx.chime(659,.18,3))]
DUR=round(TZ+4.4,1)
shots=style_reel('s4_macro_asmr',DUR,body,js,'Под лупой',ev,pad=(110,164.8,220,277.2),pad_amp=.05,check=(T[0]+1.8,1.2,T[0]+1.8,T[1]+1.8,T[3]+1.5,TZ+2.5),bg=BG)
strip(shots,'kp/chk_s4.jpg',2400); print('ok',DUR)
