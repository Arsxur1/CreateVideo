from kp import *
from peach_lib import plaster
import random
rnd = random.Random(3)
fib = ''.join(f'<path d="M{rnd.randint(0,400)} {rnd.randint(0,560)} q{rnd.randint(-40,40)} {rnd.randint(-20,20)} {rnd.randint(30,120)} {rnd.randint(-10,10)}" stroke="rgba(190,170,140,.35)" stroke-width="1.2" fill="none"/>' for _ in range(60))
def paper(x,y,w,h,rot,id,torn=False):
    hole = ''
    if torn:
        hole=f'<div id="{id}h" style="position:absolute;left:8%;top:22%;width:80%;height:30%;clip-path:polygon(2% 40%,14% 8%,28% 30%,42% 2%,58% 26%,72% 0%,88% 24%,99% 46%,90% 70%,97% 96%,76% 80%,58% 100%,40% 78%,22% 98%,6% 76%);background:#BFCBDD;box-shadow:inset 0 0 0 3px rgba(200,180,150,.8)"></div>'
    return f'''<div id="{id}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;transform:rotate({rot}deg);filter:drop-shadow(0 20px 26px rgba(40,50,80,.25))">
<svg viewBox="0 0 400 560" preserveAspectRatio="none" style="position:absolute;inset:0;width:100%;height:100%"><rect width="400" height="560" rx="10" fill="rgba(255,252,244,.82)"/>{fib}</svg>{hole}</div>'''
def mesh(x,y,w,h,rot,id,op=1):
    return f'''<div id="{id}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;transform:rotate({rot}deg);opacity:{op};border-radius:14px;background-color:rgba(250,235,215,.55);background-image:radial-gradient(circle,rgba(191,203,221,1) 5px,transparent 5.6px);background-size:22px 22px;box-shadow:0 10px 20px -8px rgba(90,60,30,.35),inset 0 0 0 2px rgba(230,200,165,.9)"></div>'''
