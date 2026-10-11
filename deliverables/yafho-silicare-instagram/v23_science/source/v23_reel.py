# Шаг 36: ролик «Наука ухода» — зачем нужна правильная повязка и насколько она помогает (≈53 с)
from scikit import *
from stylekit import style_reel, SOUT
from kp import strip
import sfx
OUT=SOUT.replace('v8_styles','v23_science')
W=1080
def head(n,label,title):
    return (f'<div style="position:absolute;left:70px;top:170px">{logo(56,ORANGE,False)}</div>'
            f'<div style="position:absolute;right:70px;top:176px;padding:10px 20px;background:{BLUE};color:#fff;{F};font-weight:800;font-size:24px;letter-spacing:.08em">{n}</div>'
            f'<div class="kk" style="position:absolute;left:70px;top:290px">{kicker(label)}</div>'
            f'<div class="tt" style="position:absolute;left:70px;right:70px;top:340px;{F};font-weight:900;font-size:68px;line-height:1.05;letter-spacing:-0.02em;color:{INK}">{title}</div>')
def src(t): return f'<div style="position:absolute;left:70px;right:70px;top:1500px;font-size:22px;line-height:1.45;color:{MUTED}">{t}</div>'
def sec(id,s,d,inner): return f'<section id="{id}" class="clip" data-start="{s}" data-duration="{d}" data-track-index="1">{bgs()}{inner}</section>'
T=lambda t: f'<span style="color:{ORANGE}">{t}</span>'
S=[0,4.2,8.0,16.0,23.6,33.4,39.6,44.4,51.2]; DUR=55.0
D=lambda i: round((S[i+1] if i+1<len(S) else DUR)-S[i],2)
body=''; js=''; ev=[]
def intro(id,t): 
    global js; js+=f'tl.from("#{id} .kk,#{id} .tt",{{opacity:0,y:30,duration:.45,stagger:.12,ease:"power3.out"}},{t+.1});'
# 0 хук
body+=sec('s0',S[0],D(0),f'<div style="position:absolute;left:70px;top:170px">{logo(56,ORANGE,False)}</div>'
  f'<div id="h1" style="position:absolute;left:60px;right:60px;top:520px;text-align:center;{F};font-weight:900;font-size:92px;line-height:1.04;letter-spacing:-0.02em;color:{INK}">«Зачем мне<br>эта повязка?<br>{T("Пластырь же есть»")}</div>'
  f'<div id="h2" style="position:absolute;left:90px;right:90px;top:1000px;text-align:center;{F};font-weight:700;font-size:40px;line-height:1.3;color:{INK}">Самый частый вопрос пациента.<br>Отвечаем <b>по исследованиям</b> —<br>простыми словами.</div>')
js+='tl.from("#h1",{scale:1.3,opacity:0,duration:.5,ease:"power3.out"},.05).from("#h2",{opacity:0,y:20,duration:.5},1.2);'
ev+=[(.05,sfx.whoosh(.6,.25)),(.3,sfx.chime(440,.12,2)),(1.2,sfx.click(.3))]
# 1 четыре работы
tiles=[('💧','Влажная среда'),('🤲','Бережное снятие'),('🛡️','Защита от давления'),('✨','Уход за рубцом')]
tl=''.join(f'<div class="t4" style="position:absolute;left:{70+(k%2)*480}px;top:{620+(k//2)*330}px;width:460px;height:300px;border-radius:36px;background:#fff;box-shadow:0 24px 50px -28px rgba(40,60,100,.4);padding:40px;box-sizing:border-box">'
           f'<div style="font-size:76px">{e}</div><div style="margin-top:18px;{F};font-weight:900;font-size:42px;line-height:1.1;color:{INK}">{k+1}. {a}</div></div>' for k,(e,a) in enumerate(tiles))
