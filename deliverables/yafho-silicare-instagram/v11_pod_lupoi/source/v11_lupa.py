# Шаг 9: серия «Под лупой» — по ролику на продукт (~14 с)
import sys
src=open('v9_e6_lupa_b2b.py').read(); exec(src[:src.index("P=[")])
V11=V9.replace('v9_series','v11_pod_lupoi')
hcol='<div style="position:absolute;inset:0;background:radial-gradient(ellipse at 45% 40%,#F1D6B0,#DDB688 65%,#C99C6C)"></div>'+''.join(f'<div class="bd" style="position:absolute;left:{x}px;top:{y}px;width:{s}px;height:{s*0.8:.0f}px;border-radius:50%;background:radial-gradient(circle at 40% 35%,rgba(255,250,235,.95),rgba(245,225,190,.75) 55%,rgba(210,175,130,.3));filter:blur(2px)"></div>' for x,y,s in [(220,300,220),(600,240,160),(660,560,240),(260,640,180),(520,860,140),(820,880,120)])+'<div class="sheen" style="position:absolute;inset:0;background:linear-gradient(115deg,transparent 35%,rgba(255,255,255,.3) 48%,transparent 60%)"></div>'
chg='<div style="position:absolute;inset:0;background:radial-gradient(ellipse at 50% 50%,#EBC7A6,#D9AE88)"></div><div style="position:absolute;left:0;right:0;top:590px;height:44px;background:linear-gradient(#f5f5f5,#cfd6de);box-shadow:0 6px 12px rgba(0,0,0,.25)"></div><div class="bd" style="position:absolute;left:390px;top:390px;width:440px;height:440px;border-radius:50%;background:radial-gradient(circle at 40% 35%,rgba(170,140,230,.85),rgba(110,80,190,.8) 60%,rgba(80,50,150,.75));box-shadow:inset 0 0 40px rgba(255,255,255,.4)"></div><div style="position:absolute;left:600px;top:390px;width:20px;height:240px;background:#D9AE88"></div><div style="position:absolute;inset:0;background:rgba(235,242,250,.18)"></div><div class="sheen" style="position:absolute;inset:0;background:linear-gradient(115deg,transparent 30%,rgba(255,255,255,.6) 45%,transparent 60%)"></div>'
# (id, имя, хук, подпись в лупе, где нужен[3], сноска, текстура)
P=[
 ('l1_wcl','Silicone Wound Contact Layer','Сетка тоньше<br><span style="color:#F38221">салфетки.</span>','ложится прямо на рану,<br>экссудат уходит сквозь ячейки',['Дерматология','Хрупкая кожа','Раны, где важна каждая перевязка'],'',mesh),
 ('l2_scar','Silicone Scar Sheet','Что делать<br><span style="color:#F38221">со шрамом?</span>','силиконовый гель-лист —<br>первая линия ухода за рубцами*',['Пластическая хирургия','После кесарева','Когда рана уже закрылась'],'* Meaume S. et al., 2014. Начинать после заживления, по назначению врача.',gel),
 ('l3_nonwoven','Silicone Nonwoven','Пластырь, который<br><span style="color:#F38221">не спорит с кожей.</span>','нетканая основа + силикон:<br>держит и снимается мягко',['Фиксация повязок и катетеров','Пожилые пациенты','Дети'],'',nonw),
 ('l4_hydrogel','Hydrogel Dressing','Рана сухая?<br><span style="color:#F38221">Ей нужна влага.</span>','гидрогель отдаёт влагу<br>сухой ране*',['Хирургия','Дерматология','Сухие раны и струп'],'* Влажная среда заживления: Winter G., Nature, 1962.',hyd),
 ('l5_hydrocolloid','Hydrocolloid Dressing','Пластырь, который<br><span style="color:#F38221">становится гелем.</span>','с экссудатом образует<br>мягкий гель на ране',['Неглубокие раны','Умеренный экссудат','Зоны трения'],'',hcol),
 ('l6_chg','CHG I.V. Fixation','Катетер стоит днями.<br><span style="color:#F38221">А место прокола?</span>','плёнка + подушечка<br>с хлоргексидином (CHG)',['ОРИТ','Онкология и гематология','Везде, где стоит катетер'],'Состав и показания — по инструкции производителя.',chg),
]
only=sys.argv[1:]
for n,(key,name,hook,sub,where,note,tex) in enumerate(P,1):
    if only and key not in only: continue
    TA=2.6; D=4.2; TB=TA+D; DB=3.6; TZ=TB+DB; DZ=4.0; DUR=round(TZ+DZ,1)
    body=f'''<section id="h0" class="clip" data-start="0" data-duration="{TA}" data-track-index="1"><div class="fill" style="background:{BG}"></div>
<div id="lz" style="{LENS};background:radial-gradient(circle,#2a221b,#0E0B09)"></div>{ticks()}
<div style="position:absolute;left:0;right:0;top:150px;text-align:center;font-family:Inter Display,sans-serif;font-weight:700;font-size:28px;letter-spacing:.3em;color:rgba(255,255,255,.5)">ПОД ЛУПОЙ · №{n}</div>
<div id="hk" style="position:absolute;left:50px;right:50px;top:760px;text-align:center;font-family:Inter Display,sans-serif;font-weight:800;font-size:{86 if len(hook)<70 else 72}px;line-height:1.08;color:#fff">{hook}</div></section>'''
    body+=scene('a',TA,D,tex,name,sub).replace('ПОД ЛУПОЙ · SILI-CARE',f'ПОД ЛУПОЙ · №{n} · YAFHO').replace('font-weight:800;font-size:66px;color:#fff','font-weight:800;font-size:52px;color:#fff;white-space:nowrap').replace('top:1500px;','top:1490px;line-height:1.25;')
    chips=''.join(f'<div class="ch" style="display:inline-block;margin:14px 10px;padding:22px 40px;border-radius:60px;border:3px solid {ORANGE};color:#fff;font-size:46px;font-weight:700;white-space:nowrap">{w}</div><br>' for w in where)
    body+=f'''<section id="b" class="clip" data-start="{TB}" data-duration="{DB}" data-track-index="1"><div class="fill" style="background:{BG}"></div>
<div id="bt" style="position:absolute;left:0;right:0;top:600px;text-align:center;font-family:Inter Display,sans-serif;font-weight:800;font-size:80px;color:{ORANGE}">Где нужен</div>
<div style="position:absolute;left:40px;right:40px;top:760px;text-align:center;font-family:Inter Display,sans-serif">{chips}</div></section>'''
    body+=f'''<section id="z" class="clip" data-start="{TZ}" data-duration="{DZ}" data-track-index="1"><div class="fill" style="background:{BG}"></div>
<div id="z1" style="position:absolute;left:40px;right:40px;top:640px;text-align:center;font-family:Inter Display,sans-serif;font-weight:800;font-size:60px;color:#fff;white-space:nowrap">{name}</div>
<div id="z2" style="position:absolute;left:0;right:0;top:800px;text-align:center;filter:drop-shadow(0 0 20px rgba(243,130,33,.4))">{logo(100)}</div>
<div id="z3" style="position:absolute;left:80px;right:80px;top:1040px;text-align:center;font-family:Inter Display,sans-serif;font-size:42px;color:#fff;font-weight:600">Образцы и каталог для клиник:<br>напишите <span style="color:{ORANGE}">«ЛУПА»</span> в директ</div>
<div style="position:absolute;left:80px;right:80px;bottom:110px;text-align:center;font-size:22px;line-height:1.5;color:rgba(255,255,255,.45)">{note+'<br>' if note else ''}Медицинское изделие. Применение — по назначению специалиста. Иллюстрация.</div></section>'''
    js='tl.from("#lz",{scale:.3,opacity:0,duration:.6,ease:"back.out(1.4)"},.05).from("#hk",{opacity:0,y:30,duration:.5},.45);'
    js+=f'tl.fromTo("#at",{{filter:"blur(18px)",scale:1.25,x:60,y:40}},{{filter:"blur(0px)",scale:1.05,x:-60,y:-40,duration:{D},ease:"power1.out"}},{TA});tl.fromTo("#at",{{filter:"blur(18px)"}},{{filter:"blur(0px)",duration:.9}},{TA});'
    js+=f'tl.from("#al",{{opacity:0,y:30,duration:.4}},{TA+.6}).from("#as",{{opacity:0,duration:.4}},{TA+1.0}).fromTo("#a .sheen",{{xPercent:-60}},{{xPercent:60,duration:{D},ease:"none"}},{TA});'
    js+=f'tl.from("#a .bd",{{scale:.4,opacity:0,duration:.8,stagger:.15,ease:"back.out(1.6)"}},{TA+.8});'
    js+=f'tl.from("#bt",{{opacity:0,y:-20,duration:.4}},{TB+.1}).from("#b .ch",{{opacity:0,scale:.6,duration:.4,stagger:.35,ease:"back.out(2)"}},{TB+.5});'
    js+=f'tl.from("#z1",{{opacity:0,y:30,duration:.5}},{TZ+.1}).from("#z2",{{opacity:0,duration:.5}},{TZ+.6}).from("#z3",{{opacity:0,y:20,duration:.5}},{TZ+1.1});'
    ev=[(.05,sfx.whoosh(.6,.25)),(.5,sfx.chime(440,.15,2)),(TA-.2,sfx.whoosh(.5,.18)),(TA+.2,sfx.tear(1.0,.05)),(TA+.7,sfx.chime(523,.12,2)),(TB,sfx.whoosh(.5,.15))]
    ev+=[(TB+.5+i*.35,sfx.click(.25)) for i in range(3)]
    ev+=[(TZ,sfx.whoosh(.9,.3)),(TZ+.3,sfx.boom(.6)),(TZ+.6,sfx.chime(659,.18,3))]
    shots=style_reel(key,DUR,body,js,f'Под лупой №{n}',ev,pad=(110,164.8,220,277.2),pad_amp=.05,check=(TA+2.2,1.2,TB+2.2,TZ+2.5),bg=BG,outdir=V11)
    strip(shots,f'kp/chk_{key}.jpg',2400); print('ok',key,DUR,flush=True)
