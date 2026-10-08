# Шаг 10: короткие кинетические версии историй отделений (~12–13 с)
import sys
from stylekit import style_reel, kick, SOUT
from brand import ORANGE, logo, sili
from kp import strip
import sfx
W='#FFFFFF'; O=ORANGE; K='#141414'; RED='#E53B2C'
V12=SOUT.replace('v8_styles','v12_kinetic')
from PIL import ImageFont
import os
_FB='/usr/share/fonts/opentype/inter/InterDisplay-Black.otf'
def fs(text,size):  # кегль по реальной ширине строки (Inter Display Black, трекинг -0.04em)
    while size>40:
        w=ImageFont.truetype(_FB,size).getlength(text)-0.04*size*(len(text)-1)
        if w<=960: return size
        size-=6
    return size
def story(name,title,cuts,end,foot,check):
    secs=''; js=''; ev=[]; t=0
    for i,(d,bg,lines,extra) in enumerate(cuts+[end]):
        inner=''
        for j,(txt,size,col,top) in enumerate(lines):
            s=fs(txt,size)
            inner+=f'<div id="c{i}w{j}" style="position:absolute;left:30px;right:30px;top:{top}px;text-align:center;font-family:\'Inter Display\';font-weight:900;font-size:{s}px;line-height:1;letter-spacing:-0.04em;color:{col};white-space:nowrap">{txt}</div>'
            js+=f'tl.from("#c{i}w{j}",{{scale:{1.9 if s>=180 else 1.4},opacity:0,duration:.22,ease:"power4.out"}},{t+.04+j*.32:.2f});'
            if s>=180 and j: ev.append((t+.04+j*.32,kick(.6)))
        if i==len(cuts):  # финальная карточка
            inner+=f'<div id="lg" style="position:absolute;left:0;right:0;top:1010px;text-align:center">{logo(110)}</div><div id="ct" style="position:absolute;left:80px;right:80px;top:1250px;text-align:center;font-size:36px;color:{"#444" if bg==W else "#eee"};font-weight:600;line-height:1.4">{extra}</div><div style="position:absolute;left:70px;right:70px;bottom:100px;text-align:center;font-size:22px;line-height:1.5;color:{"rgba(0,0,0,.45)" if bg==W else "rgba(255,255,255,.5)"}">{foot}Медицинское изделие. Применение — по назначению специалиста.</div>'
            js+=f'tl.from("#lg",{{opacity:0,duration:.4}},{t+.8}).from("#ct",{{opacity:0,duration:.4}},{t+1.2});'
            ev+=[(t+.8,sfx.chime(660,.18,2.5))]
        elif extra: inner+=extra
        secs+=f'<section id="b{i}" class="clip" data-start="{t:.2f}" data-duration="{d}" data-track-index="1"><div class="fill" style="background:{bg}"></div>{inner}</section>'
        js+=f'tl.from("#b{i}",{{yPercent:100,duration:.18,ease:"power4.out"}},{t:.2f});'
        ev.append((t,kick(.7))); t+=d
    dur=round(t,2)
    ends=[];tt=0
    for c in cuts+[end]: tt+=c[0]; ends.append(round(tt-.15,2))
    check=(ends[0],)+tuple(ends)
    shots=style_reel(name,dur,secs,js,title,ev,pad=None,check=check,bg=W,outdir=V12)
    strip(shots,f'kp/chk_{name}.jpg',2400); print('ok',name,dur,flush=True)
