# Шаг 35: постеры/карусель «Наука ухода» (1080×1350)
import os, shutil
from scikit import *
from kp import _dir, _snap, strip
from gen_lib import page
OUT='/home/user/CreateVideo/deliverables/yafho-silicare-instagram/v23_science/posters'; os.makedirs(OUT,exist_ok=True)
N=8
def frame(i,title,body,src='',sub=''):
    return (f'{bgs()}<div style="position:absolute;left:64px;top:56px">{logo(54,ORANGE,False)}</div>'
            f'<div style="position:absolute;right:64px;top:62px;padding:10px 20px;background:{BLUE};color:#fff;{F};font-weight:800;font-size:22px;letter-spacing:.08em">НАУКА УХОДА · {i}/{N}</div>'
            f'<div style="position:absolute;left:64px;right:64px;top:150px;{F};font-weight:900;font-size:62px;line-height:1.06;letter-spacing:-0.02em;color:{INK}">{title}</div>'
            +(f'<div style="position:absolute;left:64px;right:64px;top:{150+ (2 if "<br>" in title else 1)*70+24}px;font-size:30px;line-height:1.35;color:{MUTED}">{sub}</div>' if sub else '')
            +body+(f'<div style="position:absolute;left:64px;right:64px;bottom:46px;font-size:19px;line-height:1.45;color:{MUTED}">{src}</div>' if src else ''))
T=lambda t: f'<span style="color:{ORANGE}">{t}</span>'
S=[]
# 1 обложка
tiles=[('💧','Влажная среда','заживление быстрее'),('🤲','Бережное снятие','кожа остаётся целой'),('🛡️','Защита от давления','меньше пролежней'),('✨','Уход за рубцом','рубец мягче')]
tl=''.join(f'<div style="position:absolute;left:{64+(k%2)*486}px;top:{560+(k//2)*300}px;width:466px;height:280px;border-radius:32px;background:#fff;box-shadow:0 24px 50px -28px rgba(40,60,100,.4);padding:34px;box-sizing:border-box">'
           f'<div style="font-size:60px">{e}</div><div style="margin-top:14px;{F};font-weight:900;font-size:38px;color:{INK}">{k+1}. {a}</div><div style="margin-top:8px;font-size:28px;color:{MUTED}">{b}</div></div>' for k,(e,a,b) in enumerate(tiles))
S.append(frame(1,f'«Зачем мне<br>эта повязка?»',tl+f'<div style="position:absolute;right:64px;bottom:110px;{F};font-weight:800;font-size:32px;color:{ORANGE}">Листайте →</div>',
  'Медицинские изделия. Применение — по назначению специалиста.',sub='Самый частый вопрос пациента. 4 ответа из исследований — простыми словами.'))
# 2 влага
b=bars([('Под коркой',1,CTRL,'1×'),('Во влажной<br>среде',2,YAF,'≈2×')],880,label_w=270,bh=80,gap=46)
S.append(frame(2,f'1. Под повязкой рана<br>{T("затягивается быстрее")}',
  card(64,470,952,560,f'<div style="position:absolute;left:36px;top:34px">{kicker("СКОРОСТЬ ЗАТЯГИВАНИЯ РАНЫ")}</div><div style="position:absolute;left:36px;top:110px;width:880px;height:220px">{b}</div>'
       f'<div style="position:absolute;left:36px;right:36px;top:340px;font-size:30px;line-height:1.4;color:{INK}">Клеткам кожи легче ползти по <b>влажной</b> поверхности, чем прокапываться под сухую корку. Поэтому «пусть подышит» — миф.</div>'
       f'<div style="position:absolute;left:36px;top:474px">{grade("эксперимент")}</div>'),
  SOURCES[0]))
