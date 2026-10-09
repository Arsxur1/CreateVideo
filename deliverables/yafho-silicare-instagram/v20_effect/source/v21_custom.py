# Шаги 27–29: ТЕСТ №8 «Что остаётся на пластыре», №9 «Банан: 8 часов», №10 «Как правильно снимать»
import sys
from fxkit import *
which=sys.argv[1:]
WHY='position:absolute;left:60px;right:60px;top:290px;text-align:center;font-family:\'Inter Display\',sans-serif;font-weight:800;font-size:48px;line-height:1.12;color:#2B2B2B;opacity:0'
HK='position:absolute;left:60px;right:60px;top:300px;text-align:center;font-family:\'Inter Display\',sans-serif;font-weight:900;font-size:76px;line-height:1.04;letter-spacing:-0.02em;color:#2B2B2B'
def endsec(T,DUR,prod,e1,e2,cta,note):
    return f'''<section id="z" class="clip" data-start="{T}" data-duration="{DUR-T}" data-track-index="1">{bg()}
<div id="zp" style="position:absolute;left:390px;top:330px;width:300px;height:300px">{prod}</div>
<div id="z1" style="position:absolute;left:40px;right:40px;top:700px;text-align:center;{F};font-weight:900;font-size:84px;line-height:1.04;letter-spacing:-0.02em;color:{INK}">{e1}<br><span style="color:{ORANGE}">{e2}</span></div>
<div id="z2" style="position:absolute;left:0;right:0;top:1010px;text-align:center">{logo(110,ORANGE,True)}</div>
<div id="z3" style="position:absolute;left:80px;right:80px;top:1230px;text-align:center;font-size:38px;font-weight:600;line-height:1.35;color:{INK}">{cta}</div>
<div style="position:absolute;left:70px;right:70px;bottom:90px;text-align:center;font-size:20px;line-height:1.5;color:rgba(43,43,43,.55)">{note}Медицинское изделие. Применение — по назначению специалиста.</div></section>'''
def endjs(T): return f'tl.from("#zp",{{scale:2.2,opacity:0,rotation:-15,duration:.8,ease:"power3.out"}},{T}).from("#z1",{{opacity:0,y:30,duration:.5}},{T+.6}).from("#z2",{{opacity:0,duration:.5}},{T+1.2}).from("#z3",{{opacity:0,y:20,duration:.5}},{T+1.7});'
def endev(T): return [(T,sfx.whoosh(.9,.3)),(T+.6,sfx.boom(.5)),(T+1.2,sfx.chime(659,.18,3))]
def intro_js(): return 'tl.from("#hk",{scale:1.5,opacity:0,duration:.4,ease:"power3.out"},.05).from("#cl,#cr",{y:200,opacity:0,duration:.6,stagger:.12,ease:"power3.out"},.3);'
def render(name,n,DUR,body,js,ev,check):
    shots=style_reel(name,DUR,body,js,f'Тест Yafho №{n}',ev,pad=(110,164.8,220,277.2),pad_amp=.04,check=check,bg='#C9D3E3',outdir=V20)
    strip(shots,f'kp/chk_{name}.jpg',2400); print('ok',name,DUR,flush=True)
