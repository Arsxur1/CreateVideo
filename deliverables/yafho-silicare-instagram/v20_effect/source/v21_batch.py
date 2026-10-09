# Шаги 25–26: ТЕСТ №6 «Помидор», ТЕСТ №7 «Воздушный шарик»
import sys
from fxkit import *
which=sys.argv[1:]
def chip(t): return f'<div style="position:absolute;left:0;right:0;bottom:30px;text-align:center"><span style="display:inline-block;padding:10px 26px;border-radius:30px;background:rgba(255,255,255,.75);{F};font-weight:800;font-size:30px;color:#2B2B2B">{t}</span></div>'
BAND='position:absolute;left:14px;top:136px;width:332px;height:98px;transform:rotate(-8deg);border-radius:40px'
# --- №6 помидор
def tomato(id):
    return (f'<div id="{id}" style="position:absolute;inset:0"><div style="position:absolute;left:14px;top:30px;width:332px;height:310px;border-radius:50% 50% 48% 48%/52% 52% 48% 48%;'
            'background:radial-gradient(ellipse at 34% 30%,#FF8A70,#E8321F 45%,#B71C10 85%);box-shadow:0 40px 50px -25px rgba(120,20,10,.55),inset -20px -30px 50px rgba(90,10,5,.4)"></div>'
            '<div style="position:absolute;left:70px;top:70px;width:90px;height:50px;border-radius:50%;background:radial-gradient(closest-side,rgba(255,255,255,.7),transparent);filter:blur(4px)"></div>'
            '<svg viewBox="0 0 360 360" style="position:absolute;inset:0"><g transform="translate(180,40)" fill="#3E8E2E">'+''.join(f'<path d="M0 0 Q{14} {-6} {34} {6} Q12 6 0 0" transform="rotate({a})"/>' for a in range(0,360,60))+'<rect x="-4" y="-26" width="8" height="26" rx="4"/></g></svg></div>')
flesh=(f'<div style="{BAND};background:radial-gradient(ellipse,#FF9C6E,#F2603E 60%,#D9432A);box-shadow:inset 0 0 18px rgba(150,20,10,.5)">'
       +''.join(f'<div style="position:absolute;left:{x}px;top:{y}px;width:14px;height:9px;border-radius:50%;background:#F6E6A0;transform:rotate({r}deg)"></div>' for x,y,r in [(40,30,20),(80,52,-10),(130,28,30),(180,56,0),(230,32,-20),(270,54,15)])
       +'</div><div style="position:absolute;left:250px;top:228px;width:26px;height:44px;border-radius:50% 50% 50% 50%/60% 60% 40% 40%;background:radial-gradient(circle at 40% 30%,#FFB59A,#E8321F);"></div>')
peel='<div style="position:absolute;inset:8px 14px;border-radius:40px;background:linear-gradient(180deg,rgba(220,40,25,.85),rgba(190,25,15,.8))"></div>'
if not which or 't6' in which:
    effect_reel('t6_pomidor_test',6,'Что пластырь<br>сделает <span style="color:#F38221">с помидором?</span>',tomato,flesh,peel,sili(0,0,300,'transform:rotate(6deg)'),
     'Сутки спустя','Кожица осталась<br>на пластыре','Кожица цела',
     'С возрастом кожа истончается —<br>как кожица помидора.<br><span style="color:#F38221">Обычный клей забирает её с собой.<br>Силикон — нет.</span>',
     'Тонкой коже —','мягкий клей.','Перешлите тому, кто ухаживает<br>за пожилыми родителями 🤍',
     'Демонстрация на овоще, не клиническое испытание.<br>',decor=chip('🍅 тонкая кожа'))
# --- №7 воздушный шарик: лопается при рывке
def balloon(id):
    return (f'<div id="{id}" style="position:absolute;inset:0"><div style="position:absolute;left:30px;top:10px;width:300px;height:320px;border-radius:50% 50% 48% 48%/55% 55% 45% 45%;'
            'background:radial-gradient(ellipse at 35% 28%,#FFD3B0,#F7A06A 40%,#F38221 75%,#D9661A);box-shadow:0 30px 40px -20px rgba(150,70,20,.5),inset -16px -24px 40px rgba(160,60,10,.35)"></div>'
            '<div style="position:absolute;left:90px;top:50px;width:70px;height:40px;border-radius:50%;background:radial-gradient(closest-side,rgba(255,255,255,.8),transparent);filter:blur(3px);transform:rotate(-30deg)"></div>'
            '<div style="position:absolute;left:168px;top:326px;width:24px;height:18px;background:#D9661A;clip-path:polygon(50% 0,100% 100%,0 100%)"></div>'
            '<svg viewBox="0 0 360 360" style="position:absolute;inset:0;overflow:visible"><path d="M180 344 C170 380 196 400 178 440" stroke="#999" stroke-width="3" fill="none"/></svg></div>')
shreds=''.join(f'<div class="sh" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;border-radius:40% 60% 30% 70%;background:#F38221;transform:rotate({r}deg)"></div>' for x,y,w,h,r in [(60,90,60,30,20),(220,70,70,26,-30),(120,230,50,22,60),(250,220,64,28,10),(160,140,40,18,-50),(30,200,44,20,35)])
pop_js=(f'tl.to("#ol",{{scale:1.18,duration:.08}},6.5).to("#ol",{{scale:1.6,opacity:0,duration:.12}},6.58)'
        f'.fromTo("#cl",{{backgroundColor:"rgba(255,255,255,.38)"}},{{backgroundColor:"rgba(255,240,220,.95)",duration:.06,yoyo:true,repeat:1}},6.58)'
        f'.from("#dm .sh",{{scale:0,x:0,y:0,duration:.35,stagger:.02,ease:"power3.out"}},6.6);'
        f'tl.to("#or",{{scaleX:1.04,scaleY:.97,duration:.18,yoyo:true,repeat:3,ease:"sine.inOut"}},8.4);')
if not which or 't7' in which:
    effect_reel('t7_sharik',7,'Пластырь<br>на воздушном шарике.<br><span style="color:#F38221">Снимаем.</span>',balloon,shreds,'',sili(0,0,300,'transform:rotate(6deg)'),
     'Сутки спустя','БАХ. 💥','Шарик цел',
     'Отёкшая, натянутая кожа —<br>как этот шарик.<br><span style="color:#F38221">Рывок её травмирует.<br>Силикон отпускает без рывка.</span>',
     'Натянутой коже —','без рывков.','Отёки, пожилые, после операций:<br>напишите «ШАРИК» — расскажем,<br>какая повязка подойдёт',
     'Демонстрация на воздушном шаре, не клиническое испытание.<br>',decor=chip('🎈 натянутая кожа'),
     extra_js=pop_js,extra_ev=[(6.58,sfx.boom(1.0)),(6.6,sfx.tear(.25,.6)),(6.62,sfx.whoosh(.4,.3))])
