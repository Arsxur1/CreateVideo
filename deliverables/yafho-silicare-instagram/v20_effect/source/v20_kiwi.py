# Шаг 20: «Киви-тест» — пластырь и волоски
import random
from fxkit import *
r=random.Random(7)
def hairs(n,box=(20,30,340,300),col='#E2C79A',seed=1):
    rr=random.Random(seed); out=[]
    x0,y0,x1,y1=box; cx,cy=(x0+x1)/2,(y0+y1)/2; ax,ay=(x1-x0)/2,(y1-y0)/2
    while len(out)<n:
        x,y=rr.uniform(x0,x1),rr.uniform(y0,y1)
        if ((x-cx)/ax)**2+((y-cy)/ay)**2>1: continue
        a=rr.uniform(-1,1); l=rr.uniform(8,16)
        out.append(f'<line x1="{x:.0f}" y1="{y:.0f}" x2="{x+l*a:.0f}" y2="{y-l:.0f}" stroke="{col}" stroke-width="2" stroke-linecap="round" opacity="{rr.uniform(.5,.95):.2f}"/>')
    return ''.join(out)
def kiwi(id):
    return (f'<div id="{id}" style="position:absolute;inset:0">'
            '<div style="position:absolute;left:6px;top:24px;width:348px;height:300px;border-radius:52% 48% 50% 50%/55% 52% 48% 45%;background:radial-gradient(ellipse at 35% 30%,#B8935F,#8A6A3E 55%,#5E4426);box-shadow:0 40px 50px -25px rgba(40,30,20,.55),inset -20px -30px 50px rgba(30,20,10,.35)"></div>'
            f'<svg viewBox="0 0 360 360" style="position:absolute;inset:0">{hairs(1400,(12,30,348,318),"#E8CF9F",1)}{hairs(500,(12,30,348,318),"#B89363",2)}</svg></div>')
def half():  # разрезанная половинка — чтобы киви узнавался сразу
    seeds=''.join(f'<div style="position:absolute;left:{60+38*__import__("math").cos(a/12*6.283):.0f}px;top:{60+38*__import__("math").sin(a/12*6.283):.0f}px;width:7px;height:11px;border-radius:50%;background:#1d1a12;transform:rotate({a*30}deg)"></div>' for a in range(12))
    return ('<div style="position:absolute;right:26px;bottom:24px;width:128px;height:128px;border-radius:50%;background:#7A5B34;padding:6px;box-shadow:0 16px 24px -10px rgba(40,30,20,.5)">'
            '<div style="position:relative;width:116px;height:116px;border-radius:50%;background:radial-gradient(circle,#F3F0C8 0 16%,#9CC33C 30%,#6FA02A 80%,#5B8A22)">'+seeds+'</div></div>')
# под пластырем: полоса без ворса (повёрнута как пластырь)
dmg=('<div style="position:absolute;left:14px;top:136px;width:332px;height:98px;transform:rotate(-8deg);border-radius:40px;'
     'background:linear-gradient(180deg,#5B3D20,#3F2A15);box-shadow:inset 0 0 16px rgba(20,10,0,.8)"><div style="position:absolute;left:30px;right:60px;top:18px;height:12px;border-radius:6px;background:rgba(255,235,200,.35);filter:blur(3px)"></div></div>'
     '<svg viewBox="0 0 360 360" style="position:absolute;inset:0">'+hairs(14,(30,140,330,230),'#E2C79A',3)+'</svg>')
stuck=f'<svg viewBox="0 0 380 130" style="position:absolute;inset:0">{hairs(420,(20,10,360,120),"#A9824E",5)}</svg>'
pad=sili(0,0,300,'transform:rotate(6deg);opacity:.96')
effect_reel('t1_kiwi_test',1,'Что пластырь<br>сделает <span style="color:#F38221">с киви?</span>',kiwi,dmg,stuck,pad,
 'Сутки спустя','Ворс остался<br>на пластыре','Ворс на месте',
 'Обычный клей цепляется<br>за каждый волосок.<br><span style="color:#F38221">Силикон держит кожу —<br>и отпускает.</span>',
 'Снимать —','не выдирать.','Спорт, мужская кожа, дети:<br>напишите «КИВИ» — расскажем,<br>какая повязка подойдёт',
 'Демонстрация на фрукте, не клиническое испытание.<br>',decor=half())
