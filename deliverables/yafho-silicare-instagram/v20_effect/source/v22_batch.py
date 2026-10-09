# Шаги 30–31: ТЕСТ №11 «Вата на ране», №12 «Белая кожа вокруг раны» (мацерация)
import sys, random
from fxkit import *
which=sys.argv[1:]
def chip(t): return f'<div style="position:absolute;left:0;right:0;bottom:30px;text-align:center"><span style="display:inline-block;padding:10px 26px;border-radius:30px;background:rgba(255,255,255,.75);{F};font-weight:800;font-size:30px;color:#2B2B2B">{t}</span></div>'
def skin(id,shape='border-radius:28%',extra=''):
    return (f'<div id="{id}" style="position:absolute;inset:0"><div style="position:absolute;left:14px;top:14px;width:332px;height:332px;{shape};'
            'background:radial-gradient(ellipse at 38% 32%,#FBE0CB,#EFC2A0 55%,#D99C78);box-shadow:0 40px 50px -25px rgba(90,40,20,.45),inset -18px -26px 50px rgba(150,70,40,.25)">'
            '<div style="position:absolute;inset:0;border-radius:inherit;opacity:.35;background-image:radial-gradient(rgba(150,80,50,.5) 1px,transparent 1.6px);background-size:11px 11px"></div></div>'
            f'{extra}</div>')
CUT='<div style="position:absolute;left:110px;top:176px;width:150px;height:14px;border-radius:7px;background:linear-gradient(90deg,#B8362C,#D9473B,#B8362C);transform:rotate(-8deg);box-shadow:0 0 0 5px rgba(230,110,90,.35)"></div>'
r=random.Random(4)
fib=lambda n,box,col,seed: ''.join(f'<path d="M{(x:=random.Random(seed+i).uniform(box[0],box[2])):.0f} {(y:=random.Random(seed*7+i).uniform(box[1],box[3])):.0f} q{random.Random(i+seed).uniform(-30,30):.0f} {random.Random(i*3+seed).uniform(-20,20):.0f} {random.Random(i*5+seed).uniform(-50,50):.0f} {random.Random(i*9+seed).uniform(-14,14):.0f}" stroke="{col}" stroke-width="2.5" fill="none" opacity=".9"/>' for i in range(n))
cotton=('<div style="position:absolute;left:20px;top:-10px;width:340px;height:150px;border-radius:60% 50% 55% 45%/60% 55% 45% 50%;'
        'background:radial-gradient(ellipse at 40% 40%,#FFFFFF,#F2F2F2 60%,#DADADA);box-shadow:0 12px 24px rgba(30,40,60,.25);filter:blur(.5px)"></div>'
        f'<svg viewBox="0 0 380 130" style="position:absolute;inset:0;overflow:visible">{fib(60,(30,-10,350,130),"#E6E6E6",1)}</svg>')
cotton_stuck='<div style="position:absolute;left:150px;top:60px;width:110px;height:24px;border-radius:12px;background:rgba(200,60,50,.6)"></div>'
fibers_in=(f'<div style="position:absolute;left:110px;top:170px;width:150px;height:26px;border-radius:13px;background:#C9382D;transform:rotate(-8deg);box-shadow:0 0 0 8px rgba(230,90,70,.4),0 0 24px 10px rgba(230,90,70,.35)"></div>'
           f'<svg viewBox="0 0 360 360" style="position:absolute;inset:0">{fib(26,(105,160,265,205),"#FFFFFF",9)}</svg>')
island=('<div style="position:absolute;left:0;top:40px;width:300px;height:220px;border-radius:30px;background:linear-gradient(180deg,#FFFFFF,#ECEFF2);box-shadow:0 18px 30px -12px rgba(30,40,60,.35);transform:rotate(6deg)">'
        '<div style="position:absolute;left:60px;top:50px;width:180px;height:120px;border-radius:18px;background:radial-gradient(ellipse,#FCE6CC,#F0C595)"></div></div>')
finger=lambda id: skin(id,'border-radius:44% 44% 30% 30%/50% 50% 30% 30%',CUT+'<div style="position:absolute;left:96px;top:30px;width:168px;height:84px;border-radius:50% 50% 20% 20%;background:rgba(255,236,228,.85);box-shadow:inset 0 -4px 6px rgba(200,140,120,.4)"></div>')
if not which or 't11' in which:
    effect_reel('t11_vata_na_rane',11,'Порез на кухне.<br><span style="color:#F38221">Приложить вату?</span>',finger,fibers_in,cotton_stuck,island,
     'Вечером — меняем','Волокна остались<br>в ране','Чисто',
     'Волокна ваты остаются в ране.<br><span style="color:#F38221">Промыть → прижать →<br>закрыть повязкой.</span>',
     'Вату —','в косметичку.','Если кровь не останавливается за 10 минут,<br>рана глубокая или грязная — к врачу.<br>Перешлите тому, кто готовит на праздники 🎄',
     'Иллюстрация. Первая помощь: промыть чистой водой, прижать чистой салфеткой, закрыть повязкой.<br>',left_lbl='ВАТА',right_lbl='ПОВЯЗКА YAFHO',left_pad=cotton,decor=chip('🔪 палец'))
# --- №12 мацерация: белая сморщенная кожа вокруг раны
WOUND='<div style="position:absolute;left:140px;top:150px;width:90px;height:66px;border-radius:50%;background:radial-gradient(ellipse,#D9564A,#B8362C);"></div>'
wound=lambda id: skin(id,'border-radius:28%',WOUND)
macer=('<div style="position:absolute;left:96px;top:118px;width:178px;height:132px;border-radius:50%;background:radial-gradient(ellipse,transparent 34%,rgba(250,250,245,.95) 36%,rgba(240,238,232,.9) 70%,transparent 74%)"></div>'
       '<svg viewBox="0 0 360 360" style="position:absolute;inset:0">'+''.join(f'<path d="M{100+i*12} {130+(i%3)*4} q8 10 0 20 q-8 10 0 20 q8 10 0 20" stroke="rgba(190,185,175,.9)" stroke-width="2" fill="none"/>' for i in range(15))+'</svg>'
       '<div style="position:absolute;left:140px;top:150px;width:90px;height:66px;border-radius:50%;background:radial-gradient(ellipse,#D9564A,#B8362C)"></div>')
wet='<div style="position:absolute;left:150px;top:36px;width:90px;height:60px;border-radius:50%;background:radial-gradient(ellipse,rgba(240,210,150,.85),rgba(220,180,110,.6))"></div>'
if not which or 't12' in which:
    effect_reel('t12_belaya_kozha',12,'Белая сморщенная кожа<br><span style="color:#F38221">вокруг раны.</span><br>Как после ванны?',wound,macer,wet,sili(0,0,300,'transform:rotate(6deg)'),
     '2 дня спустя','Влага осталась —<br>кожа размокла','Края раны сухие',
     'Пластырь держит влагу у кожи —<br>она размокает (мацерация).<br><span style="color:#F38221">Пена забирает влагу в себя.</span>',
     'Влагу —','в повязку, не в кожу.','Перешлите тому, кто ухаживает за раной<br>дома или в отделении',
     'Иллюстрация. Как часто менять повязку — по назначению врача или медсестры.<br>',decor=chip('🩹 рана с отделяемым'))
