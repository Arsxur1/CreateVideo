from gen_lib import dress, layers
HEAD = lambda t: f'''<!doctype html><html lang="ru"><head><meta charset="UTF-8"><title>{t}</title><script src="gsap.min.js"></script><link rel="stylesheet" href="shared.css">
<style>#root{{position:relative;width:1080px;height:1920px;overflow:hidden}} .t{{position:absolute;left:90px;right:90px}} .skin{{position:absolute;border-radius:40px;background:radial-gradient(120% 100% at 50% 30%,#EFCFB6,#C99577);overflow:hidden}}</style></head><body>'''
BRAND = '<div class="brand" style="position:absolute;left:90px;top:90px;color:#F5F1EA">Yafho <i>· Silicare</i></div>'

# ================= REEL 1 — Снять, не ранив (15s)
cracks = ''.join(f'<div class="r1crack" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:5px;background:#E2573B;border-radius:3px;transform:rotate({r}deg);transform-origin:left center;box-shadow:0 0 14px rgba(226,87,59,.8)"></div>'
                 for x,y,w,r in [(330,250,170,-18),(480,200,120,25),(420,330,150,8),(560,300,110,-35),(300,360,90,40),(600,240,140,12)])
r1 = HEAD('Reel 1') + f'''<div id="root" data-composition-id="main" data-width="1080" data-height="1920" data-duration="15">
<div class="fill dark" style="z-index:0"></div>
<section id="r1a" class="clip" data-start="0" data-duration="3.4" data-track-index="1"><div class="fill dark"></div>
 <div class="t" style="top:720px;color:#F5F1EA"><h1 class="h" style="font-size:118px"><span id="r1a1">Каждая смена</span><span id="r1a2">повязки</span><span id="r1a3" style="color:#E2573B">оставляет след.</span></h1>
 <div id="r1line" style="margin-top:40px;height:6px;width:900px;background:#E2573B;transform-origin:left"></div></div></section>
<section id="r1b" class="clip" data-start="3.4" data-duration="5" data-track-index="1"><div class="fill dark"></div>
 <div class="lab" style="position:absolute;left:90px;top:150px;color:#E2573B">Агрессивный адгезив</div>
 <div class="skin" style="left:90px;top:210px;width:900px;height:620px">{cracks}<div id="r1d1" style="position:absolute;left:260px;top:110px;width:400px;height:400px"><div class="dress" style="inset:0;width:400px;height:400px;filter:saturate(.3) brightness(.95)"><div class="core"></div></div></div></div>
 <div class="lab" style="position:absolute;left:90px;top:960px;color:#9FD3C5">Силикон Silicare</div>
 <div class="skin" style="left:90px;top:1020px;width:900px;height:620px"><div id="r1ring" class="ring" style="left:210px;top:60px;width:500px;height:500px;color:rgba(255,255,255,.7)"></div><div id="r1d2" style="position:absolute;left:260px;top:110px;width:400px;height:400px"><div class="dress" style="inset:0;width:400px;height:400px"><div class="core"></div><div class="gloss"></div></div></div></div>
 <div id="r1bt" class="t" style="top:1700px;color:#F5F1EA;font-size:44px;font-weight:600">Разница — в момент снятия.</div></section>
<section id="r1c" class="clip" data-start="8.4" data-duration="3.4" data-track-index="1"><div class="fill dark"></div>
 <div id="r1stack" style="position:absolute;inset:0">{layers(540,820,None,40,1.5)}</div>
 <div class="t" style="top:1300px;color:#F5F1EA"><h2 class="h" style="font-size:96px"><span id="r1c1">Силикон держит кожу.</span><span id="r1c2" style="color:#9FD3C5">Не рану.</span></h2></div></section>
<section id="r1d" class="clip" data-start="11.8" data-duration="3.2" data-track-index="1"><div class="fill skinbg grain"></div>
 <div id="r1dd" style="position:absolute;left:330px;top:420px;width:420px;height:420px">{dress(0,0,420,'transform:rotate(-8deg)')}</div>
 <div class="t" style="top:1020px;color:#0C1A1D"><h1 class="h" style="font-size:120px"><span id="r1d1t">Снимать —</span><span id="r1d2t" style="color:#fff">не ранить.</span></h1>
 <div id="r1cta" class="body" style="margin-top:60px;font-size:38px">Образцы для клиник и дистрибьюторов — в директ</div></div>
 <div class="brand" style="position:absolute;left:90px;bottom:120px;color:#0C1A1D">Yafho <i>· Silicare</i></div></section>
</div><script>
window.__timelines={{}};const tl=gsap.timeline({{paused:true}});
tl.from(["#r1a1","#r1a2","#r1a3"],{{y:60,opacity:0,duration:.7,stagger:.35,ease:"power3.out"}},.2)
  .from("#r1line",{{scaleX:0,duration:1,ease:"power2.inOut"}},1.6)
  .from(".r1crack",{{scaleX:0,duration:.25,stagger:.08,ease:"power1.in"}},5.0)
  .to("#r1d1",{{y:-260,rotation:-14,duration:1.1,ease:"power2.in"}},4.3)
  .to("#r1d1",{{opacity:0,duration:.4}},5.6)
  .to("#r1d2",{{y:-260,rotation:8,duration:1.4,ease:"power2.inOut"}},4.3)
  .to("#r1d2",{{opacity:0,duration:.4}},5.9)
  .from("#r1ring",{{scale:.6,opacity:0,duration:1.4,ease:"power2.out"}},5.2)
  .from("#r1bt",{{y:30,opacity:0,duration:.6}},6.4)
  .from("#r1stack .iso > div",{{y:0,opacity:0,duration:1,stagger:.12,ease:"power3.out"}},8.5)
  .from(["#r1c1","#r1c2"],{{y:50,opacity:0,duration:.6,stagger:.4}},9.4)
  .from("#r1dd",{{y:-500,rotation:-30,duration:.9,ease:"back.out(1.4)"}},11.8)
  .from(["#r1d1t","#r1d2t"],{{y:50,opacity:0,duration:.6,stagger:.25}},12.4)
  .from("#r1cta",{{opacity:0,duration:.6}},13.3)
  .to({{}},{{duration:.01}},14.99);
window.__timelines["main"]=tl;</script></body></html>'''
open('reel1/index.html','w').write(r1)

