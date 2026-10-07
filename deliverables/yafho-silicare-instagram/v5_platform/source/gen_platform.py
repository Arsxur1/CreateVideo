import yaml
from lineart import svg
from brand import logo, header, wave, ORANGE, INK, MAGENTA, BLUE
from gen_lib import page
S = yaml.safe_load(open('../../deliverables/yafho-silicare-instagram/v5_platform/content_settings.yaml'))
ORDER = ['neonatology','obstetrics','plastic_surgery','dermatology','geriatrics','surgery']
SEG = S['segments']; FOOT = S['claims']['footer_medical']

# ============ 6 обложек серии / карусель «Одна линия — 6 отделений» (1080x1350)
slides=[]
slides.append(f'''<div class="fill" style="background:#fff;color:{INK}"></div>{header("Кожа помнит","")}
<div style="position:absolute;left:80px;top:200px;right:80px"><h1 class="h" style="font-size:104px"><span>Одна линия.</span><span style="color:{ORANGE}">Шесть историй.</span></h1>
<p class="body" style="margin-top:36px;font-size:34px;color:#555;max-width:860px">Кожа новорождённого, мамы после кесарева, пациента пластического хирурга, ребёнка-«бабочки», бабушки и пациента хирургии помнит разное. Но каждой нужна забота.</p></div>
<div style="position:absolute;left:80px;right:80px;top:820px;display:grid;grid-template-columns:repeat(6,1fr);gap:14px">{"".join(f'<div style="text-align:center">{svg(k,130,7)}<div style="font-size:17px;font-weight:700;color:{INK};margin-top:6px">{SEG[k]["label"]}</div></div>' for k in ORDER)}</div>
<div style="position:absolute;left:80px;bottom:70px">{logo(56)}</div><div style="position:absolute;right:80px;bottom:80px;font-size:26px;color:{ORANGE};font-weight:700">Листайте →</div>''')
for i,k in enumerate(ORDER):
    s=SEG[k]
    prods=' · '.join(s['products'])
    slides.append(f'''<div class="fill" style="background:#fff;color:{INK}"></div>{header("Кожа помнит · "+s["label"], f"{i+2}/8")}
<div style="position:absolute;left:190px;top:150px">{svg(k,700,4.5)}</div>
<div style="position:absolute;left:80px;right:80px;top:850px"><h2 class="h" style="font-size:64px">{s["hook"]}</h2>
<div style="margin-top:26px;font-size:24px;color:#666;font-weight:600;text-transform:uppercase;letter-spacing:.04em"><span style="color:{ORANGE}">◆</span> Yafho: {prods}</div></div>
<div style="position:absolute;left:80px;bottom:70px">{logo(46)}</div><div style="position:absolute;right:80px;bottom:76px;font-size:18px;color:#999;max-width:420px;text-align:right">{FOOT}</div>''')
slides.append(f'''<div class="fill" style="background:#fff;color:{INK}"></div>{header("Кожа помнит","8/8")}
<div style="position:absolute;left:80px;right:80px;top:210px"><h2 class="h" style="font-size:86px"><span>Кожа помнит всё.</span><span style="color:{ORANGE}">Пусть помнит заботу.</span></h2>
<p class="body" style="margin-top:40px;font-size:34px">🏥 Клиникам: подберём решение под ваше отделение — от роддома до хирургии.</p>
<p class="body" style="margin-top:18px;font-size:34px">📦 Дистрибьюторам: каталог Yafho 2025 и образцы — в директ.</p></div>
<div style="position:absolute;left:0;right:0;top:820px;text-align:center">{logo(120)}</div>{wave(1080,1350,150)}''')
open('plat_cov/index.html','w').write(page(slides,1080,1350,'Кожа помнит — карусель'))

