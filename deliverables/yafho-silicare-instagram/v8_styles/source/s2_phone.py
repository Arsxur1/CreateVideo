from stylekit import *
from brand import ORANGE, logo
import sfx, random
BG='#000'; CARD='#1C1C1E'; TXT='#F2F2F7'; MUT='#8E8E93'; BLUE='#0A84FF'
def status(time='03:12'):
    return f'<div style="position:absolute;left:60px;right:60px;top:40px;display:flex;justify-content:space-between;font-family:Inter Display,sans-serif;font-weight:600;font-size:34px;color:{TXT}"><span>{time}</span><span>●●● 5G ▮▮▮▯</span></div>'
Q='почему у мамы кожа рвётся от пластыря'
qchars=''.join(f'<span class="q">{c if c!=" " else "&nbsp;"}</span>' for c in Q)
body=f'''<section id="sc1" class="clip" data-start="0" data-duration="9.6" data-track-index="1"><div class="fill" style="background:{BG}"></div>{status()}
<div style="position:absolute;left:50px;right:50px;top:150px;font-family:Inter Display,sans-serif;font-weight:700;font-size:72px;color:{TXT}">Поиск</div>
<div style="position:absolute;left:50px;right:50px;top:270px;height:110px;border-radius:28px;background:{CARD};display:flex;align-items:center;padding:0 34px;font-family:Inter Display,sans-serif;font-size:40px;color:{TXT}"><span style="color:{MUT};margin-right:20px">⌕</span><span>{qchars}</span><span id="cur" style="display:inline-block;width:4px;height:52px;background:{BLUE};margin-left:4px"></span></div>
<div id="sg" style="position:absolute;left:50px;right:50px;top:420px;font-family:Inter Display,sans-serif;font-size:36px;color:{TXT}">{"".join(f'<div style="padding:28px 0;border-bottom:1px solid #2C2C2E"><span style="color:{MUT}">⌕</span>&nbsp;&nbsp;{s}</div>' for s in ["…после операции","…у пожилых","…как снимать пластырь без боли"])}</div>
<div id="ans" style="position:absolute;left:50px;right:50px;top:440px;border-radius:36px;background:{CARD};padding:44px;opacity:0">
<div style="font-family:Inter Display,sans-serif;font-size:28px;color:{MUT};letter-spacing:.06em">ОТВЕТ</div>
<div style="font-family:Inter Display,sans-serif;font-size:46px;line-height:1.35;color:{TXT};margin-top:18px">Медицинский клей может держаться за кожу <span id="hl" style="background:linear-gradient(transparent 55%,rgba(243,130,33,.55) 55%);background-size:0% 100%;background-repeat:no-repeat">крепче, чем клетки кожи друг за друга</span>. При снятии верхний слой уходит вместе с ним.</div>
<div style="font-family:Inter Display,sans-serif;font-size:40px;color:{TXT};margin-top:26px">Это называется <b style="color:{ORANGE}">MARSI</b> — травма кожи от медицинского клея.</div>
<div style="font-family:Inter Display,sans-serif;font-size:24px;color:{MUT};margin-top:26px">Консенсус по MARSI, J WOCN 2013 / 2024</div></div>
<div id="cap1" style="position:absolute;left:0;right:0;top:1500px;text-align:center;font-family:'Inter Display';font-weight:800;font-size:64px;color:#fff;text-shadow:0 4px 30px #000">3 часа ночи.<br><span style="color:{ORANGE}">Мама после операции.</span></div></section>
<section id="sc2" class="clip" data-start="9.6" data-duration="5.4" data-track-index="1"><div class="fill" style="background:{BG}"></div>{status('03:19')}
<div style="position:absolute;left:0;right:0;top:110px;height:150px;border-bottom:1px solid #2C2C2E;text-align:center;font-family:Inter"><div style="width:84px;height:84px;border-radius:50%;background:linear-gradient(135deg,#F7A04A,#F38221);margin:0 auto;font-size:42px;line-height:84px;color:#fff;font-weight:700">О</div><div style="font-size:30px;color:{TXT};margin-top:6px">Оля · медсестра</div></div>
<div style="position:absolute;left:40px;right:40px;top:330px;font-family:Inter Display,sans-serif;font-size:42px;line-height:1.3">
<div id="m1" style="margin-left:auto;max-width:760px;background:{BLUE};color:#fff;border-radius:40px;padding:26px 36px;margin-bottom:22px;width:fit-content">Оль, у мамы после пластыря кожа рвётся 😢</div>
<div id="ty" style="max-width:200px;background:#2C2C2E;color:{MUT};border-radius:40px;padding:20px 36px;margin-bottom:22px;width:fit-content;font-size:50px;line-height:1">• • •</div>
<div id="m2" style="max-width:780px;background:#2C2C2E;color:{TXT};border-radius:40px;padding:26px 36px;margin-bottom:22px;width:fit-content">Попроси <b style="color:{ORANGE}">силиконовую повязку</b>. Держит, но снимается мягко</div>
<div id="m3" style="max-width:780px;background:#2C2C2E;color:{TXT};border-radius:40px;padding:26px 36px;margin-bottom:22px;width:fit-content">Мы в отделении такие используем 👍</div>
<div id="m4" style="margin-left:auto;max-width:760px;background:{BLUE};color:#fff;border-radius:40px;padding:26px 36px;width:fit-content">Спасибо!! ❤️</div></div></section>
<section id="sc3" class="clip" data-start="15.0" data-duration="2.8" data-track-index="1"><div class="fill" style="background:#F2F2F7"></div>
<div style="position:absolute;left:60px;right:60px;top:40px;display:flex;justify-content:space-between;font-family:Inter Display,sans-serif;font-weight:600;font-size:34px;color:#000"><span>03:21</span><span>●●● 5G ▮▮▮▯</span></div>
<div style="position:absolute;left:60px;top:150px;font-family:Inter Display,sans-serif;font-weight:700;font-size:72px;color:#000">Купить утром</div>
<div style="position:absolute;left:60px;right:60px;top:320px;font-family:Inter Display,sans-serif;font-size:48px;color:#000;line-height:2">
<div>☑︎ <s style="color:#999">Хлеб</s></div>
<div style="display:flex;align-items:center;gap:20px"><div id="cb" style="width:56px;height:56px;border-radius:50%;border:4px solid #C7C7CC;position:relative"><div id="ck" style="position:absolute;inset:-4px;border-radius:50%;background:{ORANGE};color:#fff;text-align:center;line-height:56px;font-size:40px;opacity:0">✓</div></div><span><b>Силиконовая повязка</b><br><span style="font-size:38px;color:#666">Sili-Care (Yafho)</span></span></div></div></section>
<section id="sc4" class="clip" data-start="17.8" data-duration="3.4" data-track-index="1"><div class="fill" style="background:#fff"></div>
<div id="e1" style="position:absolute;left:60px;right:60px;top:520px;text-align:center;font-family:'Inter Display';font-weight:800;font-size:92px;line-height:1.05;color:#2B2B2B">Пусть утром<br><span style="color:{ORANGE}">будет не больно.</span></div>
<div id="e2" style="position:absolute;left:0;right:0;top:900px;text-align:center">{logo(110)}</div>
<div id="e3" style="position:absolute;left:80px;right:80px;top:1130px;text-align:center;font-size:36px;color:#444;font-weight:600">📌 Сохраните, чтобы не искать ночью</div>
<div style="position:absolute;left:80px;right:80px;bottom:120px;text-align:center;font-size:22px;color:#999">Сценка. Медицинское изделие. Применение — по назначению специалиста.</div></section>'''
step=.075; T0=.4
js=f'tl.from(".q",{{opacity:0,duration:.01,stagger:{step}}},{T0});tl.fromTo("#cur",{{opacity:1}},{{opacity:0,duration:.25,repeat:30,yoyo:true}},0);'
js+=f'tl.from("#cap1",{{opacity:0,y:30,duration:.4}},.1).to("#cap1",{{opacity:0,duration:.4}},3.4);'
js+=f'tl.from("#sg > div",{{opacity:0,y:20,duration:.25,stagger:.15}},{T0+len(Q)*step*.6});'
TA=T0+len(Q)*step+.4
js+=f'tl.to("#sg",{{opacity:0,duration:.25}},{TA}).to("#ans",{{opacity:1,duration:.35}},{TA}).from("#ans",{{y:60,duration:.4,ease:"power3.out"}},{TA}).to("#hl",{{backgroundSize:"100% 100%",duration:.9,ease:"power2.inOut"}},{TA+1.2});'
js+='tl.from("#m1",{opacity:0,y:40,scale:.9,transformOrigin:"right bottom",duration:.3},9.8).from("#ty",{opacity:0,duration:.2},10.6).to("#ty",{opacity:0,duration:.1},11.7).from("#m2",{opacity:0,y:40,scale:.9,transformOrigin:"left bottom",duration:.3},11.75).from("#m3",{opacity:0,y:40,duration:.3},12.9).from("#m4",{opacity:0,y:40,scale:.9,transformOrigin:"right bottom",duration:.3},13.9);'
js+='tl.to("#ck",{opacity:1,duration:.15},16.0).from("#ck",{scale:.2,duration:.35,ease:"back.out(3)"},16.0);'
js+='tl.from("#e1",{opacity:0,y:30,duration:.5},17.9).from("#e2",{opacity:0,duration:.5},18.5).from("#e3",{opacity:0,duration:.4},19.0);'
r=random.Random(4); ev=[(T0+i*step,sfx.click(r.uniform(.12,.22))) for i in range(len(Q)) if Q[i]!=' ']
ev+=[(TA,sfx.whoosh(.4,.15)),(TA+1.2,sfx.chime(1568,.08,.8)),(9.6,sfx.whoosh(.5,.2)),(9.8,sfx.whoosh(.25,.18)),(11.75,sfx.chime(1568,.14,.7)),(11.77,sfx.chime(2093,.08,.6)),(12.9,sfx.chime(1568,.12,.7)),(13.9,sfx.whoosh(.25,.18)),(16.0,sfx.chime(1046,.18,1.2)),(17.8,sfx.whoosh(.6,.25)),(18.2,sfx.chime(659,.18,2.5))]
shots=style_reel('s2_phone_3_nochi',21.2,body,js,'3 часа ночи',ev,pad=(82.4,123.5,164.8),pad_amp=.04,check=(1.5,3.0,7.5,12.5,16.5,19.8),bg=BG)
strip(shots,'kp/chk_s2.jpg',2400); print('ok')
