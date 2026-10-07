from kp import *
from PIL import Image, ImageDraw, ImageFont
import os
L='Пластическая хирургия'
# ---------- C1 Reel-открытие сериала (15 c)
ring = lambda: f'''<svg id="rg" viewBox="0 0 200 200" width="420" height="420" style="position:absolute;left:330px;top:700px"><circle cx="100" cy="100" r="88" fill="none" stroke="#F1F1F1" stroke-width="10"/>
<circle id="rgc" cx="100" cy="100" r="88" fill="none" stroke="{ORANGE}" stroke-width="10" stroke-linecap="round" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1" transform="rotate(-90 100 100)"/></svg>'''
body = clip('c1',0,6.0,f'''<div style="position:absolute;left:64px;top:84px;font-size:24px;font-weight:700;color:{ORANGE};letter-spacing:.08em">◆ СЕРИАЛ · ДЕНЬ 1 ИЗ 180</div>
<div style="position:absolute;left:190px;top:200px">{svg("plastic_surgery",700,4.5,idp="pf")}</div>
<div id="t1" class="cap" style="top:1000px;font-size:84px">Хирург отвечает<br>за шов.</div>
<div id="t2" class="cap" style="top:1230px;font-size:84px;color:{ORANGE}">Следующие 180&nbsp;дней&nbsp;—<br>за вами.</div>''') + \
clip('c2',6.0,5.0,f'''{ring()}<div id="cnt" style="position:absolute;left:330px;top:820px;width:420px;text-align:center;font-family:'Inter Display';font-weight:700;font-size:130px;color:{INK}">1</div>
<div style="position:absolute;left:330px;top:980px;width:420px;text-align:center;font-size:30px;color:#888">день из 180</div>
<div id="t3" class="cap" style="top:300px;font-size:70px">Рубец созревает<br>месяцами.</div>
<div id="t4" class="sub" style="top:1230px;font-size:38px;color:{INK}">Одна пациентка. Один рубец.<br>Каждую неделю — 7 честных секунд.</div>''') + \
clip('c3',11.0,4.0,f'''<div id="e1" class="cap" style="top:420px;font-size:88px">Подпишитесь,<br>чтобы увидеть<br><span style="color:{ORANGE}">День 7.</span></div>
<div id="e2" style="position:absolute;left:0;right:0;top:960px;text-align:center">{logo(96)}</div>
<div class="sub" style="top:1140px;font-size:26px">Уход за рубцом — по назначению хирурга. Результат индивидуален.</div>{wave(1080,1920,150)}''')
js = f'''tl.fromTo("#pf .lni",{{strokeDasharray:1,strokeDashoffset:1}},{{strokeDashoffset:0,duration:2,stagger:.12,ease:"power2.inOut"}},.1);
tl.fromTo("#pf .lna",{{strokeDasharray:1,strokeDashoffset:1}},{{strokeDashoffset:0,duration:.8}},2.3);
tl.from("#t1",{{opacity:0,y:30,duration:.5}},1.0).from("#t2",{{opacity:0,y:30,duration:.5}},3.0);
tl.from("#t3",{{opacity:0,y:30,duration:.5}},6.1).to("#rgc",{{strokeDashoffset:0,duration:3.2,ease:"power2.inOut"}},6.4);
const o={{v:1}};const ce=document.getElementById("cnt");tl.to(o,{{v:180,duration:3.2,ease:"power2.inOut",onUpdate:()=>{{ce.textContent=Math.round(o.v)}}}},6.4);
tl.from("#t4",{{opacity:0,duration:.5}},8.6);
tl.from("#e1",{{opacity:0,y:30,duration:.5}},11.1).from("#e2",{{opacity:0,duration:.5}},11.8);'''
shots = reel('c1_den_1_iz_180', 15, body, js, 'День 1 из 180', check=(4.5, 1.5, 8.0, 10.5, 13.5))
strip(shots, 'kp/chk_c1.jpg')

