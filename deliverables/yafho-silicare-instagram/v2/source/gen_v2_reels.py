from gen_lib import dress, layers
def doc(dur, body, js, title):
    return f'''<!doctype html><html lang="ru"><head><meta charset="UTF-8"><title>{title}</title><script src="gsap.min.js"></script><link rel="stylesheet" href="shared.css">
<style>#root{{position:relative;width:1080px;height:1920px;overflow:hidden}} .cap{{position:absolute;left:80px;right:80px;text-align:center;font-family:'Inter Display';font-weight:800;letter-spacing:-0.03em;line-height:1.02}} .cap span{{display:inline}}
.skin{{position:absolute;border-radius:40px;background:radial-gradient(120% 100% at 50% 30%,#EFCFB6,#C99577);overflow:hidden}}
#pbar{{position:absolute;left:0;top:0;height:10px;width:1080px;background:#E2573B;transform-origin:left;z-index:50}}</style></head><body>
<div id="root" data-composition-id="main" data-width="1080" data-height="1920" data-duration="{dur}">
<div class="fill dark" style="z-index:0"></div>
{body}
<div id="pbar" class="clip" data-start="0" data-duration="{dur}" data-track-index="9" style="inset:auto;height:10px"></div>
</div><script>window.__timelines={{}};const tl=gsap.timeline({{paused:true}});
tl.fromTo("#pbar",{{scaleX:0}},{{scaleX:1,duration:{dur},ease:"none"}},0);
{js}
window.__timelines["main"]=tl;</script></body></html>'''
def clip(id, s, d, inner, bg='dark', track=1):
    return f'<section id="{id}" class="clip" data-start="{s}" data-duration="{d}" data-track-index="{track}"><div class="fill {bg}"></div>{inner}</section>'
END = lambda pre, line2, cta: f'''<div class="fill skinbg grain"></div>{dress(330,380,420,'transform:rotate(-8deg)')}
<div class="cap" id="{pre}e1" style="top:960px;color:#0C1A1D;font-size:118px">Снимать —</div><div class="cap" id="{pre}e2" style="top:1090px;color:#fff;font-size:118px">{line2}</div>
<div class="cap" id="{pre}e3" style="top:1300px;color:#0C1A1D;font-size:40px;font-weight:600;font-family:Inter">{cta}</div>
<div class="brand" style="position:absolute;left:0;right:0;text-align:center;bottom:140px;color:#0C1A1D">Yafho <i>· Silicare</i></div>'''

# ===== R3 · Скотч-тест (viral) 15s
tape = '<div id="r3tape" style="position:absolute;left:180px;top:250px;width:540px;height:150px;background:linear-gradient(180deg,rgba(255,255,255,.85),rgba(235,235,225,.8));box-shadow:0 8px 20px rgba(0,0,0,.2);transform:rotate(-6deg)"></div>'
flecks = ''.join(f'<div class="r3f" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;border-radius:40%;background:rgba(226,87,59,.55)"></div>' for x,y,w,h in [(220,300,120,22),(380,280,80,30),(500,330,140,18),(300,350,60,26),(600,290,70,20)])
cracks = ''.join(f'<div class="r3c" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:3px;background:rgba(120,60,40,.5);transform:rotate({r}deg);transform-origin:left"></div>' for x,y,w,r in [(100,150,300,8),(420,180,260,-12),(200,420,340,5),(560,470,220,-20),(150,560,280,14),(480,620,300,-6),(90,300,200,-25)])
b = ''.join([
 clip('r3a',0,2,f'<div class="skin" style="left:90px;top:300px;width:900px;height:640px">{tape}</div><div class="cap" id="r3a1" style="top:1080px;color:#F5F1EA;font-size:104px">Приклейте скотч<br>к руке.</div>'),
 clip('r3b',2,2,f'<div class="skin" id="r3skinb" style="left:90px;top:300px;width:900px;height:640px">{flecks}<div id="r3tape2" style="position:absolute;left:180px;top:250px;width:540px;height:150px;background:linear-gradient(180deg,rgba(255,255,255,.85),rgba(235,235,225,.8));box-shadow:0 8px 20px rgba(0,0,0,.2);transform:rotate(-6deg)"></div></div><div class="cap" id="r3b1" style="top:1080px;color:#F5F1EA;font-size:130px"><span class="hl">Резко</span><br>оторвите.</div>'),
 clip('r3c',4,3,f'<div class="skin" style="left:90px;top:300px;width:900px;height:640px;filter:saturate(.45) brightness(1.05)">{cracks}</div><div class="cap" id="r3c1" style="top:1060px;color:#F5F1EA;font-size:92px">А теперь представьте,<br>что вам <span style="color:#E2A857">85</span>.</div><div class="cap" id="r3c2" style="top:1440px;color:#F5F1EA;font-size:56px;font-weight:600;opacity:.8">Кожа тонкая, как бумага.</div>'),
 clip('r3d',7,2.4,f'<div class="cap" style="top:640px;color:#F5F1EA;font-size:96px">И так —<br>на каждой<br>перевязке.</div><div class="cap" id="r3cnt" style="top:1150px;color:#E2573B;font-size:200px;font-family:Inter Display;font-weight:300">×1</div>'),
 clip('r3e',9.4,2.6,f'<div class="skin" style="left:90px;top:300px;width:900px;height:640px"><div class="ring" id="r3ring" style="left:200px;top:70px;width:500px;height:500px;color:rgba(255,255,255,.75)"></div><div id="r3sd" style="position:absolute;left:250px;top:120px;width:400px;height:400px"><div class="dress" style="inset:0;width:400px;height:400px"><div class="core"></div><div class="gloss"></div></div></div></div><div class="cap" id="r3e1" style="top:1080px;color:#F5F1EA;font-size:92px">Силикон<br><span class="hlm">отпускает</span> кожу.</div>'),
 clip('r3f',12,3,END('r3','не ранить.','Отправьте коллеге, который делает перевязки'),'')])
