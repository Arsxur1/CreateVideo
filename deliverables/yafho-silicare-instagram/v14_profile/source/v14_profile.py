# Шаг 14: оформление профиля — аватар, обложки «Актуального», шапка, макет профиля
import os, shutil, base64
from kp import _dir, _snap
from gen_lib import page
from brand import logo, sili, ORANGE, MAGENTA, INK, GREY, STAGE
from lineart import svg
D='/home/user/CreateVideo/deliverables/yafho-silicare-instagram'; OUT=f'{D}/v14_profile'; os.makedirs(OUT,exist_ok=True)
F="font-family:'Inter Display',sans-serif"
NAME='Yafho · Силиконовые повязки'
BIO='Yafho Wound Care — повязки, которые держат и отпускают мягко 🧡\nРоддом · ОРИТН · пластика · хирургия\nКлиникам: «КАТАЛОГ» в директ ↓'
assert len(NAME)<=64 and len(BIO)<=150, (len(NAME),len(BIO))
LENS='<svg viewBox="0 0 600 600" width="360" height="360"><circle cx="270" cy="270" r="170" fill="none" stroke="#fff" stroke-width="10"/><line x1="395" y1="395" x2="520" y2="520" stroke="#fff" stroke-width="22" stroke-linecap="round"/><circle cx="270" cy="270" r="120" fill="none" stroke="#F38221" stroke-width="7" stroke-dasharray="8 22"/></svg>'
ART_KEY={'feet':'neonatology','belly':'obstetrics','profile':'plastic_surgery','butterfly':'dermatology'}
HL=[('Кожа помнит','feet'),('#ПисьмоШраму','belly'),('Дети-бабочки','butterfly'),('Сериал 180','profile'),('Под лупой','lens'),('Для клиник','sili')]
def hl(art):
    if art=='lens': icon=LENS
    elif art=='sili': icon=f'<div style="position:relative;width:340px;height:340px;margin:auto">{sili(30,30,280,"transform:rotate(-8deg)")}</div>'
    else: icon=svg(ART_KEY[art],380,9,ink='#fff')
    # круг показа «Актуального» — центр 1080×1920, видимая зона ~ круг 700 px
    return f'<div class="fill" style="background:{ORANGE}"></div><div style="position:absolute;left:190px;top:610px;width:700px;height:700px;border-radius:50%;background:radial-gradient(circle at 40% 35%,#F7A04A,{ORANGE} 70%);display:flex;align-items:center;justify-content:center">{icon}</div>'
avatar=f'<div class="fill" style="background:#fff"></div><div style="position:absolute;left:0;right:0;top:390px;text-align:center">{logo(250,ORANGE,True)}</div>'
slides=[hl(a) for _,a in HL]
d=_dir('v14_profile')
open(os.path.join(d,'index.html'),'w').write(page(slides,1080,1920,'Профиль'))
shots=_snap(d,[i+.5 for i in range(len(slides))])[:len(slides)]
from PIL import Image
for (t,a),sh in zip(HL,shots[:6]):
    shutil.copy(sh,f'{OUT}/highlight_{a}.png')
da=_dir('v14_avatar')
avatar=f'<div class="fill" style="background:#fff;display:flex;align-items:center;justify-content:center"><div style="transform:translateX(-30px)">{logo(240,ORANGE,True)}</div></div>'
open(os.path.join(da,'index.html'),'w').write(page([avatar],1080,1080,'Аватар'))
shutil.copy(_snap(da,[.5])[0],f'{OUT}/avatar_1080.png')
def circ(p):  # видимая часть обложки «Актуального» — центральный круг
    im=Image.open(p).convert('RGB').crop((190,610,890,1310)).resize((300,300)); q=p.replace('.png','_circle.png'); im.save(q); return q
# --- макет профиля через 6 недель ---
def b64(p,w=360):
    im=Image.open(p).convert('RGB'); im.thumbnail((w,int(w*16/9)))
    from io import BytesIO; b=BytesIO(); im.save(b,'JPEG',quality=80); return 'data:image/jpeg;base64,'+base64.b64encode(b.getvalue()).decode()