body+=sec('s1',S[1],D(1),head('НАУКА УХОДА','ПРАВИЛЬНАЯ ПОВЯЗКА ДЕЛАЕТ',f'4 работы<br>{T("правильной повязки")}')+tl)
intro('s1',S[1]); js+=f'tl.from("#s1 .t4",{{scale:.6,opacity:0,duration:.4,stagger:.35,ease:"back.out(1.8)"}},{S[1]+.7});'
ev+=[(S[1],sfx.whoosh(.6,.2))]+[(S[1]+.7+k*.35,sfx.click(.3)) for k in range(4)]
# 2 влага
b=bars([('Под коркой',1,CTRL,'1×'),('Во влажной<br>среде',2,YAF,'≈2×')],880,label_w=270,bh=96,gap=50,idp='wb')
body+=sec('s2',S[2],D(2),head('1 / 4','💧 ВЛАЖНАЯ СРЕДА',f'Под повязкой рана<br>{T("затягивается быстрее")}')+
  card(70,640,940,820,f'<div style="position:absolute;left:36px;top:36px">{kicker("СКОРОСТЬ ЗАТЯГИВАНИЯ")}</div><div style="position:absolute;left:30px;top:130px;width:880px;height:260px">{b}</div>'
       f'<div id="wtx" style="position:absolute;left:40px;right:40px;top:440px;{F};font-weight:700;font-size:38px;line-height:1.3;color:{INK}">Клеткам кожи легче ползти<br>по <span style="color:{ORANGE}">влажной</span> поверхности,<br>чем прокапываться под корку.</div>'
       f'<div id="wgr" style="position:absolute;left:40px;top:700px">{grade("эксперимент")}</div>')+src('Winter G.D., Nature, 1962 — эксперимент на животных.'))
intro('s2',S[2]); t=S[2]+1.2
js+=f'tl.from("#wb0,#wb1",{{scaleX:0,duration:1.0,stagger:.5,ease:"power2.out"}},{t}).from("#wbv0,#wbv1",{{opacity:0,duration:.3,stagger:.5}},{t+.8}).from("#wtx",{{opacity:0,y:20,duration:.5}},{t+2.4}).from("#wgr",{{opacity:0,duration:.4}},{t+3.4});'
ev+=[(S[2],sfx.whoosh(.6,.2)),(t+.9,sfx.chime(523,.12,1.6)),(t+1.4,sfx.chime(784,.14,2))]
# 3 снятие
st1=f'<div style="position:absolute;left:40px;top:50px;width:420px">{stat("<span id=c16>0</span>%","пациентов реанимации — повреждение кожи клеем","метаанализ, J Wound Care, 2024")}</div>'
st2=f'<div style="position:absolute;left:500px;top:50px;width:410px">{stat("<span id=c40>0</span>%","пациентов: смена повязки — самое тяжёлое","Price et al., 2008")}</div>'
body+=sec('s3',S[3],D(3),head('2 / 4','🤲 БЕРЕЖНОЕ СНЯТИЕ',f'Обычный клей<br>{T("срывает верхний слой кожи")}')+
  card(70,640,940,820,st1+st2+f'<div id="mtx" style="position:absolute;left:40px;right:40px;top:440px;{F};font-weight:700;font-size:38px;line-height:1.3;color:{INK}">Это называется <span style="color:{ORANGE}">MARSI</span>.<br>Силиконовый клей держит кожу —<br>и отпускает без срыва.</div>'
       f'<div id="mgr" style="position:absolute;left:40px;top:700px">{grade("масштаб")}</div>')+src('MARSI в ОРИТ ≈16% — метаанализ, J Wound Care 2024; консенсус MARSI — McNichol et al., 2013. Price P. et al., Int Wound J 2008.'))
intro('s3',S[3]); t=S[3]+1.0
js+=f'const a16={{v:0}},a40={{v:0}};tl.to(a16,{{v:16,duration:1.2,ease:"power2.out",onUpdate:()=>{{document.getElementById("c16").textContent="≈"+Math.round(a16.v)}}}},{t}).to(a40,{{v:40,duration:1.2,ease:"power2.out",onUpdate:()=>{{document.getElementById("c40").textContent=Math.round(a40.v)}}}},{t+.4});'
js+=f'tl.from("#mtx",{{opacity:0,y:20,duration:.5}},{t+2.2}).from("#mgr",{{opacity:0,duration:.4}},{t+3.2});'
ev+=[(S[3],sfx.whoosh(.6,.2))]+[(t+k*.12,sfx.click(.15)) for k in range(10)]
# 4 давление
pp=lambda n,idp: f'<div style="position:relative;width:{10*36}px;height:{10*36}px">{people(n,size=30,gap=6,idp=idp)}</div>'
body+=sec('s4',S[4],D(4),head('3 / 4','🛡️ ЗАЩИТА ОТ ДАВЛЕНИЯ',f'Пена на крестце:<br>{T("пролежней ≈ вдвое меньше")}')+
  card(70,640,940,840,f'<div style="position:absolute;left:36px;top:34px">{kicker("ОБЗОР COCHRANE · 18 ИССЛЕДОВАНИЙ · 5903 ПАЦ.")}</div>'
       f'<div id="fo" style="position:absolute;left:0;top:76px;width:940px;height:250px">{forest(940,idp="ff")}</div>'
       f'<div id="g1" style="position:absolute;left:60px;top:340px">{pp(10,"pa")}<div style="margin-top:10px;{F};font-weight:800;font-size:30px;color:{INK}">Без повязки: <span style="color:{MUTED}">10 из 100*</span></div></div>'
       f'<div id="g2" style="position:absolute;left:520px;top:340px">{pp(5,"pb")}<div style="margin-top:10px;{F};font-weight:800;font-size:30px;color:{INK}">С пеной: <span style="color:{ORANGE}">≈5 (3–8)</span></div></div>'
       f'<div id="pgr" style="position:absolute;right:30px;top:290px">{grade("низкая")}</div>')+
  src('Patton D. et al., Cochrane Database Syst Rev 2024 (CD009362.pub4): RR 0,50 (95% ДИ 0,33–0,77), низкая достоверность. *Иллюстрация при исходном риске 10 из 100. Повязка не заменяет смену положения тела.'))
