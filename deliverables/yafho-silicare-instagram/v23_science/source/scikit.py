# «Наука ухода»: общие научные компоненты (графики, плитки, источники) для ролика и постеров
from brand import logo, sili, ORANGE, INK, GREY, STAGE, BLUE
F="font-family:'Inter Display',sans-serif"
CTRL='#3F7FD1'; YAF='#F38221'   # палитра проверена validate_palette.js на белом фоне (все проверки PASS; у оранжевого — подписи значений обязательны)
MUTED='#5A6472'
def bgs(): return (f'<div class="fill" style="background:{STAGE}"></div>'
                   '<div class="fill" style="background:radial-gradient(ellipse 80% 40% at 50% 100%,rgba(255,255,255,.55),transparent 70%)"></div>')
def card(x,y,w,h,inner,id=''):
    return f'<div id="{id}" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;border-radius:36px;background:#fff;box-shadow:0 30px 60px -30px rgba(40,60,100,.35)">{inner}</div>'
def kicker(t,x=0,y=0,col=ORANGE): return f'<div style="{F};font-weight:800;font-size:26px;letter-spacing:.14em;color:{col}">{t}</div>'
def bars(rows,w,label_w=280,bh=64,gap=34,maxv=None,idp='b'):
    """Горизонтальные столбики: rows=[(подпись, значение, цвет, текст значения)]. Подпись и значение — текстом (не только цветом)."""
    maxv=maxv or max(r[1] for r in rows); out=''; plot=w-label_w-140
    for i,(lab,v,col,vt) in enumerate(rows):
        y=i*(bh+gap); bw=max(8,int(plot*v/maxv))
        out+=(f'<div style="position:absolute;left:0;top:{y}px;width:{label_w-20}px;height:{bh}px;display:flex;align-items:center;justify-content:flex-end;{F};font-weight:700;font-size:30px;color:{INK};text-align:right;line-height:1.1">{lab}</div>'
              f'<div id="{idp}{i}" style="position:absolute;left:{label_w}px;top:{y}px;width:{bw}px;height:{bh}px;background:{col};border-radius:0 6px 6px 0;transform-origin:0 50%"></div>'
              f'<div id="{idp}v{i}" style="position:absolute;left:{label_w+bw+16}px;top:{y}px;height:{bh}px;display:flex;align-items:center;{F};font-weight:900;font-size:40px;color:{INK}">{vt}</div>')
    out+=f'<div style="position:absolute;left:{label_w}px;top:-14px;width:2px;height:{len(rows)*(bh+gap)-gap+28}px;background:#9AA3AE"></div>'
    return out
def forest(w,est=.50,lo=.33,hi=.77,xmax=1.25,idp='f'):
    """Форест-плот одной оценки: относительный риск с 95% ДИ, линия «нет эффекта» на 1."""
    X=lambda v: int(40+(w-80)*v/xmax)
    ticks=''.join(f'<div style="position:absolute;left:{X(t)-1}px;top:150px;width:2px;height:14px;background:#9AA3AE"></div><div style="position:absolute;left:{X(t)-40}px;top:170px;width:80px;text-align:center;font-size:24px;color:{MUTED}">{str(t).replace(".",",")}</div>' for t in (0,.25,.5,.75,1))
    return (f'<div style="position:absolute;left:40px;top:150px;width:{w-80}px;height:2px;background:#9AA3AE"></div>{ticks}'
            f'<div style="position:absolute;left:{X(1)-1}px;top:20px;width:0;height:140px;border-left:3px dashed #9AA3AE"></div>'
            f'<div style="position:absolute;left:{X(1)+10}px;top:16px;font-size:22px;color:{MUTED};line-height:1.2">нет<br>эффекта</div>'
            f'<div id="{idp}ci" style="position:absolute;left:{X(lo)}px;top:84px;width:{X(hi)-X(lo)}px;height:6px;border-radius:3px;background:{YAF};transform-origin:50% 50%"></div>'
            f'<div id="{idp}pt" style="position:absolute;left:{X(est)-16}px;top:71px;width:32px;height:32px;border-radius:50%;background:{YAF};box-shadow:0 0 0 4px #fff"></div>'
            f'<div id="{idp}lb" style="position:absolute;left:{X(lo)-60}px;top:22px;width:{X(hi)-X(lo)+120}px;text-align:center;{F};font-weight:900;font-size:34px;color:{INK}">0,50 <span style="font-weight:600;font-size:26px;color:{MUTED}">(0,33–0,77)</span></div>'
            f'<div style="position:absolute;left:40px;top:212px;font-size:22px;color:{MUTED}">← относительный риск: меньше — лучше</div>')
