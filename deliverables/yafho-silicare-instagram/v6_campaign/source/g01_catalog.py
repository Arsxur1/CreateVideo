from kp import *
# простые продуктовые иллюстрации
def prod(kind):
    sh='box-shadow:0 30px 50px -24px rgba(30,40,70,.45)'
    if kind=='square': return sili(330,560,420,'transform:rotate(-6deg)')
    if kind=='heart': return sili(320,540,440,'',heart=True)
    if kind=='mesh': return f'<div style="position:absolute;left:250px;top:600px;width:580px;height:380px;border-radius:20px;transform:rotate(-4deg);background-color:rgba(250,232,210,.75);background-image:radial-gradient(circle,#C9D3E3 7px,transparent 7.8px);background-size:30px 30px;{sh}"></div>'
    if kind=='nonwoven': return f'<div style="position:absolute;left:280px;top:580px;width:520px;height:420px;border-radius:26px;background:#fff;background-image:radial-gradient(rgba(150,160,180,.35) 1.4px,transparent 2px);background-size:9px 9px;{sh}"><div style="position:absolute;inset:70px;border-radius:16px;background:#F3F5F8;border:3px solid #E4E8EE"></div></div>'
    if kind=='roll': return f'<div style="position:absolute;left:250px;top:640px;width:580px;height:150px;border-radius:75px;transform:rotate(-4deg);background:linear-gradient(180deg,rgba(246,214,180,.95),rgba(232,186,140,.9));{sh}"></div>'
    if kind=='kit': return f'<div style="position:absolute;left:230px;top:600px;width:360px;height:300px;border-radius:30px;background:#fff;{sh}"><div style="position:absolute;inset:50px;border-radius:16px;background:#F3F5F8;border:3px solid #E4E8EE"></div></div><div style="position:absolute;left:640px;top:640px;width:200px;height:240px;border-radius:30px;background:#fff;{sh}"><div style="position:absolute;left:70px;top:70px;width:60px;height:60px;border-radius:50%;background:{RED}"></div></div><div style="position:absolute;left:585px;top:740px;width:60px;height:8px;background:#C9D3E3"></div>'
    if kind=='island': return f'<div style="position:absolute;left:230px;top:600px;width:620px;height:380px;border-radius:30px;background:rgba(255,255,255,.92);{sh}"><div style="position:absolute;left:180px;top:110px;right:180px;bottom:110px;border-radius:14px;background:#F7F7F7;border:3px solid #E4E7EA"></div></div>'
    if kind=='foam': return f'<div style="position:absolute;left:330px;top:560px;width:420px;height:420px;border-radius:30px;background:linear-gradient(145deg,#F6D2AE,#E8B485);background-image:radial-gradient(rgba(150,90,40,.25) 1.4px,transparent 2px),linear-gradient(145deg,#F6D2AE,#E8B485);background-size:8px 8px,100% 100%;{sh}"></div>'
    if kind=='hydrogel': return f'<div style="position:absolute;left:310px;top:560px;width:460px;height:420px;border-radius:40px;background:rgba(255,255,255,.75);{sh}"><div style="position:absolute;inset:60px;border-radius:30px;background:radial-gradient(circle at 40% 35%,rgba(220,235,255,.95),rgba(180,205,240,.8))"></div></div>'
    if kind=='iv': return f'<div style="position:absolute;left:300px;top:560px;width:480px;height:440px;border-radius:120px 120px 40px 40px;background:rgba(255,255,255,.9);{sh}"><div style="position:absolute;left:150px;top:90px;width:180px;height:120px;border-radius:18px;background:rgba(155,27,116,.18);border:3px solid rgba(155,27,116,.5)"></div></div>'
