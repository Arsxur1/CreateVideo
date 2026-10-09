# Шаги 32–34: ТЕСТ №13 «На сгибе», №14 «Ожог от противня», №15 «Шрам: 12 недель»
import sys
from fxkit import *
which=sys.argv[1:]
HK=f'position:absolute;left:60px;right:60px;top:300px;text-align:center;{F};font-weight:900;font-size:76px;line-height:1.04;letter-spacing:-0.02em;color:{INK}'
WHY=f'position:absolute;left:60px;right:60px;top:290px;text-align:center;{F};font-weight:800;font-size:48px;line-height:1.12;color:{INK};opacity:0'
def endsec(T,DUR,prod,e1,e2,cta,note):
    return f'''<section id="z" class="clip" data-start="{T}" data-duration="{DUR-T}" data-track-index="1">{bg()}
<div id="zp" style="position:absolute;left:390px;top:330px;width:300px;height:300px">{prod}</div>
<div id="z1" style="position:absolute;left:40px;right:40px;top:700px;text-align:center;{F};font-weight:900;font-size:80px;line-height:1.04;letter-spacing:-0.02em;color:{INK}">{e1}<br><span style="color:{ORANGE}">{e2}</span></div>
<div id="z2" style="position:absolute;left:0;right:0;top:1010px;text-align:center">{logo(110,ORANGE,True)}</div>
<div id="z3" style="position:absolute;left:70px;right:70px;top:1230px;text-align:center;font-size:36px;font-weight:600;line-height:1.35;color:{INK}">{cta}</div>
<div style="position:absolute;left:70px;right:70px;bottom:90px;text-align:center;font-size:20px;line-height:1.5;color:rgba(43,43,43,.55)">{note}Медицинское изделие. Применение — по назначению специалиста.</div></section>'''
def endjs(T): return f'tl.from("#zp",{{scale:2.2,opacity:0,rotation:-15,duration:.8,ease:"power3.out"}},{T}).from("#z1",{{opacity:0,y:30,duration:.5}},{T+.6}).from("#z2",{{opacity:0,duration:.5}},{T+1.2}).from("#z3",{{opacity:0,y:20,duration:.5}},{T+1.7});'
def endev(T): return [(T,sfx.whoosh(.9,.3)),(T+.6,sfx.boom(.5)),(T+1.2,sfx.chime(659,.18,3))]
INTRO='tl.from("#hk",{scale:1.5,opacity:0,duration:.4,ease:"power3.out"},.05).from("#cl,#cr",{y:200,opacity:0,duration:.6,stagger:.12,ease:"power3.out"},.3);'
def badges_js(T3): return f'tl.from("#bl",{{scale:.4,opacity:0,duration:.35,ease:"back.out(2)"}},{T3}).from("#br",{{scale:.4,opacity:0,duration:.35,ease:"back.out(2)"}},{T3+.4});'
def why_js(T4): return f'tl.to("#dy",{{opacity:0,duration:.2}},{T4}).to("#hk",{{opacity:0,y:-20,duration:.3}},{T4}).to("#wy",{{opacity:1,duration:.4}},{T4+.2});'
def chip_counter(txt): return f'<div id="dy" style="position:absolute;left:0;right:0;top:{CY-86}px;text-align:center;opacity:0"><span id="dyt" style="display:inline-block;padding:16px 40px;border-radius:50px;background:{INK};color:#fff;{F};font-weight:800;font-size:44px">{txt}</span></div>'
def render(name,n,DUR,body,js,ev,check):
    shots=style_reel(name,DUR,body,js,f'Тест Yafho №{n}',ev,pad=(110,164.8,220,277.2),pad_amp=.04,check=check,bg='#C9D3E3',outdir=V20)
    strip(shots,f'kp/chk_{name}.jpg',2400); print('ok',name,DUR,flush=True)