js = '''tl.from("#r3a1",{y:60,opacity:0,duration:.4,ease:"power3.out"},.1).from("#r3tape",{scaleX:0,transformOrigin:"left",duration:.5,ease:"power2.out"},.4)
.to("#r3tape2",{y:-500,x:120,rotation:-30,duration:.35,ease:"power4.in"},2.5).from(".r3f",{opacity:0,scale:.3,duration:.25,stagger:.04},2.8)
.fromTo("#r3skinb",{x:0},{x:14,duration:.05,repeat:7,yoyo:true},2.8).from("#r3b1",{scale:1.4,opacity:0,duration:.3,ease:"back.out(2)"},2.05)
.from(".r3c",{scaleX:0,duration:.6,stagger:.08},4.2).from("#r3c1",{y:40,opacity:0,duration:.5},4.1).from("#r3c2",{opacity:0,duration:.5},5.3)
.to({n:1},{n:1,duration:0},7)
.from("#r3sd",{y:0},9.4).to("#r3sd",{y:-560,rotation:8,duration:1.4,ease:"power2.inOut"},9.9).from("#r3ring",{scale:.6,opacity:0,duration:1.2},10.6).from("#r3e1",{y:40,opacity:0,duration:.5},9.6)
.from("#r3dress",{},12).from(["#r3e1","#r3e2"].map(x=>x.replace("r3e","r3e")),{},12)
.from("#r3e3",{opacity:0,duration:.5},13.4).from(["#r3e1x"],{},12);
const cnt=document.getElementById("r3cnt");const o={v:1};tl.to(o,{v:30,duration:2.2,ease:"power2.in",onUpdate:()=>{cnt.textContent="×"+Math.round(o.v)}},7.1);
tl.from(["#r3e1","#r3e2"],{},0);'''
# simpler, explicit end-card animation
js = js.replace('.from("#r3dress",{},12).from(["#r3e1","#r3e2"].map(x=>x.replace("r3e","r3e")),{},12)\n.from("#r3e3",{opacity:0,duration:.5},13.4).from(["#r3e1x"],{},12);','.from("#r3e3",{opacity:0,duration:.5},13.4);').replace('tl.from(["#r3e1","#r3e2"],{},0);','')
open('r3/index.html','w').write(doc(15,b,js,'Reel скотч-тест'))

# ===== R4 · Почему пластырь снимает кожу (explain) 16s
def bricks(prefix, rows=5, top=760):
    out=[]
    for r in range(rows):
        off = 0 if r%2==0 else -60
        for c in range(9):
            out.append(f'<div class="{prefix}b {prefix}r{r}" style="position:absolute;left:{off+c*125+40}px;top:{top+r*70}px;width:118px;height:62px;border-radius:10px;background:{"#E8C3A6" if r<2 else "#D9A98A"};box-shadow:inset 0 -4px 0 rgba(0,0,0,.06)"></div>')
    return ''.join(out)
