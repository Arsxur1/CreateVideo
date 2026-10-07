from cinekit import *
from cine import *
from brand import ORANGE, sili
from peach_lib import peach, damage, plaster
import sfx
SPOT = '<div class="fill" style="background:radial-gradient(42% 30% at 50% 47%,rgba(255,214,170,.28),transparent 70%)"></div>'
def shreds(color1,color2,id,x,y):
    bits=''.join(f'<div style="position:absolute;left:{a}px;top:{b}px;width:{c}px;height:{d}px;border-radius:40% 60% 50% 45%;background:radial-gradient(circle at 40% 35%,{color1},{color2})"></div>' for a,b,c,d in [(40,34,60,34),(130,26,40,34),(200,40,70,28),(300,30,36,30)])
    return f'<div id="{id}" style="position:absolute;left:{x}px;top:{y}px;width:420px;height:120px;opacity:0;transform:rotate(-5deg)"><div style="position:absolute;inset:0;border-radius:60px;background:linear-gradient(180deg,#fff,#DCE0E5);box-shadow:0 0 40px rgba(255,255,255,.25)"></div>{bits}</div>'

def build(name, title, hook1, hook2, stage_html, tear_ids, sili_id, plaster_id, clock, verdictL, verdictR, endl1, endl2, cta, pad, s1c, s2c):
    T_APPLY=2.3; T_WAIT=4.4; T_TEAR=(6.8 if clock else 4.8); T_SIL=T_TEAR+3.0; T_VER=T_SIL+2.6; T_END=T_VER+2.8; DUR=round(T_END+4.8,1)
    body=f'''<section id="st" class="clip" data-start="0" data-duration="{T_END}" data-track-index="1">{backdrop(21)}{SPOT}
<div id="stage" style="position:absolute;inset:0">{stage_html}</div>{shreds(s1c,s2c,"sh",90,1420)}
<div id="ring" style="position:absolute;left:600px;top:700px;width:340px;height:340px;border-radius:50%;border:5px solid {ORANGE};box-shadow:0 0 40px {ORANGE},inset 0 0 30px rgba(243,130,33,.5);opacity:0"></div>
{kin("h1",hook1.split(),170,92)}{kin("h2",hook2.split(),290,92,accent_idx=(len(hook2.split())-1,))}
{kin("a1",["Клеим","пластырь","и","Sili-Care."],230,76,accent_idx=(3,),extra="opacity:0")}
{kin("w1",["Ждём","сутки."],210,96,extra="opacity:0")}
<div id="clk" style="position:absolute;left:0;right:0;top:330px;text-align:center;font-family:'Inter Display';font-weight:700;font-size:84px;color:{ORANGE};opacity:0;text-shadow:0 0 30px rgba(243,130,33,.7)">00:00</div>
{kin("t1",["Снимаем","пластырь…"],230,90,extra="opacity:0")}{kin("t2",["Снимаем","Sili-Care."],230,90,accent_idx=(1,),extra="opacity:0")}
<div id="vL" style="position:absolute;left:60px;top:1330px;width:480px;text-align:center;opacity:0"><div style="font-size:30px;color:#FF6B4A;font-weight:700;letter-spacing:.06em">ОБЫЧНЫЙ ПЛАСТЫРЬ</div><div style="font-family:'Inter Display';font-size:64px;font-weight:800;color:#fff;margin-top:8px">{verdictL}</div></div>
<div id="vR" style="position:absolute;left:540px;top:1330px;width:480px;text-align:center;opacity:0"><div style="font-size:30px;color:{ORANGE};font-weight:700;letter-spacing:.06em">SILI-CARE</div><div style="font-family:'Inter Display';font-size:64px;font-weight:800;color:#fff;margin-top:8px;text-shadow:0 0 24px rgba(243,130,33,.6)">{verdictR}</div></div></section>
<section id="en" class="clip" data-start="{T_END}" data-duration="{round(DUR-T_END,1)}" data-track-index="1">{end_card("ec",endl1,endl2,cta)}</section>'''
    js=drift_js(0,DUR)+f'tl.from("#stage",{{opacity:0,scale:.9,duration:.8,ease:"power2.out"}},.05);'+slam_js('h1',.15,.1)+slam_js('h2',.6,.12)
    js+=f'tl.to(["#h1","#h2"],{{opacity:0,duration:.3}},{T_APPLY-.2}).to("#a1",{{opacity:1,duration:.01}},{T_APPLY});'+slam_js('a1',T_APPLY,.08)
    js+=f'tl.from("#{plaster_id}",{{y:-900,rotation:-60,opacity:0,duration:.5,ease:"power3.out"}},{T_APPLY+.3}).from("#{sili_id}",{{y:-900,rotation:40,opacity:0,duration:.5,ease:"power3.out"}},{T_APPLY+.9});'
    ev=[(.15,sfx.click(.4)),(.6,sfx.boom(.55)),(T_APPLY+.55,sfx.click(.6)),(T_APPLY+1.15,sfx.click(.6))]
    if clock:
        js+=f'tl.to("#a1",{{opacity:0,duration:.3}},{T_WAIT-.3}).to(["#w1","#clk"],{{opacity:1,duration:.3}},{T_WAIT});'
        js+=f'const ck=document.getElementById("clk");const co={{v:0}};tl.to(co,{{v:24,duration:1.9,ease:"power2.in",onUpdate:()=>{{const h=Math.floor(co.v);ck.textContent=String(h).padStart(2,"0")+":"+String(Math.floor((co.v-h)*60)).padStart(2,"0")}}}},{T_WAIT+.1});'
        js+=f'tl.fromTo("#stage",{{filter:"brightness(1)"}},{{filter:"brightness(.6)",duration:.9,repeat:1,yoyo:true}},{T_WAIT+.1});'
        ev+=[(T_WAIT+.1+i*.16,sfx.click(.3)) for i in range(12)]
        js+=f'tl.to(["#w1","#clk"],{{opacity:0,duration:.3}},{T_TEAR-.3});'
    else:
        js+=f'tl.to("#a1",{{opacity:0,duration:.3}},{T_TEAR-.3});'
    js+=f'tl.to("#t1",{{opacity:1,duration:.01}},{T_TEAR});'+slam_js('t1',T_TEAR,.1)
    js+=f'tl.to("#{plaster_id}",{{y:-640,x:-70,rotation:-55,duration:.55,ease:"power4.in"}},{T_TEAR+.4}).to("#{plaster_id}",{{opacity:0,duration:.2}},{T_TEAR+.95});'
    for tid in tear_ids: js+=f'tl.fromTo("#{tid}",{{opacity:0}},{{opacity:1,duration:.05}},{T_TEAR+.72});'
    js+=f'tl.fromTo("#stage",{{x:0}},{{x:16,duration:.04,repeat:7,yoyo:true}},{T_TEAR+.72}).to("#sh",{{opacity:1,duration:.4}},{T_TEAR+1.2}).from("#sh",{{y:60,duration:.5}},{T_TEAR+1.2});'
    ev+=[(T_TEAR,sfx.whoosh(.5,.2)),(T_TEAR+.55,sfx.tear(.55,.85)),(T_TEAR+.72,sfx.boom(.55))]
    js+=f'tl.to("#t1",{{opacity:0,duration:.3}},{T_SIL-.3}).to("#t2",{{opacity:1,duration:.01}},{T_SIL});'+slam_js('t2',T_SIL,.1)
    js+=f'tl.to("#{sili_id}",{{y:-640,rotation:-8,duration:1.3,ease:"power2.inOut"}},{T_SIL+.3}).to("#{sili_id}",{{opacity:0,duration:.3}},{T_SIL+1.5}).to("#ring",{{opacity:1,duration:.4}},{T_SIL+1.5}).from("#ring",{{scale:.5,duration:.9,ease:"back.out(1.5)"}},{T_SIL+1.5});'
    ev+=[(T_SIL,sfx.whoosh(.5,.2)),(T_SIL+1.5,sfx.chime(880,.22,2.6)),(T_SIL+1.52,sfx.chime(1320,.12,2.6))]
    js+=f'tl.to("#sh",{{opacity:0,duration:.3}},{T_VER-.4}).to("#t2",{{opacity:0,duration:.3}},{T_VER}).to("#vL",{{opacity:1,duration:.3}},{T_VER}).from("#vL",{{scale:1.4,duration:.35,ease:"power3.out"}},{T_VER}).to("#vR",{{opacity:1,duration:.3}},{T_VER+.5}).from("#vR",{{scale:1.4,duration:.35,ease:"power3.out"}},{T_VER+.5});'
    ev+=[(T_VER,sfx.boom(.45)),(T_VER+.5,sfx.boom(.45)),(T_END-1.3,sfx.riser(1.3,.25)),(T_END,sfx.boom(.85)),(T_END+.5,sfx.chime(523,.2,3))]
    f,fj=flash('ft',T_TEAR+.72,'#FFF0E0'); body+=f'<div class="clip" data-start="{T_TEAR}" data-duration="1.5" data-track-index="7">{f}</div>'; js+=fj
    f2,fj2=flash('fe',T_END); body+=f'<div class="clip" data-start="{T_END-.4}" data-duration="1" data-track-index="6">{f2}</div>'; js+=fj2
    js+=slam_js('eca',T_END+.1,.1)+slam_js('ecb',T_END+.6,.1)+f'tl.from("#ecl",{{opacity:0,scale:.9,duration:.7}},{T_END+1.3}).from("#ecc",{{opacity:0,y:20,duration:.6}},{T_END+1.9});'
    shots=cine_reel(name,DUR,body,js,title,ev,pad=pad,check=(T_TEAR+1.6,1.2,T_APPLY+1.6,T_WAIT+1.0 if clock else T_TEAR+.9,T_VER+1.2,T_END+3))
    return shots

# ---- ПЕРСИК
cx,cy,d=540,900,700
peach_stage = peach(cx,cy,d,'pch') + f'<div id="dmw" style="position:absolute;left:{cx-325}px;top:{cy-110}px;transform:rotate(-20deg)">{damage(0,0,280,130,"dm")}</div>' + plaster(cx-330,cy-100,300,110,-20,'pl') + f'<div id="si" style="position:absolute;left:{cx+50}px;top:{cy-140}px;width:260px;height:260px;transform:rotate(10deg)">{sili(0,0,260)}</div>'
s=build('m4_persik_cinematic','Персиковый тест','Этот персик —','кожа вашей бабушки.',peach_stage,['dmw'],'si','pl',True,'Кожица порвана','Персик цел','Снимать —','не ранить.','👵 Перешлите тем, кто ухаживает за родителями<br>🏥 Клиникам — образцы Sili-Care в директ',(110,138.6,164.8,220),'#F48A54','#C9433A')
strip(s,'kp/chk_m4.jpg')
print('peach ok')