def people(n_bad,total=100,cols=10,size=34,gap=8,idp='pp'):
    """100 человечков: закрашены те, у кого случился пролежень (иллюстрация при исходном риске)."""
    out=''
    for i in range(total):
        r,c=divmod(i,cols); bad=i>=total-n_bad
        out+=(f'<div class="{idp}{"b" if bad else "g"}" style="position:absolute;left:{c*(size+gap)}px;top:{r*(size+gap)}px;width:{size}px;height:{size}px">'
              f'<div style="position:absolute;left:{size*.3:.0f}px;top:0;width:{size*.4:.0f}px;height:{size*.4:.0f}px;border-radius:50%;background:{YAF if bad else "#C9D1DC"}"></div>'
              f'<div style="position:absolute;left:{size*.15:.0f}px;top:{size*.45:.0f}px;width:{size*.7:.0f}px;height:{size*.55:.0f}px;border-radius:{size*.35:.0f}px {size*.35:.0f}px 4px 4px;background:{YAF if bad else "#C9D1DC"}"></div></div>')
    return out
def stat(big,small,src,col=INK):
    return (f'<div style="{F};font-weight:900;font-size:120px;line-height:.95;letter-spacing:-0.03em;color:{col}">{big}</div>'
            f'<div style="margin-top:14px;{F};font-weight:700;font-size:34px;line-height:1.2;color:{INK}">{small}</div>'
            f'<div style="margin-top:12px;font-size:22px;color:{MUTED}">{src}</div>')
def grade(level):
    """Метка уровня доказательности — чтобы зритель видел, насколько уверены данные."""
    m={'низкая':('#B26B00','●○○'),'умеренная':('#7A6A00','●●○'),'эксперимент':('#5A6472','◇'),'рекомендация':('#2E7D4F','✓'),'масштаб':('#5A6472','ⓘ')}
    c,s=m[level]
    txt={'низкая':'Достоверность: низкая','умеренная':'Достоверность: умеренная','эксперимент':'Эксперимент на животных','рекомендация':'Клиническая рекомендация','масштаб':'Цифры — о масштабе проблемы'}[level]
    return f'<span style="display:inline-block;padding:8px 18px;border-radius:30px;border:2px solid {c};color:{c};{F};font-weight:800;font-size:22px">{s} {txt}</span>'
QUESTIONS=['Какая повязка мне нужна — и почему именно она?','Как часто её менять и кто это делает?','Как снимать, чтобы не травмировать кожу?','Какие признаки — повод сразу прийти?','Когда начинать уход за рубцом?']
RED_FLAGS=['краснота расползается','жар, озноб','гной или неприятный запах','боль усиливается, а не стихает']
SOURCES=['Winter G.D. Nature, 1962; 193:293–294 — влажная среда (эксперимент на животных).',
 'MARSI в ОРИТ ≈16% — метаанализ, J Wound Care, 2024. Консенсус MARSI: McNichol L. et al., 2013.',
 'Price P. et al. Int Wound J, 2008 — 40,3% пациентов: смена повязки — худшее.',
 'Patton D. et al. Cochrane Database Syst Rev, 2024 (CD009362.pub4): силиконовая пена vs без повязки, профилактика пролежней — RR 0,50 (95% ДИ 0,33–0,77), 18 РКИ, 5903 пациента, низкая достоверность.',
 'Meaume S. et al. Wound Repair Regen, 2014 — силикон: первая линия ухода за рубцами.']
