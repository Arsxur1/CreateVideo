# Yafho brand system (from yafho.com + Yafho Catalog 2025)
ORANGE='#F38221'; MAGENTA='#9B1B74'; YELLOW='#FFE000'; BLUE='#0B5AC2'; INK='#2B2B2B'; GREY='#7A7A7A'
RED='#D93A2F'
STAGE='linear-gradient(160deg,#9FB0CC 0%,#C9D3E3 55%,#E4E9F1 100%)'   # фон карточек товаров на сайте

def logo(size=56, color=ORANGE, sub=True):
    cross = f'<span style="display:inline-block;position:relative;width:{size*.62:.0f}px;height:{size*.62:.0f}px;border:{max(3,size//14)}px solid {color};border-radius:50%;vertical-align:{-size*.04:.0f}px;margin-left:1px"><span style="position:absolute;left:50%;top:50%;width:62%;height:20%;background:{MAGENTA};transform:translate(-50%,-50%);border-radius:2px"></span><span style="position:absolute;left:50%;top:50%;width:20%;height:62%;background:{MAGENTA};transform:translate(-50%,-50%);border-radius:2px"></span></span>'
    s = f'<div style="display:inline-block;line-height:1"><div style="font-family:Inter;font-weight:300;letter-spacing:-0.05em;font-size:{size}px;color:{color}">Yafh{cross}</div>'
    if sub: s += f'<div style="font-family:Inter;font-weight:300;font-size:{size*.24:.0f}px;letter-spacing:.02em;color:{GREY};margin-left:{size*.95:.0f}px;margin-top:2px">WOUND CARE</div>'
    return s + '</div>'

def header(label, idx='', w=1080):
    return f'''<div style="position:absolute;left:0;top:64px;width:{w}px;display:flex;align-items:center">
<div style="width:56px;height:34px;background:{ORANGE}"></div>
<div style="margin-left:18px;font-family:'Inter Display',sans-serif;font-weight:700;font-size:28px;letter-spacing:.04em;color:{ORANGE};text-transform:uppercase">{label}</div>
<div style="margin-left:14px;width:4px;height:34px;background:{ORANGE}"></div>
<div style="margin-left:auto;margin-right:64px;font-size:22px;color:{GREY};letter-spacing:.1em">{idx}</div></div>'''

def wave(w=1080, h=1350, height=150):
    return f'''<div style="position:absolute;left:0;bottom:0;width:{w}px;height:{height}px;overflow:hidden">
<div style="position:absolute;left:-10%;top:0;width:120%;height:{height*2}px;border-radius:50% 50% 0 0/{height*.5:.0f}px {height*.5:.0f}px 0 0;background:{YELLOW};transform:rotate(-2deg)"></div>
<div style="position:absolute;left:-10%;top:{height*.28:.0f}px;width:120%;height:{height*2}px;border-radius:50% 50% 0 0/{height*.6:.0f}px {height*.6:.0f}px 0 0;background:{ORANGE};transform:rotate(-2deg)"></div></div>'''

def sili(x, y, s, extra='', heart=False):
    # Sili-Care Border: peach/tan silicone foam with lighter central pad
    if heart:
        return f'''<div style="position:absolute;left:{x}px;top:{y}px;width:{s}px;height:{s}px;{extra}">
<svg viewBox="0 0 100 100" width="{s}" height="{s}" style="filter:drop-shadow(0 20px 26px rgba(80,40,10,.35))"><defs><radialGradient id="hg" cx="40%" cy="35%"><stop offset="0" stop-color="#FBE3C6"/><stop offset="1" stop-color="#E9B886"/></radialGradient></defs>
<path d="M50 92 C20 72 4 55 6 33 C8 14 30 6 50 24 C70 6 92 14 94 33 C96 55 80 72 50 92Z" fill="#EFC49A"/>
<path d="M50 80 C28 65 18 53 19 37 C20 24 36 19 50 33 C64 19 80 24 81 37 C82 53 72 65 50 80Z" fill="url(#hg)"/></svg></div>'''
    return f'''<div class="sili" style="position:absolute;left:{x}px;top:{y}px;width:{s}px;height:{s}px;border-radius:12%;background:linear-gradient(145deg,#F6D2AE,#E8B485);box-shadow:0 30px 50px -22px rgba(80,40,10,.5),inset 0 2px 0 rgba(255,255,255,.6);{extra}">
<div style="position:absolute;inset:16%;border-radius:10%;background:radial-gradient(circle at 40% 35%,#FCE6CC,#F0C595);box-shadow:inset 0 2px 8px rgba(150,90,40,.25),0 1px 0 rgba(255,255,255,.7)"></div>
<div style="position:absolute;inset:0;border-radius:12%;background-image:radial-gradient(rgba(160,100,50,.18) 1.2px,transparent 1.8px);background-size:10px 10px"></div></div>'''

def tab(text, x, y, w=420):
    return f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;background:{BLUE};padding:14px 24px;color:#fff;font-family:Inter;font-weight:700;font-size:24px">{logo(26,"#F7A04A",False)}<div style="margin-top:6px">{text}</div></div>'
