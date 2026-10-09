# Шаги 21, 23, 24: «Новые туфли», «Мама, только не отрывай!», «Красный квадрат»
import sys, random
from fxkit import *
def skin(id,shape='border-radius:46%',extra=''):
    return (f'<div id="{id}" style="position:absolute;inset:0"><div style="position:absolute;left:14px;top:14px;width:332px;height:332px;{shape};'
            'background:radial-gradient(ellipse at 38% 32%,#FBE0CB,#EFC2A0 55%,#D99C78);box-shadow:0 40px 50px -25px rgba(90,40,20,.45),inset -18px -26px 50px rgba(150,70,40,.25)">'
            '<div style="position:absolute;inset:0;border-radius:inherit;opacity:.35;background-image:radial-gradient(rgba(150,80,50,.5) 1px,transparent 1.6px);background-size:11px 11px"></div></div>'
            f'{extra}</div>')
BAND='position:absolute;left:14px;top:136px;width:332px;height:98px;transform:rotate(-8deg);border-radius:40px'
def raw(alpha=1):  # содранный участок кожи под пластырем
    return (f'<div style="{BAND};opacity:{alpha};background:radial-gradient(ellipse at 50% 50%,#F07C6E,#D9473B 70%,#B83228);box-shadow:0 0 0 8px rgba(230,90,70,.35),0 0 24px 10px rgba(230,90,70,.35)">'
            '<div style="position:absolute;inset:10px 24px;border-radius:30px;background:linear-gradient(180deg,rgba(255,255,255,.35),transparent 60%)"></div></div>')