# 3 снятие
c1=f'<div style="position:absolute;left:36px;top:40px;width:400px">{stat("≈16%","пациентов реанимации — повреждение кожи медицинским клеем","метаанализ, J Wound Care 2024")}</div>'
c2=f'<div style="position:absolute;left:510px;top:40px;width:400px">{stat("40%","пациентов: смена повязки — самое тяжёлое в жизни с раной","Price et al., 2008")}</div>'
S.append(frame(3,f'2. Обычный клей<br>{T("срывает верхний слой кожи")}',
  card(64,470,952,660,c1+c2+f'<div style="position:absolute;left:36px;right:36px;top:420px;font-size:30px;line-height:1.4;color:{INK}">У этого есть название — <b>MARSI</b>. Силиконовый клей держит кожу, но отпускает без срыва — поэтому его выбирают для тонкой, пожилой, детской кожи.</div>'
       f'<div style="position:absolute;left:36px;top:590px">{grade("масштаб")}</div>'),
  SOURCES[1]+'<br>'+SOURCES[2]))
# 4 давление
pp=lambda n: f'<div style="position:relative;width:{10*30-8}px;height:{10*30-8}px">{people(n,size=24,gap=6,idp="q"+str(n))}</div>'
S.append(frame(4,f'3. Пена на крестце:<br>{T("пролежней ≈ вдвое меньше")}',
  card(64,430,952,750,f'<div style="position:absolute;left:36px;top:34px">{kicker("18 ИССЛЕДОВАНИЙ · 5903 ПАЦИЕНТА")}</div><div style="position:absolute;right:30px;top:272px">{grade("низкая")}</div>'
       f'<div style="position:absolute;left:0;top:70px;width:952px;height:250px">{forest(952)}</div>'
       f'<div style="position:absolute;left:70px;top:336px;width:320px">{pp(10)}<div style="margin-top:14px;{F};font-weight:800;font-size:28px;line-height:1.2;color:{INK}">Без повязки<br><span style="color:{MUTED};font-weight:700">10 из 100*</span></div></div>'
       f'<div style="position:absolute;left:530px;top:336px;width:360px">{pp(5)}<div style="margin-top:14px;{F};font-weight:800;font-size:28px;line-height:1.2;color:{INK}">С силиконовой пеной<br><span style="color:{ORANGE}">≈5 из 100 (от 3 до 8)</span></div></div>'),
  SOURCES[3]+'<br>*Иллюстрация при исходном риске 10 из 100. Повязка не заменяет регулярную смену положения тела.'))
# 5 рубец
steps=[('1','Рана зажила,<br>швы сняты','начинать — только после заживления'),('2','Пластина —<br>каждый день','большую часть суток*'),('3','Месяцы,<br>а не дни','обычно не меньше 2 месяцев*')]
st=''.join(f'<div style="position:absolute;left:{36+k*300}px;top:120px;width:270px"><div style="width:72px;height:72px;border-radius:50%;background:{YAF};color:#fff;{F};font-weight:900;font-size:40px;line-height:72px;text-align:center">{n}</div>'
           f'<div style="margin-top:20px;{F};font-weight:900;font-size:34px;line-height:1.1;color:{INK}">{a}</div><div style="margin-top:10px;font-size:24px;line-height:1.3;color:{MUTED}">{c}</div></div>' for k,(n,a,c) in enumerate(steps))
st+=''.join(f'<div style="position:absolute;left:{120+k*300}px;top:154px;width:200px;height:4px;background:#E1E6EE"></div>' for k in range(2))
S.append(frame(5,f'4. Силиконовая пластина —<br>{T("первая линия ухода за рубцом")}',
  card(64,470,952,600,f'<div style="position:absolute;left:36px;top:34px">{kicker("КАК ЭТО РАБОТАЕТ НА ПРАКТИКЕ")}</div>{st}'
       f'<div style="position:absolute;left:36px;right:36px;top:420px;font-size:30px;line-height:1.4;color:{INK}">Пластина удерживает влагу в рубце и мягко прижимает его — так рубец со временем становится мягче и бледнее.</div>'
       f'<div style="position:absolute;left:36px;top:534px">{grade("рекомендация")}</div>'),
  SOURCES[4]+'<br>*Режим ношения — по инструкции к изделию и рекомендации врача. Результат индивидуален.'))
