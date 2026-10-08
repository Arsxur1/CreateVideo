# Шаг 13: пакет сторис под мастер-календарь (1080×1920, безопасные зоны: верх 250, низ 340)
import os, shutil
from kp import _dir, _snap, strip
from gen_lib import page
from brand import logo, sili, ORANGE, INK, GREY, STAGE
from lineart import svg
OUT=os.path.abspath('../../deliverables/yafho-silicare-instagram/v13_stories')
ART_KEY={'feet':'neonatology','belly':'obstetrics','profile':'plastic_surgery','butterfly':'dermatology','peach':'geriatrics','suture':'surgery'}
DARK='radial-gradient(ellipse at 50% 30%,#2a1d14,#0E0B09 70%)'
F="font-family:'Inter Display',sans-serif"
def poll(opts,dark):  # макет стикера: место, куда кладётся настоящий стикер
    bg='rgba(255,255,255,.96)'
    rows=''.join(f'<div style="margin-top:14px;padding:22px 26px;border-radius:18px;background:#F2F2F2;{F};font-weight:700;font-size:36px;color:#262626;text-align:center">{o}</div>' for o in opts)
    return f'<div style="background:{bg};border-radius:30px;padding:20px 26px 28px;box-shadow:0 20px 50px rgba(0,0,0,.25)">{rows}</div>'
def quiz(opts,dark):
    L='ABCD'
    rows=''.join(f'<div style="margin-top:14px;display:flex;align-items:center;padding:18px 22px;border-radius:18px;background:#F2F2F2;{F};font-weight:700;font-size:32px;color:#262626"><span style="flex:0 0 52px;height:52px;border-radius:50%;background:#fff;border:3px solid #ddd;display:flex;align-items:center;justify-content:center;font-size:26px;margin-right:18px">{L[i]}</span>{o}</div>' for i,o in enumerate(opts))
    return f'<div style="background:#fff;border-radius:30px;padding:20px 26px 28px;box-shadow:0 20px 50px rgba(0,0,0,.25)">{rows}</div>'
def question(hint,dark):
    return f'<div style="background:#fff;border-radius:30px;overflow:hidden;box-shadow:0 20px 50px rgba(0,0,0,.25)"><div style="background:linear-gradient(90deg,{ORANGE},#E0567A);padding:26px;{F};font-weight:800;font-size:36px;color:#fff;text-align:center">Задайте вопрос</div><div style="padding:30px;font-size:32px;color:#999;text-align:center">{hint}</div></div>'
def slider(emoji,dark):
    return f'<div style="background:#fff;border-radius:30px;padding:40px 46px;box-shadow:0 20px 50px rgba(0,0,0,.25)"><div style="position:relative;height:14px;border-radius:7px;background:linear-gradient(90deg,#ddd,{ORANGE})"><div style="position:absolute;left:38%;top:-38px;font-size:80px;line-height:1">{emoji}</div></div></div>'
def link(text,dark):
    return f'<div style="display:inline-block;background:#fff;border-radius:22px;padding:22px 40px;{F};font-weight:800;font-size:38px;color:#2E6BE6;box-shadow:0 20px 50px rgba(0,0,0,.25)">🔗 {text}</div>'
def addyours(text,dark):
    return f'<div style="background:#fff;border-radius:30px;padding:30px 36px;box-shadow:0 20px 50px rgba(0,0,0,.25)"><div style="font-size:26px;color:#999;text-align:center;letter-spacing:.1em">ДОБАВЬ СВОЁ</div><div style="margin-top:10px;{F};font-weight:800;font-size:40px;color:#262626;text-align:center">{text}</div><div style="margin:18px auto 0;width:240px;padding:14px;border-radius:14px;background:#2E6BE6;color:#fff;text-align:center;font-weight:700;font-size:28px">Добавить</div></div>'