SKIN='background:linear-gradient(90deg,#E9B08C,#F6D2B8 45%,#EBB896);box-shadow:inset -10px 0 18px rgba(150,70,40,.25)'
# ---------- №13 на сгибе
if not which or 't13' in which:
    def leg(s):
        if s=='L':
            pad_top=''; pad_bot=''
            pl=('<div id="Lpl" style="position:absolute;left:258px;top:300px;width:46px;height:170px;border-radius:23px;background:linear-gradient(90deg,#fff,#E2E5E8);box-shadow:0 6px 12px rgba(30,40,60,.3);transform-origin:50% 0">'
                '<div style="position:absolute;left:8px;top:58px;width:30px;height:54px;border-radius:8px;background:#F2F4F6;border:2px solid #D7DCE1"></div></div>')
        else:
            pl=''
            pad_top='<div style="position:absolute;left:62px;top:136px;width:46px;height:92px;border-radius:16px 16px 0 0;background:linear-gradient(90deg,#E0904E,#F3B57E);border:3px solid #fff;border-bottom:none;box-shadow:0 4px 10px rgba(120,60,20,.35)"></div>'
            pad_bot='<div style="position:absolute;left:60px;top:-6px;width:46px;height:92px;border-radius:0 0 16px 16px;background:linear-gradient(90deg,#E0904E,#F3B57E);border:3px solid #fff;border-top:none;box-shadow:0 4px 10px rgba(120,60,20,.35)"></div>'
        return (f'<div style="position:absolute;left:190px;top:160px;width:100px;height:230px;border-radius:50px 50px 40px 40px;{SKIN}">{pad_top}</div>'
                f'<div id="{s}sh" style="position:absolute;left:192px;top:380px;width:96px;height:250px;border-radius:44px 44px 40px 40px;{SKIN};transform-origin:50% 0">{pad_bot}'
                f'<div style="position:absolute;left:0;bottom:-6px;width:150px;height:40px;border-radius:20px 30px 16px 16px;background:linear-gradient(180deg,#F1C6A6,#DFA581)"></div></div>'
                f'<div style="position:absolute;left:188px;top:345px;width:104px;height:80px;border-radius:50%;background:radial-gradient(ellipse at 60% 40%,#F8D8C0,#EDBC9A)"></div>{pl}')
    T0=2.4; B=.7; NB=5; T3=T0+NB*2*B+.3; T4=T3+1.4; T5=13.4; DUR=18.4
    body=f'''<section id="a" class="clip" data-start="0" data-duration="{T5}" data-track-index="1">{bg()}{top(13)}
<div id="hk" style="{HK}">Пластырь<br>на колене.<br><span style="color:{ORANGE}">10 приседаний.</span></div>
<div id="wy" style="{WHY}">Обычный пластырь жёсткий —<br>на сгибе края отходят.<br><span style="color:{ORANGE}">Мягкая пена гнётся<br>вместе с кожей.</span></div>
{card(LX,"cl","ОБЫЧНЫЙ ПЛАСТЫРЬ",GREY,leg("L"))}{card(RX,"cr","ПЕНА SILI-CARE",ORANGE,leg("R"))}
{chip_counter("× 0")}
{badge("bl",LX,False,"Край отклеился")}{badge("br",RX,True,"Держится на сгибе")}
<div style="position:absolute;left:60px;right:60px;bottom:90px;text-align:center;font-size:20px;color:rgba(43,43,43,.55)">Иллюстрация. Медицинское изделие. Применение — по назначению специалиста.</div></section>
{endsec(T5,DUR,sili(0,0,300,"transform:rotate(-6deg)"),"Колено, локоть —","пена гнётся вместе.","Спорт, дети, после операций<br>на суставах: напишите «СГИБ»","")}'''
    js=INTRO+f'tl.to("#dy",{{opacity:1,duration:.3}},{T0-.2});'
    ev=[(.05,sfx.whoosh(.6,.25)),(.3,sfx.chime(440,.12,2))]
    for i in range(NB):
        t=T0+i*2*B
        js+=f'tl.to("#Lsh,#Rsh",{{rotation:70,duration:{B},ease:"power2.inOut"}},{t}).to("#Lsh,#Rsh",{{rotation:0,duration:{B},ease:"power2.inOut"}},{t+B});'
        js+=f'tl.call(()=>{{document.getElementById("dyt").textContent="× {2*(i+1)}"}},null,{t+B});'
        ev+=[(t+B*.9,sfx.click(.25))]
    # обычный пластырь: с каждым сгибом нижний край отходит всё сильнее
    js+=f'tl.to("#Lpl",{{rotation:-14,x:16,duration:{NB*2*B},ease:"power1.in"}},{T0});'
    js+=badges_js(T3)+why_js(T4)+endjs(T5)
    ev+=[(T3,sfx.boom(.3)),(T3+.4,sfx.chime(784,.16,2.2)),(T4,sfx.whoosh(.5,.15))]+endev(T5)
    render('t13_na_sgibe',13,DUR,body,js,ev,(T3+.8,1.2,T0+B,T3+.6,T4+1.5,T5+3))