# 6 честно + красные флаги
nots=''.join(f'<div style="margin-top:16px;{F};font-weight:700;font-size:32px;color:{INK}"><span style="color:#C0392B">✕</span>&nbsp; {t}</div>' for t in ['не лечит инфекцию','не заменяет осмотр врача','не заменяет переворачивание лежачего'])
flags=''.join(f'<div style="margin-top:14px;{F};font-weight:700;font-size:32px;color:{INK}"><span style="display:inline-block;width:40px;height:40px;border-radius:50%;background:#C0392B;color:#fff;text-align:center;line-height:40px;font-size:26px">!</span>&nbsp; {t}</div>' for t in RED_FLAGS)
S.append(frame(6,f'Честно: чего повязка<br>{T("НЕ делает")}',
  card(64,450,952,330,f'<div style="position:absolute;left:36px;top:30px">{kicker("ПОВЯЗКА")}</div><div style="position:absolute;left:36px;top:60px">{nots}</div>')+
  card(64,810,952,410,f'<div style="position:absolute;left:36px;top:30px">{kicker("СРАЗУ К ВРАЧУ, ЕСЛИ","",0,"#C0392B")}</div><div style="position:absolute;left:36px;top:60px">{flags}</div>'),
  'Признаки, при которых нужен осмотр, — общие рекомендации NHS по уходу за раной. Не является медицинской консультацией.'))
# 7 вопросы врачу
qs=''.join(f'<div style="display:flex;align-items:flex-start;margin-top:{0 if k==0 else 26}px"><div style="flex:0 0 52px;height:52px;border-radius:12px;border:4px solid {YAF};margin-right:24px"></div><div style="{F};font-weight:800;font-size:34px;line-height:1.2;color:{INK}">{q}</div></div>' for k,q in enumerate(QUESTIONS))
S.append(frame(7,f'Закрываем пробел:<br>{T("5 вопросов врачу при выписке")}',
  card(64,450,952,640,f'<div style="position:absolute;left:40px;right:40px;top:44px">{qs}</div>')+
  f'<div style="position:absolute;left:64px;right:64px;top:1120px;{F};font-weight:800;font-size:32px;line-height:1.3;color:{INK}">📌 Сохраните и покажите на приёме.<br><span style="color:{ORANGE}">Напишите «ПАМЯТКА» — пришлём PDF.</span></div>',
  'Пациенты часто не знают, что спросить. Эти вопросы помогают получить план ухода до выхода из больницы.'))
# 8 источники
src=''.join(f'<div style="margin-top:20px;font-size:26px;line-height:1.4;color:{INK}"><b>{k+1}.</b> {s}</div>' for k,s in enumerate(SOURCES))
S.append(frame(8,f'Источники',card(64,300,952,800,f'<div style="position:absolute;left:40px;right:40px;top:20px">{src}</div>')+
  f'<div style="position:absolute;left:0;right:0;top:1140px;text-align:center">{logo(84,ORANGE,True)}</div>',
  'Медицинские изделия. Показания и режим применения — по инструкции производителя и назначению специалиста.'))
d=_dir('v23_posters')
open(os.path.join(d,'index.html'),'w').write(page(S,1080,1350,'Наука ухода'))
shots=_snap(d,[i+.5 for i in range(len(S))])[:len(S)]
for i,sh in enumerate(shots): shutil.copy(sh,f'{OUT}/nauka_{i+1:02d}.png')
from PIL import Image
G=Image.new('RGB',(4*540+30,2*675+10),(30,30,30))
for i,sh in enumerate(shots): G.paste(Image.open(sh).convert('RGB').resize((540,675)),((i%4)*550,(i//4)*685))
G.save(f'{OUT}/../posters_sheet.jpg',quality=86); print('ok',len(shots))
