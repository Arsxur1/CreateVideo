from peach_lib import peach, damage, plaster
from gen_lib import page
from brand import *

def scene(cx=540, cy=900, d=700, dmg=True, pl=True, si=True, sfx=''):
    out = peach(cx, cy, d, 'pch'+sfx)
    if dmg: out += f'<div id="dmgwrap{sfx}" style="position:absolute;left:{cx-325}px;top:{cy-110}px;transform:rotate(-20deg)">{damage(0,0,280,130,"dmg"+sfx)}</div>'
    if pl:  out += plaster(cx-330, cy-100, 300, 110, -20, 'pl'+sfx)
    if si:  out += f'<div id="si{sfx}" style="position:absolute;left:{cx+50}px;top:{cy-140}px;width:260px;height:260px;transform:rotate(10deg)">{sili(0,0,260)}</div>'
    return out

def stage(x, y, w, h, r=36):
    return f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;border-radius:{r}px;background:{STAGE}"></div>'

# ============ REEL 20s (1080x1920)
cap = lambda id, top, html, size=84, color=INK, extra='': f'<div id="{id}" style="position:absolute;left:70px;right:70px;top:{top}px;text-align:center;font-family:Inter Display;font-weight:800;letter-spacing:-0.03em;line-height:1.06;font-size:{size}px;color:{color};{extra}">{html}</div>'
clips = []
def clip(id, s, d, inner, track=2):
    clips.append(f'<section id="{id}" class="clip" data-start="{s}" data-duration="{d}" data-track-index="{track}">{inner}</section>')

