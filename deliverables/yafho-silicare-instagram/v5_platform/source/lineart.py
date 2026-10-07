# Single-line SVG drawings (viewBox 0 0 600 600). Each returns list of (path_d, accent_bool)
def mirror(d):  # mirror x around 300 for simple absolute-coord paths (M/C/L/Q with numbers)
    import re
    toks = re.findall(r'[MCLQZ]|-?\d+\.?\d*', d); out=[]; i=0; xflag=True
    for t in toks:
        if t in 'MCLQZ': out.append(t); xflag=True; continue
        v=float(t)
        if xflag: v=600-v
        out.append(f'{v:g}'); xflag=not xflag
    return ' '.join(out)

def feet():
    foot = "M235 500 C185 500 170 430 180 365 C190 300 205 258 245 250 C285 243 302 285 297 345 C292 405 292 500 235 500 Z"
    toes = ["M281 232 m-14 0 a14 14 0 1 0 28 0 a14 14 0 1 0 -28 0","M252 220 m-10 0 a10 10 0 1 0 20 0 a10 10 0 1 0 -20 0","M229 224 m-9 0 a9 9 0 1 0 18 0 a9 9 0 1 0 -18 0","M210 236 m-8 0 a8 8 0 1 0 16 0 a8 8 0 1 0 -16 0","M196 254 m-7 0 a7 7 0 1 0 14 0 a7 7 0 1 0 -14 0"]
    left = [(foot,0)]+[(t,0) for t in toes]
    shift = lambda d: d  # second foot drawn via transform in render
    tape = ("M200 380 L290 372 L292 408 L202 416 Z",1)
    return {'paths': left+[tape], 'twin': True}

def belly():
    L="M150 50 C130 190 105 280 150 380 C178 445 160 520 140 600"
    return {'paths':[(L,0),(mirror(L),0),("M300 320 C294 320 294 344 300 344 C306 344 306 320 300 320",0),("M215 475 Q300 500 385 475",1)]}

def profile():
    face="M250 30 C300 50 330 100 334 165 C336 196 352 218 374 248 C382 262 372 270 354 272 C358 288 354 298 342 304 C350 314 346 328 332 332 C338 350 330 378 300 390 C276 400 268 430 268 470 C268 520 282 560 300 600"
    back="M250 30 C180 40 150 110 160 190 C168 250 190 300 205 360 C214 400 210 470 190 600"
    return {'paths':[(face,0),(back,0),("M296 178 Q310 170 324 178",0),("M222 250 Q206 292 222 336",1)]}

def butterfly():
    uw="M300 230 C230 110 80 110 92 235 C104 330 225 320 300 292"
    lw="M300 300 C225 330 140 385 172 455 C202 515 272 455 300 382"
    ant="M300 186 C290 140 270 118 252 108"
    return {'paths':[("M300 182 L300 440",0),(uw,1),(mirror(uw),1),(lw,0),(mirror(lw),0),(ant,0),(mirror(ant),0)]}

def peach():
    return {'paths':[("M300 130 C420 130 500 220 500 340 C500 460 410 540 300 540 C190 540 100 460 100 340 C100 220 180 130 300 130",0),
                     ("M300 140 C322 250 312 400 292 530",0),("M300 132 C340 86 412 86 444 108 C404 140 342 146 300 132",0),
                     ("M196 300 L270 280 L276 312 L202 332 Z",1)]}

def suture():
    paths=[("M90 300 C220 288 380 312 510 300",0)]
    for x in range(140,480,48): paths.append((f"M{x} 270 L{x+12} 330",1))
    return {'paths':paths}

ART = {'neonatology':feet,'obstetrics':belly,'plastic_surgery':profile,'dermatology':butterfly,'geriatrics':peach,'surgery':suture}

def svg(key, size=600, stroke=5, ink='#2B2B2B', accent='#F38221', cls='ln', idp=''):
    a = ART[key](); out=[]
    def draw(paths, tr=''):
        for i,(d,acc) in enumerate(paths):
            col = accent if acc else ink; w = stroke*1.8 if acc else stroke
            fill = 'rgba(243,130,33,.18)' if acc and d.strip().endswith('Z') else 'none'
            out.append(f'<path class="{cls} {cls}{"a" if acc else "i"}" pathLength="1" d="{d}" fill="{fill}" stroke="{col}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round" {tr}/>')
    if a.get('twin'):
        out.append('<g transform="translate(-75,0)">'); draw(a['paths']); out.append('</g>')
        out.append('<g transform="translate(675,25) scale(-1,1)">'); draw([p for p in a['paths'] if not p[1]]); out.append('</g>')
    else:
        draw(a['paths'])
    return f'<svg id="{idp}" viewBox="0 0 600 600" width="{size}" height="{size}" style="overflow:visible">{"".join(out)}</svg>'
