# Серия «ТЕСТ YAFHO»: эффект «обычный пластырь vs силикон» на фоне в стиле yafho.com
import random
from stylekit import style_reel, SOUT
from brand import logo, sili, tab, ORANGE, INK, GREY, STAGE, BLUE, MAGENTA
from peach_lib import plaster
from kp import strip
import sfx
V20=SOUT.replace('v8_styles','v20_effect')
F="font-family:'Inter Display',sans-serif"
RED='#D93A2F'; GREEN='#2E9E5B'
CW,CH=470,700; CY=640; LX,RX=45,565   # карточки сравнения
def bg():
    # фон как на карточках товаров yafho.com: серо-голубой градиент + мягкий «пол»
    return (f'<div class="fill" style="background:{STAGE}"></div>'
            '<div class="fill" style="background:radial-gradient(ellipse 80% 40% at 50% 100%,rgba(255,255,255,.55),transparent 70%)"></div>')
def top(n):
    return (f'<div style="position:absolute;left:60px;top:150px">{logo(64,ORANGE,True)}</div>'
            f'<div style="position:absolute;right:60px;top:160px;padding:12px 22px;background:{BLUE};color:#fff;{F};font-weight:800;font-size:26px;letter-spacing:.08em">ТЕСТ YAFHO №{n}</div>')
def card(x,id,label,col,inner):
    return (f'<div id="{id}" style="position:absolute;left:{x}px;top:{CY}px;width:{CW}px;height:{CH}px;border-radius:44px;background:rgba(255,255,255,.38);box-shadow:inset 0 0 0 2px rgba(255,255,255,.6),0 30px 60px -30px rgba(40,60,100,.35)">'
            f'<div class="lb" style="position:absolute;left:0;right:0;top:26px;text-align:center;{F};font-weight:800;font-size:28px;letter-spacing:.06em;color:{col}">{label}</div>{inner}</div>')
def badge(id,x,ok,text):
    c=GREEN if ok else RED; s='✓' if ok else '✕'
    return (f'<div id="{id}" style="position:absolute;left:{x}px;top:{CY+CH+28}px;width:{CW}px;text-align:center">'
            f'<span style="display:inline-block;width:84px;height:84px;border-radius:50%;background:{c};color:#fff;{F};font-weight:900;font-size:56px;line-height:84px">{s}</span>'
            f'<div style="margin-top:12px;{F};font-weight:700;font-size:32px;line-height:1.2;color:{INK}">{text}</div></div>')
