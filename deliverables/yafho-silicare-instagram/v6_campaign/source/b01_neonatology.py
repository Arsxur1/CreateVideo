from kp import *
from peach_lib import plaster

def petal(x, y, w, h, rot, id, torn=False):
    hole = ''
    if torn:
        hole = f'''<div id="{id}h" style="position:absolute;left:20%;top:30%;width:58%;height:20%;clip-path:polygon(4% 30%,18% 6%,34% 22%,50% 0%,66% 20%,84% 4%,98% 32%,90% 64%,96% 92%,74% 80%,54% 100%,36% 82%,16% 96%,2% 70%);background:#C3CEE0;box-shadow:inset 0 0 12px rgba(150,30,60,.6)"></div>'''
    P = "M50 100 C22 88 3 60 5 30 C7 10 24 1 38 7 C44 10 48 14 50 19 C52 14 56 10 62 7 C76 1 93 10 95 30 C97 60 78 88 50 100 Z"
    return f'''<div id="{id}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;transform:rotate({rot}deg);filter:drop-shadow(0 26px 30px rgba(120,20,50,.35))">
<svg viewBox="0 0 100 100" preserveAspectRatio="none" style="position:absolute;inset:0;width:100%;height:100%"><defs><radialGradient id="g{id}" cx="50%" cy="85%" r="90%"><stop offset="0" stop-color="#FBD9E1"/><stop offset=".45" stop-color="#F29CB2"/><stop offset="1" stop-color="#D9577B"/></radialGradient></defs>
<path d="{P}" fill="url(#g{id})"/><path d="M50 98 C50 70 49 45 50 22 M50 72 C42 58 32 48 22 34 M50 62 C58 50 68 40 78 28 M50 46 C45 38 40 30 34 20 M50 44 C55 36 60 28 66 20" stroke="#fff" stroke-opacity=".45" stroke-width=".7" fill="none"/></svg>
<div style="position:absolute;left:18%;top:10%;width:34%;height:16%;border-radius:50%;background:radial-gradient(closest-side,rgba(255,255,255,.6),transparent);filter:blur(4px)"></div>{hole}</div>'''

def mini_sili(x,y,s,rot,id):
    return f'<div id="{id}" style="position:absolute;left:{x}px;top:{y}px;width:{s}px;height:{s*0.62:.0f}px;transform:rotate({rot}deg);border-radius:18px;background:linear-gradient(145deg,rgba(246,214,180,.95),rgba(232,186,140,.92));box-shadow:0 14px 24px -12px rgba(90,50,20,.45)"><div style="position:absolute;inset:18%;border-radius:10px;background:rgba(252,232,206,.9)"></div></div>'

def shreds(x,y,id):
    bits=''.join(f'<div style="position:absolute;left:{a}px;top:{b}px;width:{c}px;height:{d}px;border-radius:40% 60% 50% 45%;background:linear-gradient(135deg,#F19BB1,#E06C8C)"></div>' for a,b,c,d in [(30,30,46,22),(100,22,30,26),(160,34,52,20),(230,26,26,24)])
    return f'<div id="{id}" style="position:absolute;left:{x}px;top:{y}px;width:330px;height:100px;transform:rotate(-4deg)"><div style="position:absolute;inset:0;border-radius:50px;background:linear-gradient(180deg,#FFFFFF,#E4E7EA);box-shadow:0 10px 24px rgba(30,40,60,.3)"></div>{bits}</div>'