P=[('Sili-Care Border','square','Гериатрия · пролежни · хрупкая кожа'),
   ('Sili-Care Sacrum','heart','Крестец · 18×18 и 23×23 см'),
   ('Silicone Wound Contact Layer','mesh','Дерматология · самая хрупкая кожа'),
   ('Silicone Nonwoven','nonwoven','Мягкая силиконовая фиксация'),
   ('Silicone Scar Sheet','roll','Пластика · акушерство · рубцы'),
   ('Reco Dressing Kit','kit','Послеоперационные разрезы · живот / Y для груди*'),
   ('Island Film Dressing','island','Хирургия · послеоперационные швы'),
   ('Silicel Adhesive','foam','Умеренный и обильный экссудат'),
   ('Hydrogel Dressing','hydrogel','Влажная среда для сухих ран'),
   ('CHG I.V. Fixation','iv','Катетеры и венозный доступ')]
D=2.7; T0=3.0
body = clip('i0',0,T0,f'''<div id="i1" class="cap" style="top:560px;font-size:110px">Одна линейка.</div><div id="i2" class="cap" style="top:700px;font-size:110px;color:{ORANGE}">Весь стационар.</div>
<div id="i3" style="position:absolute;left:0;right:0;top:960px;text-align:center">{logo(110)}</div><div id="i4" class="sub" style="top:1180px;font-size:34px">Каталог Yafho 2025 за 30 секунд →</div>''')
js='tl.from("#i1",{opacity:0,y:30,duration:.4},.05).from("#i2",{opacity:0,y:30,duration:.4},.4).from("#i3",{opacity:0,duration:.4},.8).from("#i4",{opacity:0,duration:.4},1.2);'
for i,(n,k,dep) in enumerate(P):
    t=round(T0+i*D,2)
    body+=clip(f'p{i}',t,D,f'''<div style="position:absolute;left:64px;top:90px;font-size:26px;font-weight:700;color:{ORANGE};letter-spacing:.08em">{i+1:02d} / {len(P)}</div>
<div style="position:absolute;left:40px;top:430px;width:1000px;height:760px;border-radius:40px;background:{STAGE}"></div>
<div id="pp{i}">{prod(k)}</div>
<div style="position:absolute;left:40px;top:430px;background:{BLUE};padding:16px 30px;color:#fff;font-weight:700;font-size:30px;border-radius:40px 0 24px 0">{n}</div>
<div id="pd{i}" class="cap" style="top:1260px;font-size:62px">{dep}</div>''')
    js+=f'tl.from("#pp{i}",{{opacity:0,scale:.85,y:40,duration:.45,ease:"back.out(1.6)"}},{t+.05}).from("#pd{i}",{{opacity:0,y:20,duration:.35}},{t+.3});'
TE=round(T0+len(P)*D,2); DUR=round(TE+4.5,1)
body+=clip('end',TE,DUR-TE,f'''<div id="z1" class="cap" style="top:420px;font-size:90px">Роддом. Пластика.<br>Дерматология. Хирургия.<br><span style="color:{ORANGE}">Одна линия заботы.</span></div>
<div id="z2" style="position:absolute;left:0;right:0;top:900px;text-align:center">{logo(110)}</div>
<div id="z3" class="cap" style="top:1110px;font-size:52px">Дистрибьюторам и клиникам:<br>напишите <span style="color:{ORANGE}">«КАТАЛОГ»</span> в директ</div>
<div class="sub" style="top:1330px;font-size:22px;color:#999">* назначение Reco Dressing Kit уточняйте по документации производителя</div>{wave(1080,1920,150)}''')
js+=f'tl.from("#z1",{{opacity:0,y:30,duration:.5}},{TE+.1}).from("#z2",{{opacity:0,duration:.5}},{TE+.7}).from("#z3",{{opacity:0,y:20,duration:.5}},{TE+1.2});'
shots=reel('g1_katalog_za_30_sekund',DUR,body,js,'Линейка Yafho',check=(1.6,T0+1.5,T0+D*1+1.5,T0+D*5+1.5,T0+D*8+1.5,TE+2.5))
strip(shots,'kp/chk_g1.jpg'); print('done',DUR)