# ============ Манифест-Reel 26 с (1080x1920)
LINES = {'neonatology':'Кожа помнит<br><span style="color:%s">первое прикосновение.</span>',
         'obstetrics':'Самый<br><span style="color:%s">счастливый день.</span>',
         'plastic_surgery':'Каждый<br><span style="color:%s">шов.</span>',
         'dermatology':'Каждое касание —<br><span style="color:%s">если она хрупкая, как крыло.</span>',
         'geriatrics':'Каждую<br><span style="color:%s">перевязку.</span>',
         'surgery':'Даже когда<br><span style="color:%s">шов уже зажил.</span>'}
D=3.4; clips=[]; js=[]
for i,k in enumerate(ORDER):
    t=round(i*D,2)
    clips.append(f'''<section id="m{i}" class="clip" data-start="{t}" data-duration="{D}" data-track-index="1"><div class="fill" style="background:#fff"></div>
<div style="position:absolute;left:64px;top:90px;font-size:24px;font-weight:700;color:{ORANGE};letter-spacing:.08em;text-transform:uppercase">◆ {SEG[k]["label"]}</div>
<div style="position:absolute;left:115px;top:330px">{svg(k,850,4,idp="sv"+str(i))}</div>
<div id="mt{i}" style="position:absolute;left:70px;right:70px;top:1310px;text-align:center;font-family:Inter Display;font-weight:800;font-size:76px;letter-spacing:-0.03em;line-height:1.08;color:{INK}">{LINES[k] % ORANGE}</div></section>''')
    js.append(f'tl.fromTo("#sv{i} .lni",{{strokeDasharray:1,strokeDashoffset:1}},{{strokeDashoffset:0,duration:1.6,ease:"power2.inOut",stagger:.12}},{t+0.05})')
    js.append(f'tl.fromTo("#sv{i} .lna",{{strokeDasharray:1,strokeDashoffset:1,opacity:0}},{{strokeDashoffset:0,opacity:1,duration:.7,ease:"power2.out"}},{t+1.5})')
    js.append(f'tl.from("#mt{i}",{{opacity:0,y:30,duration:.5}},{t+0.6})')
T=round(6*D,2)
clips.append(f'''<section id="mend" class="clip" data-start="{T}" data-duration="{26-T}" data-track-index="1"><div class="fill" style="background:#fff"></div>
<div id="me1" style="position:absolute;left:70px;right:70px;top:520px;text-align:center;font-family:Inter Display;font-weight:800;font-size:104px;letter-spacing:-0.03em;line-height:1.05;color:{INK}">Кожа помнит всё.<br><span style="color:{ORANGE}">Пусть помнит заботу.</span></div>
<div id="me2" style="position:absolute;left:0;right:0;top:900px;text-align:center">{logo(140)}</div>
<div id="me3" style="position:absolute;left:90px;right:90px;top:1180px;text-align:center;font-size:30px;font-weight:600;color:#555;line-height:1.6">Неонатология · Акушерство · Пластическая хирургия<br>Дерматология · Гериатрия · Хирургия</div>
<div id="me4" style="position:absolute;left:90px;right:90px;top:1360px;text-align:center;font-size:30px;color:{INK}">Клиникам и дистрибьюторам — каталог и образцы в директ</div>
{wave(1080,1920,180)}</section>''')
js.append(f'tl.from("#me1",{{opacity:0,y:40,duration:.6}},{T+.1}).from("#me2",{{opacity:0,scale:.9,duration:.6}},{T+.7}).from(["#me3","#me4"],{{opacity:0,duration:.6,stagger:.4}},{T+1.3})')
html=f'''<!doctype html><html lang="ru"><head><meta charset="UTF-8"><title>Кожа помнит — манифест</title><script src="gsap.min.js"></script><link rel="stylesheet" href="shared.css">
<style>#root{{position:relative;width:1080px;height:1920px;overflow:hidden}}</style></head><body>
<div id="root" data-composition-id="main" data-width="1080" data-height="1920" data-duration="26">{"".join(clips)}</div>
<script>window.__timelines={{}};const tl=gsap.timeline({{paused:true}});{";".join(js)};tl.to({{}},{{duration:.01}},25.99);window.__timelines["main"]=tl;</script></body></html>'''
open('plat_reel/index.html','w').write(html)
print('ok', len(slides))