# ---------- №8 стена рогового слоя
if not which or 't8' in which:
    def wall(s):
        rows=''
        for r in range(6):
            bricks=''.join(f'<div id="{s}b{r}{c}" style="position:absolute;left:{(c*58)+(29 if r%2 else 0)-20}px;top:0;width:54px;height:30px;border-radius:7px;background:linear-gradient(180deg,#FBE3CF,#EFC5A3);box-shadow:inset 0 -2px 0 rgba(170,100,60,.35)"></div>' for c in range(8))
            rows+=f'<div id="{s}r{r}" style="position:absolute;left:30px;width:410px;height:30px;top:{250+r*34}px;overflow:hidden">{bricks}</div>'
        return (f'<div style="position:absolute;left:0;right:0;top:250px;height:210px;overflow:hidden"></div>{rows}'
                f'<div id="{s}live" style="position:absolute;left:20px;width:430px;top:{250+6*34}px;height:70px;border-radius:12px;background:linear-gradient(180deg,#F08A78,#D9473B)"></div>'
                f'<div style="position:absolute;left:0;right:0;top:{250+6*34+84}px;text-align:center;font-size:24px;color:#555">роговой слой ↑ · живая кожа ↓</div>'
                f'<div id="{s}p" style="position:absolute;left:40px;top:120px;width:390px;height:70px;border-radius:35px;'
                +('background:linear-gradient(180deg,#fff,#E4E7EA);box-shadow:0 10px 20px rgba(30,40,60,.25)' if s=='L' else 'background:linear-gradient(145deg,#F6D2AE,#E8B485);box-shadow:0 10px 20px rgba(80,40,10,.3)')+'">'
                +(''.join(f'<div id="Ls{i}" style="position:absolute;left:24px;width:342px;top:{6+i*12}px;height:9px;border-radius:5px;background:repeating-linear-gradient(90deg,#EFC5A3 0 50px,#D9A07C 50px 54px);opacity:0"></div>' for i in range(5)) if s=='L'
                  else ''.join(f'<div id="Rs{i}" style="position:absolute;left:{120+i*90}px;top:24px;width:44px;height:20px;border-radius:6px;background:#EFC5A3;box-shadow:inset 0 -2px 0 rgba(170,100,60,.4);opacity:0"></div>' for i in range(2)))+'</div>')
    T0=2.6; C=.95; T3=T0+5*C+.3; T4=T3+1.4; T5=12.8; DUR=17.8
    body=f'''<section id="a" class="clip" data-start="0" data-duration="{T5}" data-track-index="1">{bg()}{top(8)}
<div id="hk" style="{HK}">Что остаётся<br><span style="color:{ORANGE}">на пластыре?</span></div>
<div id="wy" style="{WHY}">Каждый рывок забирает<br>слой рогового слоя кожи.<br><span style="color:{ORANGE}">5 перевязок — 5 слоёв.<br>Силикон забирает меньше.</span></div>
{card(LX,"cl","ОБЫЧНЫЙ ПЛАСТЫРЬ",GREY,wall("L"))}{card(RX,"cr","СИЛИКОН YAFHO",ORANGE,wall("R"))}
<div id="dy" style="position:absolute;left:0;right:0;top:{CY-86}px;text-align:center;opacity:0"><span id="dyt" style="display:inline-block;padding:16px 40px;border-radius:50px;background:{INK};color:#fff;{F};font-weight:800;font-size:44px">Перевязка 1</span></div>
{badge("bl",LX,False,"Живая кожа<br>уже близко")}{badge("br",RX,True,"Слой почти цел")}
<div style="position:absolute;left:60px;right:60px;bottom:90px;text-align:center;font-size:20px;color:rgba(43,43,43,.55)">Схема. Снятие рогового слоя клейкой лентой (tape stripping) — стандартный метод дерматологических исследований.</div></section>
{endsec(T5,DUR,sili(0,0,300,"transform:rotate(-6deg)"),"Перевязка —","не наждачка.","Частые перевязки, хрупкая кожа:<br>напишите «СЛОЙ» — подберём повязку","")}'''
    js=intro_js()+f'tl.to("#dy",{{opacity:1,duration:.3}},{T0-.2});'
    ev=[(.05,sfx.whoosh(.6,.25)),(.3,sfx.chime(440,.12,2))]
    rgone={0,2}  # у силикона за 5 перевязок уходит лишь пара отдельных «кирпичиков»
    for i in range(5):
        t=T0+i*C
        js+=f'tl.call(()=>{{document.getElementById("dyt").textContent="Перевязка {i+1}"}},null,{t});'
        js+=f'tl.to("#Lp,#Rp",{{y:110,duration:.22,ease:"power2.in"}},{t}).to("#Lp,#Rp",{{y:0,duration:.35,ease:"power3.out"}},{t+.42});'
        js+=f'tl.to("#Lr{i}",{{y:-60,opacity:0,duration:.2,ease:"power3.out"}},{t+.42}).to("#Ls{i}",{{opacity:1,duration:.1}},{t+.45});'
        if i in rgone: k=sorted(rgone).index(i); js+=f'tl.to("#Rb{i}{3+i}",{{y:-60,opacity:0,duration:.2}},{t+.42}).to("#Rs{k}",{{opacity:1,duration:.1}},{t+.45});'
        ev+=[(t+.22,sfx.click(.4)),(t+.42,sfx.tear(.3,.4 if True else .1))]
    js+=f'tl.to("#Llive",{{boxShadow:"0 0 30px 10px rgba(230,70,50,.7)",duration:.4}},{T3-.3});'
    js+=f'tl.from("#bl",{{scale:.4,opacity:0,duration:.35,ease:"back.out(2)"}},{T3}).from("#br",{{scale:.4,opacity:0,duration:.35,ease:"back.out(2)"}},{T3+.4});'
    js+=f'tl.to("#dy",{{opacity:0,duration:.2}},{T4}).to("#hk",{{opacity:0,y:-20,duration:.3}},{T4}).to("#wy",{{opacity:1,duration:.4}},{T4+.2});'+endjs(T5)
    ev+=[(T3,sfx.boom(.3)),(T3+.4,sfx.chime(784,.16,2.2)),(T4,sfx.whoosh(.5,.15))]+endev(T5)
    render('t8_chto_na_plastyre',8,DUR,body,js,ev,(T3+.8,1.2,T0+2*C+.6,T3+.6,T4+1.5,T5+3))