def effect_reel(name,n,hook,obj,dmg,stuck,right_pad,wait_txt,bad_txt,good_txt,why,end1,end2,cta,note,left_lbl='ОБЫЧНЫЙ ПЛАСТЫРЬ',right_lbl='СИЛИКОН YAFHO',extra_js='',extra_ev=(),decor=''):
    """obj(id) — объект 360×360 в центре карточки; dmg — повреждение под левым пластырем; stuck — что остаётся на пластыре;
       right_pad — html силиконовой повязки (в коробке 300×300)."""
    T1,T2,T3,T4,T5,T6=2.4,4.4,6.2,7.8,9.6,13.4; DUR=18.4
    S=420; ox,oy=(CW-S)//2,150
    # объект рисуется в коробке 360 и масштабируется до S
    sc=f'transform:scale({S/360});transform-origin:0 0'
    L=(f'<div style="position:absolute;left:{ox}px;top:{oy}px;width:360px;height:360px;{sc}">{obj("ol")}'
       f'<div id="dm" style="position:absolute;inset:0;opacity:0">{dmg}</div>'
       f'<div id="pl" style="position:absolute;left:-10px;top:120px;width:380px;height:130px">{plaster(0,0,380,130,-8,"plx")}'
       f'<div id="st" style="position:absolute;inset:0;opacity:0;transform:rotate(-8deg)">{stuck}</div></div></div>{decor}')
    R=(f'<div style="position:absolute;left:{ox}px;top:{oy}px;width:360px;height:360px;{sc}">{obj("or")}'
       f'<div id="pr" style="position:absolute;left:30px;top:30px;width:300px;height:300px">{right_pad}</div></div>{decor}')
    body=f'''<section id="a" class="clip" data-start="0" data-duration="{T6}" data-track-index="1">{bg()}{top(n)}
<div id="hk" style="position:absolute;left:60px;right:60px;top:300px;text-align:center;{F};font-weight:900;font-size:76px;line-height:1.04;letter-spacing:-0.02em;color:{INK}">{hook}</div>
<div id="wy" style="position:absolute;left:70px;right:70px;top:290px;text-align:center;{F};font-weight:800;font-size:50px;line-height:1.1;color:{INK};opacity:0">{why}</div>
{card(LX,"cl",left_lbl,GREY,L)}{card(RX,"cr",right_lbl,ORANGE,R)}
<div id="wt" style="position:absolute;left:0;right:0;top:{CY+CH//2-50}px;text-align:center;opacity:0"><span style="display:inline-block;padding:22px 46px;border-radius:60px;background:{INK};color:#fff;{F};font-weight:800;font-size:46px">⏳ {wait_txt}</span></div>
{badge("bl",LX,False,bad_txt)}{badge("br",RX,True,good_txt)}
<div style="position:absolute;left:60px;right:60px;bottom:90px;text-align:center;font-size:20px;color:rgba(43,43,43,.55)">Иллюстрация. Медицинское изделие. Применение — по назначению специалиста.</div></section>
<section id="z" class="clip" data-start="{T6}" data-duration="{DUR-T6}" data-track-index="1">{bg()}
<div id="zp" style="position:absolute;left:390px;top:330px;width:300px;height:300px">{right_pad}</div>
<div id="z1" style="position:absolute;left:50px;right:50px;top:720px;text-align:center;{F};font-weight:900;font-size:92px;line-height:1.02;letter-spacing:-0.02em;color:{INK}">{end1}<br><span style="color:{ORANGE}">{end2}</span></div>
<div id="z2" style="position:absolute;left:0;right:0;top:1010px;text-align:center">{logo(110,ORANGE,True)}</div>
<div id="z3" style="position:absolute;left:80px;right:80px;top:1230px;text-align:center;font-size:38px;font-weight:600;line-height:1.35;color:{INK}">{cta}</div>
<div style="position:absolute;left:70px;right:70px;bottom:90px;text-align:center;font-size:20px;line-height:1.5;color:rgba(43,43,43,.55)">{note}Медицинское изделие. Применение — по назначению специалиста.</div></section>'''
    js=(f'tl.from("#hk",{{scale:1.5,opacity:0,duration:.4,ease:"power3.out"}},.05).from("#cl,#cr",{{y:200,opacity:0,duration:.6,stagger:.12,ease:"power3.out"}},.3);'
        f'tl.from("#pl",{{y:-700,rotation:-30,opacity:0,duration:.5,ease:"power2.in"}},{T1}).from("#pr",{{y:-700,rotation:20,opacity:0,duration:.5,ease:"power2.in"}},{T1+.35});'
        f'tl.to("#cl,#cr",{{scale:.985,duration:.08,yoyo:true,repeat:1}},{T1+.5});'
        f'tl.to("#wt",{{opacity:1,scale:1.05,duration:.3}},{T2}).to("#wt",{{opacity:0,duration:.3}},{T3-.35});'
        f'tl.to("#pl",{{x:6,duration:.05,repeat:5,yoyo:true}},{T3}).to("#st",{{opacity:1,duration:.01}},{T3+.3}).to("#pl",{{y:-250,rotation:6,scale:.85,duration:.5,ease:"power3.out"}},{T3+.32}).to("#cl .lb",{{opacity:0,duration:.2}},{T3+.3}).to("#dm",{{opacity:1,duration:.15}},{T3+.4});'
        f'tl.from("#bl",{{scale:.4,opacity:0,duration:.35,ease:"back.out(2)"}},{T3+.8});'
        f'tl.to("#pr",{{y:-40,rotation:6,duration:.6,ease:"power1.out"}},{T4}).to("#pr",{{y:-280,rotation:-4,scale:.62,duration:.6,ease:"power2.out"}},{T4+.6}).to("#cr .lb",{{opacity:0,duration:.2}},{T4+.5});'
        f'tl.from("#br",{{scale:.4,opacity:0,duration:.35,ease:"back.out(2)"}},{T4+1.2});'
        f'tl.to("#hk",{{opacity:0,y:-20,duration:.3}},{T5}).to("#wy",{{opacity:1,duration:.4}},{T5+.2});'
        f'tl.from("#zp",{{scale:2.2,opacity:0,rotation:-15,duration:.8,ease:"power3.out"}},{T6}).from("#z1",{{opacity:0,y:30,duration:.5}},{T6+.6}).from("#z2",{{opacity:0,duration:.5}},{T6+1.2}).from("#z3",{{opacity:0,y:20,duration:.5}},{T6+1.7});'+extra_js)
    ev=[(.05,sfx.whoosh(.6,.25)),(.3,sfx.chime(440,.12,2)),(T1+.45,sfx.click(.5)),(T1+.8,sfx.click(.45)),(T2,sfx.whoosh(.5,.15))]
    ev+=[(T2+.3+i*.25,sfx.click(.18)) for i in range(6)]
    ev+=[(T3+.3,sfx.tear(.5,.55)),(T3+.8,sfx.boom(.35)),(T4+.1,sfx.whoosh(.8,.12)),(T4+1.2,sfx.chime(784,.16,2.2)),(T5,sfx.whoosh(.5,.15)),(T6,sfx.whoosh(.9,.3)),(T6+.6,sfx.boom(.5)),(T6+1.2,sfx.chime(659,.18,3))]+list(extra_ev)
    shots=style_reel(name,DUR,body,js,f'Тест Yafho №{n}',ev,pad=(110,164.8,220,277.2),pad_amp=.04,check=(T3+1.4,1.2,T2+.6,T4+1.8,T5+1.5,T6+3),bg='#C9D3E3',outdir=V20)
    strip(shots,f'kp/chk_{name}.jpg',2400); print('ok',name,DUR,flush=True)