clips.append(f'''<section id="stg" class="clip" data-start="0" data-duration="15.2" data-track-index="1"><div class="fill" style="background:#fff"></div>
<div style="position:absolute;left:64px;top:70px">{logo(64)}</div>
{stage(40,470,1000,880)}{scene(540,910,700)}
<div id="under" style="position:absolute;left:110px;top:1400px;width:440px;height:150px;opacity:0">{plaster(0,0,420,140,-6,"plu",under=True)}<div class="lab" style="position:absolute;left:0;top:170px;width:700px;white-space:nowrap;font-size:26px;color:{RED}">кожица осталась на пластыре</div></div>
<div id="okring" class="ring" style="left:595px;top:735px;width:330px;height:330px;color:{BLUE};border-width:4px;opacity:0"></div>
<div id="labL" style="position:absolute;left:70px;top:1380px;width:440px;text-align:center;opacity:0;font-weight:700;font-size:32px;color:{RED}">Обычный пластырь</div>
<div id="labR" style="position:absolute;left:570px;top:1380px;width:440px;text-align:center;opacity:0;font-weight:700;font-size:32px;color:{ORANGE}">Sili-Care</div>
{wave(1080,1920,170)}</section>''', )
clips[-1] = clips[-1]
clip('c1', 0, 2.2, cap('c1t', 230, f'Этот персик —<br>кожа вашей <span style="color:{ORANGE}">бабушки.</span>', 86))
clip('c2', 2.2, 2.0, cap('c2t', 250, f'Клеим обычный пластырь<br>и <span style="color:{ORANGE}">Sili-Care.</span>', 72))
clip('c3', 4.2, 2.0, cap('c3t', 250, 'Ждём сутки.<br><span style="font-size:54px;color:#7A7A7A">Как в больнице.</span>', 80))
clip('c4', 6.2, 3.0, cap('c4t', 270, 'Снимаем пластырь…', 84))
clip('c5', 9.2, 3.0, cap('c5t', 270, f'Снимаем <span style="color:{ORANGE}">Sili-Care.</span>', 84))
clip('c6', 12.2, 3.0, cap('c6t', 230, 'Пожилая кожа<br>такая же тонкая.', 78) + cap('c6b', 1500, 'Разница — в том,<br>что её касается.', 60, INK, 'z-index:5'))
end = f'''<div class="fill" style="background:#fff"></div>
<div id="elogo" style="position:absolute;left:0;right:0;top:150px;text-align:center">{logo(110)}</div>
{stage(140,460,800,560)}
<div id="eprod">{sili(260,560,330,'transform:rotate(-8deg)')}{sili(560,580,320,'',heart=True)}</div>
{cap('e1', 1100, 'Снимать —', 116)}{cap('e2', 1225, f'<span style="color:{ORANGE}">не ранить.</span>', 116)}
{cap('e3', 1410, 'Силиконовая пенная повязка Sili-Care', 40, INK, 'font-family:Inter;font-weight:600')}
{cap('e4', 1490, 'Ухаживаете за близким — спросите силиконовую повязку.<br>Клиникам и дистрибьюторам — образцы в директ.', 30, '#555', 'font-family:Inter;font-weight:500;line-height:1.4')}
{wave(1080,1920,170)}'''
clip('end', 15.2, 4.8, end, 1)
js = '''
tl.from("#pl",{y:-700,rotation:-60,opacity:0,duration:.6,ease:"power3.out"},2.4)
  .from("#si",{y:-700,rotation:40,opacity:0,duration:.6,ease:"power3.out"},3.0)
  .from("#dmgwrap",{opacity:0,duration:.01},6.9)
  .to("#pl",{y:-520,x:-60,rotation:-55,duration:.7,ease:"power3.in"},6.6)
  .to("#pl",{opacity:0,duration:.2},7.3)
  .fromTo("#pch",{x:0},{x:12,duration:.05,repeat:5,yoyo:true},6.9)
  .to("#under",{opacity:1,duration:.4},7.6).from("#under",{y:60,duration:.5},7.6)
  .to("#si",{y:-600,rotation:-10,duration:1.2,ease:"power2.inOut"},9.6)
  .to("#si",{opacity:0,duration:.3},10.7)
  .to("#okring",{opacity:1,duration:.5},10.6).from("#okring",{scale:.6,duration:.8},10.6)
  .to("#under",{opacity:0,duration:.3},12.0)
  .to(["#labL","#labR"],{opacity:1,duration:.4},12.4)
  .from("#c1t",{y:40,opacity:0,duration:.4},.1).from("#pch",{scale:.7,opacity:0,duration:.6,ease:"back.out(1.6)"},.05)
  .from("#c2t",{opacity:0,duration:.3},2.25).from("#c3t",{opacity:0,duration:.3},4.25)
  .from("#c4t",{opacity:0,duration:.3},6.25).from("#c5t",{opacity:0,duration:.3},9.25)
  .from(["#c6t","#c6b"],{opacity:0,y:30,duration:.4,stagger:.5},12.25)
  .from("#elogo",{opacity:0,y:-30,duration:.5},15.25).from("#eprod",{opacity:0,y:60,duration:.6},15.4)
  .from(["#e1","#e2"],{y:50,opacity:0,duration:.5,stagger:.2},15.8).from(["#e3","#e4"],{opacity:0,duration:.5,stagger:.4},16.6);'''
html = f'''<!doctype html><html lang="ru"><head><meta charset="UTF-8"><title>Персиковый тест</title><script src="gsap.min.js"></script><link rel="stylesheet" href="shared.css">
<style>#root{{position:relative;width:1080px;height:1920px;overflow:hidden}} #pbar{{position:absolute;left:0;top:0;height:10px;width:1080px;background:{ORANGE};transform-origin:left;z-index:50}}</style></head><body>
<div id="root" data-composition-id="main" data-width="1080" data-height="1920" data-duration="20">
<div class="fill" style="background:#fff;z-index:0"></div>{''.join(clips)}
<div id="pbar" class="clip" data-start="0" data-duration="20" data-track-index="9" style="inset:auto;height:10px"></div>
</div><script>window.__timelines={{}};const tl=gsap.timeline({{paused:true}});tl.fromTo("#pbar",{{scaleX:0}},{{scaleX:1,duration:20,ease:"none"}},0);{js}
window.__timelines["main"]=tl;</script></body></html>'''
open('peach_reel/index.html','w').write(html)

# ============ CAROUSEL 6 slides (1080x1350)
def sl(inner, i):
    return f'<div class="fill" style="color:{INK}"><div class="fill" style="background:#fff"></div>{header("Персиковый тест", f"{i}/6")}{inner}<div style="position:absolute;right:64px;bottom:60px">{logo(50)}</div></div>'
