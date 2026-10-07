from kp import *
from lineart import belly
BABY_HAND = "M232 480 C206 430 208 370 228 338 L214 236 C211 214 240 208 244 230 L258 318 L264 200 C266 176 296 176 296 200 L293 312 L308 214 C312 190 340 193 337 216 L326 322 L348 256 C356 234 382 243 375 265 L350 365 C340 425 320 455 300 482"
def belly_svg(size, idp, hand=False, stroke=4.5):
    paths = belly()['paths']; out=[]
    for d,acc in paths:
        col = ORANGE if acc else INK; w = stroke*2 if acc else stroke
        out.append(f'<path class="{"ba" if acc else "bi"}" pathLength="1" d="{d}" fill="none" stroke="{col}" stroke-width="{w}" stroke-linecap="round"/>')
    if hand:
        out.append(f'<g transform="translate(232,236) scale(.36) rotate(-8 300 340)"><path class="bh" pathLength="1" d="{BABY_HAND}" fill="none" stroke="{INK}" stroke-width="{stroke/.42:.1f}" stroke-linecap="round" stroke-linejoin="round"/></g>')
    return f'<svg id="{idp}" viewBox="0 0 600 600" width="{size}" height="{size}" style="overflow:visible">{"".join(out)}</svg>'

def scar_sheet(x, y, w, h, rot=0):
    return f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;transform:rotate({rot}deg);border-radius:{h//2}px;background:linear-gradient(180deg,rgba(246,214,180,.95),rgba(232,186,140,.9));box-shadow:0 18px 30px -14px rgba(90,50,20,.45),inset 0 2px 0 rgba(255,255,255,.7)"><div style="position:absolute;left:8%;top:14%;width:50%;height:28%;border-radius:999px;background:rgba(255,255,255,.45);filter:blur(3px)"></div></div>'

# ---------------- A1 · Карусель «Её первый шрам» (6)
L = 'Акушерство'
S = []
S.append(slide_frame(L, '1/6', f'''<div style="position:absolute;left:190px;top:130px">{belly_svg(700,"x1")}</div>
<div style="position:absolute;left:80px;right:80px;top:860px"><h1 class="h" style="font-size:80px"><span>Её первый шрам —</span><span style="color:{ORANGE}">от самого счастливого дня.</span></h1>
<p class="body" style="margin-top:24px;font-size:30px;color:#666">Листайте: что происходит с кожей после кесарева →</p></div>'''))
dots = ''.join(f'<div style="width:120px;height:120px;border-radius:50%;{"background:"+ORANGE if i==2 else "border:5px solid #2B2B2B"}"></div>' for i in range(5))
S.append(slide_frame(L, '2/6', f'''<div style="position:absolute;left:80px;right:80px;top:200px"><div class="num" style="font-size:260px;color:{ORANGE};line-height:1;font-weight:500">1 из 5</div>
<div style="display:flex;gap:44px;margin-top:60px">{dots}</div>
<h2 class="h" style="font-size:58px;margin-top:70px">Примерно каждые пятые роды в мире — кесарево сечение.</h2>
<p class="body" style="margin-top:22px;font-size:30px;color:#555">21% родов. К 2030 году прогноз — около 29%. Это миллионы мам и миллионы шрамов каждый год.</p>
<p style="margin-top:22px;font-size:20px;color:#999">ВОЗ; Betran A.P. et al., BMJ Global Health, 2021</p></div>'''))
TL = [('0–14 дней','Шов под повязкой','#2B2B2B'),('~6 недель','Рана заживает, мама восстанавливается','#2B2B2B'),('до 12+ месяцев','Рубец созревает: краснеет, уплотняется, потом светлеет',ORANGE)]
rows = ''.join(f'<div style="display:flex;gap:30px;align-items:flex-start;margin-top:46px"><div style="position:relative;z-index:1;width:34px;height:34px;border-radius:50%;background:{c};border:6px solid #fff;margin-top:8px;flex:none"></div><div><div style="font-size:30px;font-weight:700;color:{c}">{a}</div><div style="font-size:40px;font-weight:700;margin-top:6px;line-height:1.15">{b}</div></div></div>' for a,b,c in TL)
S.append(slide_frame(L, '3/6', f'''<div style="position:absolute;left:80px;right:80px;top:180px"><h2 class="h" style="font-size:70px"><span>Шов заживает недели.</span><span style="color:{ORANGE}">Рубец формируется месяцы.</span></h2>
<div style="position:relative;margin-top:30px;padding-left:4px"><div style="position:absolute;left:15px;top:60px;bottom:30px;width:4px;background:#E5E5E5;z-index:0"></div>{rows}</div></div>'''))
S.append(slide_frame(L, '4/6', f'''<div style="position:absolute;left:60px;top:170px;width:960px;height:520px;border-radius:36px;background:{STAGE}"></div>
<div style="position:absolute;left:300px;top:250px;width:480px;height:360px;border-radius:40px;background:linear-gradient(180deg,#fff,#EEF1F4);box-shadow:0 30px 60px -30px rgba(0,0,0,.45)"><div style="position:absolute;left:90px;top:80px;right:90px;bottom:80px;border-radius:24px;background:#F7F7F7;border:3px solid #E4E7EA"></div></div>
<div style="position:absolute;left:80px;right:80px;top:740px"><div style="font-size:26px;font-weight:700;color:{ORANGE};letter-spacing:.06em">◆ ЭТАП 1 — ШОВ</div>
<h2 class="h" style="font-size:60px;margin-top:14px">Повязка, которую не страшно снимать.</h2>
<p class="body" style="margin-top:20px;font-size:30px;color:#555">Первые дни повязку меняют, а кожа вокруг шва нежная. Важно, чтобы клей не тянул её при снятии. Вид повязки и сроки назначает врач.</p></div>'''))
S.append(slide_frame(L, '5/6', f'''<div style="position:absolute;left:60px;top:170px;width:960px;height:520px;border-radius:36px;background:{STAGE}"></div>
{scar_sheet(250,360,580,120,-4)}
<div style="position:absolute;left:80px;right:80px;top:740px"><div style="font-size:26px;font-weight:700;color:{ORANGE};letter-spacing:.06em">◆ ЭТАП 2 — РУБЕЦ</div>
<h2 class="h" style="font-size:60px;margin-top:14px">Силиконовая пластина — первая линия ухода за рубцом.</h2>
<p class="body" style="margin-top:20px;font-size:30px;color:#555">Так считают практические руководства по рубцам. Начинают только на полностью зажившей коже и по рекомендации врача. Результат индивидуален.</p>
<p style="margin-top:14px;font-size:20px;color:#999">Meaume S. et al., Management of scars: updated practical guidelines, 2014 · Yafho Silicone Scar Sheet</p></div>'''))
S.append(slide_frame(L, '6/6', f'''<div style="position:absolute;left:80px;right:80px;top:200px"><h2 class="h" style="font-size:84px"><span>Шрам — это память.</span><span style="color:{ORANGE}">Пусть она будет мягкой.</span></h2>
<p class="body" style="margin-top:40px;font-size:36px">💌 Напишите письмо своему шраму в комментариях или сторис с <b style="color:{ORANGE}">#ПисьмоШраму</b>.</p>
<p class="body" style="margin-top:18px;font-size:30px;color:#555">Лучшие письма (с вашего согласия) опубликуем, а ваш шрам нарисуем одной линией — в подарок.</p>
<p class="body" style="margin-top:30px;font-size:28px;color:#555">🏥 Роддомам и дистрибьюторам — каталог и образцы Yafho в директ.</p></div>
<div style="position:absolute;left:330px;top:820px">{belly_svg(420,"x6",hand=True)}</div>''', footer=True))
carousel('a1_ee_pervyi_shram', S, 'Её первый шрам')

# ---------------- A2 · Reel «Письмо шраму» (25 c)
LET = [(0.4,'Привет, шрам.'),(2.8,'Ты появился в 03:47.'),(5.4,'В ту минуту я впервые услышала её крик.'),(8.8,'Я долго тебя стеснялась.'),(11.6,'А теперь знаю: ты — дверь, через которую она пришла в этот мир.')]
lines = ''.join(f'<div class="lt" id="lt{i}" style="font-family:Inter;font-style:italic;font-weight:400;font-size:{58 if i==0 else 46}px;line-height:1.3;color:{INK};margin-top:{0 if i==0 else 22}px">{t}</div>' for i,(_,t) in enumerate(LET))
body = clip('s1', 0, 19.2, f'''<div style="position:absolute;left:64px;top:84px;font-size:24px;font-weight:700;color:{ORANGE};letter-spacing:.08em">◆ #ПИСЬМОШРАМУ</div>
<div style="position:absolute;left:190px;top:170px">{belly_svg(700,"bs",hand=True)}</div>
<div style="position:absolute;left:90px;right:90px;top:940px">{lines}<div id="thx" style="font-family:'Inter Display';font-weight:800;font-size:96px;color:{ORANGE};margin-top:30px">Спасибо.</div></div>''') + \
clip('s2', 19.2, 5.8, f'''<div class="fill" style="background:#fff"></div>
<div id="e1" class="cap" style="top:300px;font-size:92px">Шрам — это память.<br><span style="color:{ORANGE}">Пусть она будет мягкой.</span></div>
<div id="e2" style="position:absolute;left:0;right:0;top:640px;height:260px">{scar_sheet(230,70,620,120,-3)}</div>
<div id="e3" class="sub" style="top:930px;font-size:30px">Уход за рубцом — на зажившей коже<br>и по рекомендации врача.</div>
<div id="e4" class="cap" style="top:1110px;font-size:58px">Напишите письмо своему шраму<br><span style="color:{ORANGE}">#ПисьмоШраму</span></div>
<div id="e5" style="position:absolute;left:0;right:0;top:1390px;text-align:center">{logo(96)}</div>{wave(1080,1920,170)}''')
js = f'''tl.fromTo("#bs .bi",{{strokeDasharray:1,strokeDashoffset:1}},{{strokeDashoffset:0,duration:2.2,ease:"power2.inOut",stagger:.15}},0.1);
tl.fromTo("#bs .ba",{{strokeDasharray:1,strokeDashoffset:1}},{{strokeDashoffset:0,duration:1.4,ease:"power1.inOut"}},2.6);
''' + ''.join(f'tl.from("#lt{i}",{{opacity:0,y:20,duration:.6}},{t});' + (f'tl.to("#lt{i-1}",{{opacity:.3,duration:.6}},{t});' if i else '') for i,(t,_) in enumerate(LET)) + f'''
tl.to("#lt4",{{opacity:.3,duration:.5}},15.6);
tl.fromTo("#bs .bh",{{strokeDasharray:1,strokeDashoffset:1}},{{strokeDashoffset:0,duration:1.8,ease:"power2.out"}},15.0);
tl.from("#thx",{{opacity:0,scale:.9,transformOrigin:"left center",duration:.7,ease:"back.out(1.6)"}},16.4);
tl.to("#bs .ba",{{stroke:"#F7B57A",duration:1.2}},17.0);
tl.from("#e1",{{opacity:0,y:30,duration:.6}},19.3).from("#e2",{{opacity:0,y:40,duration:.6}},19.9).from("#e3",{{opacity:0,duration:.5}},20.4).from("#e4",{{opacity:0,y:20,duration:.6}},21.2).from("#e5",{{opacity:0,duration:.6}},22.0);'''
shots = reel('a2_pismo_shramu', 25, body, js, 'Письмо шраму', check=(17.5, 1.5, 6.5, 13.0, 23.5))
strip(shots, 'kp/chk_a2.jpg')

# ---------------- A3 · Карусель «7 вещей после кесарева» (9)
TIPS = [('Кашлять, чихать, смеяться','Прижмите к шву ладони, свёрнутое полотенце или маленькую подушку и слегка наклонитесь вперёд.','🤧'),
        ('Вставать с кровати','Через бок: повернитесь, спустите ноги и оттолкнитесь руками. Так меньше нагрузка на живот.','🛏'),
        ('Поднимать тяжести','Ничего тяжелее малыша — первые недели (часто говорят о 6 неделях). Попросите о помощи.','👶'),
        ('Одежда','Свободная, мягкая, хлопковое бельё. Резинка не должна давить на шов.','👕'),
        ('Повязка','Не снимайте и не мочите её раньше, чем разрешили врач или акушерка.','🩹'),
        ('Когда срочно к врачу','Покраснение и отёк вокруг шва, выделения, температура, боль, которая усиливается, а не проходит.','🚨'),
        ('Рубец','Уход начинают, когда кожа полностью зажила. Силиконовые пластины — по рекомендации врача.','✨')]
T = [slide_frame('Акушерство · памятка', '1/9', f'''<div style="position:absolute;left:80px;right:80px;top:190px"><div style="font-size:30px;font-weight:700;color:{ORANGE}">◆ СОХРАНИТЕ, ПРИГОДИТСЯ</div>
<h1 class="h" style="font-size:100px;margin-top:24px"><span>7 вещей,</span><span>о которых редко</span><span>говорят после</span><span style="color:{ORANGE}">кесарева.</span></h1></div>
<div style="position:absolute;right:20px;top:640px">{belly_svg(460,"x3")}</div>''')]
for i,(t,txt,em) in enumerate(TIPS):
    T.append(slide_frame('Акушерство · памятка', f'{i+2}/9', f'''<div class="num" style="position:absolute;left:70px;top:150px;font-size:320px;color:#F6E2CF;line-height:1;font-weight:500">0{i+1}</div>
<div style="position:absolute;right:90px;top:200px;font-size:150px">{em}</div>
<div style="position:absolute;right:-60px;bottom:120px;opacity:.22">{belly_svg(520,"bb"+str(i))}</div>
<div style="position:absolute;left:80px;right:80px;top:520px"><h2 class="h" style="font-size:72px;color:{RED if i==5 else INK}">{t}</h2>
<p class="body" style="margin-top:28px;font-size:44px;line-height:1.3;max-width:860px">{txt}</p></div>'''))
T.append(slide_frame('Акушерство · памятка', '9/9', f'''<div style="position:absolute;left:80px;right:80px;top:200px"><h2 class="h" style="font-size:78px"><span>Каждое восстановление</span><span style="color:{ORANGE}">индивидуально.</span></h2>
<p class="body" style="margin-top:36px;font-size:34px">Эта памятка — не замена врачу. Слушайте своего акушера и своё тело.</p>
<p class="body" style="margin-top:24px;font-size:34px">💌 Отправьте подруге, которая скоро рожает.</p>
<p style="margin-top:40px;font-size:22px;color:#999;line-height:1.5">По материалам NHS: Mid Kent / MKUH «Advice and exercises following a caesarean section»; East & North Herts NHS «Recovering from an emergency caesarean»; NHS Grampian «Recovering following a caesarean section».</p></div>'''))
carousel('a3_7_veshchei_posle_kesareva', T, '7 вещей после кесарева')
print('done')