# ================= REEL 2 — Влага внутрь (12s)
import random
rnd = random.Random(7)
drops = ''.join(f'<div class="r2drop" style="position:absolute;left:{rnd.randint(330,730)}px;top:{rnd.randint(1250,1330)}px;width:{(s:=rnd.randint(18,34))}px;height:{s}px;border-radius:50%;background:radial-gradient(circle at 35% 30%,#F6D49A,#D9963F)"></div>' for _ in range(22))
rain = ''.join(f'<div class="r2rain" style="position:absolute;left:{rnd.randint(120,940)}px;top:{rnd.randint(-300,-40)}px;width:{(s:=rnd.randint(22,46))}px;height:{s}px;border-radius:50% 50% 50% 0;transform:rotate(-45deg);background:radial-gradient(circle at 35% 30%,#F6D49A,#D9963F)"></div>' for _ in range(16))
band = lambda top,h,bg,lab,lc='#0C1A1D',id='': f'<div {id} style="position:absolute;left:150px;width:780px;top:{top}px;height:{h}px;border-radius:14px;background:{bg}"></div><div class="lab" style="position:absolute;left:150px;top:{top+h//2-12}px;width:780px;text-align:center;color:{lc};font-size:18px">{lab}</div>'
r2 = HEAD('Reel 2') + f'''<div id="root" data-composition-id="main" data-width="1080" data-height="1920" data-duration="12">
<div class="fill dark" style="z-index:0"></div>
<section id="r2a" class="clip" data-start="0" data-duration="3" data-track-index="1"><div class="fill dark"></div>{rain}
 <div class="t" style="top:820px;color:#F5F1EA"><h1 class="h" style="font-size:150px"><span id="r2a1">Экссудат.</span></h1><div id="r2a2" class="body" style="margin-top:30px;color:#E2A857;font-size:44px">Его нельзя остановить. Но можно удержать.</div></div></section>
<section id="r2b" class="clip" data-start="3" data-duration="5.2" data-track-index="1"><div class="fill dark"></div>
 <div class="lab" style="position:absolute;left:90px;top:200px;color:#9FD3C5">Silicare в разрезе</div>
 {band(560,90,'rgba(255,255,255,.25)','ПУ-плёнка','#F5F1EA')}
 <div style="position:absolute;left:230px;width:620px;top:670px;height:200px;border-radius:14px;background:repeating-linear-gradient(0deg,rgba(18,58,64,.12) 0 3px,transparent 3px 12px),#FFFFFF;overflow:hidden"><div id="r2fill" style="position:absolute;left:0;right:0;bottom:0;height:200px;background:linear-gradient(0deg,#D9963F,#F0C27A);transform-origin:bottom;opacity:.9"></div></div><div class="lab" style="position:absolute;left:230px;top:758px;width:620px;text-align:center;font-size:18px;color:#0C1A1D">Суперабсорбент</div>
 {band(890,190,'radial-gradient(circle,rgba(150,125,95,.35) 2px,transparent 2.6px) 0 0/18px 18px,#F3ECE1','Пена')}
 {band(1100,40,'#9FD3C5','Силикон')}
 <div style="position:absolute;left:0;right:0;top:1160px;height:360px;background:linear-gradient(#DDAF90,#B98466)"></div>
 <div style="position:absolute;left:330px;top:1160px;width:420px;height:160px;border-radius:0 0 210px 210px;background:radial-gradient(circle at 50% 0,#B5523F,#7E2E25)"></div>
 {drops}
 <div id="r2edgeL" class="lab" style="position:absolute;left:60px;top:1400px;color:#0C1A1D;font-size:20px">✓ Край сухой</div>
 <div id="r2edgeR" class="lab" style="position:absolute;right:60px;top:1400px;color:#0C1A1D;font-size:20px">Край сухой ✓</div>
 <div class="t" style="top:1600px;color:#F5F1EA;font-size:56px;font-weight:700;font-family:'Inter Display'"><div id="r2t1" style="position:absolute">Впитывается.</div><div id="r2t2" style="position:absolute;color:#E2A857">Запирается внутри.</div></div></section>
<section id="r2c" class="clip" data-start="8.2" data-duration="3.8" data-track-index="1"><div class="fill mintbg grain"></div>
 <div class="t" style="top:640px;color:#0C1A1D"><h1 class="h" style="font-size:140px"><span id="r2c1">Влажно.</span><span id="r2c2" style="color:#E2573B">Но не мокро.</span></h1>
 <div id="r2c3" class="body" style="margin-top:50px;font-size:40px;max-width:860px">Влажная среда для заживления — без мацерации краёв раны.</div></div>
 <div class="brand" style="position:absolute;left:90px;bottom:120px;color:#0C1A1D">Yafho <i>· Silicare</i></div>
 <div id="r2cta" class="chip" style="position:absolute;right:90px;bottom:100px;background:#0C1A1D;color:#F5F1EA">Образцы → директ</div></section>
</div><script>
window.__timelines={{}};const tl=gsap.timeline({{paused:true}});
tl.to(".r2rain",{{y:2300,duration:2.6,stagger:.09,ease:"power1.in"}},0)
  .from("#r2a1",{{y:60,opacity:0,duration:.7,ease:"power3.out"}},.3)
  .from("#r2a2",{{opacity:0,duration:.7}},1.2)
  .to(".r2drop",{{y:-560,duration:1.6,stagger:.05,ease:"power2.inOut"}},3.6)
  .to(".r2drop",{{opacity:0,duration:.3,stagger:.05}},4.9)
  .from("#r2fill",{{scaleY:0,duration:1.6,ease:"power2.out"}},4.9)
  .from("#r2t1",{{opacity:0,y:30,duration:.5}},3.8)
  .to("#r2t1",{{opacity:0,duration:.3}},5.4)
  .from("#r2t2",{{opacity:0,y:30,duration:.5}},5.7)
  .from(["#r2edgeL","#r2edgeR"],{{opacity:0,duration:.5}},6.6)
  .from(["#r2c1","#r2c2"],{{y:60,opacity:0,duration:.6,stagger:.35,ease:"power3.out"}},8.4)
  .from("#r2c3",{{opacity:0,duration:.6}},9.4)
  .from("#r2cta",{{opacity:0,scale:.9,duration:.5}},10.2)
  .to({{}},{{duration:.01}},11.99);
window.__timelines["main"]=tl;</script></body></html>'''
open('reel2/index.html','w').write(r2)
