from kp import *
def raw_svg(paths, size, stroke=4.5, idp=''):
    out=[]
    for d,acc in paths:
        out.append(f'<path class="{"lna" if acc else "lni"}" pathLength="1" d="{d}" fill="none" stroke="{ORANGE if acc else INK}" stroke-width="{stroke*2 if acc else stroke}" stroke-linecap="round" stroke-linejoin="round"/>')
    return f'<svg id="{idp}" viewBox="0 0 600 600" width="{size}" height="{size}" style="overflow:visible">{"".join(out)}</svg>'
KNEE=[("M190 40 C205 170 225 245 262 292 C290 326 318 336 336 352 C356 372 362 430 356 600",0),("M330 40 C326 150 350 222 392 262 C430 298 446 340 440 420 C436 480 430 540 428 600",0),("M352 300 Q376 312 392 338",1)]
APP=[("M150 50 C130 190 105 280 150 380 C178 445 160 520 140 600",0),("M450 50 C470 190 495 280 450 380 C422 445 440 520 460 600",0),("M302 316 C294 326 294 340 301 350",0),("M352 440 L410 400",1)]
from lineart import belly
CS=belly()['paths']
EX=[('Аппендицит, 9 лет.','«Мама всю ночь держала меня за руку. Шрам — это её рука.»','пример истории',APP),
    ('Колено, 7 лет.','«Первый велосипед без страховки. Я тогда всё-таки поехал.»','пример истории',KNEE),
    ('Кесарево, 2023.','«Её зовут Ева. Шрам — это дверь, через которую она пришла.»','пример истории',CS)]
L='#КожаПомнит'
U=[slide_frame(L,'1/5',f'''<div style="position:absolute;left:80px;right:80px;top:170px"><h1 class="h" style="font-size:88px"><span>Пришлите историю</span><span>своего шрама —</span><span style="color:{ORANGE}">мы нарисуем его</span><span style="color:{ORANGE}">одной линией.</span></h1></div>
<div style="position:absolute;left:520px;top:700px">{raw_svg(KNEE,460)}</div>
<div style="position:absolute;left:80px;top:880px;font-size:34px;line-height:1.5;max-width:440px">В подарок. В фирменном стиле. Навсегда ваше.</div>''', footer=False)]
STEPS=[('Напишите в директ','2–3 предложения: где шрам и какая история за ним.'),('Если хотите — пришлите фото контура','Без лица и без открытых ран. Можно просто описать.'),('Получите рисунок','Мы нарисуем шрам одной линией и пришлём вам картинку.'),('Поделитесь','С хэштегом #КожаПомнит. Лучшие истории опубликуем — только с вашего согласия.')]
rows=''.join(f'<div style="display:flex;gap:26px;padding:26px 0;border-bottom:2px solid #EEE"><div style="font-family:Inter Display;font-size:58px;color:{ORANGE};font-weight:600;width:70px">{i+1}</div><div><div style="font-size:38px;font-weight:700">{a}</div><div style="font-size:28px;color:#555;margin-top:6px">{b}</div></div></div>' for i,(a,b) in enumerate(STEPS))
U.append(slide_frame(L,'2/5',f'<div style="position:absolute;left:80px;right:80px;top:170px"><h2 class="h" style="font-size:68px">Как это работает</h2><div style="margin-top:30px">{rows}</div></div><div style="position:absolute;left:600px;top:860px;opacity:.9">{raw_svg(APP,380)}</div>', footer=False))
for i,(t,q,a,P) in enumerate(EX):
    U.append(slide_frame(L,f'{i+3}/5',f'''<div style="position:absolute;left:70px;top:150px;width:940px;height:620px;border-radius:36px;background:#FAFAFA"></div>
<div style="position:absolute;left:240px;top:170px">{raw_svg(P,600)}</div>
<div style="position:absolute;right:90px;top:180px;font-size:20px;color:#aaa;letter-spacing:.1em">ПРИМЕР РАБОТЫ</div>
<div style="position:absolute;left:80px;right:80px;top:820px"><div style="font-size:30px;font-weight:700;color:{ORANGE}">◆ {t}</div>
<div style="font-family:Inter;font-style:italic;font-size:46px;line-height:1.3;margin-top:18px">{q}</div><div style="font-size:26px;color:#777;margin-top:16px">— {a}</div></div>''', footer=False))
carousel('f1_narisuem_odnoi_liniei', U, 'Нарисуем одной линией')

# Шаблон итогов #ПисьмоШраму
T=[slide_frame('#ПисьмоШраму','1/2',f'''<div style="position:absolute;left:80px;right:80px;top:180px"><div style="font-size:30px;font-weight:700;color:{ORANGE}">◆ ВАШИ ПИСЬМА</div>
<h1 class="h" style="font-size:96px;margin-top:20px"><span>Вы написали</span><span style="color:{ORANGE}">[N] писем</span><span>своим шрамам.</span></h1>
<p class="body" style="margin-top:36px;font-size:34px">Мы прочитали каждое. Вот несколько — с разрешения авторов →</p></div>
<div style="position:absolute;left:560px;top:780px">{raw_svg(CS,420)}</div>''', footer=False),
slide_frame('#ПисьмоШраму','2/2',f'''<div style="position:absolute;left:80px;right:80px;top:200px"><div style="font-size:120px;color:{ORANGE};font-family:Georgia;line-height:.6">“</div>
<div style="font-family:Inter;font-style:italic;font-size:54px;line-height:1.3;margin-top:10px">[Текст письма — до 250 знаков. Копируйте этот слайд для каждого письма.]</div>
<div style="font-size:30px;color:#777;margin-top:30px">— [Имя], [год]</div></div>
<div style="position:absolute;left:300px;top:840px">{raw_svg(CS,380)}</div>''', footer=False)]
carousel('f2_shablon_itogi_pismo_shramu', T, 'Итоги #ПисьмоШраму')
print('done')
