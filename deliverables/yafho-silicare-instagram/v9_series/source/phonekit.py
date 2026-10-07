# Набор экранов телефона: поиск, ответ, чат, заметки, напоминания, галерея, список, финал
import random, sfx
from brand import ORANGE, logo
F='font-family:Inter Display,sans-serif;'
BG='#000'; CARD='#1C1C1E'; TXT='#F2F2F7'; MUT='#8E8E93'; BLUE='#0A84FF'; SEP='#2C2C2E'
_r = random.Random(4)
class Ep:
    def __init__(s): s.body=''; s.js=''; s.ev=[]; s.n=0
    def uid(s,p): s.n+=1; return f'{p}{s.n}'
    def add(s,html,js,ev): s.body+=html; s.js+=js; s.ev+=ev
def status(t, dark=True):
    c = TXT if dark else '#000'
    return f'<div style="position:absolute;left:60px;right:60px;top:40px;display:flex;justify-content:space-between;{F}font-weight:600;font-size:34px;color:{c}"><span>{t}</span><span>●●● 5G ▮▮▮▯</span></div>'
def section(id,t,d,inner,bg=BG):
    return f'<section id="{id}" class="clip" data-start="{t}" data-duration="{d}" data-track-index="1"><div class="fill" style="background:{bg}"></div>{inner}</section>'
def caption(id, html, top=1500):
    return f'<div id="{id}" style="position:absolute;left:40px;right:40px;top:{top}px;text-align:center;{F}font-weight:800;font-size:62px;line-height:1.1;color:#fff;text-shadow:0 4px 30px #000">{html}</div>'
def search(ep, t, d, time, query, suggestions, answer_html, source, cap=None, step=.07):
    u=ep.uid('sr'); q=f'<span class="{u}q"> </span>'.join('<span style="white-space:nowrap">'+''.join(f'<span class="{u}q">{c}</span>' for c in w)+'</span>' for w in query.split(' '))
    sg=''.join(f'<div style="padding:28px 0;border-bottom:1px solid {SEP}"><span style="color:{MUT}">⌕</span>&nbsp;&nbsp;{x}</div>' for x in suggestions)
    capd = caption(u+'c',cap) if cap else ''
    html=section(u,t,d,f'''{status(time)}<div style="position:absolute;left:50px;top:150px;{F}font-weight:700;font-size:72px;color:{TXT}">Поиск</div>
<div style="position:absolute;left:50px;right:50px;top:270px;min-height:110px;border-radius:28px;background:{CARD};display:flex;align-items:center;padding:20px 34px;{F}font-size:40px;line-height:1.25;color:{TXT}"><span style="color:{MUT};margin-right:20px;flex:none">⌕</span><span style="flex:1;min-width:0">{q}<span id="{u}cur" style="display:inline-block;width:4px;height:48px;background:{BLUE};margin-left:4px;vertical-align:middle"></span></span></div>
<div id="{u}sg" style="position:absolute;left:50px;right:50px;top:480px;{F}font-size:36px;color:{TXT}">{sg}</div>
<div id="{u}an" style="position:absolute;left:50px;right:50px;top:490px;border-radius:36px;background:{CARD};padding:44px;opacity:0;{F}">
<div style="font-size:28px;color:{MUT};letter-spacing:.06em">ОТВЕТ</div><div style="font-size:44px;line-height:1.35;color:{TXT};margin-top:18px">{answer_html}</div>
<div style="font-size:24px;color:{MUT};margin-top:26px">{source}</div></div>{capd}''')
    ta=t+.35+len(query)*step+.4
    js=f'tl.from(".{u}q",{{opacity:0,duration:.01,stagger:{step}}},{t+.35});tl.fromTo("#{u}cur",{{opacity:1}},{{opacity:0,duration:.25,repeat:{int(d/.25)},yoyo:true}},{t});'
    js+=f'tl.from("#{u}sg > div",{{opacity:0,y:20,duration:.25,stagger:.15}},{t+.35+len(query)*step*.5});'
    js+=f'tl.to("#{u}sg",{{opacity:0,duration:.25}},{ta}).to("#{u}an",{{opacity:1,duration:.35}},{ta}).from("#{u}an",{{y:60,duration:.4,ease:"power3.out"}},{ta});'
    js+=f'tl.to("#{u}an .HL",{{backgroundSize:"100% 100%",duration:.9,ease:"power2.inOut",stagger:.4}},{ta+1.1});'
    if cap: js+=f'tl.from("#{u}c",{{opacity:0,y:30,duration:.4}},{t+.1}).to("#{u}c",{{opacity:0,duration:.4}},{ta-.3});'
    ev=[(t+.35+i*step,sfx.click(_r.uniform(.12,.22))) for i,c in enumerate(query) if c!=' ']+[(ta,sfx.whoosh(.4,.15)),(ta+1.1,sfx.chime(1568,.08,.8))]
    ep.add(html,js,ev); return ta
