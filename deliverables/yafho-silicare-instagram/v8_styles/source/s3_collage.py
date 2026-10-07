from stylekit import *
from brand import ORANGE, logo
import sfx, random
r=random.Random(9)
KRAFT='#C69C6D'
kraft_bg=f'''<div class="fill" style="background:{KRAFT}"></div><div class="fill" style="opacity:.35;background-image:radial-gradient(rgba(90,60,30,.5) 1px,transparent 1.6px),radial-gradient(rgba(255,240,210,.4) 1px,transparent 1.8px);background-size:7px 7px,11px 11px;background-position:0 0,3px 5px"></div>
<div class="fill" style="background:radial-gradient(ellipse at center,transparent 50%,rgba(60,35,10,.45))"></div>'''
TORN="polygon(0% 3%,6% 0%,14% 2%,22% 0%,31% 3%,40% 0%,52% 2%,61% 0%,72% 3%,83% 0%,92% 2%,100% 0%,99% 30%,100% 62%,98% 100%,88% 97%,77% 100%,66% 97%,55% 100%,44% 97%,33% 100%,21% 97%,10% 100%,0% 98%,2% 60%,0% 30%)"
def tape(x,y,w,rot,id=''):
    return f'<div {"id="+chr(34)+id+chr(34) if id else ""} style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:56px;transform:rotate({rot}deg);background:rgba(255,246,200,.6);box-shadow:0 2px 4px rgba(0,0,0,.1)"></div>'
def dymo(txt):
    return f'<span style="display:inline-block;background:#111;color:#fff;font-family:Inter Display,sans-serif;font-weight:700;font-size:34px;letter-spacing:.14em;padding:12px 22px;border-radius:6px;box-shadow:inset 0 2px 0 rgba(255,255,255,.15),0 4px 8px rgba(0,0,0,.3)">{txt}</span>'
# ransom letters
COLS=['#fff','#F38221','#111','#FFE000','#F6D2AE','#fff','#9B1B74','#fff','#111','#F38221']
letters=''
i=0
for word in 'ЧТО ВНУТРИ?'.split():
    letters+='<span style="display:inline-block;white-space:nowrap;margin:0 20px">'
    for ch in word:
        bg=COLS[i%len(COLS)]; fg='#fff' if bg in('#111','#9B1B74','#F38221') else '#111'
        fnt=['Inter Display','DejaVu Serif','Inter Display','DejaVu Sans Mono'][i%4]
        letters+=f'<span class="rl" style="display:inline-block;margin:5px;padding:8px 14px;background:{bg};color:{fg};font-family:{fnt},sans-serif;font-weight:800;font-size:{r.choice([108,118,126])}px;transform:rotate({r.uniform(-9,9):.1f}deg);box-shadow:0 6px 10px rgba(0,0,0,.25)">{ch}</span>'
        i+=1
    letters+='</span>'
LAY=[('ПЕРФОРИРОВАННЫЙ СИЛИКОН','background-color:#F2C49A;background-image:radial-gradient(circle,#C69C6D 7px,transparent 7.8px);background-size:30px 30px'),
     ('МЯГКАЯ ПЕНА','background-color:#F7E4C8;background-image:radial-gradient(rgba(150,100,50,.35) 2px,transparent 2.6px);background-size:12px 12px'),
     ('СВЯЗУЮЩИЙ СЛОЙ','background:#FBF8F2'),
     ('СУПЕРАБСОРБЕНТ','background-color:#fff;background-image:repeating-linear-gradient(0deg,rgba(0,80,160,.12) 0 3px,transparent 3px 12px)'),
     ('ЗАЩИТНЫЙ ВЕРХНИЙ СЛОЙ','background:rgba(255,255,255,.55)')]
stack=''; labels=''
for i,(lab,sty) in enumerate(LAY):
    y=1250-i*150
    stack+=f'<div class="ly" id="ly{i}" style="position:absolute;left:{140+r.randint(-10,10)}px;top:{y}px;width:800px;height:150px;clip-path:{TORN};{sty};transform:rotate({r.uniform(-2.5,2.5):.1f}deg);filter:drop-shadow(0 6px 6px rgba(0,0,0,.3))"></div>'
    labels+=f'<div class="lb" id="lb{i}" style="position:absolute;left:{r.choice([60,420])}px;top:{y+40}px;transform:rotate({r.uniform(-4,4):.1f}deg)">{dymo(lab)}</div>'