PIN=['v7_cinematic/m1_manifest_cinematic/cover.png','v6_campaign/c1_den_1_iz_180/cover.png','v5_platform/carousel_odna_liniya/slide1.png']
LAST=['v7_cinematic/posters/poster_kozha_pomnit_vsyo.png','v11_pod_lupoi/l5_hydrocolloid/cover.png','v6_campaign/c3_kak_nosit_plastinu/slide1.png','v8_styles/s3_paper_collage/cover.png','v11_pod_lupoi/l4_hydrogel/cover.png','v8_styles/s1_kinetic_type/cover.png']
av=b64(f'{OUT}/avatar_1080.png',200)
cells=''
for i,p in enumerate(PIN+LAST):
    pin='<div style="position:absolute;right:12px;top:10px;font-size:26px;color:#fff;text-shadow:0 1px 4px rgba(0,0,0,.6)">📌</div>' if i<3 else ''
    cells+=f'<div style="position:relative;aspect-ratio:3/4;overflow:hidden;background:#eee"><img src="{b64(f"{D}/{p}")}" style="width:100%;height:100%;object-fit:cover">{pin}</div>'
hls=''.join(f'<div style="width:150px;text-align:center"><div style="width:130px;height:130px;margin:auto;border-radius:50%;padding:5px;border:2px solid #ddd"><img src="{b64(circ(f"{OUT}/highlight_{a}.png"),300)}" style="width:100%;height:100%;border-radius:50%;display:block"></div><div style="margin-top:10px;font-size:22px;color:#262626;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">{t}</div></div>' for t,a in HL)
bio='<br>'.join(BIO.split('\n'))
prof=f'''<div class="fill" style="background:#fff"></div>
<div style="position:absolute;left:0;right:0;top:0;padding:60px 40px 0;font-family:Inter,sans-serif;color:#262626">
<div style="font-size:40px;font-weight:700">yafho.woundcare ⌄</div>
<div style="display:flex;align-items:center;margin-top:40px"><img src="{av}" style="width:190px;height:190px;border-radius:50%;border:2px solid #eee">
<div style="flex:1;display:flex;justify-content:space-around;text-align:center;font-size:26px"><div><b style="font-size:36px">51</b><br>публикация</div><div><b style="font-size:36px">—</b><br>подписчики</div><div><b style="font-size:36px">—</b><br>подписки</div></div></div>
<div style="margin-top:24px;font-size:28px;font-weight:700">{NAME}</div>
<div style="font-size:26px;color:#737373">Медицинское оборудование</div>
<div style="margin-top:6px;font-size:28px;line-height:1.4">{bio}</div>
<div style="font-size:28px;color:#00376B;font-weight:600">🔗 yafho.com</div>
<div style="display:flex;gap:14px;margin-top:26px"><div style="flex:1;background:#EFEFEF;border-radius:14px;padding:18px;text-align:center;font-weight:600;font-size:26px">Написать</div><div style="flex:1;background:#0095F6;color:#fff;border-radius:14px;padding:18px;text-align:center;font-weight:600;font-size:26px">Подписаться</div><div style="flex:1;background:#EFEFEF;border-radius:14px;padding:18px;text-align:center;font-weight:600;font-size:26px">Каталог</div></div>
<div style="display:flex;gap:16px;margin-top:34px;overflow:hidden">{hls}</div></div>
<div style="position:absolute;left:0;right:0;top:930px;display:grid;grid-template-columns:repeat(3,1fr);gap:4px">{cells}</div>'''
d2=_dir('v14_profile_mock')
open(os.path.join(d2,'index.html'),'w').write(page([prof],1080,2250,'Профиль — макет'))
sh=_snap(d2,[.5])[0]; shutil.copy(sh,f'{OUT}/profile_mockup.png')
open(f'{OUT}/bio.txt','w').write(f'Имя (поле «Имя», ищется в поиске):\n{NAME}\n\nБио:\n{BIO}\n')
print('ok',len(NAME),len(BIO))