# ---------- B1 Reel «Лепесток» (16 c)
STG = f'<div style="position:absolute;left:40px;top:430px;width:1000px;height:900px;border-radius:40px;background:{STAGE}"></div>'
petals = petal(150,560,360,520,-8,'pL',torn=True) + petal(570,560,360,520,8,'pR')
body = clip('n1',0,2.4, STG + petal(330,540,420,600,0,'p0') + f'<div id="h1" class="cap" style="top:170px;font-size:84px">Её кожа тоньше<br><span style="color:{ORANGE}">этого лепестка.</span></div>') + \
clip('n2',2.4,2.8, f'<div style="position:absolute;left:140px;top:380px">{svg("neonatology",800,4,idp="ft")}</div><div id="h2" class="cap" style="top:170px;font-size:68px">Датчики, зонды, катетеры —<br><span style="color:{ORANGE}">всё крепят к её коже.</span></div><div id="h2b" class="sub" style="top:1300px;font-size:34px">И снимают. Снова и снова.</div>') + \
clip('n3',5.2,7.4, STG + petals + plaster(200,770,250,86,-14,'tp') + mini_sili(640,760,230,10,'ts') + shreds(80,1420,'sh') +
     f'<div id="h3" class="cap" style="top:200px;font-size:72px">Проверим<br>на лепестках.</div><div id="h4" class="cap" style="top:200px;font-size:72px;opacity:0">Обычный пластырь…</div><div id="h5" class="cap" style="top:200px;font-size:72px;opacity:0">…и <span style="color:{ORANGE}">силикон.</span></div>'
     f'<div id="lbL" style="position:absolute;left:120px;top:1150px;width:420px;text-align:center;font-weight:700;font-size:30px;color:{RED};opacity:0">Обычный пластырь</div><div id="lbR" style="position:absolute;left:560px;top:1150px;width:400px;text-align:center;font-weight:700;font-size:30px;color:{ORANGE};opacity:0">Силикон</div>') + \
clip('n4',12.6,3.4, f'''<div id="e1" class="cap" style="top:330px;font-size:84px">Её кожа помнит<br>первое прикосновение.</div>
<div id="e2" class="cap" style="top:560px;font-size:84px;color:{ORANGE}">Пусть оно будет мягким.</div>
<div style="position:absolute;left:290px;top:760px" id="e3">{svg("neonatology",500,4)}</div>
<div id="e4" style="position:absolute;left:0;right:0;top:1330px;text-align:center">{logo(90)}</div>
<div class="sub" style="top:1500px;font-size:24px;color:#999">{FOOT}</div>{wave(1080,1920,150)}''')
js = '''tl.from("#p0",{scale:.6,opacity:0,rotation:-20,duration:.8,ease:"back.out(1.5)"},.05).from("#h1",{opacity:0,y:30,duration:.5},.2);
tl.fromTo("#ft .lni",{strokeDasharray:1,strokeDashoffset:1},{strokeDashoffset:0,duration:1.4,stagger:.05,ease:"power2.inOut"},2.45);
tl.fromTo("#ft .lna",{opacity:0},{opacity:1,duration:.4},3.6);
tl.from("#h2",{opacity:0,y:30,duration:.5},2.5).from("#h2b",{opacity:0,duration:.5},3.8);
tl.from(["#pL","#pR"],{y:80,opacity:0,duration:.6,stagger:.15},5.25).from("#h3",{opacity:0,duration:.4},5.3);
tl.from("#tp",{y:-600,rotation:-60,opacity:0,duration:.55,ease:"power3.out"},5.9).from("#ts",{y:-600,rotation:40,opacity:0,duration:.55,ease:"power3.out"},6.3);
tl.to("#h3",{opacity:0,duration:.3},7.2).to("#h4",{opacity:1,duration:.3},7.3);
tl.from("#pLh",{opacity:0,duration:.01},8.05).to("#tp",{y:-560,x:-80,rotation:-50,duration:.6,ease:"power3.in"},7.7).to("#tp",{opacity:0,duration:.2},8.3);
tl.fromTo("#pL",{x:0},{x:10,duration:.05,repeat:5,yoyo:true},8.05);
tl.from("#sh",{opacity:0,y:40,duration:.5},8.5);
tl.to("#h4",{opacity:0,duration:.3},9.7).to("#h5",{opacity:1,duration:.3},9.8);
tl.to("#ts",{y:-560,rotation:-8,duration:1.1,ease:"power2.inOut"},10.1).to("#ts",{opacity:0,duration:.3},11.1);
tl.to(["#lbL","#lbR"],{opacity:1,duration:.4},11.4).to("#sh",{opacity:0,duration:.3},11.6);
tl.from("#e1",{opacity:0,y:30,duration:.5},12.7).from("#e2",{opacity:0,y:30,duration:.5},13.2).from("#e3",{opacity:0,duration:.6},13.6).from("#e4",{opacity:0,duration:.5},14.1);'''
shots = reel('b1_lepestok', 16, body, js, 'Лепесток', check=(6.9, 1.2, 3.9, 8.9, 11.8, 15.0))
strip(shots, 'kp/chk_b1.jpg')

