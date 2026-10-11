# «Наука ухода» в современном стиле «ФАКТЫ»: тёмный фон, свечение, огромная цифра, стеклянные плашки
from brand import logo, ORANGE
F="font-family:'Inter Display',sans-serif"; M="font-family:'DejaVu Sans Mono',monospace"
BG='#0E1014'; INKW='#F5F3EF'; SUB='rgba(245,243,239,.62)'; LINE='rgba(255,255,255,.10)'
OR=ORANGE; BL='#3F7FD1'; RED='#E5484D'
GRAD=f'background:linear-gradient(100deg,#FFB070 0%,{OR} 45%,#E2557A 100%);-webkit-background-clip:text;background-clip:text;color:transparent'
def bg(W,H,v=0):
    blobs=[(.85,.12,OR,.42),(.05,.85,BL,.30)] if v%2==0 else [(.1,.15,OR,.35),(.95,.8,'#E2557A',.25)]
    b=''.join(f'<div style="position:absolute;left:{int(W*x)-450}px;top:{int(H*y)-450}px;width:900px;height:900px;border-radius:50%;background:radial-gradient(closest-side,{c},transparent);opacity:{o};filter:blur(40px)"></div>' for x,y,c,o in blobs)
    grid=f'<div class="fill" style="background-image:linear-gradient({LINE} 1px,transparent 1px),linear-gradient(90deg,{LINE} 1px,transparent 1px);background-size:90px 90px;opacity:.35;-webkit-mask-image:radial-gradient(ellipse at 50% 40%,#000 30%,transparent 80%)"></div>'
    return f'<div class="fill" style="background:{BG}"></div>{b}{grid}'
def top(W,label,y=60):
    return (f'<div style="position:absolute;left:64px;top:{y}px">{logo(52,OR,False)}</div>'
            f'<div style="position:absolute;right:64px;top:{y+10}px;{M};font-size:24px;letter-spacing:.12em;color:{SUB}">{label}</div>')
def glass(inner,pad='14px 22px',r=40):
    return f'<span style="display:inline-block;padding:{pad};border-radius:{r}px;background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.16);backdrop-filter:blur(8px);{M};font-size:21px;line-height:1.35;color:{SUB}">{inner}</span>'
GR={'эксперимент':'◇ эксперимент на животных','масштаб':'ⓘ масштаб проблемы','низкая':'●○○ достоверность низкая','рекомендация':'✓ клиническая рекомендация'}
def dots(n_on,size=22,gap=10,cols=10,cls='d',on=OR):
    return ''.join(f'<div class="{cls}{"on" if i>=100-n_on else "off"}" style="position:absolute;left:{(i%cols)*(size+gap)}px;top:{(i//cols)*(size+gap)}px;width:{size}px;height:{size}px;border-radius:50%;background:{on if i>=100-n_on else "rgba(255,255,255,.14)"}"></div>' for i in range(100))
def fact(W,H,label,big,statement,src,grade,extra='',v=0,bid='num',big_px=300,top_y=60,num_y=None,stat_y=None,extra_y=None,foot_y=None):
    num_y=num_y or int(H*.17); stat_y=stat_y or num_y+big_px+10; foot_y=foot_y or H-200
    return (bg(W,H,v)+top(W,label,top_y)
      +f'<div class="fx-n" style="position:absolute;left:58px;top:{num_y}px;{F};font-weight:900;font-size:{big_px}px;line-height:.9;letter-spacing:-0.05em;{GRAD}"><span id="{bid}">{big}</span></div>'
      +f'<div class="fx-s" style="position:absolute;left:64px;right:64px;top:{stat_y}px;{F};font-weight:800;font-size:54px;line-height:1.1;letter-spacing:-0.01em;color:{INKW}">{statement}</div>'
      +(f'<div class="fx-x" style="position:absolute;left:64px;right:64px;top:{extra_y}px">{extra}</div>' if extra else '')
      +f'<div class="fx-f" style="position:absolute;left:64px;right:64px;top:{foot_y}px;display:flex;flex-wrap:wrap;gap:12px">{glass(src)}{glass(GR[grade],r=40) if grade else ""}</div>')