C = []
C.append(sl(f'''<div class="pad" style="top:60px"><h1 class="h" style="font-size:78px"><span>Мы наклеили пластырь</span><span>на персик.</span></h1></div>
{stage(60,400,960,700)}{scene(540,760,560,sfx="_1",dmg=False)}
<div class="pad" style="top:1130px"><h2 class="h" style="font-size:60px;color:{ORANGE}">Вот что случилось →</h2></div>''', 1))
C.append(sl(f'''{stage(60,170,960,600)}{peach(540,470,460,"p2")}
<div class="pad" style="top:820px"><div style="font-size:26px;font-weight:700;color:{ORANGE};text-transform:uppercase;letter-spacing:.06em">◆ Почему персик?</div>
<h2 class="h" style="font-size:56px;margin-top:18px">Его кожица тонкая и нежная — как кожа пожилого человека.</h2>
<p class="body" style="margin-top:20px;font-size:30px;color:#555;max-width:720px">Повязку меняют снова и снова. И каждый раз снимают с кожи.</p></div>''', 2))
C.append(sl(f'''{stage(60,170,960,640)}{scene(540,490,520,sfx="_3",pl=False)}
<div style="position:absolute;left:90px;top:860px">{plaster(0,0,380,130,-6,"u3",under=True)}</div>
<div class="pad" style="top:850px;left:520px;padding:0 70px 0 0"><div style="font-size:24px;font-weight:700;color:{RED};text-transform:uppercase;letter-spacing:.06em">◆ Снимаем пластырь</div><h2 class="h" style="font-size:54px;margin-top:14px">Кожица осталась на пластыре.</h2></div>''', 3))
C.append(sl(f'''{stage(60,170,960,640)}{scene(540,490,520,sfx="_4",pl=False,si=False)}
<div class="ring" style="left:605px;top:345px;width:270px;height:270px;color:{BLUE};border-width:4px"></div>
<div class="pad" style="top:860px"><div style="font-size:24px;font-weight:700;color:{ORANGE};text-transform:uppercase;letter-spacing:.06em">◆ Снимаем Sili-Care</div><h2 class="h" style="font-size:96px;margin-top:14px">Персик цел.</h2></div>''', 4))
LAY=[('Защитный верхний слой','барьер снаружи, пропускает пар'),('Суперабсорбирующий слой','запирает экссудат'),('Связующий слой','держит конструкцию'),('Мягкий пенный слой','влажная среда у раны'),('Перфорированный мягкий силикон','фиксирует и отпускает кожу')]
rows=''.join(f'<div style="display:flex;gap:22px;align-items:baseline;padding:16px 0;border-bottom:2px solid #EEE"><div style="color:{ORANGE};font-size:26px">◆</div><div style="font-size:34px;font-weight:700;width:470px">{a}</div><div style="font-size:26px;color:#666;flex:1">{b}</div></div>' for a,b in LAY)
C.append(sl(f'''<div class="pad" style="top:150px"><h2 class="h" style="font-size:64px"><span>Почему персик цел?</span><span style="color:{ORANGE}">5 слоёв Sili-Care Border.</span></h2>
<div style="margin-top:40px">{rows}</div>
<p class="body" style="margin-top:34px;font-size:30px;color:#444">Обычный клей держится за кожу крепче, чем клетки кожи — друг за друга. Мягкий силикон держит повязку, но отпускает кожу целой.</p></div>''', 5))
C.append(sl(f'''{stage(60,170,960,520)}{sili(250,250,330,'transform:rotate(-8deg)')}{sili(560,260,330,'',heart=True)}
<div class="pad" style="top:730px"><h2 class="h" style="font-size:84px"><span>Снимать —</span><span style="color:{ORANGE}">не ранить.</span></h2>
<p class="body" style="margin-top:28px;font-size:32px">👵 Ухаживаете за близким? Перешлите тому, кто делает перевязки.</p>
<p class="body" style="margin-top:14px;font-size:32px">🏥 Клиникам и дистрибьюторам — образцы Sili-Care в директ.</p></div>''', 6))
open('peach_car/index.html','w').write(page(C,1080,1350,'Персиковый тест — карусель'))
