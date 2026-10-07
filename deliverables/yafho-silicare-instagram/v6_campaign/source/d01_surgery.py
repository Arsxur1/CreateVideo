from kp import *
def person(kind, size, idp):
    s=4.5
    head='<circle cx="150" cy="170" r="92" fill="none" stroke="#2B2B2B" stroke-width="%s"/>'%s
    body='<path d="M40 420 C50 320 100 280 150 280 C200 280 250 320 260 420" fill="none" stroke="#2B2B2B" stroke-width="%s" stroke-linecap="round"/>'%s
    if kind=='surgeon':
        extra=f'''<path d="M62 150 C62 70 238 70 238 150 Z" fill="#E8F0FB" stroke="{BLUE}" stroke-width="{s}"/>
<path d="M78 180 L222 180 L214 238 C190 262 110 262 86 238 Z" fill="#E8F0FB" stroke="{BLUE}" stroke-width="{s}"/><path d="M78 186 L58 172 M222 186 L242 172" stroke="{BLUE}" stroke-width="{s}"/>
<path id="{idp}e1" d="M112 160 L132 160 M168 160 L188 160" stroke="#2B2B2B" stroke-width="{s+1}" stroke-linecap="round"/>'''
    else:
        extra=f'''<path d="M70 120 C80 60 220 60 230 120 L216 132 L84 132 Z" fill="#fff" stroke="#2B2B2B" stroke-width="{s}"/>
<rect x="139" y="84" width="22" height="8" fill="{MAGENTA}"/><rect x="146" y="77" width="8" height="22" fill="{MAGENTA}"/>
<path d="M118 172 Q124 166 132 172 M168 172 Q176 166 182 172" stroke="#2B2B2B" stroke-width="{s}" fill="none" stroke-linecap="round"/>
<path id="{idp}br" d="M164 150 L190 142" stroke="#2B2B2B" stroke-width="{s}" stroke-linecap="round"/>
<path d="M130 218 Q150 224 170 214" stroke="#2B2B2B" stroke-width="{s}" fill="none" stroke-linecap="round"/>'''
    return f'<svg id="{idp}" viewBox="0 0 300 440" width="{size}" height="{size*440/300:.0f}">{head}{extra}{body}</svg>'
def bubble(txt, x, y, w, id, dark=False, tail='left'):
    bg = INK if dark else '#F2F2F2'; col = '#fff' if dark else INK
    t = f'<div style="position:absolute;{"left:60px" if tail=="left" else "right:60px"};bottom:-26px;width:0;height:0;border-left:22px solid transparent;border-right:22px solid transparent;border-top:28px solid {bg}"></div>'
    return f'<div id="{id}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;background:{bg};color:{col};border-radius:40px;padding:34px 40px;font-size:50px;font-weight:700;line-height:1.15">{txt}{t}</div>'