b = ''.join([
 clip('r4a',0,2.2,'<div class="cap" id="r4a1" style="top:700px;color:#F5F1EA;font-size:128px">Пластырь<br>сильнее<br><span class="hl">вашей кожи.</span></div>'),
 clip('r4b',2.2,4.6,f'''<div class="lab" style="position:absolute;left:80px;top:220px;color:#9FD3C5">#ПочемуТак · кожа под микроскопом</div>
<div id="r4glue" style="position:absolute;left:40px;top:560px;width:1000px;height:120px;border-radius:16px;background:repeating-linear-gradient(90deg,#F3EEE6 0 20px,#E9E1D3 20px 40px);box-shadow:0 10px 30px rgba(0,0,0,.4)"></div>
<div id="r4gluet" class="lab" style="position:absolute;left:0;right:0;text-align:center;top:605px;color:#0C1A1D">Клей</div>
<div id="r4teeth">{"".join(f'<div style="position:absolute;left:{70+i*110}px;top:680px;width:20px;height:80px;background:#E9E1D3;border-radius:0 0 10px 10px"></div>' for i in range(9))}</div>
<div id="r4bricks">{bricks('r4')}</div>
<div class="lab" style="position:absolute;left:80px;top:1130px;color:#F5F1EA;opacity:.6">Клетки верхнего слоя кожи</div>
<div class="cap" id="r4b1" style="top:1300px;color:#F5F1EA;font-size:62px">Клей держится за клетки кожи <span style="color:#E2573B">крепче</span>, чем клетки — друг за друга.</div>'''),
 clip('r4c',6.8,3.2,f'''<div id="r4lift" style="position:absolute;inset:0"><div style="position:absolute;left:40px;top:560px;width:1000px;height:120px;border-radius:16px;background:repeating-linear-gradient(90deg,#F3EEE6 0 20px,#E9E1D3 20px 40px)"></div>{bricks('r4x',2)}</div>
<div>{bricks('r4y',3,900)}</div>
<div class="cap" id="r4c1" style="top:1300px;color:#F5F1EA;font-size:62px;line-height:1.25">При снятии верхний слой кожи<br><span class="hl">уходит вместе с клеем.</span></div>
<div class="cap" id="r4c2" style="top:1560px;color:#F5F1EA;font-size:30px;font-weight:500;font-family:Inter;opacity:.65">Так возникает MARSI — травма кожи от медицинского клея</div>'''),
 clip('r4d',10,3.2,f'''<div id="r4sil" style="position:absolute;left:40px;top:640px;width:1000px;height:120px;border-radius:60px;background:linear-gradient(180deg,#E6F5F0,#9FD3C5)"></div>
<div class="lab" style="position:absolute;left:0;right:0;text-align:center;top:690px;color:#0C1A1D" id="r4silt">Мягкий силикон</div>
{bricks('r4z')}
<div class="cap" id="r4d1" style="top:1300px;color:#F5F1EA;font-size:62px;line-height:1.25">Силикон ложится мягко<br>и <span class="hlm">отпускает кожу целой.</span></div>'''),
 clip('r4e',13.2,2.8,END('r4','не ранить.','Сохраните, чтобы объяснить пациенту'),'')])
js = '''tl.from("#r4a1",{scale:1.25,opacity:0,duration:.45,ease:"back.out(1.8)"},.05)
.from("#r4glue,#r4gluet",{y:-300,opacity:0,duration:.6,ease:"power3.out"},2.4).from("#r4teeth",{opacity:0,scaleY:0,transformOrigin:"top",duration:.5},3.1)
.from(".r4b",{opacity:0,y:20,duration:.3,stagger:.006},2.3).from("#r4b1",{y:40,opacity:0,duration:.5},3.6)
.to("#r4lift",{y:-420,rotation:-4,duration:1.1,ease:"power3.in"},7.2).from("#r4c1",{y:40,opacity:0,duration:.5},7.9).from("#r4c2",{opacity:0,duration:.5},8.7)
.from("#r4sil,#r4silt",{y:-300,opacity:0,duration:.6,ease:"power3.out"},10.1).to("#r4sil,#r4silt",{y:-380,duration:1,ease:"power2.inOut"},11.2).from("#r4d1",{y:40,opacity:0,duration:.5},10.6)
.from("#r4e1,#r4e2",{y:50,opacity:0,duration:.5,stagger:.2},13.4).from("#r4e3",{opacity:0,duration:.5},14.3);'''
open('r4/index.html','w').write(doc(16,b,js,'Reel почему пластырь'))