flakes=''.join(f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;border-radius:40% 60% 50% 45%;background:rgba(240,190,160,.95);box-shadow:0 0 0 1px rgba(200,120,90,.5)"></div>' for x,y,w,h in [(40,30,60,26),(120,52,44,20),(190,28,70,30),(270,58,50,22),(90,80,36,16),(230,84,40,18)])
hydro=('<div style="position:absolute;left:10px;top:30px;width:280px;height:240px;border-radius:50%;transform:rotate(6deg);'
       'background:radial-gradient(ellipse at 50% 50%,rgba(250,245,232,.95) 0 30%,rgba(232,200,160,.92) 55%,rgba(214,176,132,.9));'
       'box-shadow:0 18px 30px -12px rgba(90,60,30,.45),inset 0 2px 0 rgba(255,255,255,.6)"></div>')
which=sys.argv[1:]
def chip(t):  # подпись внизу карточки — чтобы сразу понимать, что за участок кожи
    return f'<div style="position:absolute;left:0;right:0;bottom:30px;text-align:center"><span style="display:inline-block;padding:10px 26px;border-radius:30px;background:rgba(255,255,255,.75);{F};font-weight:800;font-size:30px;color:#2B2B2B">{t}</span></div>'
# --- №2 «Новые туфли»: мозоль на пятке
heel=lambda id: skin(id,'border-radius:50% 50% 46% 46%/58% 58% 42% 42%',
   '<div style="position:absolute;left:120px;top:142px;width:130px;height:96px;border-radius:50%;background:radial-gradient(ellipse at 40% 35%,rgba(255,255,255,.9),rgba(255,236,220,.75) 45%,rgba(240,170,140,.7));box-shadow:0 0 0 6px rgba(235,120,100,.35),0 6px 10px rgba(150,60,40,.3)"></div>')
blister_torn=('<div style="position:absolute;left:112px;top:136px;width:146px;height:108px;border-radius:50%;background:radial-gradient(ellipse,#F27565,#D23B30 70%,#A92A22);box-shadow:0 0 0 10px rgba(230,90,70,.4),0 0 30px 12px rgba(230,90,70,.35)"></div>')
blister_roof=('<div style="position:absolute;left:150px;top:30px;width:120px;height:80px;border-radius:50%;background:radial-gradient(ellipse at 40% 35%,rgba(255,245,235,.95),rgba(240,190,170,.85));box-shadow:0 0 0 2px rgba(200,110,90,.6)"></div>')
if not which or 't2' in which:
    effect_reel('t2_novye_tufli',2,'Новые туфли.<br><span style="color:#F38221">Мозоль. Что клеить?</span>',heel,blister_torn,blister_roof,hydro,
     '10 000 шагов','Пластырь прилип<br>и сорвал мозоль','Мозоль под защитой',
     'Обычный пластырь прилипает<br>к пузырю и трётся.<br><span style="color:#F38221">Гидроколлоид смягчает трение<br>и защищает мозоль.</span>',
     'Мозоль —','не прокалывать.','Напишите «ТУФЛИ» —<br>подскажем, что взять в сумку',
     'Если мозоль лопнула, воспалилась или болит сильнее — к врачу.<br>',right_lbl='ГИДРОКОЛЛОИД YAFHO',decor=chip('👠 пятка'))
# --- №4 «Мама, только не отрывай!»: детская коленка
knee=lambda id: skin(id,'border-radius:50%','<div style="position:absolute;left:150px;top:176px;width:70px;height:10px;border-radius:5px;background:#D9473B;transform:rotate(-12deg);box-shadow:0 0 6px rgba(217,71,59,.6)"></div>')
ouch=(raw(.9)+'<div style="position:absolute;left:120px;top:262px;padding:14px 26px;border-radius:30px;background:#fff;'+F+';font-weight:900;font-size:44px;color:#D93A2F;white-space:nowrap;transform:rotate(-8deg);box-shadow:0 10px 20px rgba(0,0,0,.15)">АЙ!!! 😭</div>')
if not which or 't4' in which:
    effect_reel('t4_mama_ne_otryvai',4,'«Мама, только<br><span style="color:#F38221">не отрывай!»</span>',knee,ouch,flakes,sili(0,0,300,'transform:rotate(6deg)'),
     'Вечером — снимаем','Слёзы и красная<br>полоса','«Уже всё?» 🙂',
     'Детская кожа тоньше взрослой.<br>Обычный клей забирает<br>её верхний слой.<br><span style="color:#F38221">Силикон отпускает мягко.</span>',
     'Снимать —','без слёз.','Перешлите маме,<br>которая знает этот крик 💛','',decor=chip('🦵 коленка'))
# --- №5 «Красный квадрат»: след после пластыря
arm=lambda id: skin(id,'border-radius:28%')
# клей держит по краю: красная «рамка», центр под подушечкой почти не задет, по контуру — следы клея
square=('<div style="position:absolute;left:4px;top:126px;width:352px;height:118px;transform:rotate(-8deg);border-radius:20px;'
        'border:26px solid #D9473B;background:rgba(240,150,130,.35);box-shadow:0 0 18px 8px rgba(230,90,70,.4),inset 0 0 14px rgba(180,40,30,.6)"></div>'
        '<div style="position:absolute;left:-4px;top:118px;width:368px;height:134px;transform:rotate(-8deg);border-radius:26px;border:5px dashed rgba(110,110,110,.55)"></div>')
if not which or 't5' in which:
    effect_reel('t5_krasnyi_kvadrat',5,'Красный квадрат<br><span style="color:#F38221">после пластыря.</span><br>Знакомо?',arm,square,flakes,sili(0,0,300,'transform:rotate(6deg)'),
     'Через 3 дня','Содран верхний<br>слой кожи','Кожа цела',
     'Красный след — часто не «аллергия»,<br>а содранный клеем слой кожи.<br><span style="color:#F38221">У этого есть название — MARSI.</span>',
     'Пластырь ушёл —','кожа осталась.','Сохраните, чтобы снимать<br>бережнее: медленно, вдоль кожи,<br>придерживая её пальцем',
     'MARSI — повреждение кожи медицинским клеем (консенсус McNichol et al., 2013). Если покраснение не проходит — к врачу.<br>',decor=chip('💪 предплечье'))
