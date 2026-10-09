# Шаг 21: «Миф: ране надо подышать» — корка vs влажная среда (Winter, Nature 1962)
from fxkit import *
def section(side):
    # разрез кожи в карточке 470×700: эпидермис, дерма, жир; рана по центру
    gap='polygon(140px 0,330px 0,290px 150px,250px 230px,220px 230px,180px 150px)'
    cover=('<div style="position:absolute;left:110px;top:150px;width:250px;height:80px;border-radius:30px 40px 20px 34px;background:radial-gradient(ellipse at 40% 40%,#6B3B22,#4A2614 60%,#341A0D);box-shadow:0 6px 12px rgba(40,20,10,.5)"></div>'
           if side=='L' else
           '<div style="position:absolute;left:150px;top:200px;width:170px;height:170px;clip-path:polygon(0 0,100% 0,82% 60%,58% 100%,42% 100%,18% 60%);background:linear-gradient(180deg,rgba(150,200,240,.85),rgba(120,175,225,.7))"></div>'
           '<div style="position:absolute;left:20px;top:168px;width:430px;height:36px;border-radius:18px;background:linear-gradient(180deg,rgba(248,232,205,.97),rgba(226,196,155,.95));box-shadow:0 6px 12px rgba(90,60,30,.3)"></div>')
    y=262 if side=='L' else 212  # под коркой клетки ползут глубже, во влажной среде — по поверхности
    cells=lambda k,x0,d: ''.join(f'<div class="c{k}" style="position:absolute;left:{x0+d*i*28}px;top:{y}px;width:26px;height:26px;border-radius:50%;background:radial-gradient(circle at 35% 35%,#FFD9A0,#F38221);box-shadow:0 0 6px rgba(243,130,33,.6)"></div>' for i in range(4))
    return (f'<div style="position:absolute;left:0;top:200px;width:470px;height:40px;background:#F3CBAA"></div>'
            f'<div style="position:absolute;left:0;top:240px;width:470px;height:180px;background:linear-gradient(180deg,#EBA98E,#DF8F75)"></div>'
            f'<div style="position:absolute;left:0;top:420px;width:470px;height:110px;background:linear-gradient(180deg,#F6E2AE,#EFD08E)"></div>'
            f'<div id="w{side}" style="position:absolute;left:0;top:200px;width:470px;height:230px;clip-path:{gap};background:radial-gradient(ellipse at 50% 30%,#D9564A,#B8362C);transform-origin:50% 0"></div>'
            # новая кожа растёт от краёв раны (во влажной среде — по поверхности, под коркой — глубже)
            f'<div id="n{side}l" style="position:absolute;left:140px;top:{204 if side=="R" else 246}px;width:96px;height:{34 if side=="R" else 26}px;border-radius:0 18px 18px 0;background:linear-gradient(180deg,#FFD9C2,#F6B99A);box-shadow:0 0 0 3px #F38221;transform-origin:0 50%;transform:scaleX(0)"></div>'
            f'<div id="n{side}r" style="position:absolute;left:234px;top:{204 if side=="R" else 246}px;width:96px;height:{34 if side=="R" else 26}px;border-radius:18px 0 0 18px;background:linear-gradient(180deg,#FFD9C2,#F6B99A);box-shadow:0 0 0 3px #F38221;transform-origin:100% 50%;transform:scaleX(0)"></div>'
            f'{cover}<div id="g{side}l" style="position:absolute;inset:0">{cells(side+"l",52,1)}</div><div id="g{side}r" style="position:absolute;inset:0">{cells(side+"r",398,-1)}</div>'
            f'<div style="position:absolute;left:0;right:0;top:560px;text-align:center;font-size:26px;color:#555;line-height:1.3">{"корка сверху" if side=="L" else "плёнка + влажная среда"}</div>')