def hl(txt): return f'<span class="HL" style="background:linear-gradient(transparent 55%,rgba(243,130,33,.55) 55%);background-size:0% 100%;background-repeat:no-repeat">{txt}</span>'
def chat(ep, t, d, time, name, avatar_letter, msgs, typing_before=()):
    """msgs: list of (side 'me'/'them', text, at_time_offset)"""
    u=ep.uid('ch'); bub=''
    for i,(side,txt,off) in enumerate(msgs):
        me = side=='me'
        bub+=f'<div id="{u}m{i}" style="{"margin-left:auto;" if me else ""}max-width:780px;background:{BLUE if me else "#2C2C2E"};color:{"#fff" if me else TXT};border-radius:40px;padding:26px 36px;margin-bottom:22px;width:fit-content">{txt}</div>'
        if i+1<len(msgs) and msgs[i+1][0]=='them' and (i+1) in typing_before:
            bub+=f'<div id="{u}ty{i+1}" style="max-width:200px;background:#2C2C2E;color:{MUT};border-radius:40px;padding:20px 36px;margin-bottom:22px;width:fit-content;font-size:50px;line-height:1">• • •</div>'
    html=section(u,t,d,f'''{status(time)}<div style="position:absolute;left:0;right:0;top:110px;height:150px;border-bottom:1px solid {SEP};text-align:center;{F}"><div style="width:84px;height:84px;border-radius:50%;background:linear-gradient(135deg,#F7A04A,#F38221);margin:0 auto;font-size:42px;line-height:84px;color:#fff;font-weight:700">{avatar_letter}</div><div style="font-size:30px;color:{TXT};margin-top:6px">{name}</div></div>
<div style="position:absolute;left:40px;right:40px;top:330px;{F}font-size:42px;line-height:1.3">{bub}</div>''')
    js=''; ev=[]
    for i,(side,txt,off) in enumerate(msgs):
        me=side=='me'; tt=t+off
        if i in typing_before:
            js+=f'tl.from("#{u}ty{i}",{{opacity:0,duration:.2}},{tt-1.0}).to("#{u}ty{i}",{{opacity:0,height:0,padding:0,margin:0,duration:.1}},{tt-.05});'
        js+=f'tl.from("#{u}m{i}",{{opacity:0,y:40,scale:.9,transformOrigin:"{"right" if me else "left"} bottom",duration:.3}},{tt});'
        ev.append((tt, sfx.whoosh(.25,.16) if me else sfx.chime(1568,.12,.6)))
    ep.add(html,js,ev)
def notes(ep, t, d, time, title, lines, step=.55, light=True):
    u=ep.uid('nt'); bg='#FFFDF5' if light else BG; c='#000' if light else TXT
    ls=''.join(f'<div class="{u}l" style="padding:14px 0">{x}</div>' for x in lines)
    html=section(u,t,d,f'''{status(time,dark=not light)}<div style="position:absolute;left:60px;top:140px;{F}font-size:30px;color:#D9A400;font-weight:600">‹ Заметки</div>
<div style="position:absolute;left:60px;right:60px;top:220px;{F}font-weight:700;font-size:66px;color:{c};line-height:1.1">{title}</div>
<div style="position:absolute;left:60px;right:60px;top:400px;{F}font-size:46px;line-height:1.35;color:{c}">{ls}</div>''',bg)
    js=f'tl.from(".{u}l",{{opacity:0,x:-20,duration:.25,stagger:{step}}},{t+.4});'
    ev=[(t+.4+i*step,sfx.click(.2)) for i in range(len(lines))]
    ep.add(html,js,ev)
def checklist(ep, t, d, time, title, items, tick_idx, tick_at=1.0):
    u=ep.uid('cl'); rows=''
    for i,(a,b) in enumerate(items):
        if i==tick_idx:
            rows+=f'<div style="display:flex;align-items:center;gap:22px;padding:12px 0"><div style="width:56px;height:56px;border-radius:50%;border:4px solid #C7C7CC;position:relative;flex:none"><div id="{u}ck" style="position:absolute;inset:-4px;border-radius:50%;background:{ORANGE};color:#fff;text-align:center;line-height:56px;font-size:40px;opacity:0">✓</div></div><span><b>{a}</b>{"<br><span style=font-size:36px;color:#666>"+b+"</span>" if b else ""}</span></div>'
        else:
            rows+=f'<div style="display:flex;align-items:center;gap:22px;padding:12px 0;color:#999"><div style="width:56px;height:56px;border-radius:50%;background:#C7C7CC;color:#fff;text-align:center;line-height:56px;font-size:36px;flex:none">✓</div><s>{a}</s></div>'
    html=section(u,t,d,f'''{status(time,dark=False)}<div style="position:absolute;left:60px;top:150px;{F}font-weight:700;font-size:70px;color:#000">{title}</div>
<div style="position:absolute;left:60px;right:60px;top:320px;{F}font-size:46px;color:#000;line-height:1.3">{rows}</div>''','#F2F2F7')
    js=f'tl.to("#{u}ck",{{opacity:1,duration:.15}},{t+tick_at}).from("#{u}ck",{{scale:.2,duration:.35,ease:"back.out(3)"}},{t+tick_at});'
    ep.add(html,js,[(t+tick_at,sfx.chime(1046,.18,1.2))])