body=f'''<section id="c1" class="clip" data-start="0" data-duration="2.8" data-track-index="1">{kraft_bg}
<div style="position:absolute;left:60px;right:60px;top:560px;text-align:center;line-height:1.1">{letters}</div>
<div id="hint" style="position:absolute;left:0;right:0;top:1180px;text-align:center">{dymo("SILI-CARE BORDER")}</div></section>
<section id="c2" class="clip" data-start="2.8" data-duration="11.2" data-track-index="1">{kraft_bg}
<div style="position:absolute;left:70px;top:150px;transform:rotate(-2deg);background:#fff;clip-path:{TORN};padding:40px 50px;font-family:Inter Display,sans-serif;font-weight:800;font-size:76px;color:#111" id="tt">5 слоёв<br><span style="color:{ORANGE}">одной повязки</span></div>{tape(90,140,220,-12)}
{stack}{labels}
<div id="stamp" style="position:absolute;left:250px;top:620px;width:580px;height:250px;border:12px solid {ORANGE};border-radius:24px;color:{ORANGE};font-family:Inter Display,sans-serif;font-weight:900;font-size:110px;text-align:center;line-height:230px;transform:rotate(-12deg);opacity:0;mix-blend-mode:multiply">SILI-CARE</div></section>
<section id="c3" class="clip" data-start="14.0" data-duration="4.5" data-track-index="1">{kraft_bg}
<div id="card" style="position:absolute;left:90px;top:430px;width:900px;height:760px;background:#fff;clip-path:{TORN};transform:rotate(1.5deg)"></div>{tape(380,400,320,3,"tp1")}
<div id="e1" style="position:absolute;left:150px;right:150px;top:560px;text-align:center;font-family:Inter Display,sans-serif;font-weight:900;font-size:110px;line-height:1;color:#111">Снимать —<br><span style="color:{ORANGE}">не ранить.</span></div>
<div id="e2" style="position:absolute;left:0;right:0;top:870px;text-align:center">{logo(100)}</div>
<div id="e3" style="position:absolute;left:0;right:0;top:1060px;text-align:center">{dymo("5 СЛОЁВ · ОДНА ЗАДАЧА")}</div>
<div style="position:absolute;left:80px;right:80px;bottom:120px;text-align:center;font-size:22px;color:rgba(40,20,0,.7)">Медицинское изделие. Применение — по назначению специалиста.</div></section>'''
J='tl.fromTo("#root",{rotation:0},{rotation:.25,duration:.125,ease:"steps(1)",repeat:147,yoyo:true},0);'
J+='tl.from(".rl",{opacity:0,scale:2.2,rotation:30,duration:.25,ease:"steps(3)",stagger:.16},.05).from("#hint",{opacity:0,y:30,duration:.25,ease:"steps(3)"},1.9);'
J+='tl.from("#tt",{x:-900,duration:.4,ease:"steps(4)"},2.9);'
ev=[(.05+i*.16,kick(.35)) for i in range(9)]+[(1.9,sfx.click(.4)),(2.85,sfx.whoosh(.35,.25))]
for i in range(5):
    t=3.6+i*1.75
    J+=f'tl.from("#ly{i}",{{x:{1200 if i%2 else -1200},rotation:{(-1)**i*8},duration:.45,ease:"steps(5)"}},{t}).from("#lb{i}",{{opacity:0,scale:1.6,duration:.25,ease:"steps(3)"}},{t+.55});'
    ev+=[(t,sfx.whoosh(.35,.28)),(t+.42,kick(.55)),(t+.58,sfx.click(.35))]
J+='tl.to(".lb",{opacity:0,duration:.25,ease:"steps(2)"},12.4).to(".ly",{y:(i)=>i*28,duration:.5,ease:"steps(5)"},12.4).to("#stamp",{opacity:1,duration:.01},13.1).from("#stamp",{scale:2.4,duration:.2,ease:"steps(3)"},13.1);'
ev+=[(12.4,sfx.whoosh(.5,.3)),(13.25,kick(.95)),(13.3,sfx.chime(784,.14,2))]
J+='tl.from("#card",{y:1400,rotation:20,duration:.45,ease:"steps(5)"},14.05).from("#tp1",{opacity:0,duration:.1},14.6).from("#e1",{opacity:0,duration:.2,ease:"steps(2)"},14.7).from("#e2",{opacity:0,duration:.25,ease:"steps(3)"},15.3).from("#e3",{opacity:0,scale:1.5,duration:.25,ease:"steps(3)"},15.8);'
ev+=[(14.05,sfx.whoosh(.4,.3)),(14.5,kick(.6)),(15.8,sfx.click(.4)),(16.0,sfx.chime(523,.16,2.5))]
shots=style_reel('s3_paper_collage',18.5,body,J,'Бумажный коллаж',ev,pad=None,check=(13.6,1.9,4.6,8.5,11.8,16.8),bg=KRAFT)
strip(shots,'kp/chk_s3.jpg',2400); print('ok')