days = ''.join(f'<div class="dy" style="width:120px;text-align:center"><div style="font-size:26px;color:#888;font-weight:600">День {i+1}</div><div class="tk{" on" if i in (0,1,3,5) else ""}" style="margin-top:10px;width:96px;height:96px;margin-left:12px;border-radius:24px;border:4px solid {"#F38221" if i in (0,1,3,5) else "#E5E5E5"};display:flex;align-items:center;justify-content:center;font-size:52px;color:{ORANGE}">{"✓" if i in (0,1,3,5) else ""}</div></div>' for i in range(7))
body = clip('h1',0,4.2,f'''<div style="position:absolute;left:90px;top:760px">{person("surgeon",380,"sg")}</div>
{bubble("Я сделал<br>идеальный шов.",90,380,640,"b1")}
<div id="nr" style="position:absolute;left:620px;top:860px;opacity:.25">{person("nurse",340,"ns")}</div>''') + \
clip('h2',4.2,6.0,f'''<div style="position:absolute;left:640px;top:120px">{person("nurse",300,"ns2")}</div>
{bubble("А я потом меняла на нём повязку.",70,180,560,"b2",dark=True,tail='right')}
<div style="position:absolute;left:90px;top:700px">{svg("surgery",900,4)}</div>
<div id="dg" style="position:absolute;left:40px;right:40px;top:1260px;display:flex;justify-content:space-between">{days}</div>
<div id="h2t" class="cap" style="top:1560px;font-size:64px">Снова. И снова.</div>''') + \
clip('h3',10.2,4.8,f'''<div id="e0" class="cap" style="top:300px;font-size:72px">Хорошо, когда повязку<br>можно снять <span style="color:{ORANGE}">бережно.</span></div>
<div id="e1" class="cap" style="top:640px;font-size:96px">Шов делает хирург.<br><span style="color:{ORANGE}">Кожу бережёт<br>медсестра.</span></div>
<div id="e2" class="sub" style="top:1150px;font-size:40px;color:{INK}">👇 Отметьте медсестру, без которой<br>шов был бы просто шов</div>
<div id="e3" style="position:absolute;left:0;right:0;top:1400px;text-align:center">{logo(90)}</div>{wave(1080,1920,150)}''')
js = f'''tl.from("#sg",{{y:60,opacity:0,duration:.5}},.05).from("#b1",{{scale:.6,opacity:0,transformOrigin:"left bottom",duration:.45,ease:"back.out(2)"}},.4);
tl.to("#nr",{{opacity:1,duration:.4}},2.6).fromTo("#nsbr",{{y:0}},{{y:-10,duration:.25,repeat:1,yoyo:true}},3.2);
tl.from("#ns2",{{opacity:0,y:-40,duration:.4}},4.25).from("#b2",{{scale:.6,opacity:0,transformOrigin:"right bottom",duration:.45,ease:"back.out(2)"}},4.5);
tl.from(".dy",{{opacity:0,y:30,duration:.3,stagger:.45}},5.3).from(".tk.on",{{scale:0,duration:.3,stagger:.7,ease:"back.out(3)"}},5.6);
tl.from("#h2t",{{opacity:0,y:20,duration:.5}},8.6);
tl.from("#e0",{{opacity:0,y:20,duration:.5}},10.3).to("#e0",{{opacity:0,duration:.3}},11.9).from("#e1",{{opacity:0,y:30,duration:.6}},12.1).from("#e2",{{opacity:0,duration:.5}},12.8).from("#e3",{{opacity:0,duration:.5}},13.3);'''
shots = reel('d1_hirurg_vs_medsestra', 15, body, js, 'Хирург vs медсестра', check=(3.6, 1.5, 7.5, 9.5, 11.0, 14.0))
strip(shots,'kp/chk_d1.jpg')