STG = f'<div style="position:absolute;left:40px;top:430px;width:1000px;height:900px;border-radius:40px;background:{STAGE}"></div>'
# ---------- E1 Reel (20 c)
body = clip('r1',0,11.2, STG + paper(130,530,380,560,-4,'pl',torn=True) + paper(570,530,380,560,4,'pr') + plaster(150,700,330,110,-10,'tp') + mesh(610,660,300,220,6,'tm') +
  f'<div id="c1" class="cap" style="top:170px;font-size:76px">Эта бумага —<br>как кожа <span style="color:{ORANGE}">ребёнка-бабочки.</span></div>'
  f'<div id="c2" class="cap" style="top:170px;font-size:70px;opacity:0">Обычный пластырь<br>и <span style="color:{ORANGE}">силиконовая сетка.</span></div>'
  f'<div id="c3" class="cap" style="top:190px;font-size:76px;opacity:0">Снимаем пластырь…</div>'
  f'<div id="c4" class="cap" style="top:190px;font-size:76px;opacity:0">Снимаем <span style="color:{ORANGE}">силикон.</span></div>'
  f'<div id="lL" style="position:absolute;left:100px;top:1360px;width:440px;text-align:center;font-size:32px;font-weight:700;color:{RED};opacity:0">Обычный пластырь</div>'
  f'<div id="lR" style="position:absolute;left:560px;top:1360px;width:420px;text-align:center;font-size:32px;font-weight:700;color:{ORANGE};opacity:0">Силикон — лист цел</div>') + \
 clip('r2',11.2,4.4, f'''<div style="position:absolute;left:140px;top:420px">{svg("dermatology",800,4.5,idp="bf")}</div>
<div id="c5" class="cap" style="top:180px;font-size:72px">Для детей-бабочек<br>это не эксперимент.</div>
<div id="c6" class="cap" style="top:1300px;font-size:84px;color:{ORANGE}">Это каждая<br>перевязка.</div>''') + \
 clip('r3',15.6,4.4, f'''<div id="d1" class="cap" style="top:300px;font-size:120px;color:{ORANGE}">25–31<br>октября</div>
<div id="d2" class="cap" style="top:620px;font-size:58px">Неделя осведомлённости<br>о буллёзном эпидермолизе</div>
<div id="d3" class="sub" style="top:860px;font-size:36px;color:{INK}">Расскажите о детях-бабочках —<br>поделитесь этим видео 🦋</div>
<div id="d4" class="sub" style="top:1040px;font-size:28px">[ссылка на фонд-партнёр]</div>
<div id="d5" style="position:absolute;left:0;right:0;top:1200px;text-align:center">{logo(90)}</div>{wave(1080,1920,150)}''')
js = '''tl.from(["#pl","#pr"],{opacity:0,y:60,duration:.6,stagger:.15},.05).from("#c1",{opacity:0,y:30,duration:.5},.2);
tl.to("#c1",{opacity:0,duration:.3},2.4).to("#c2",{opacity:1,duration:.3},2.5);
tl.from("#tp",{y:-700,rotation:-50,opacity:0,duration:.55,ease:"power3.out"},2.7).from("#tm",{y:-700,rotation:40,opacity:0,duration:.55,ease:"power3.out"},3.2);
tl.to("#c2",{opacity:0,duration:.3},4.8).to("#c3",{opacity:1,duration:.3},4.9);
tl.to("#tp",{y:-560,x:-60,rotation:-45,duration:.6,ease:"power3.in"},5.4).to("#tp",{opacity:0,duration:.2},6.0).from("#plh",{opacity:0,duration:.01},5.75);
tl.fromTo("#pl",{x:0},{x:10,duration:.05,repeat:5,yoyo:true},5.75).to("#lL",{opacity:1,duration:.4},6.4);
tl.to("#c3",{opacity:0,duration:.3},7.8).to("#c4",{opacity:1,duration:.3},7.9);
tl.to("#tm",{y:-560,rotation:-6,duration:1.1,ease:"power2.inOut"},8.3).to("#tm",{opacity:0,duration:.3},9.3).to("#lR",{opacity:1,duration:.4},9.5);
tl.fromTo("#bf .lni",{strokeDasharray:1,strokeDashoffset:1},{strokeDashoffset:0,duration:1.6,stagger:.1,ease:"power2.inOut"},11.3);
tl.fromTo("#bf .lna",{strokeDasharray:1,strokeDashoffset:1},{strokeDashoffset:0,duration:1.3,ease:"power2.inOut"},11.6);
tl.to("#bf",{y:-40,duration:1.2,repeat:1,yoyo:true,ease:"sine.inOut"},12.9);
tl.from("#c5",{opacity:0,y:30,duration:.5},11.3).from("#c6",{opacity:0,y:30,duration:.5},12.9);
tl.from("#d1",{opacity:0,scale:.9,duration:.5},15.7).from("#d2",{opacity:0,duration:.5},16.2).from("#d3",{opacity:0,duration:.5},16.8).from(["#d4","#d5"],{opacity:0,duration:.5},17.4);'''
shots = reel('e1_test_risovaya_bumaga', 20, body, js, 'Тест на рисовой бумаге', check=(4.4, 1.5, 7.0, 10.5, 14.0, 18.5))
strip(shots,'kp/chk_e1.jpg')

# ---------- E2 Фото-манифест: бабочка из силиконовой сетки
UW="M300 230 C230 110 80 110 92 235 C104 330 225 320 300 292 Z"; LW="M300 300 C225 330 140 385 172 455 C202 515 272 455 300 382 Z"
def mir(d):
    from lineart import mirror; return mirror(d)
wings = ''.join(f'<path d="{d}" fill="url(#mp)" stroke="#E8B486" stroke-width="3"/>' for d in [UW,mir(UW),LW,mir(LW)])
bfly = f'''<svg viewBox="40 80 520 460" width="820" height="725"><defs>
<pattern id="mp" width="18" height="18" patternUnits="userSpaceOnUse"><rect width="18" height="18" fill="rgba(248,222,190,.9)"/><circle cx="9" cy="9" r="4.2" fill="rgba(255,255,255,.95)"/></pattern>
<radialGradient id="glow" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="#fff" stop-opacity=".9"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient></defs>
<ellipse cx="300" cy="320" rx="260" ry="220" fill="url(#glow)"/>{wings}
<path d="M300 186 L300 440" stroke="#C98E5E" stroke-width="7" stroke-linecap="round"/><path d="M300 190 C290 144 270 122 252 112 M300 190 C310 144 330 122 348 112" stroke="#C98E5E" stroke-width="3" fill="none"/></svg>'''
M=[f'''<div class="fill" style="background:{STAGE}"></div>{header("Кожа помнит · Дерматология","")}
<div style="position:absolute;left:130px;top:150px;filter:drop-shadow(0 30px 40px rgba(60,70,110,.35))">{bfly}</div>
<div style="position:absolute;left:80px;right:80px;top:850px"><h1 class="h" style="font-size:72px;color:{INK}"><span>Есть дети, чья кожа хрупкая,</span><span style="color:#fff">как крыло бабочки.</span></h1>
<div style="margin-top:24px;font-size:28px;font-weight:600;color:{INK}">25–31 октября · Неделя осведомлённости о буллёзном эпидермолизе</div></div>
<div style="position:absolute;left:80px;bottom:60px">{logo(50)}</div><div style="position:absolute;right:80px;bottom:70px;font-size:20px;color:#4a5568;max-width:430px;text-align:right">Бабочка вырезана из силиконового контактного слоя</div>''']
carousel('e2_foto_manifest_babochka', M, 'Крыло бабочки')