# ---------- №14 ожог от противня
if not which or 't14' in which:
    def arm(s):
        burn=(f'<div id="{s}heat" style="position:absolute;left:150px;top:300px;width:180px;height:130px;border-radius:50%;background:radial-gradient(ellipse,rgba(255,90,40,.95),rgba(240,70,40,.75) 45%,rgba(240,90,60,.0) 75%)"></div>'
              f'<div id="{s}glow" style="position:absolute;left:120px;top:270px;width:240px;height:190px;border-radius:50%;background:radial-gradient(ellipse,rgba(255,170,60,.55),transparent 70%)"></div>')
        extra=('<div id="Loil" style="position:absolute;left:170px;top:315px;width:140px;height:100px;border-radius:50%;background:radial-gradient(ellipse at 35% 30%,rgba(255,250,200,.95),rgba(240,200,60,.75) 60%,rgba(220,170,30,.5));opacity:0"></div>'
               '<div id="Ltag" style="position:absolute;left:40px;top:150px;'+F+';font-weight:800;font-size:30px;color:#B8860B;opacity:0">масло / паста</div>'
               if s=='L' else
               '<div id="Rwat" style="position:absolute;left:200px;top:80px;width:80px;height:330px;opacity:0;background:repeating-linear-gradient(180deg,rgba(120,180,240,.0) 0 18px,rgba(120,180,240,.75) 18px 46px);border-radius:40px;filter:blur(1px)"></div>'
               '<div id="Rtag" style="position:absolute;left:40px;top:150px;'+F+';font-weight:800;font-size:30px;color:#1E6FD9;opacity:0">прохладная вода</div>')
        return (f'<div style="position:absolute;left:30px;top:250px;width:410px;height:230px;border-radius:110px;{SKIN.replace("90deg","180deg")}"></div>{burn}{extra}')
    T0=2.4; T3=8.6; T4=10.0; T5=13.8; DUR=18.8
    body=f'''<section id="a" class="clip" data-start="0" data-duration="{T5}" data-track-index="1">{bg()}{top(14)}
<div id="hk" style="{HK}">Обожглись<br>о противень.<br><span style="color:{ORANGE}">Что делать?</span></div>
<div id="wy" style="{WHY}">Масло и паста держат жар,<br>лёд повреждает кожу.<br><span style="color:{ORANGE}">20 минут прохладной воды,<br>потом — накрыть плёнкой.</span></div>
{card(LX,"cl","МИФ: МАСЛО",GREY,arm("L"))}{card(RX,"cr","ВОДА 20 МИНУТ",ORANGE,arm("R"))}
{chip_counter("⏱ 00:00")}
{badge("bl",LX,False,"Жар остался<br>в коже")}{badge("br",RX,True,"Кожа остыла")}
<div style="position:absolute;left:60px;right:60px;bottom:90px;text-align:center;font-size:20px;color:rgba(43,43,43,.55)">Иллюстрация. Первая помощь при ожогах — British Burn Association, NHS.</div></section>
{endsec(T5,DUR,'<div style="position:absolute;inset:20px;border-radius:30px;background:rgba(255,255,255,.55);box-shadow:inset 0 0 0 3px rgba(255,255,255,.9),0 20px 30px -10px rgba(30,40,60,.3);background-image:radial-gradient(rgba(243,130,33,.35) 3px,transparent 4px);background-size:22px 22px"></div>',"Ожог —","под воду, 20 минут.","Большой ожог, лицо, руки, пах,<br>ребёнок или пожилой — сразу к врачу.<br>Перешлите тем, кто печёт к празднику 🎄","Силиконовые контактные слои Yafho — для ухода за ожогом по назначению врача.<br>")}'''
    js=INTRO+f'tl.to("#Lheat,#Rheat,#Lglow,#Rglow",{{opacity:.75,duration:.4,yoyo:true,repeat:3}},{.6});'
    js+=f'tl.to("#Loil,#Ltag",{{opacity:1,duration:.4}},{T0}).to("#Rwat,#Rtag",{{opacity:1,duration:.4}},{T0+.3}).to("#Rwat",{{backgroundPositionY:"280px",duration:{T3-T0},ease:"none"}},{T0+.3});'
    js+=f'tl.to("#dy",{{opacity:1,duration:.3}},{T0});const dd=document.getElementById("dyt");const o={{m:0}};tl.to(o,{{m:20,duration:{T3-T0-.6},ease:"power1.in",onUpdate:()=>{{dd.textContent="⏱ "+String(Math.round(o.m)).padStart(2,"0")+":00"}}}},{T0+.3});'
    js+=f'tl.to("#Rheat",{{opacity:.15,scale:.7,duration:{T3-T0-.6}}},{T0+.3}).to("#Rglow",{{opacity:0,duration:{T3-T0-.6}}},{T0+.3});'
    js+=f'tl.to("#Lheat",{{scale:1.15,duration:{T3-T0-.6}}},{T0+.3}).to("#Lglow",{{opacity:1,scale:1.15,duration:.8,yoyo:true,repeat:5}},{T0+.3});'
    js+=badges_js(T3)+why_js(T4)+endjs(T5)
    ev=[(.05,sfx.whoosh(.6,.25)),(.3,sfx.chime(440,.12,2)),(T0+.3,sfx.whoosh(T3-T0,.06))]+[(T0+.5+i*.55,sfx.click(.15)) for i in range(11)]
    ev+=[(T3,sfx.boom(.3)),(T3+.4,sfx.chime(784,.16,2.2)),(T4,sfx.whoosh(.5,.15))]+endev(T5)
    render('t14_ozhog',14,DUR,body,js,ev,(T3+.8,1.0,T0+3,T3+.6,T4+1.5,T5+3))