intro('s4',S[4]); t=S[4]+1.0
js+=f'tl.from("#ffci",{{scaleX:0,duration:.8,ease:"power2.out"}},{t}).from("#ffpt",{{scale:0,duration:.4,ease:"back.out(2.5)"}},{t+.6}).from("#fflb",{{opacity:0,duration:.4}},{t+.9});'
js+=f'tl.from("#g1,#g2",{{opacity:0,y:30,duration:.5,stagger:.2}},{t+2.0}).from(".pab,.pbb",{{scale:0,duration:.3,stagger:.06,ease:"back.out(2)"}},{t+2.8}).from("#pgr",{{opacity:0,duration:.4}},{t+4.2});'
ev+=[(S[4],sfx.whoosh(.6,.2)),(t+.6,sfx.chime(659,.14,2))]+[(t+2.8+k*.06,sfx.click(.12)) for k in range(15)]
# 5 рубец
steps=[('1','Рана зажила','швы сняты'),('2','Каждый день','большую часть суток*'),('3','Месяцы','обычно ≥ 2 месяцев*')]
stp=''.join(f'<div class="st" style="position:absolute;left:{40+k*300}px;top:120px;width:270px"><div style="width:86px;height:86px;border-radius:50%;background:{YAF};color:#fff;{F};font-weight:900;font-size:48px;line-height:86px;text-align:center">{n}</div>'
            f'<div style="margin-top:22px;{F};font-weight:900;font-size:40px;line-height:1.1;color:{INK}">{a}</div><div style="margin-top:10px;font-size:28px;color:{MUTED}">{c}</div></div>' for k,(n,a,c) in enumerate(steps))
body+=sec('s5',S[5],D(5),head('4 / 4','✨ УХОД ЗА РУБЦОМ',f'Силиконовая пластина —<br>{T("первая линия ухода")}')+
  card(70,640,940,820,f'<div style="position:absolute;left:36px;top:36px">{kicker("КАК НОСИТЬ")}</div>{stp}'
       f'<div id="stx" style="position:absolute;left:40px;right:40px;top:480px;{F};font-weight:700;font-size:38px;line-height:1.3;color:{INK}">Пластина держит влагу в рубце<br>и мягко прижимает его —<br>рубец становится <span style="color:{ORANGE}">мягче и бледнее</span>.</div>'
       f'<div id="sgr" style="position:absolute;left:40px;top:700px">{grade("рекомендация")}</div>')+src('Meaume S. et al., Wound Repair Regen 2014. *Режим — по инструкции и рекомендации врача. Результат индивидуален.'))
intro('s5',S[5]); t=S[5]+1.0
js+=f'tl.from("#s5 .st",{{opacity:0,y:30,duration:.4,stagger:.4}},{t}).from("#stx",{{opacity:0,y:20,duration:.5}},{t+1.6}).from("#sgr",{{opacity:0,duration:.4}},{t+2.4});'
ev+=[(S[5],sfx.whoosh(.6,.2))]+[(t+k*.4,sfx.click(.3)) for k in range(3)]
# 6 честно
nots=''.join(f'<div class="nn" style="margin-top:18px;{F};font-weight:800;font-size:40px;color:{INK}"><span style="color:#C0392B">✕</span>&nbsp; {x}</div>' for x in ['не лечит инфекцию','не заменяет осмотр врача','не заменяет переворачивание'])
flags=''.join(f'<div class="fl" style="margin-top:16px;{F};font-weight:800;font-size:38px;color:{INK}"><span style="display:inline-block;width:46px;height:46px;border-radius:50%;background:#C0392B;color:#fff;text-align:center;line-height:46px;font-size:30px">!</span>&nbsp; {x}</div>' for x in RED_FLAGS)
body+=sec('s6',S[6],D(6),head('ЧЕСТНО',' ',f'Чего повязка<br>{T("НЕ делает")}')+
  card(70,600,940,340,f'<div style="position:absolute;left:40px;top:40px">{nots}</div>')+
  card(70,980,940,500,f'<div style="position:absolute;left:40px;top:34px">{kicker("СРАЗУ К ВРАЧУ, ЕСЛИ","",0,"#C0392B")}</div><div style="position:absolute;left:40px;top:70px">{flags}</div>'))
