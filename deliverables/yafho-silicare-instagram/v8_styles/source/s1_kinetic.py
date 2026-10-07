from stylekit import *
from brand import ORANGE, INK, logo, sili
import sfx
W='#FFFFFF'; O=ORANGE; K='#141414'
def block(id,s,d,bg,inner,track=1):
    return f'<section id="{id}" class="clip" data-start="{s}" data-duration="{d}" data-track-index="{track}"><div class="fill" style="background:{bg}"></div>{inner}</section>'
def big(id,txt,size,color,top=None,extra=''):
    pos = f'top:{top}px' if top is not None else 'top:50%;transform:translateY(-50%)'
    return f'<div id="{id}" style="position:absolute;left:40px;right:40px;{pos};text-align:center;font-family:\'Inter Display\';font-weight:900;font-size:{size}px;line-height:.92;letter-spacing:-0.05em;color:{color};{extra}">{txt}</div>'
cuts=[]; js=''; ev=[]
def cut(t,d,bg,inner,anim):
    global js
    i=len(cuts); cuts.append(block(f'b{i}',t,d,bg,inner)); js_part=anim(i,t)
    js+=js_part+f'tl.from("#b{i}",{{yPercent:100,duration:.18,ease:"power4.out"}},{t});'
    ev.append((t,kick(.7)))
# 0 СТОП
cut(0,.9,K,big('w0','СТОП.',300,W),lambda i,t:f'tl.from("#w0",{{scale:2.2,opacity:0,duration:.25,ease:"power4.out"}},{t+.02});')
# 1 Ты срываешь пластырь
words=[('ТЫ',320),('СРЫВАЕШЬ',170),('ПЛАСТЫРЬ.',165)]
for k,(w,s) in enumerate(words):
    t=.9+k*.45; cut(t,.45,O if k%2==0 else W,big(f'x{k}',w,s,K if k%2==0 else O),lambda i,t,k=k:f'tl.from("#x{k}",{{scale:1.6,duration:.2,ease:"power3.out"}},{t});')
# 2 А он срывает КОЖУ
t=2.25; cut(t,1.6,W,big('y1','А ОН<br>СРЫВАЕТ',150,K,560)+big('y2','КОЖУ.',300,'#E53B2C',900)+'<div id="y3" style="position:absolute;left:140px;top:1230px;width:800px;height:30px;background:#E53B2C;transform-origin:left"></div>',
  lambda i,t:f'tl.from("#y2",{{scale:1.8,opacity:0,duration:.25,ease:"power4.out"}},{t+.5}).from("#y3",{{scaleX:0,duration:.35,ease:"power2.out"}},{t+.8});')
ev.append((2.75,kick(.9)))
# 3 счётчик
t=3.85; cut(t,1.8,K,big('c0','×1',360,O,620)+big('c1','ПЕРЕВЯЗОК',90,W,1060),
  lambda i,t:f'const ce=document.getElementById("c0");const o={{v:1}};tl.to(o,{{v:30,duration:1.4,ease:"power2.in",onUpdate:()=>{{ce.textContent="×"+Math.round(o.v)}}}},{t+.1});tl.fromTo("#c0",{{scale:1}},{{scale:1.12,duration:.12,repeat:9,yoyo:true}},{t+.1});')
ev+=[(3.95+i*.14,sfx.click(.35)) for i in range(10)]
# 4 клей держится крепче
t=5.65; cut(t,2.4,W,big('k1','КЛЕЙ ДЕРЖИТСЯ<br>ЗА КОЖУ',110,K,430)+big('k2','КРЕПЧЕ,',230,O,760)+big('k3','ЧЕМ КЛЕТКИ КОЖИ<br>ДРУГ ЗА ДРУГА.',92,K,1060),
  lambda i,t:f'tl.from("#k1",{{opacity:0,y:40,duration:.25}},{t+.1}).from("#k2",{{scale:2,opacity:0,duration:.25,ease:"power4.out"}},{t+.6}).from("#k3",{{opacity:0,y:40,duration:.25}},{t+1.2});')
ev+=[(6.25,kick(.6)),(6.85,kick(.5))]
# 5 Силикон держит и ОТПУСКАЕТ
t=8.05; cut(t,2.6,O,big('s1','СИЛИКОН<br>ДЕРЖИТ',150,W,520)+big('s2','И ОТПУСКАЕТ.',92,K,900,'white-space:nowrap'),
  lambda i,t:f'tl.from("#s1",{{opacity:0,y:40,duration:.25}},{t+.05}).from("#s2",{{opacity:0,duration:.2}},{t+.8}).fromTo("#s2",{{letterSpacing:"-0.05em"}},{{letterSpacing:"0.08em",duration:1.2,ease:"power2.out"}},{t+.8});')
ev+=[(8.85,sfx.whoosh(1.0,.35)),(9.4,sfx.chime(880,.18,2))]
# 6 Sili-Care
t=10.65; cut(t,2.5,K,f'<div id="p0" style="position:absolute;left:330px;top:520px">{sili(0,0,420,"transform:rotate(-8deg)")}</div>'+big('p1','SILI-CARE',170,O,1060)+big('p2','5 слоёв. Мягкий силикон.',48,W,1260,'font-weight:600;letter-spacing:0'),
  lambda i,t:f'tl.from("#p0",{{y:-900,rotation:-40,duration:.5,ease:"back.out(1.4)"}},{t+.05}).from("#p1",{{scale:1.8,opacity:0,duration:.25,ease:"power4.out"}},{t+.5}).from("#p2",{{opacity:0,duration:.3}},{t+1.0});')
ev+=[(11.15,kick(.8))]
# 7 финал
t=13.15; cut(t,3.35,W,big('e1','СНИМАТЬ —',150,K,560)+big('e2','НЕ РАНИТЬ.',150,O,720)+f'<div id="e3" style="position:absolute;left:0;right:0;top:1010px;text-align:center">{logo(110)}</div><div id="e4" style="position:absolute;left:80px;right:80px;top:1250px;text-align:center;font-size:34px;color:#444;font-weight:600">Перешлите тому, кто срывает пластырь «одним рывком»</div>',
  lambda i,t:f'tl.from("#e1",{{opacity:0,x:-200,duration:.25}},{t+.05}).from("#e2",{{opacity:0,x:200,duration:.25}},{t+.35}).from("#e3",{{opacity:0,duration:.4}},{t+.8}).from("#e4",{{opacity:0,duration:.4}},{t+1.3});')
ev+=[(13.5,kick(.8)),(14.0,sfx.chime(660,.18,2.5))]
shots=style_reel('s1_kinetic_type',16.5,''.join(cuts),js,'Кинетическая типографика',ev,pad=None,check=(2.9,.4,1.5,5.0,7.5,9.6,12.0,15.5),bg=W)
strip(shots,'kp/chk_s1.jpg',2400); print('ok')