def lockscreen(ep, t, d, time, date, notifs, step=.5):
    """notifs: list of (app, title, text)"""
    u=ep.uid('ls')
    ns=''.join(f'<div class="{u}n" style="background:rgba(40,40,44,.82);border-radius:34px;padding:26px 30px;margin-bottom:18px;{F}"><div style="display:flex;justify-content:space-between;font-size:26px;color:{MUT}"><span>{a}</span><span>сейчас</span></div><div style="font-size:36px;color:#fff;font-weight:700;margin-top:6px">{b}</div><div style="font-size:34px;color:#ddd;margin-top:4px">{c}</div></div>' for a,b,c in notifs)
    html=section(u,t,d,f'''<div class="fill" style="background:radial-gradient(120% 80% at 50% 20%,#3a2a1e,#0b0b0d 70%)"></div>
<div style="position:absolute;left:0;right:0;top:150px;text-align:center;{F}font-size:40px;color:#ddd">{date}</div>
<div style="position:absolute;left:0;right:0;top:200px;text-align:center;{F}font-weight:700;font-size:200px;color:#fff;line-height:1">{time}</div>
<div style="position:absolute;left:50px;right:50px;top:500px">{ns}</div>''','#000')
    js=f'tl.from(".{u}n",{{opacity:0,y:-40,scale:.95,duration:.3,stagger:{step},ease:"back.out(1.6)"}},{t+.3});'
    ep.add(html,js,[(t+.3+i*step,sfx.chime(1318,.12,.6)) for i in range(len(notifs))])
def gallery(ep, t, d, time, title, tiles):
    """tiles: list of (label, css_background)"""
    u=ep.uid('gl')
    ts=''.join(f'<div class="{u}t" style="position:relative;aspect-ratio:1;background:{bgc};border-radius:6px;overflow:hidden"><div style="position:absolute;left:10px;bottom:8px;{F}font-size:24px;color:#fff;font-weight:700;text-shadow:0 2px 6px #000">{lab}</div></div>' for lab,bgc in tiles)
    html=section(u,t,d,f'''{status(time)}<div style="position:absolute;left:50px;top:140px;{F}font-weight:700;font-size:66px;color:{TXT}">{title}</div>
<div style="position:absolute;left:30px;right:30px;top:260px;display:grid;grid-template-columns:repeat(3,1fr);gap:8px">{ts}</div>''')
    js=f'tl.from(".{u}t",{{opacity:0,scale:.8,duration:.25,stagger:.12}},{t+.3});'
    ep.add(html,js,[(t+.3,sfx.whoosh(.5,.15))])
def endcard(ep, t, d, l1, l2, cta, foot='Сценка. Медицинское изделие. Применение — по назначению специалиста.'):
    u=ep.uid('ec'); fs = 88 if max(len(l1),len(l2))<=20 else 70
    html=section(u,t,d,f'''<div id="{u}1" style="position:absolute;left:60px;right:60px;top:500px;text-align:center;{F}font-weight:800;font-size:{fs}px;line-height:1.08;color:#2B2B2B">{l1}<br><span style="color:{ORANGE}">{l2}</span></div>
<div id="{u}2" style="position:absolute;left:0;right:0;top:960px;text-align:center">{logo(110)}</div>
<div id="{u}3" style="position:absolute;left:80px;right:80px;top:1180px;text-align:center;font-size:36px;color:#444;font-weight:600;line-height:1.4">{cta}</div>
<div style="position:absolute;left:80px;right:80px;bottom:120px;text-align:center;font-size:22px;color:#999">{foot}</div>''','#fff')
    js=f'tl.from("#{u}1",{{opacity:0,y:30,duration:.5}},{t+.1}).from("#{u}2",{{opacity:0,duration:.5}},{t+.7}).from("#{u}3",{{opacity:0,duration:.4}},{t+1.2});'
    ep.add(html,js,[(t,sfx.whoosh(.6,.25)),(t+.4,sfx.chime(659,.18,2.5))])