# ---------- №15 шрам: 12 недель
if not which or 't15' in which:
    def scar(s):
        sheet=('<div id="Rsheet" style="position:absolute;left:80px;top:290px;width:310px;height:130px;border-radius:34px;background:rgba(255,255,255,.35);box-shadow:inset 0 0 0 3px rgba(255,255,255,.85),0 10px 20px -8px rgba(30,40,60,.25)"></div>' if s=='R' else '')
        return (f'<div style="position:absolute;left:30px;top:230px;width:410px;height:260px;border-radius:70px;{SKIN.replace("90deg","180deg")}"></div>'
                f'<div id="{s}sc" style="position:absolute;left:110px;top:345px;width:250px;height:22px;border-radius:11px;background:linear-gradient(180deg,#E0566A,#B83248);box-shadow:0 4px 0 rgba(150,40,60,.4),0 0 14px 4px rgba(224,86,106,.35)"></div>{sheet}')
    T0=2.4; T3=8.6; T4=10.0; T5=13.6; DUR=18.6
    body=f'''<section id="a" class="clip" data-start="0" data-duration="{T5}" data-track-index="1">{bg()}{top(15)}
<div id="hk" style="{HK}">Шрам.<br><span style="color:{ORANGE}">12 недель<br>за 6 секунд.</span></div>
<div id="wy" style="{WHY};font-size:44px">Силиконовые пластины —<br>первая линия ухода за рубцами*.<br><span style="color:{ORANGE}">Начинать после заживления,<br>носить ежедневно, месяцами.</span></div>
{card(LX,"cl","БЕЗ УХОДА",GREY,scar("L"))}{card(RX,"cr","СИЛИКОНОВАЯ ПЛАСТИНА",ORANGE,scar("R"))}
{chip_counter("Неделя 1")}
{badge("bl",LX,False,"Может стать<br>ярким и выпуклым")}{badge("br",RX,True,"Мягче и бледнее")}
<div style="position:absolute;left:60px;right:60px;bottom:90px;text-align:center;font-size:20px;color:rgba(43,43,43,.55)">Иллюстрация. Результат индивидуален.</div></section>
{endsec(T5,DUR,'<div style="position:absolute;left:10px;top:60px;width:280px;height:180px;border-radius:40px;background:linear-gradient(145deg,rgba(255,240,225,.9),rgba(240,205,170,.85));box-shadow:inset 0 0 0 3px rgba(255,255,255,.8),0 20px 30px -10px rgba(90,60,30,.35)"></div>',"Шрам —","это 12 недель заботы.","Напишите «ШРАМ» — пришлём памятку:<br>когда начинать и сколько носить","*Meaume S. et al., 2014. Режим ношения — по инструкции и рекомендации врача.<br>")}'''
    js=INTRO+f'tl.to("#dy",{{opacity:1,duration:.3}},{T0-.2});const dd=document.getElementById("dyt");const o={{w:1}};tl.to(o,{{w:12,duration:{T3-T0-.4},ease:"none",onUpdate:()=>{{dd.textContent="Неделя "+Math.round(o.w)}}}},{T0});'
    js+=f'tl.from("#Rsheet",{{y:-300,opacity:0,duration:.4}},{T0-.4});'
    js+=f'tl.to("#Lsc",{{height:30,top:341,background:"linear-gradient(180deg,#D9435E,#A82640)",boxShadow:"0 6px 0 rgba(140,30,50,.5),0 0 18px 6px rgba(217,67,94,.4)",duration:{T3-T0}}},{T0});'
    js+=f'tl.to("#Rsc",{{height:12,top:350,background:"linear-gradient(180deg,#F0B4A6,#E39C8E)",boxShadow:"0 1px 0 rgba(150,90,80,.2),0 0 0 0 rgba(0,0,0,0)",duration:{T3-T0}}},{T0});'
    js+=f'tl.to("#Rsheet",{{opacity:.25,duration:.4}},{T3-.4});'
    js+=badges_js(T3)+why_js(T4)+endjs(T5)
    ev=[(.05,sfx.whoosh(.6,.25)),(.3,sfx.chime(440,.12,2)),(T0-.4,sfx.click(.3))]+[(T0+i*(T3-T0)/11,sfx.click(.15)) for i in range(12)]
    ev+=[(T3,sfx.boom(.3)),(T3+.4,sfx.chime(784,.16,2.2)),(T4,sfx.whoosh(.5,.15))]+endev(T5)
    render('t15_shram_12_nedel',15,DUR,body,js,ev,(T3+.8,1.2,T0+3,T3+.6,T4+1.5,T5+3))
