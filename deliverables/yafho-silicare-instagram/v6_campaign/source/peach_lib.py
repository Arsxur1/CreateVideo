# Illustrated "peach test" components
def peach(cx, cy, d, id='pch', inner=''):
    r = d // 2
    return f'''<div id="{id}" style="position:absolute;left:{cx-r}px;top:{cy-r}px;width:{d}px;height:{d}px">
<div style="position:absolute;inset:0;border-radius:50% 50% 48% 52%/52% 50% 50% 48%;background:radial-gradient(ellipse at 72% 70%,rgba(200,40,50,.0) 0%,rgba(200,40,50,0) 30%),radial-gradient(ellipse 70% 60% at 70% 62%,rgba(214,52,58,.95) 0%,rgba(226,80,60,.75) 40%,rgba(240,130,70,0) 75%),radial-gradient(circle at 30% 26%,#FFF0C8 0%,#FFD488 22%,#FBB462 50%,#EE8A4E 80%,#C9503F 100%);box-shadow:0 60px 90px -40px rgba(80,20,10,.6),inset -30px -40px 80px rgba(120,20,30,.35)"></div>
<div style="position:absolute;inset:0;border-radius:50%;opacity:.45;background-image:radial-gradient(rgba(255,245,230,.7) .9px,transparent 1.4px),radial-gradient(rgba(255,245,230,.5) .7px,transparent 1.2px);background-size:7px 7px,5px 5px;background-position:0 0,3px 2px;mix-blend-mode:screen"></div>
<div style="position:absolute;left:{r-8}px;top:{int(d*.06)}px;width:26px;height:{int(d*.62)}px;border-radius:50%;background:linear-gradient(90deg,transparent,rgba(140,30,30,.45),rgba(255,220,180,.25),transparent);transform:rotate(10deg)"></div>
<div style="position:absolute;left:{r+20}px;top:{-int(d*.08)}px;width:{int(d*.32)}px;height:{int(d*.13)}px;border-radius:0 100% 0 100%;background:linear-gradient(135deg,#8DBF5A,#4E8A3A);transform:rotate(-18deg);box-shadow:inset 0 -4px 8px rgba(0,0,0,.2)"></div>
<div style="position:absolute;left:{r-4}px;top:{-int(d*.03)}px;width:10px;height:{int(d*.07)}px;background:#6B4A2E;border-radius:4px"></div>
<div style="position:absolute;left:{int(d*.2)}px;top:{int(d*.14)}px;width:{int(d*.28)}px;height:{int(d*.16)}px;border-radius:50%;background:radial-gradient(closest-side,rgba(255,255,255,.55),transparent);filter:blur(6px)"></div>
{inner}</div>'''

def damage(x, y, w, h, id='dmg'):
    # torn skin: exposed flesh with jagged edge
    poly = "6% 18%,22% 4%,38% 14%,55% 2%,72% 12%,92% 6%,97% 30%,90% 52%,99% 74%,86% 95%,64% 88%,44% 98%,26% 90%,8% 96%,2% 70%,10% 48%"
    return f'''<div id="{id}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px">
<div style="position:absolute;inset:-6px;clip-path:polygon({poly});background:#C9433A;filter:blur(1px)"></div>
<div style="position:absolute;inset:0;clip-path:polygon({poly});background:radial-gradient(circle at 40% 40%,#FFE08A,#F7BE55 55%,#E79A3C);box-shadow:inset 0 0 30px rgba(180,60,30,.6)"></div>
<div style="position:absolute;inset:0;clip-path:polygon({poly});background-image:radial-gradient(rgba(255,240,180,.8) 1.5px,transparent 2.5px);background-size:16px 16px;opacity:.5"></div></div>'''

def plaster(x, y, w, h, rot, id='pl', under=False):
    pad = '' if under else f'<div style="position:absolute;left:{int(w*.33)}px;top:{int(h*.14)}px;width:{int(w*.34)}px;height:{int(h*.72)}px;border-radius:12px;background:#F2F4F6;border:2px solid #D7DCE1"></div>'
    holes = '' if under else f'<div style="position:absolute;inset:0;border-radius:{h//2}px;background-image:radial-gradient(rgba(120,130,140,.35) 2px,transparent 2.6px);background-size:22px 22px;background-position:6px 6px;opacity:.6"></div>'
    bits = ''
    if under:
        bits = ''.join(f'<div style="position:absolute;left:{int(w*a)}px;top:{int(h*b)}px;width:{int(w*c)}px;height:{int(h*e)}px;border-radius:40% 60% 50% 45%;background:radial-gradient(circle at 40% 35%,#F48A54,#C9433A)"></div>' for a,b,c,e in [(.08,.2,.18,.5),(.3,.15,.12,.35),(.62,.25,.2,.55),(.82,.18,.1,.4),(.45,.6,.14,.3)])
    return f'''<div id="{id}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;transform:rotate({rot}deg)">
<div style="position:absolute;inset:0;border-radius:{h//2}px;background:linear-gradient(180deg,#FFFFFF,#E4E7EA);box-shadow:0 10px 24px rgba(30,40,60,.3)"></div>{holes}{pad}{bits}</div>'''