# ===== R5 · Ключ (proof/opportunity) 16s
nodes=[('Хрупкая кожа',540,560),('Травма при снятии',860,880),('Мацерация',540,1200),('Рана растёт',220,880)]
ring=''.join(f'<div class="r5n" id="r5n{i}" style="position:absolute;left:{x-150}px;top:{y-60}px;width:300px;height:120px;border-radius:60px;background:{"#E2573B" if i else "#1C3A40"};color:#fff;display:flex;align-items:center;justify-content:center;text-align:center;font-size:30px;font-weight:700;padding:0 20px">{t}</div>' for i,(t,x,y) in enumerate(nodes))
b = ''.join([
 clip('r5a',0,2.6,'<div class="cap" id="r5a1" style="top:600px;color:#E2573B;font-size:150px;font-weight:700;white-space:nowrap">$26,8 млрд</div><div class="cap" id="r5a2" style="top:860px;color:#F5F1EA;font-size:68px">в год стоят внутрибольничные<br>пролежни. Только в США.</div><div class="cap" id="r5a3" style="top:1600px;color:#F5F1EA;font-size:26px;font-family:Inter;font-weight:400;opacity:.5">Padula W. et al., Int Wound J, 2019</div>'),
 clip('r5b',2.6,4.4,f'<div class="cap" id="r5b0" style="top:200px;color:#F5F1EA;font-size:64px">Почему проблема<br>не уходит?</div><div id="r5ring" style="position:absolute;left:290px;top:630px;width:500px;height:500px;border-radius:50%;border:4px dashed rgba(226,87,59,.5)"></div>{ring}<div class="cap" id="r5b1" style="top:1450px;color:#F5F1EA;font-size:60px">Это <span class="hl">замкнутый круг.</span></div>'),
 clip('r5c',7,4,f'<div class="cap" id="r5c1" style="top:260px;color:#F5F1EA;font-size:70px">Разорвать его можно<br>в одной точке —</div><div class="cap" id="r5c2" style="top:470px;color:#9FD3C5;font-size:70px">там, где повязка<br>касается кожи.</div><div id="r5stack" style="position:absolute;inset:0">{layers(540,1150,0,55,1.3)}</div><div class="cap" id="r5c3" style="top:1600px;color:#F5F1EA;font-size:40px;font-weight:600;font-family:Inter">силикон отпускает · пена держит влагу · суперабсорбент запирает</div>'),
 clip('r5d',11,2.4,'<div class="cap" id="r5d1" style="top:640px;color:#F5F1EA;font-size:84px">Для клиник —<br><span style="color:#9FD3C5">меньше осложнений.</span></div><div class="cap" id="r5d2" style="top:1000px;color:#F5F1EA;font-size:84px">Для дистрибьюторов&nbsp;—<br><span style="color:#E2A857">возможность.</span></div>'),
 clip('r5e',13.4,2.6,END('r5','не ранить.','Образцы и спецификация — в директ'),'')])
js = '''tl.from("#r5a1",{scale:.6,opacity:0,duration:.5,ease:"back.out(1.7)"},.05).from("#r5a2",{y:40,opacity:0,duration:.5},.6).from("#r5a3",{opacity:0,duration:.4},1.2)
.from("#r5b0",{opacity:0,y:30,duration:.4},2.7).from("#r5ring",{rotation:-90,opacity:0,duration:1.2},2.9).from(".r5n",{scale:0,opacity:0,duration:.4,stagger:.35,ease:"back.out(2)"},3.1).to("#r5ring",{rotation:180,duration:3,ease:"none"},4.0).from("#r5b1",{y:40,opacity:0,duration:.5},5.2)
.from("#r5c1",{y:30,opacity:0,duration:.5},7.1).from("#r5c2",{y:30,opacity:0,duration:.5},7.8).from("#r5stack .iso > div",{opacity:0,y:60,duration:.6,stagger:.15},8.2).from("#r5c3",{opacity:0,duration:.5},9.6)
.from("#r5d1",{y:40,opacity:0,duration:.5},11.1).from("#r5d2",{y:40,opacity:0,duration:.5},11.8)
.from("#r5e1,#r5e2",{y:50,opacity:0,duration:.5,stagger:.2},13.6).from("#r5e3",{opacity:0,duration:.5},14.5);'''
open('r5/index.html','w').write(doc(16,b,js,'Reel ключ'))