FACTS=[ # (big, count-up target, prefix/suffix, statement, source, grade, extra-kind)
 ('≈2×',2,'≈|×','быстрее затягивается рана<br>во влажной среде,<br><span style="color:'+OR+'">чем под коркой</span>','Winter G.D. · Nature · 1962','эксперимент','bars'),
 ('16%',16,'|%','пациентов реанимации —<br>травма кожи<br><span style="color:'+OR+'">от медицинского клея</span>','MARSI · метаанализ · J Wound Care 2024','масштаб','d16'),
 ('40%',40,'|%','пациентов: смена повязки —<br><span style="color:'+OR+'">самое тяжёлое</span><br>в жизни с раной','Price P. et al. · Int Wound J · 2008','масштаб','d40'),
 ('−50%',50,'−|%','пролежней —<br><span style="color:'+OR+'">с силиконовой пеной</span><br>на крестце','Cochrane 2024 · 18 РКИ · 5903 пац. · RR 0,50 (0,33–0,77)','низкая','press'),
 ('№1',1,'№|','силиконовая пластина —<br><span style="color:'+OR+'">первая линия</span><br>ухода за рубцом','Meaume S. et al. · 2014','рекомендация','steps'),
]
def extra(kind,W):
    if kind=='bars':
        row=lambda lab,w,c,v,i: (f'<div style="display:flex;align-items:center;gap:18px;margin-top:{0 if i==0 else 22}px"><div style="flex:0 0 250px;{M};font-size:24px;color:{SUB}">{lab}</div>'
                                 f'<div class="br" style="height:18px;width:{w}px;border-radius:9px;background:{c};transform-origin:0 50%"></div><div style="{F};font-weight:800;font-size:34px;color:{INKW}">{v}</div></div>')
        return row('под коркой',260,BL,'1×',0)+row('влажная среда',520,OR,'≈2×',1)
    if kind in ('d16','d40'):
        n=int(kind[1:]); return f'<div style="position:relative;height:{10*32}px">{dots(n,cls="d"+kind)}</div>'
    if kind=='press':
        g=lambda n,c: f'<div style="position:relative;width:{10*26}px;height:{10*26}px">{dots(n,size=18,gap=8,cls=c)}</div>'
        return (f'<div style="display:flex;gap:70px;align-items:flex-start"><div>{g(10,"pa")}<div style="margin-top:14px;{M};font-size:24px;color:{SUB}">без повязки: 10/100*</div></div>'
                f'<div>{g(5,"pb")}<div style="margin-top:14px;{M};font-size:24px;color:{OR}">с пеной: ≈5/100</div></div></div>')
    if kind=='steps':
        return ''.join(f'<span class="stp" style="display:inline-block;margin:0 14px 14px 0">{glass(f"<b style=color:{INKW}>{a}</b>",pad="16px 26px")}</span>' for a in ('01 · рана зажила','02 · каждый день','03 · месяцы, не дни'))
    return ''
QUESTIONS=['Какая повязка нужна — и почему?','Как часто менять и кто это делает?','Как снимать, не травмируя кожу?','Какие признаки — повод прийти сразу?','Когда начинать уход за рубцом?']
RED_FLAGS=['краснота расползается','жар, озноб','гной или запах','боль усиливается']
SOURCES=['Winter G.D. Nature, 1962; 193:293–294 (эксперимент на животных).','MARSI в ОРИТ ≈16% — метаанализ, J Wound Care, 2024; консенсус MARSI — McNichol L. et al., 2013.','Price P. et al. Int Wound J, 2008.','Patton D. et al. Cochrane Database Syst Rev, 2024 (CD009362.pub4): RR 0,50 (95% ДИ 0,33–0,77), 18 РКИ, 5903 пациента, низкая достоверность.','Meaume S. et al. Wound Repair Regen, 2014.','Тревожные признаки — общие рекомендации NHS.']