# ---------- D2 Карусель «Шов зажил» (6)
L='Хирургия и стационар'
TYP=[('Снятие эпидермиса','верхний слой уходит вместе с клеем'),('Натяжной пузырь','кожа «тянется» под жёсткой повязкой'),('Разрыв кожи','особенно у пожилых и хрупкой кожи'),('Мацерация','кожа размокает под повязкой')]
cards=''.join(f'<div style="border:3px solid #EEE;border-radius:28px;padding:40px 34px;min-height:300px"><div style="width:54px;height:10px;background:{ORANGE};border-radius:5px"></div><div style="font-size:44px;font-weight:700;margin-top:24px;line-height:1.1">{a}</div><div style="font-size:30px;color:#666;margin-top:14px">{b}</div></div>' for a,b in TYP)
STEPS=[('Медленно и низко','Почти параллельно коже, «складывая» повязку назад.'),('Поддержите кожу','Палец — у линии отклеивания.'),('По росту волос','И при необходимости — средство для удаления клея.'),('Мягкий контакт','Силиконовые повязки — там, где их допускают показания.')]
rows=''.join(f'<div style="display:flex;gap:26px;padding:24px 0;border-bottom:2px solid #EEE"><div style="font-family:Inter Display;font-size:54px;color:{ORANGE};font-weight:600;width:64px">{i+1}</div><div><div style="font-size:36px;font-weight:700">{a}</div><div style="font-size:27px;color:#555;margin-top:6px">{b}</div></div></div>' for i,(a,b) in enumerate(STEPS))
C=[slide_frame(L,'1/6',f'''<div style="position:absolute;left:140px;top:120px">{svg("surgery",800,4.5)}</div>
<div style="position:absolute;left:80px;right:80px;top:820px"><h1 class="h" style="font-size:90px"><span>Шов зажил.</span><span style="color:{ORANGE}">Кожа помнит</span><span style="color:{ORANGE}">каждую перевязку.</span></h1></div>'''),
slide_frame(L,'2/6',f'''<div style="position:absolute;left:80px;right:80px;top:200px"><div class="num" style="font-size:300px;color:{ORANGE};line-height:1;font-weight:500">16%</div>
<h2 class="h" style="font-size:60px;margin-top:40px">взрослых пациентов реанимации получают повреждения кожи от медицинского клея.</h2>
<p class="body" style="margin-top:24px;font-size:30px;color:#555">У этого есть название — MARSI. Профилактика начинается с выбора повязки и техники снятия.</p>
<p style="margin-top:24px;font-size:20px;color:#999">Мета-анализ, J Wound Care, 2024</p></div>'''),
slide_frame(L,'3/6',f'''<div style="position:absolute;left:80px;right:80px;top:170px"><h2 class="h" style="font-size:66px">Как выглядит MARSI</h2>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:26px;margin-top:50px">{cards}</div>
<p style="margin-top:30px;font-size:20px;color:#999">Классификация по консенсусу по MARSI (McNichol et al., 2013; обновление 2024)</p></div>'''),
slide_frame(L,'4/6',f'''<div style="position:absolute;left:80px;right:80px;top:200px"><div style="font-size:28px;font-weight:700;color:{ORANGE}">◆ ПОЧЕМУ ТАК</div>
<h2 class="h" style="font-size:74px;margin-top:20px"><span>Клей держится за кожу</span><span>крепче, чем клетки кожи</span><span style="color:{ORANGE}">друг за друга.</span></h2>
<p class="body" style="margin-top:40px;font-size:36px">Поэтому при резком снятии верхний слой уходит вместе с повязкой — и так при каждой перевязке.</p></div>
<div style="position:absolute;left:560px;top:880px;opacity:.9">{svg("surgery",420,4.5)}</div>'''),
slide_frame(L,'5/6',f'''<div style="position:absolute;left:80px;right:80px;top:160px"><h2 class="h" style="font-size:64px">Как снимать бережнее</h2><div style="margin-top:24px">{rows}</div>
<p style="margin-top:22px;font-size:20px;color:#999">По консенсусу по MARSI. Протокол вашего отделения — главный.</p></div>'''),
slide_frame(L,'6/6',f'''<div style="position:absolute;left:80px;right:80px;top:200px"><h2 class="h" style="font-size:82px"><span>Для хирургических</span><span style="color:{ORANGE}">отделений.</span></h2>
<div style="margin-top:44px;font-size:34px;line-height:1.7"><span style="color:{ORANGE}">◆</span> Island Film Dressing — послеоперационные швы<br><span style="color:{ORANGE}">◆</span> Silicel Adhesive — силиконовая адгезия<br><span style="color:{ORANGE}">◆</span> CHG I.V. &amp; Catheter Fixation — катетеры</div>
<p class="body" style="margin-top:40px;font-size:32px">📦 Каталог Yafho 2025 и образцы — в директ.</p></div>
<div style="position:absolute;left:60px;top:760px;width:960px;height:420px;border-radius:36px;background:{STAGE}"></div>
<div style="position:absolute;left:250px;top:840px;width:580px;height:260px;border-radius:36px;background:linear-gradient(180deg,#fff,#EEF1F4);box-shadow:0 30px 60px -30px rgba(0,0,0,.45);transform:rotate(-3deg)"><div style="position:absolute;left:150px;top:60px;right:150px;bottom:60px;border-radius:20px;background:#F7F7F7;border:3px solid #E4E7EA"></div></div>''')]
carousel('d2_shov_zazhil', C, 'Шов зажил')
print('done')