# ---------- B2 Карусель для медсестёр ОРИТН (4)
def bricks(rows, w=380, bw=44, bh=16, gap=4, col='#F2C9AE'):
    out=[]; n=w//(bw+gap)
    for r in range(rows):
        off = 0 if r%2==0 else -(bw//2)
        for c in range(n+1):
            out.append(f'<div style="position:absolute;left:{off+c*(bw+gap)}px;top:{r*(bh+gap)}px;width:{bw}px;height:{bh}px;border-radius:4px;background:{col}"></div>')
    return f'<div style="position:relative;width:{w}px;height:{rows*(bh+gap)}px;overflow:hidden">{"".join(out)}</div>'
L='Неонатология'
C=[]
C.append(slide_frame(L,'1/4',f'''<div style="position:absolute;left:240px;top:120px">{svg("neonatology",600,4.5)}</div>
<div style="position:absolute;left:80px;right:80px;top:760px"><h1 class="h" style="font-size:96px"><span>Её кожа —</span><span style="color:{ORANGE}">2–3 слоя клеток.</span><span>Ваша — 10–20.</span></h1></div>'''))
C.append(slide_frame(L,'2/4',f'''<div style="position:absolute;left:80px;right:80px;top:170px"><h2 class="h" style="font-size:62px">Роговой слой — защитная «кладка» кожи</h2>
<div style="display:flex;gap:60px;margin-top:70px;align-items:flex-end">
<div><div style="height:330px;display:flex;align-items:flex-end">{bricks(15,400,col='#E9C2A4')}</div><div style="font-size:30px;font-weight:700;margin-top:20px">Взрослый</div><div style="font-size:26px;color:#666">10–20 слоёв</div></div>
<div><div style="height:330px;display:flex;align-items:flex-end">{bricks(2,400,col='#F4A9BB')}</div><div style="font-size:30px;font-weight:700;margin-top:20px;color:{ORANGE}">Недоношенный &lt;30 нед.</div><div style="font-size:26px;color:#666">2–3 слоя</div></div></div>
<p class="body" style="margin-top:60px;font-size:34px">Когда клей снимает «верхний ряд» у взрослого, остаётся ещё десяток. У самых маленьких — почти ничего.</p>
<p style="margin-top:20px;font-size:20px;color:#999">Цитируется в неонатальных обзорах по уходу за кожей (Lund et al.); проверить по первоисточнику.</p></div>'''))
STEPS=[('Медленно и низко','Тяните фиксацию почти параллельно коже, а не вверх.'),('Поддерживайте кожу','Пальцем у линии отклеивания, двигаясь вместе с ней.'),('Помогите растворителем','Силиконовые средства для удаления клея снижают тягу.'),('Выбирайте мягкий контакт','Силиконовые фиксации и повязки там, где это допустимо по показаниям.')]
rows=''.join(f'<div style="display:flex;gap:26px;padding:26px 0;border-bottom:2px solid #EEE"><div style="font-family:Inter Display;font-size:56px;color:{ORANGE};font-weight:600;width:70px">{i+1}</div><div><div style="font-size:38px;font-weight:700">{a}</div><div style="font-size:28px;color:#555;margin-top:6px">{b}</div></div></div>' for i,(a,b) in enumerate(STEPS))
C.append(slide_frame(L,'3/4',f'''<div style="position:absolute;left:80px;right:80px;top:160px"><h2 class="h" style="font-size:64px">Как снимать бережнее</h2><div style="margin-top:30px">{rows}</div>
<p style="margin-top:24px;font-size:20px;color:#999">По консенсусу по MARSI (McNichol et al., J WOCN 2013; обновление 2024). Протокол отделения — главный.</p></div>'''))
C.append(slide_frame(L,'4/4',f'''<div style="position:absolute;left:80px;right:80px;top:220px"><h2 class="h" style="font-size:80px"><span>Вы знаете это</span><span style="color:{ORANGE}">лучше всех.</span></h2>
<p class="body" style="margin-top:40px;font-size:38px">Медсёстры ОРИТН, как вы снимаете фиксацию у самых маленьких? Поделитесь в комментариях — соберём ваши лайфхаки в отдельный пост 👇</p>
<p class="body" style="margin-top:30px;font-size:30px;color:#555">🏥 Отделениям — образцы силиконовых решений Yafho по запросу.</p></div>
<div style="position:absolute;left:380px;top:860px">{svg("neonatology",320,5)}</div>'''))
carousel('b2_oritn_2_sloya', C, 'Её кожа — 2–3 слоя')
print('done')
