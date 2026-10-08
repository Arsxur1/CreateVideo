# Шаг 15: B2B-набор — одностраничник A4 (PNG+PDF)
import os, shutil
from kp import _dir, _snap
from gen_lib import page
from brand import logo, sili, ORANGE, MAGENTA, INK, GREY, STAGE, BLUE
from lineart import svg
OUT='/home/user/CreateVideo/deliverables/yafho-silicare-instagram/v15_b2b'; os.makedirs(OUT,exist_ok=True)
F="font-family:'Inter Display',sans-serif"
W,H=1240,1754  # A4 при 150 dpi
ROWS=[('obstetrics','Акушерство','Sili-Care Border · Silicone Scar Sheet · Island Film Dressing','Шов после кесарева, затем уход за рубцом'),
 ('neonatology','Неонатология / ОРИТН','Silicone Nonwoven · Silicone Wound Contact Layer','Фиксация датчиков и катетеров на очень тонкой коже'),
 ('plastic_surgery','Пластическая хирургия','Silicone Scar Sheet · Sili-Care · Island Film Dressing','Послеоперационные швы и рубцы'),
 ('dermatology','Дерматология','Silicone Wound Contact Layer · Hydrogel · Silicone Nonwoven','Хрупкая кожа, частые перевязки'),
 ('geriatrics','Гериатрия / уход','Sili-Care Sacrum · Sili-Care Border · Hydrocolloid','Профилактика и уход при пролежнях'),
 ('surgery','Хирургия / ОРИТ','Sili-Care · Island Film · CHG I.V. Fixation · Hydrocolloid','Послеоперационные раны, фиксация катетеров')]
rows=''.join(f'''<div style="display:flex;align-items:center;padding:12px 0;border-bottom:1px solid #E3E6EC">
<div style="flex:0 0 120px;text-align:center">{svg(k,84,7)}</div>
<div style="flex:0 0 300px;{F};font-weight:800;font-size:30px;color:{INK}">{d}</div>
<div style="flex:1"><div style="{F};font-weight:700;font-size:25px;color:{ORANGE}">{p}</div><div style="margin-top:6px;font-size:23px;color:#555">{t}</div></div></div>''' for k,d,p,t in ROWS)
facts=[('21%','родов в мире — кесарево','ВОЗ, Betran 2021'),('~16%','пациентов ОРИТ — MARSI','J Wound Care 2024'),('40,3%','пациентов: смена повязки — худшее','Price 2008'),('$26,8 млрд','в год — пролежни (США)','Padula 2019')]
fx=''.join(f'<div style="flex:1;padding:22px 18px;background:#fff;border-radius:18px"><div style="{F};font-weight:900;font-size:44px;color:{ORANGE};white-space:nowrap">{a}</div><div style="margin-top:6px;font-size:21px;line-height:1.3;color:{INK}">{b}</div><div style="margin-top:8px;font-size:16px;color:{GREY}">{c}</div></div>' for a,b,c in facts)
html=f'''<div class="fill" style="background:#fff"></div>
<div style="position:absolute;left:0;right:0;top:0;height:330px;background:{STAGE}"></div>
<div style="position:absolute;left:80px;top:70px">{logo(90,ORANGE,True)}</div>
<div style="position:absolute;left:80px;top:200px;{F};font-weight:800;font-size:50px;line-height:1.1;color:{INK}">Повязки, которые держат<br>и <span style="color:{ORANGE}">отпускают мягко</span></div>
<div style="position:absolute;right:300px;top:70px">{sili(0,0,200,"transform:rotate(-8deg)")}</div>
<div style="position:absolute;left:80px;right:80px;top:380px;{F};font-weight:700;font-size:24px;letter-spacing:.12em;color:{GREY}">ОДНА ЛИНЕЙКА — ШЕСТЬ ОТДЕЛЕНИЙ</div>
<div style="position:absolute;left:80px;right:80px;top:420px">{rows}</div>
<div style="position:absolute;left:80px;right:80px;top:1150px;padding:22px;border-radius:24px;background:{STAGE};display:flex;gap:16px">{fx}</div>
<div style="position:absolute;left:80px;right:80px;top:1420px;display:flex;justify-content:space-between;align-items:flex-end">
<div style="font-size:24px;line-height:1.6;color:{INK}"><b>Образцы и каталог 2025</b><br>Instagram: напишите «КАТАЛОГ» в директ<br>Сайт: yafho.com<br>Контакт: [имя менеджера, телефон, e-mail]</div>
<div style="text-align:right;font-size:18px;line-height:1.5;color:{GREY}">Рег. удостоверения: [№ / страна]<br>Условия поставки: [регион, сроки, минимальная партия]</div></div>
<div style="position:absolute;left:80px;right:80px;bottom:40px;font-size:16px;line-height:1.5;color:{GREY}">Медицинские изделия. Показания, противопоказания и режим применения — по инструкции производителя и назначению специалиста. Состав линейки — по каталогу Yafho 2025. Иллюстрации схематичны.</div>'''
d=_dir('v15_onepager')
open(os.path.join(d,'index.html'),'w').write(page([html],W,H,'Yafho для клиник'))
sh=_snap(d,[.5])[0]; shutil.copy(sh,f'{OUT}/onepager_A4.png')
from PIL import Image
Image.open(sh).convert('RGB').save(f'{OUT}/onepager_A4.pdf',resolution=150)
print('ok')