STK={'Опрос':poll,'Викторина':quiz,'Вопросы':question,'Шкала':slider,'Ссылка':link,'Добавь своё':addyours}
def story(n,date,kicker,title,body,stype,sarg,art,dark,extra=''):
    ink='#fff' if dark else INK; sub='rgba(255,255,255,.75)' if dark else '#555'
    bg=DARK if dark else STAGE
    a='' if not art else (f'<div style="position:absolute;left:0;right:0;top:340px;text-align:center;opacity:{.95 if dark else 1}">{svg(ART_KEY[art],360,6,ink=ink)}</div>' if art!='sili' else sili(400,350,280,'transform:rotate(-6deg)'))
    tt=730 if art else 470
    s=STK[stype](*sarg,dark) if isinstance(sarg,tuple) else STK[stype](sarg,dark)
    return f'''<div class="fill" style="background:{bg}"></div>
<div style="position:absolute;left:0;right:0;top:0;height:250px;border-bottom:2px dashed rgba(255,0,0,.0)"></div>
<div style="position:absolute;left:70px;top:270px;{F};font-weight:700;font-size:28px;letter-spacing:.14em;color:{ORANGE}">{kicker}</div>
{a}{extra}
<div style="position:absolute;left:70px;right:70px;top:{tt}px;text-align:center"><div style="{F};font-weight:800;font-size:{74 if len(title)<40 else 62}px;line-height:1.08;letter-spacing:-0.02em;color:{ink}">{title}</div>
<div style="margin-top:26px;font-size:34px;line-height:1.4;color:{sub}">{body}</div></div>
<div style="position:absolute;left:110px;right:110px;top:1150px;text-align:center">
<div style="font-size:20px;letter-spacing:.12em;color:{sub};margin-bottom:12px">↓ СТИКЕР «{stype.upper()}» — ПОЛОЖИТЬ ПОВЕРХ</div>{s}</div>
<div style="position:absolute;left:0;right:0;top:1700px;text-align:center">{logo(44,ORANGE,False)}</div>'''
S=[
 ('12.10','НОВЫЙ REEL','Твоя кожа<br>помнит <span style="color:#F38221">всё.</span>','Шесть историй — одна линия.<br>Смотрите в ленте.','Ссылка','Смотреть Reel','feet',1),
 ('13.10','ОПРОС','Как вы снимаете<br>пластырь?','Честно 🙂','Опрос',(['Одним рывком 💥','Медленно 🐢'],),'peach',0),
 ('16.10','ВИКТОРИНА','Клей обычного пластыря держится за кожу…','','Викторина',(['слабее, чем клетки кожи друг за друга','крепче, чем клетки кожи друг за друга ✓','так же'],),None,0),
 ('19.10','#ПИСЬМОШРАМУ','Привет, шрам…','Допишите письмо своему шраму.<br>Лучшие (с вашего согласия) опубликуем.','Добавь своё','Привет, шрам…','belly',1),
 ('20.10','ОПРОС','У вас было<br>кесарево?','','Опрос',(['Да','Нет','Скоро узнаю 🤰'],),'belly',0),
 ('22.10','МЕДСЁСТРАМ ОРИТН','Ваш лайфхак:<br>как снять фиксацию<br>у самых маленьких?','Соберём ответы в отдельный пост.','Вопросы','Ваш лайфхак…','feet',0),
 ('25.10','25–31 ОКТЯБРЯ','Неделя<br>детей-<span style="color:#F38221">бабочек</span>','Всю неделю рассказываем<br>о буллёзном эпидермолизе.','Ссылка','Фонд-партнёр','butterfly',1),
 ('26.10','ВИКТОРИНА','Почему детей с БЭ<br>называют «бабочками»?','','Викторина',(['Кожа хрупкая, как крыло ✓','Любят бабочек','Рождаются весной'],),'butterfly',0),
 ('30.10','СЕГОДНЯ СТАРТ','Сериал<br>«День 1 из 180»','Одна пациентка, один шрам.<br>7 честных секунд каждую неделю.','Ссылка','Смотреть День 1','profile',1),
 ('02.11','ОПРОС','Кто важнее<br>для шва?','','Опрос',(['Хирург 🩺','Медсестра 💉'],),'suture',0),
 ('04.11','ШКАЛА','Насколько больно<br>вам было снимать<br>повязку?','','Шкала','😬','suture',0),
 ('05.11','ФАКТ','16% пациентов ОРИТ —<br>повреждения кожи<br>от медклея','У этого есть название — MARSI.<br>J Wound Care, 2024.','Ссылка','Как снимать бережнее','suture',1),
 ('09.11','КЛИНИКАМ И ДИСТРИБЬЮТОРАМ','Для кого<br>вы закупаете?','','Опрос',(['Клиника / стационар','Аптека','Дистрибуция'],),None,0),
 ('10.11','ПОД ЛУПОЙ','Какой продукт<br>показать<br>следующим?','Wound Contact Layer, Scar Sheet,<br>Hydrogel, CHG…','Вопросы','Продукт…',None,1),
 ('12.11','КАТАЛОГ 2025','Напишите<br>«КАТАЛОГ»<br>в директ','Пришлём каталог Yafho<br>и условия по образцам.','Ссылка','Написать в директ','sili',0),
 ('16.11','ВИКТОРИНА','Какой слой Sili-Care касается кожи?','','Викторина',(['Мягкая пена','Перфорированный силикон ✓','Защитная плёнка'],),'sili',0),
 ('19.11','ВОПРОС','Что рассказать<br>о шрамах?','Ответим в следующих постах.','Вопросы','Мой вопрос…','profile',0),
 ('22.11','ИТОГИ 6 НЕДЕЛЬ','Какая серия<br>понравилась больше?','Спасибо, что были с нами 🧡','Опрос',(['Кино-истории','Экран телефона','Кинетика','Под лупой'],),None,1),
]
slides=[story(i+1,*s[:6],s[6],s[7]) for i,s in enumerate(S)]
# метки «правильный ответ» убираем из макета (в стикере викторины его отмечают в настройках)
slides=[x.replace(' ✓','') for x in slides]
d=_dir('v13_stories')
open(os.path.join(d,'index.html'),'w').write(page(slides,1080,1920,'Сторис'))
shots=_snap(d,[i+.5 for i in range(len(slides))])[:len(slides)]
os.makedirs(OUT,exist_ok=True)
names=[]
for i,(sh,s) in enumerate(zip(shots,S)):
    nm=f'st{i+1:02d}_{s[0].replace(".","-")}.png'; shutil.copy(sh,os.path.join(OUT,nm)); names.append(nm)
strip(shots,'kp/chk_v13.jpg',2400); print('ok',len(names))