# ---------- E3 Просветительская карусель (5)
L='Дерматология'
E=[slide_frame(L,'1/5',f'''<div style="position:absolute;left:140px;top:120px">{svg("dermatology",800,4.5)}</div>
<div style="position:absolute;left:80px;right:80px;top:860px"><h1 class="h" style="font-size:92px"><span>Кто такие</span><span style="color:{ORANGE}">дети-бабочки?</span></h1></div>'''),
slide_frame(L,'2/5',f'''<div style="position:absolute;left:80px;right:80px;top:200px"><div style="font-size:28px;font-weight:700;color:{ORANGE}">◆ БУЛЛЁЗНЫЙ ЭПИДЕРМОЛИЗ</div>
<h2 class="h" style="font-size:68px;margin-top:20px">Редкое генетическое заболевание: кожа образует пузыри и раны от малейшего трения.</h2>
<p class="body" style="margin-top:36px;font-size:36px">Объятие, шов на одежде, неудачный пластырь — то, чего мы не замечаем, для них может стать новой раной.</p></div><div style="position:absolute;left:620px;top:860px;opacity:.25">{svg("dermatology",380,4)}</div>'''),
slide_frame(L,'3/5',f'''<div style="position:absolute;left:80px;right:80px;top:200px"><h2 class="h" style="font-size:72px"><span>Перевязки —</span><span style="color:{ORANGE}">часть каждого дня.</span></h2>
<p class="body" style="margin-top:36px;font-size:36px">Поэтому особенно важно, что касается кожи и как это снимается. Каждое снятие — потенциальная новая рана.</p></div>
<div style="position:absolute;left:300px;top:700px;opacity:.9">{svg("dermatology",480,4.5)}</div>'''),
slide_frame(L,'4/5',f'''<div style="position:absolute;left:80px;right:80px;top:200px"><div style="font-size:28px;font-weight:700;color:{ORANGE}">◆ ЧТО РЕКОМЕНДУЮТ</div>
<h2 class="h" style="font-size:66px;margin-top:20px">Нелипкие повязки на силиконовой основе — вместо обычного пластыря.</h2>
<p class="body" style="margin-top:30px;font-size:34px">Обычные клейкие повязки могут повредить кожу при БЭ. Выбор всегда индивидуален — его делают семья и медицинская команда.</p>
<p style="margin-top:24px;font-size:20px;color:#999">Great Ormond Street Hospital — «EB: blister management and dressings»; DEBRA — «Choose products»</p></div>
<div style="position:absolute;left:250px;top:880px">{mesh(0,0,580,260,-3,"mz")}</div>'''),
slide_frame(L,'5/5',f'''<div style="position:absolute;left:80px;right:80px;top:200px"><h2 class="h" style="font-size:80px"><span>Как помочь</span><span style="color:{ORANGE}">прямо сейчас</span></h2>
<div style="margin-top:44px;font-size:36px;line-height:1.7">🦋 Поделитесь этим постом 25–31 октября<br>🤝 Узнайте о фонде: [фонд-партнёр]<br>💬 Напишите слова поддержки в комментариях</div>
<p class="body" style="margin-top:40px;font-size:28px;color:#555">Yafho Silicone Wound Contact Layer · Silicone Nonwoven — для самой хрупкой кожи. Отделениям дерматологии — образцы в директ.</p></div><div style="position:absolute;left:330px;top:800px;transform:scale(.5);transform-origin:top left;filter:drop-shadow(0 20px 30px rgba(60,70,110,.3))">{bfly}</div>''')]
carousel('e3_kto_takie_deti_babochki', E, 'Кто такие дети-бабочки')
print('done')