T1,T2,T3,T4,T5=2.4,3.0,7.4,8.4,12.6; DUR=17.6
body=f'''<section id="a" class="clip" data-start="0" data-duration="{T5}" data-track-index="1">{bg()}{top(3)}
<div id="hk" style="position:absolute;left:60px;right:60px;top:300px;text-align:center;{F};font-weight:900;font-size:80px;line-height:1.04;letter-spacing:-0.02em;color:{INK}">«Пусть подышит,<br>подсохнет»? <span style="color:{ORANGE}">Миф.</span></div>
<div id="wy" style="position:absolute;left:60px;right:60px;top:290px;text-align:center;{F};font-weight:800;font-size:48px;line-height:1.12;color:{INK};opacity:0">Опыт Винтера (Nature, 1962):<br>под плёнкой раны затягивались<br><span style="color:{ORANGE}">примерно вдвое быстрее,<br>чем под коркой.</span></div>
{card(LX,"cl","КОРКА",GREY,section("L"))}{card(RX,"cr","ВЛАЖНАЯ СРЕДА",ORANGE,section("R"))}
<div id="dy" style="position:absolute;left:0;right:0;top:{CY-86}px;text-align:center;opacity:0"><span id="dyt" style="display:inline-block;padding:16px 40px;border-radius:50px;background:{INK};color:#fff;{F};font-weight:800;font-size:44px">День 1</span></div>
{badge("bl",LX,False,"Клеткам приходится<br>ползти под корку")}{badge("br",RX,True,"Края сошлись")}
<div style="position:absolute;left:60px;right:60px;bottom:90px;text-align:center;font-size:20px;color:rgba(43,43,43,.55)">Схема. Эксперимент на животных: Winter G.D., Nature, 1962.</div></section>
<section id="z" class="clip" data-start="{T5}" data-duration="{DUR-T5}" data-track-index="1">{bg()}
<div id="zp" style="position:absolute;left:390px;top:350px;width:300px;height:260px"><div style="position:absolute;inset:0;border-radius:50%;background:radial-gradient(ellipse,rgba(250,245,232,.95) 0 30%,rgba(232,200,160,.92) 55%,rgba(214,176,132,.9));box-shadow:0 30px 40px -16px rgba(90,60,30,.45)"></div></div>
<div id="z1" style="position:absolute;left:40px;right:40px;top:700px;text-align:center;{F};font-weight:900;font-size:82px;line-height:1.04;letter-spacing:-0.02em;color:{INK}">Ране не нужно «дышать».<br><span style="color:{ORANGE}">Ей нужна влага.</span></div>
<div id="z2" style="position:absolute;left:0;right:0;top:1010px;text-align:center">{logo(110,ORANGE,True)}</div>
<div id="z3" style="position:absolute;left:80px;right:80px;top:1230px;text-align:center;font-size:38px;font-weight:600;line-height:1.35;color:{INK}">Перешлите тому, кто говорит<br>«пусть подсохнет» 😉</div>
<div style="position:absolute;left:70px;right:70px;bottom:90px;text-align:center;font-size:20px;line-height:1.5;color:rgba(43,43,43,.55)">Гидроколлоидные и гидрогелевые повязки Yafho. Глубокие, укушенные, грязные или воспалённые раны — сразу к врачу.<br>Медицинское изделие. Применение — по назначению специалиста.</div></section>'''
js=(f'tl.from("#hk",{{scale:1.5,opacity:0,duration:.4,ease:"power3.out"}},.05).from("#cl,#cr",{{y:200,opacity:0,duration:.6,stagger:.12,ease:"power3.out"}},.3);'
    f'tl.from(".cLl,.cLr,.cRl,.cRr",{{scale:0,duration:.3,stagger:.04,ease:"back.out(2)"}},{T1});'
    f'tl.to("#dy",{{opacity:1,duration:.3}},{T2});'
    f'const dd=document.getElementById("dyt");const o={{d:1}};tl.to(o,{{d:7,duration:{T3-T2-.6},ease:"none",onUpdate:()=>{{dd.textContent="День "+Math.round(o.d)}}}},{T2+.3});'
    f'tl.to("#gLl",{{x:28,duration:{T3-T2},ease:"none"}},{T2}).to("#gLr",{{x:-28,duration:{T3-T2},ease:"none"}},{T2});'
    f'tl.to("#gRl",{{x:86,duration:{T3-T2-.6},ease:"power1.inOut"}},{T2}).to("#gRr",{{x:-86,duration:{T3-T2-.6},ease:"power1.inOut"}},{T2});'
    f'tl.to("#nLl,#nLr",{{scaleX:.3,duration:{T3-T2},ease:"none"}},{T2}).to("#nRl,#nRr",{{scaleX:1,duration:{T3-T2-.6},ease:"power1.inOut"}},{T2});'
    f'tl.to("#wR",{{scaleY:.45,duration:{T3-T2},ease:"power1.inOut"}},{T2}).to("#wL",{{scaleY:.92,duration:{T3-T2}}},{T2});'
    f'tl.from("#bl",{{scale:.4,opacity:0,duration:.35,ease:"back.out(2)"}},{T3}).from("#br",{{scale:.4,opacity:0,duration:.35,ease:"back.out(2)"}},{T3+.4});'
    f'tl.to("#hk",{{opacity:0,y:-20,duration:.3}},{T4}).to("#wy",{{opacity:1,duration:.4}},{T4+.2});'
    f'tl.from("#zp",{{scale:2.2,opacity:0,duration:.8,ease:"power3.out"}},{T5}).from("#z1",{{opacity:0,y:30,duration:.5}},{T5+.6}).from("#z2",{{opacity:0,duration:.5}},{T5+1.2}).from("#z3",{{opacity:0,y:20,duration:.5}},{T5+1.7});')
ev=[(.05,sfx.whoosh(.6,.25)),(.3,sfx.chime(440,.12,2)),(T1,sfx.click(.3)),(T2,sfx.whoosh(.5,.15))]+[(T2+.3+i*.62,sfx.click(.22)) for i in range(7)]
ev+=[(T3,sfx.boom(.3)),(T3+.4,sfx.chime(784,.16,2.2)),(T4,sfx.whoosh(.5,.15)),(T5,sfx.whoosh(.9,.3)),(T5+.6,sfx.boom(.5)),(T5+1.2,sfx.chime(659,.18,3))]
shots=style_reel('t3_mif_podyshat',DUR,body,js,'Тест Yafho №3',ev,pad=(110,164.8,220,277.2),pad_amp=.04,check=(T3+.6,1.2,T2+2,T3+.8,T4+1.5,T5+3),bg='#C9D3E3',outdir=V20)
strip(shots,'kp/chk_t3_mif_podyshat.jpg',2400); print('ok',DUR)
