src=open('s4_macro.py').read(); exec(src[:src.index("holes=")])
from v9_common import V9
from kp import strip
mesh='<div style="position:absolute;inset:0;background-color:#F4E3CC;background-image:radial-gradient(circle at 50% 50%,#1a0f08 0 34px,#9a7350 38px,transparent 44px);background-size:110px 110px"></div><div class="sheen" style="position:absolute;inset:0;background:linear-gradient(115deg,transparent 35%,rgba(255,255,255,.4) 48%,transparent 60%)"></div>'
gel='<div style="position:absolute;inset:0;background:radial-gradient(ellipse at 40% 35%,#FBE3C8,#EDBF92 60%,#D9A272)"></div><div style="position:absolute;inset:0;opacity:.35;background-image:radial-gradient(rgba(255,255,255,.9) 2px,transparent 3px);background-size:26px 26px"></div><div class="sheen" style="position:absolute;inset:0;background:linear-gradient(115deg,transparent 30%,rgba(255,255,255,.55) 45%,transparent 60%)"></div>'
nfib=''.join(f'<path d="M{r.randint(-100,1300)} {r.randint(-100,1300)} l{r.randint(-600,600)} {r.randint(-600,600)}" stroke="rgba(255,255,255,.95)" stroke-width="{r.choice([4,5,7])}" stroke-linecap="round"/>' for _ in range(220))
nonw=f'<div style="position:absolute;inset:0;background:#E7E9EE"><svg viewBox="0 0 1220 1220" style="position:absolute;inset:0;width:100%;height:100%">{nfib}</svg></div><div style="position:absolute;inset:0;background-image:radial-gradient(circle,rgba(243,196,150,.65) 10px,transparent 12px);background-size:90px 90px"></div>'
hyd='<div style="position:absolute;inset:0;background:radial-gradient(circle at 45% 40%,rgba(225,240,255,1),rgba(170,200,235,1) 60%,rgba(120,160,210,1))"></div>'+''.join(f'<div class="bd" style="position:absolute;left:{x}px;top:{y}px;width:{s}px;height:{s}px;border-radius:50%;background:radial-gradient(circle at 35% 30%,rgba(255,255,255,.95),rgba(200,225,250,.4) 50%,rgba(140,175,220,.2));box-shadow:0 8px 16px rgba(40,70,120,.25)"></div>' for x,y,s in [(200,260,160),(560,200,110),(680,480,190),(300,600,130),(560,760,90),(240,880,120),(760,820,70)])+'<div class="sheen" style="position:absolute;inset:0;background:linear-gradient(115deg,transparent 30%,rgba(255,255,255,.5) 45%,transparent 60%)"></div>'
P=[('Silicone Wound Contact Layer','дерматология · самая хрупкая кожа',mesh),('Silicone Scar Sheet','пластика · акушерство · рубцы',gel),('Silicone Nonwoven','мягкая фиксация на хрупкой коже',nonw),('Hydrogel Dressing','влажная среда для сухих ран',hyd)]
D=3.2; T=[2.4+i*D for i in range(4)]
body=f'''<section id="h0" class="clip" data-start="0" data-duration="2.4" data-track-index="1"><div class="fill" style="background:{BG}"></div>
<div id="lz" style="{LENS};background:radial-gradient(circle,#2a221b,#0E0B09)"></div>{ticks()}
<div id="hk" style="position:absolute;left:60px;right:60px;top:740px;text-align:center;font-family:Inter Display,sans-serif;font-weight:800;font-size:92px;line-height:1.05;color:#fff">Одна лупа —<br><span style="color:{ORANGE}">четыре отделения.</span></div></section>'''
js='tl.from("#lz",{scale:.3,opacity:0,duration:.6,ease:"back.out(1.4)"},.05).from("#hk",{opacity:0,y:30,duration:.5},.5);'
ev=[(.05,sfx.whoosh(.6,.25)),(.6,sfx.chime(440,.15,2))]
for i,((n,dep,tex),t) in enumerate(zip(P,T)):
    k='abcd'[i]; body+=scene(k,t,D,tex,n,dep).replace('font-weight:800;font-size:66px;color:#fff','font-weight:800;font-size:56px;color:#fff;white-space:nowrap')
    js+=f'tl.fromTo("#{k}t",{{filter:"blur(18px)",scale:1.25,x:60,y:40}},{{filter:"blur(0px)",scale:1.05,x:-60,y:-40,duration:{D},ease:"power1.out"}},{t});tl.fromTo("#{k}t",{{filter:"blur(18px)"}},{{filter:"blur(0px)",duration:.9}},{t});'
    js+=f'tl.from("#{k}l",{{opacity:0,y:30,duration:.4}},{t+.6}).from("#{k}s",{{opacity:0,duration:.4}},{t+1.0}).fromTo("#{k} .sheen",{{xPercent:-60}},{{xPercent:60,duration:{D},ease:"none"}},{t});'
    ev+=[(t-.2,sfx.whoosh(.5,.18)),(t+.2,sfx.tear(1.0,.05)),(t+.7,sfx.chime([523,587,659,784][i],.12,2))]
js+=f'tl.from("#d .bd",{{scale:0,duration:.4,stagger:.12,ease:"back.out(2)"}},{T[3]+.3});'
TZ=T[3]+D
body+=f'''<section id="z" class="clip" data-start="{TZ}" data-duration="4.6" data-track-index="1"><div class="fill" style="background:{BG}"></div>
<div id="z1" style="position:absolute;left:60px;right:60px;top:560px;text-align:center;font-family:Inter Display,sans-serif;font-weight:800;font-size:84px;line-height:1.1;color:#fff">Роддом. Пластика.<br>Дерматология. Хирургия.<br><span style="color:{ORANGE}">Одна линейка.</span></div>
<div id="z2" style="position:absolute;left:0;right:0;top:1000px;text-align:center;filter:drop-shadow(0 0 20px rgba(243,130,33,.4))">{logo(100)}</div>
<div id="z3" style="position:absolute;left:80px;right:80px;top:1200px;text-align:center;font-family:Inter Display,sans-serif;font-size:40px;color:#fff;font-weight:600">Дистрибьюторам и клиникам:<br>напишите <span style="color:{ORANGE}">«КАТАЛОГ»</span> в директ</div>
<div style="position:absolute;left:80px;right:80px;bottom:110px;text-align:center;font-size:22px;color:rgba(255,255,255,.4)">Медицинские изделия. Применение — по назначению специалиста. Иллюстрация.</div></section>'''
js+=f'tl.from("#z1",{{opacity:0,y:30,duration:.5}},{TZ+.1}).from("#z2",{{opacity:0,duration:.5}},{TZ+.8}).from("#z3",{{opacity:0,y:20,duration:.5}},{TZ+1.3});'
ev+=[(TZ,sfx.whoosh(.9,.3)),(TZ+.3,sfx.boom(.6)),(TZ+.8,sfx.chime(659,.18,3))]
DUR=round(TZ+4.6,1)
shots=style_reel('e6_b2b_pod_lupoi_lineika',DUR,body,js,'Под лупой: линейка',ev,pad=(110,164.8,220,277.2),pad_amp=.05,check=(T[0]+1.8,1.2,T[1]+1.8,T[2]+1.8,T[3]+1.8,TZ+2.5),bg=BG,outdir=V9)
strip(shots,'kp/chk_e6.jpg',2400); print('ok',DUR)