S=[
 ('k1_akusherstvo','Акушерство',[
   (1.2,K,[('КЕСАРЕВО —',150,W,700),('КАЖДЫЕ',150,W,880),('5-Е РОДЫ.',260,O,1050)],''),
   (1.6,W,[('3-Й ДЕНЬ',170,K,640),('ДОМА.',300,K,840),('ШОВ ПОД ПЛАСТЫРЕМ.',120,O,1180)],''),
   (1.5,O,[('СНИМАТЬ',220,W,700),('СТРАШНО.',220,K,950)],''),
   (1.6,K,[('А ЕСЛИ',150,W,640),('ПЛАСТЫРЬ',200,W,820),('ОТПУСКАЕТ',200,O,1040),('МЯГКО?',150,W,1270)],''),
   (2.1,W,[('СИЛИКОН',220,K,560),('ДЕРЖИТ ШОВ.',150,O,800),('НЕ КОЖУ.',150,K,980)],'')],
  (3.6,W,[('МАМЕ —',140,K,520),('НЕ БОЛЬНО.',160,O,690)],'Перешлите той, кто скоро рожает'),
  'Кесарево ≈ 21% родов в мире: ВОЗ, Betran A.P. et al., BMJ Glob Health 2021.<br>',(.6,1.6,3.5,5.2,7.0,8.6,11.0)),
 ('k2_neonatologiya','Неонатология',[
   (1.3,K,[('1 420',300,W,640),('ГРАММОВ.',180,O,980)],''),
   (1.6,W,[('КОЖА',260,K,580),('ТОНЬШЕ',200,K,880),('БУМАГИ.',200,RED,1110)],''),
   (1.6,O,[('КАЖДЫЙ',200,W,620),('ПЛАСТЫРЬ',200,K,850),('— ИСПЫТАНИЕ.',130,W,1080)],''),
   (1.5,K,[('ДАТЧИКИ.',170,W,560),('ЗОНДЫ.',170,W,760),('КАТЕТЕРЫ.',170,O,960)],''),
   (2.2,W,[('СИЛИКОН',220,K,560),('ДЕРЖИТ',200,O,800),('И ОТПУСКАЕТ.',150,K,1030)],'')],
  (3.6,K,[('ПЕРВОЕ КАСАНИЕ —',110,W,520),('МЯГКОЕ.',200,O,680)],'Для отделений ОРИТН: напишите «КАТАЛОГ»'),
  'Сценка. Вес — пример.<br>',(.7,1.6,3.6,4.9,6.5,8.2,11.0)),
 ('k3_plastika','Пластическая хирургия',[
   (1.3,K,[('ОПЕРАЦИЯ —',170,W,640),('ЧАСЫ.',300,O,860)],''),
   (1.3,W,[('ШРАМ —',220,K,640),('МЕСЯЦЫ.',240,RED,900)],''),
   (1.9,O,[('СИЛИКОН —',180,W,560),('ПЕРВАЯ ЛИНИЯ*',140,K,800),('УХОДА',180,W,980),('ЗА РУБЦАМИ.',150,W,1180)],''),
   (1.8,K,[('НЕДЕЛЯ 1',160,W,620),('→',160,O,820),('НЕДЕЛЯ 12',160,W,1020)],''),
   (1.9,W,[('ШРАМ',260,K,600),('ЗАСЛУЖИВАЕТ',150,O,900),('ЗАБОТЫ.',200,K,1080)],'')],
  (3.6,W,[('SILICONE',160,K,520),('SCAR SHEET',160,O,690)],'После заживления — по назначению хирурга'),
  '* Meaume S. et al., Wound Repair Regen 2014.<br>',(.6,1.6,2.9,5.0,6.7,8.4,11.2)),
 ('k4_babochki','Дерматология',[
   (1.4,K,[('ДЕТИ-',220,W,620),('БАБОЧКИ.',230,O,880)],''),
   (1.6,W,[('КОЖА',260,K,560),('КАК КРЫЛО',190,K,860),('БАБОЧКИ.',190,O,1080)],''),
   (1.5,O,[('ОБЫЧНЫЙ',190,W,640),('ПЛАСТЫРЬ —',170,K,860),('НЕЛЬЗЯ.',200,W,1060)],''),
   (1.9,K,[('СИЛИКОНОВЫЕ',150,W,580),('ПОВЯЗКИ',190,O,780),('РЕКОМЕНДУЮТ*',140,W,1010)],''),
   (1.9,W,[('25–31',260,K,580),('ОКТЯБРЯ',190,O,880),('НЕДЕЛЯ БЭ.',150,K,1100)],'')],
  (3.6,K,[('УЗНАЙТЕ.',160,W,520),('РАССКАЖИТЕ.',140,O,690)],'Перешлите — чем больше людей знают о БЭ, тем легче семьям'),
  '* GOSH, DEBRA: рекомендации по уходу при буллёзном эпидермолизе.<br>',(.7,1.7,3.6,5.0,6.8,8.6,11.2)),
 ('k5_hirurgiya','Хирургия',[
   (1.3,K,[('СМЕНА',240,W,620),('12 ЧАСОВ.',220,O,900)],''),
   (1.9,W,[('40%',340,RED,520),('ПАЦИЕНТОВ*:',130,K,900),('ПЕРЕВЯЗКА —',130,K,1060),('ХУДШЕЕ.',190,O,1220)],''),
   (1.5,O,[('КРИК.',240,W,600),('СЛЁЗЫ.',240,K,860)],''),
   (1.6,K,[('А ЕСЛИ',160,W,640),('ПОВЯЗКА',200,W,820),('НЕ РАНИТ?',190,O,1050)],''),
   (2.0,W,[('СИЛИКОН',220,K,580),('СНИМАЕТСЯ',170,O,820),('МЯГКО.',200,K,1030)],'')],
  (3.6,W,[('ПЕРЕВЯЗКА',150,K,520),('БЕЗ СЛЁЗ.',160,O,690)],'Отметьте медсестру, которая это поймёт'),
  '* 40,3% пациентов назвали смену повязки худшим в жизни с раной: Price P. et al., Int Wound J 2008.<br>',(.6,1.6,2.6,4.2,5.6,7.3,10.8)),
 ('k6_geriatriya','Гериатрия',[
   (1.5,K,[('$26,8',290,O,600),('МЛРД В ГОД*',150,W,940)],''),
   (1.5,W,[('СТОЯТ',220,K,640),('ПРОЛЕЖНИ.',200,RED,900)],''),
   (1.6,O,[('КОЖА',240,W,580),('БАБУШКИ —',180,K,860),('КАК ПЕРСИК.',160,W,1080)],''),
   (1.7,K,[('КРЕСТЕЦ.',200,W,620),('ПЯТКИ.',200,W,860),('ЛОПАТКИ.',200,O,1100)],''),
   (2.0,W,[('SACRUM —',180,K,560),('ПОВЯЗКА',180,O,800),('«СЕРДЦЕ».',180,K,1030)],'')],
  (3.6,K,[('БЕРЕЖНО —',150,W,520),('КАЖДЫЙ ДЕНЬ.',140,O,690)],'Перешлите тому, кто ухаживает за родителями'),
  '* Затраты на пролежни в США: Padula W.V. et al., Int Wound J 2019.<br>',(.7,1.6,3.0,4.7,6.4,8.4,11.2)),
]
only=sys.argv[1:]
for name,title,cuts,end,foot,chk in S:
    if only and name not in only: continue
    story(name,title,cuts,end,foot,chk)