# ---------- C2 Оверлеи для эпизодов (прозрачные PNG)
od = os.path.join(OUT, 'c2_overlei_serii'); os.makedirs(od, exist_ok=True)
FB = '/usr/share/fonts/opentype/inter/InterDisplay-Bold.otf'; FR = '/usr/share/fonts/opentype/inter/Inter-Medium.otf'
fb = lambda s: ImageFont.truetype(FB, s); fr = lambda s: ImageFont.truetype(FR, s)
OR=(243,130,33,255); WH=(255,255,255,255)
for day in [1,7,14,21,30,45,60,90,120,150,180]:
    im = Image.new('RGBA',(1080,1920),(0,0,0,0)); d = ImageDraw.Draw(im)
    # верхняя плашка с градиентной подложкой для читаемости
    for yy in range(0,420): d.line([(0,yy),(1080,yy)], fill=(0,0,0,int(110*(1-yy/420))))
    d.rectangle([60,96,96,132], fill=OR)
    d.text((116,92), 'СЕРИАЛ · РУБЕЦ ПОД ЛУПОЙ', font=fr(30), fill=WH)
    d.text((60,150), f'ДЕНЬ {day}', font=fb(150), fill=WH)
    w = d.textlength(f'ДЕНЬ {day}', font=fb(150))
    d.text((60+w+20,240), '/ 180', font=fb(56), fill=(255,255,255,200))
    d.rounded_rectangle([60,340,1020,356], radius=8, fill=(255,255,255,90))
    d.rounded_rectangle([60,340,60+int(960*day/180),356], radius=8, fill=OR)
    # нижняя плашка
    for yy in range(1600,1920): d.line([(0,yy),(1080,yy)], fill=(0,0,0,int(120*((yy-1600)/320))))
    d.text((60,1760), 'Yafho', font=fb(64), fill=OR)
    d.text((262,1784), 'WOUND CARE · Silicone Scar Sheet', font=fr(28), fill=WH)
    d.text((60,1850), 'Результат индивидуален. Уход — по назначению хирурга.', font=fr(24), fill=(255,255,255,200))
    im.save(os.path.join(od, f'overlay_den_{day:03d}.png'))
# превью на сером фоне для проверки
pv = Image.new('RGBA',(1080,1920),(120,110,105,255)); pv.alpha_composite(Image.open(os.path.join(od,'overlay_den_030.png'))); pv.convert('RGB').save('kp/chk_c2.jpg')

# ---------- C3 Карусель «Как носить силиконовую пластину» (7)
STEP=[('Только на зажившую кожу','Чистую, сухую, без корочек и открытых участков. Когда начинать — решает хирург.','✅'),
      ('Привыкайте постепенно','Начинают с нескольких часов в день и понемногу увеличивают время.','⏱'),
      ('Цель — долго и регулярно','Обычно говорят о ≥12 часах в сутки (до круглосуточного ношения) — точный режим по инструкции к изделию и словам врача.','🕛'),
      ('Месяцы, а не дни','Курс ухода за рубцом длится месяцами: часто называют 2–4 месяца и дольше.','⏳'),
      ('Если кожа раздражена','Сделайте паузу, пока не пройдёт, и возвращайтесь постепенно. При сомнениях — к врачу.','⚠️')]
C=[slide_frame(L,'1/7',f'''<div style="position:absolute;left:60px;top:150px;width:960px;height:520px;border-radius:36px;background:{STAGE}"></div>
<div style="position:absolute;left:230px;top:330px;width:620px;height:150px;transform:rotate(-4deg);border-radius:75px;background:linear-gradient(180deg,rgba(246,214,180,.95),rgba(232,186,140,.9));box-shadow:0 22px 34px -16px rgba(90,50,20,.45)"></div>
<div style="position:absolute;left:80px;right:80px;top:720px"><div style="font-size:28px;font-weight:700;color:{ORANGE}">◆ ИНСТРУКЦИЯ, КОТОРУЮ СОХРАНЯЮТ</div>
<h1 class="h" style="font-size:86px;margin-top:20px"><span>Как носить</span><span style="color:{ORANGE}">силиконовую пластину.</span></h1></div>''')]
for i,(t,txt,em) in enumerate(STEP):
    C.append(slide_frame(L,f'{i+2}/7',f'''<div class="num" style="position:absolute;left:70px;top:150px;font-size:320px;color:#F6E2CF;line-height:1;font-weight:500">0{i+1}</div>
<div style="position:absolute;right:90px;top:200px;font-size:150px">{em}</div>
<div style="position:absolute;right:-40px;bottom:150px;opacity:.18">{svg("plastic_surgery",480,4)}</div>
<div style="position:absolute;left:80px;right:80px;top:520px"><h2 class="h" style="font-size:70px">{t}</h2><p class="body" style="margin-top:28px;font-size:42px;line-height:1.3;max-width:820px">{txt}</p></div>'''))
C.append(slide_frame(L,'7/7',f'''<div style="position:absolute;left:80px;right:80px;top:200px"><h2 class="h" style="font-size:80px"><span>Хирург сделал шов.</span><span style="color:{ORANGE}">Рубец — ваш проект.</span></h2>
<p class="body" style="margin-top:36px;font-size:34px">Смотрите наш сериал «День 1 из 180» — как это выглядит в жизни, неделя за неделей.</p>
<p class="body" style="margin-top:22px;font-size:30px;color:#555">🏥 Клиникам пластической хирургии — Yafho Silicone Scar Sheet: размеры и образцы в директ.</p>
<p style="margin-top:34px;font-size:21px;color:#999;line-height:1.5">По памяткам NHS: St George's «Silicone for scars»; Chelsea and Westminster «Silicone gel sheets»; University Hospitals of Leicester. Практические рекомендации по рубцам — Meaume et al., 2014.</p></div><div style="position:absolute;left:600px;top:800px;opacity:.9">{svg('plastic_surgery',360,4.5)}</div>'''))
carousel('c3_kak_nosit_plastinu', C, 'Как носить силиконовую пластину')
print('done')