# ---------- №9 банан: 8 часов давления
if not which or 't9' in which:
    def banana(s):
        pad=(f'<div id="{s}pad" style="position:absolute;left:150px;top:300px;width:170px;height:60px;border-radius:30px;background:linear-gradient(145deg,#F6D2AE,#E8B485);box-shadow:0 8px 16px rgba(80,40,10,.3)"></div>' if s=='R' else '')
        return (f'<svg viewBox="0 0 470 700" style="position:absolute;inset:0"><defs><linearGradient id="bg{s}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFE680"/><stop offset="1" stop-color="#E9BE2A"/></linearGradient></defs>'
                f'<path d="M50 330 Q235 430 420 320 Q438 312 432 334 Q240 470 40 352 Q30 340 50 330 Z" fill="url(#bg{s})" stroke="#B88A10" stroke-width="3"/>'
                f'<path d="M420 320 L440 306" stroke="#5A4A1A" stroke-width="10" stroke-linecap="round"/><circle cx="44" cy="344" r="7" fill="#3A2E10"/></svg>'
                f'<div id="{s}br" style="position:absolute;left:{170 if s=="L" else 205}px;top:{352 if s=="L" else 360}px;width:{130 if s=="L" else 60}px;height:{60 if s=="L" else 26}px;border-radius:50%;background:radial-gradient(ellipse,{"#2A1A08" if s=="L" else "rgba(120,80,20,.6)"},{"#5A3A10" if s=="L" else "rgba(150,110,30,.25)"} 60%,transparent 75%);opacity:0;transform:scale(.2)"></div>'
                f'{pad}<div id="{s}w" style="position:absolute;left:160px;top:60px;width:150px;height:170px">'
                f'<div style="position:absolute;left:35px;top:0;width:80px;height:70px;border-radius:40px 40px 0 0;border:18px solid #3B3F46;border-bottom:none"></div>'
                f'<div style="position:absolute;left:0;top:44px;width:150px;height:126px;border-radius:50% 50% 40% 40%;background:radial-gradient(circle at 35% 30%,#6B717B,#2F3238);display:flex;align-items:center;justify-content:center;color:#fff;{F};font-weight:900;font-size:40px">8 ч</div></div>')
    T0=2.6; T3=7.6; T4=9.0; T5=13.2; DUR=18.2
    body=f'''<section id="a" class="clip" data-start="0" data-duration="{T5}" data-track-index="1">{bg()}{top(9)}
<div id="hk" style="{HK}">8 часов<br>в одной позе.<br><span style="color:{ORANGE}">Тест на банане.</span></div>
<div id="wy" style="{WHY};font-size:44px">Так начинаются пролежни:<br>давление в одной точке часами.<br><span style="color:{ORANGE}">Силиконовую пену рекомендуют<br>для профилактики на крестце*.</span></div>
{card(LX,"cl","БЕЗ ЗАЩИТЫ",GREY,banana("L"))}{card(RX,"cr","ПЕНА SILI-CARE",ORANGE,banana("R"))}
<div id="dy" style="position:absolute;left:0;right:0;top:{CY-86}px;text-align:center;opacity:0"><span id="dyt" style="display:inline-block;padding:16px 40px;border-radius:50px;background:{INK};color:#fff;{F};font-weight:800;font-size:44px">⏳ 0 ч</span></div>
{badge("bl",LX,False,"Тёмное пятно —<br>след давления")}{badge("br",RX,True,"Давление<br>распределилось")}
<div style="position:absolute;left:60px;right:60px;bottom:90px;text-align:center;font-size:20px;color:rgba(43,43,43,.55)">Демонстрация на фрукте, не клиническое испытание.</div></section>
{endsec(T5,DUR,sili(0,0,300,"",heart=True),"Давление —","не в одну точку.","Повязка не заменяет переворачивание.<br>Перешлите тому, кто ухаживает<br>за лежачим близким 🤍","*EPUAP/NPIAP/PPPIA, международное руководство по профилактике пролежней, 2019.<br>")}'''
    js=intro_js()+f'tl.from("#Rpad",{{y:-400,opacity:0,duration:.45,ease:"power2.in"}},{T0-.6});'
    js+=f'tl.from("#Lw,#Rw",{{y:-500,opacity:0,duration:.5,ease:"power2.in"}},{T0}).to("#Lw",{{y:200,duration:.25,ease:"power2.in"}},{T0+.5}).to("#Rw",{{y:170,duration:.25,ease:"power2.in"}},{T0+.5});'
    js+=f'tl.to("#cl,#cr",{{y:6,duration:.08,yoyo:true,repeat:1}},{T0+.75});'
    js+=f'tl.to("#dy",{{opacity:1,duration:.3}},{T0+.9});const dh=document.getElementById("dyt");const oh={{h:0}};tl.to(oh,{{h:8,duration:{T3-T0-1.6},ease:"none",onUpdate:()=>{{dh.textContent="⏳ "+Math.round(oh.h)+" ч"}}}},{T0+1.1});'
    js+=f'tl.to("#Lbr",{{opacity:1,scale:1,duration:{T3-T0-1.6},ease:"power1.in"}},{T0+1.1}).to("#Rbr",{{opacity:.8,scale:1,duration:{T3-T0-1.6}}},{T0+1.1});'
    js+=f'tl.to("#Lw,#Rw",{{y:-500,opacity:0,duration:.5,ease:"power2.in"}},{T3-.5}).to("#Rpad",{{y:-120,opacity:.0,duration:.4}},{T3-.2});'
    js+=f'tl.from("#bl",{{scale:.4,opacity:0,duration:.35,ease:"back.out(2)"}},{T3}).from("#br",{{scale:.4,opacity:0,duration:.35,ease:"back.out(2)"}},{T3+.4});'
    js+=f'tl.to("#dy",{{opacity:0,duration:.2}},{T4}).to("#hk",{{opacity:0,y:-20,duration:.3}},{T4}).to("#wy",{{opacity:1,duration:.4}},{T4+.2});'+endjs(T5)
    ev=[(.05,sfx.whoosh(.6,.25)),(.3,sfx.chime(440,.12,2)),(T0-.2,sfx.click(.3)),(T0+.75,sfx.boom(.6))]+[(T0+1.1+i*.62,sfx.click(.2)) for i in range(8)]
    ev+=[(T3-.5,sfx.whoosh(.5,.2)),(T3,sfx.boom(.3)),(T3+.4,sfx.chime(784,.16,2.2)),(T4,sfx.whoosh(.5,.15))]+endev(T5)
    render('t9_banan_8_chasov',9,DUR,body,js,ev,(T3+.8,1.2,T0+3,T3+.6,T4+1.5,T5+3))