intro('s6',S[6]); js+=f'tl.from("#s6 .nn",{{opacity:0,x:-30,duration:.3,stagger:.25}},{S[6]+.8}).from("#s6 .fl",{{opacity:0,x:-30,duration:.3,stagger:.25}},{S[6]+1.9});'
ev+=[(S[6],sfx.whoosh(.6,.2))]+[(S[6]+1.9+k*.25,sfx.click(.2)) for k in range(4)]
# 7 пять вопросов
qs=''.join(f'<div class="qq" style="display:flex;align-items:flex-start;margin-top:{0 if k==0 else 30}px"><div style="flex:0 0 58px;height:58px;border-radius:14px;border:5px solid {YAF};margin-right:26px;position:relative"><div class="ck" style="position:absolute;left:6px;top:-12px;{F};font-weight:900;font-size:56px;color:{ORANGE}">✓</div></div><div style="{F};font-weight:800;font-size:38px;line-height:1.2;color:{INK}">{q}</div></div>' for k,q in enumerate(QUESTIONS))
body+=sec('s7',S[7],D(7),head('ЗАКРЫВАЕМ ПРОБЕЛ','ПАЦИЕНТ ЧАСТО НЕ ЗНАЕТ, ЧТО СПРОСИТЬ',f'5 вопросов врачу<br>{T("при выписке")}')+
  card(70,620,940,860,f'<div style="position:absolute;left:44px;right:44px;top:50px">{qs}</div>'))
intro('s7',S[7]); js+=f'tl.from("#s7 .qq",{{opacity:0,x:-30,duration:.35,stagger:.55}},{S[7]+.8}).from("#s7 .ck",{{scale:0,opacity:0,duration:.25,stagger:.55,ease:"back.out(3)"}},{S[7]+1.3});'
ev+=[(S[7],sfx.whoosh(.6,.2))]+[(S[7]+1.3+k*.55,sfx.click(.35)) for k in range(5)]
# 8 финал
body+=sec('s8',S[8],D(8),f'<div id="z0" style="position:absolute;left:60px;right:60px;top:430px;text-align:center;{F};font-weight:900;font-size:80px;line-height:1.05;letter-spacing:-0.02em;color:{INK}">Правильная повязка —<br>{T("часть лечения,")}<br>а не просто пластырь.</div>'
  f'<div id="z1" style="position:absolute;left:0;right:0;top:860px;text-align:center">{logo(120,ORANGE,True)}</div>'
  f'<div id="z2" style="position:absolute;left:80px;right:80px;top:1100px;text-align:center;{F};font-weight:700;font-size:40px;line-height:1.35;color:{INK}">📌 Сохраните и покажите на приёме.<br><span style="color:{ORANGE}">Напишите «ПАМЯТКА» — пришлём PDF</span><br>с вопросами и уходом.</div>'
  f'<div style="position:absolute;left:80px;right:80px;top:1480px;text-align:center;font-size:22px;line-height:1.5;color:{MUTED}">Не является медицинской консультацией. Медицинские изделия.<br>Применение — по назначению специалиста.</div>')
js+=f'tl.from("#z0",{{opacity:0,y:30,duration:.5}},{S[8]+.1}).from("#z1",{{opacity:0,duration:.5}},{S[8]+.8}).from("#z2",{{opacity:0,y:20,duration:.5}},{S[8]+1.3});'
ev+=[(S[8],sfx.whoosh(.9,.3)),(S[8]+.8,sfx.boom(.5)),(S[8]+1.0,sfx.chime(659,.18,3))]
chk=(S[4]+6,2.5,S[1]+2.5,S[2]+6,S[3]+5,S[4]+6,S[5]+4.5,S[6]+3.5,S[7]+5,S[8]+3)
shots=style_reel('nauka_uhoda_reel',DUR,body,js,'Наука ухода',ev,pad=(110,164.8,220,277.2),pad_amp=.035,check=chk,bg='#C9D3E3',outdir=OUT)
strip(shots,'kp/chk_nauka.jpg',3000); print('ok',DUR)