# ---------- №10 как правильно снимать
if not which or 't10' in which:
    def tech(s):
        flat='M0 380 C120 380 350 380 470 380'; tent='M0 380 C110 380 120 300 150 280 C180 300 200 380 470 380'
        skin=(f'<svg viewBox="0 0 470 700" style="position:absolute;inset:0"><path id="{s}sk" d="{flat} L470 520 L0 520 Z" fill="#F0C4A4"/>'
              f'<path id="{s}sl" d="{flat}" stroke="#C98B66" stroke-width="5" fill="none"/></svg>'
              f'<div id="{s}red" style="position:absolute;left:90px;top:270px;width:130px;height:120px;border-radius:50%;background:radial-gradient(closest-side,rgba(230,70,50,.55),transparent);opacity:0"></div>')
        pl=(f'<div id="{s}pl" style="position:absolute;left:60px;top:358px;width:350px;height:24px;border-radius:12px;background:linear-gradient(180deg,#fff,#DDE1E5);box-shadow:0 4px 8px rgba(30,40,60,.25);transform-origin:100% 50%"></div>')
        arr=('<div style="position:absolute;left:30px;top:150px;'+F+';font-weight:900;font-size:90px;color:#D93A2F">↑</div><div style="position:absolute;left:100px;top:180px;font-size:28px;color:#D93A2F;font-weight:800">90°</div>'
             if s=='L' else
             '<div id="Rfg" style="position:absolute;left:20px;top:330px;width:46px;height:60px;border-radius:24px 24px 20px 20px;background:linear-gradient(180deg,#F7D2B8,#E8AE8A);box-shadow:0 4px 8px rgba(90,40,20,.3)"></div>'
             '<div style="position:absolute;left:250px;top:250px;'+F+';font-weight:900;font-size:90px;color:#2E9E5B">←</div><div style="position:absolute;left:250px;top:220px;font-size:28px;color:#2E9E5B;font-weight:800">180°, медленно</div>')
        return skin+pl+f'<div id="{s}ar" style="position:absolute;inset:0;opacity:0">{arr}</div>'
    T0=2.6; T1=3.4; T3=7.6; T4=9.0; T5=13.2; DUR=18.2
    body=f'''<section id="a" class="clip" data-start="0" data-duration="{T5}" data-track-index="1">{bg()}{top(10)}
<div id="hk" style="{HK}">Как правильно<br><span style="color:{ORANGE}">снимать пластырь?</span></div>
<div id="wy" style="{WHY}">Не вверх, а вдоль кожи:<br>низко, медленно, придерживая<br>кожу пальцем.<br><span style="color:{ORANGE}">Так советует консенсус по MARSI.</span></div>
{card(LX,"cl","РЫВКОМ ВВЕРХ",RED,tech("L"))}{card(RX,"cr","НИЗКО И МЕДЛЕННО",ORANGE,tech("R"))}
{badge("bl",LX,False,"Кожа тянется<br>за клеем")}{badge("br",RX,True,"Кожа на месте")}
<div style="position:absolute;left:60px;right:60px;bottom:90px;text-align:center;font-size:20px;color:rgba(43,43,43,.55)">Схема. Техника снятия — McNichol L. et al., консенсус по MARSI, 2013.</div></section>
{endsec(T5,DUR,sili(0,0,300,"transform:rotate(-6deg)"),"Низко","и медленно.","А для хрупкой кожи — силикон Yafho.<br>Сохраните 📌 и перешлите","")}'''
    tent='M0 380 C110 380 120 300 150 280 C180 300 200 380 470 380'
    js=intro_js()+f'tl.to("#Lar,#Rar",{{opacity:1,duration:.3}},{T0});'
    # слева: рывок вверх — кожа «шатром» тянется за пластырем
    js+=f'tl.to("#Lpl",{{rotation:62,duration:.5,ease:"power3.in"}},{T1}).to("#Lsl",{{attr:{{d:"{tent}"}},duration:.35,ease:"power3.out"}},{T1+.3}).to("#Lsk",{{attr:{{d:"{tent} L470 520 L0 520 Z"}},duration:.35,ease:"power3.out"}},{T1+.3}).to("#Lred",{{opacity:1,duration:.3}},{T1+.5});'
    js+=f'tl.to("#Lpl",{{y:-260,x:-60,opacity:0,duration:.4}},{T1+1.3}).to("#Lsl",{{attr:{{d:"M0 380 C120 380 350 380 470 380"}},duration:.6,ease:"elastic.out(1,.4)"}},{T1+1.3}).to("#Lsk",{{attr:{{d:"M0 380 C120 380 350 380 470 380 L470 520 L0 520 Z"}},duration:.6,ease:"elastic.out(1,.4)"}},{T1+1.3});'
    # справа: палец придерживает кожу, пластырь отгибается назад вдоль кожи
    js+=f'tl.from("#Rfg",{{y:-200,opacity:0,duration:.4}},{T1}).to("#Rpl",{{scaleX:0,duration:2.4,ease:"power1.inOut"}},{T1+.5}).to("#Rfg",{{x:300,duration:2.4,ease:"power1.inOut"}},{T1+.5});'
    js+=f'tl.from("#bl",{{scale:.4,opacity:0,duration:.35,ease:"back.out(2)"}},{T3}).from("#br",{{scale:.4,opacity:0,duration:.35,ease:"back.out(2)"}},{T3+.4});'
    js+=f'tl.to("#hk",{{opacity:0,y:-20,duration:.3}},{T4}).to("#wy",{{opacity:1,duration:.4}},{T4+.2});'+endjs(T5)
    ev=[(.05,sfx.whoosh(.6,.25)),(.3,sfx.chime(440,.12,2)),(T1+.3,sfx.tear(.45,.55)),(T1+.5,sfx.boom(.3)),(T1+.5,sfx.whoosh(2.4,.08))]
    ev+=[(T3,sfx.boom(.3)),(T3+.4,sfx.chime(784,.16,2.2)),(T4,sfx.whoosh(.5,.15))]+endev(T5)
    render('t10_kak_snimat',10,DUR,body,js,ev,(T1+.8,1.2,T1+1.6,T3+.6,T4+1.5,T5+3))
