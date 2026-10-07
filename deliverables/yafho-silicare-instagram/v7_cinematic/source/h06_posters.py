from cinekit import *
from cine import *
from kp import carousel, OUT
from brand import ORANGE, logo
import lineart, shutil, os
FOOT='<div style="position:absolute;left:0;right:0;bottom:56px;text-align:center;font-size:18px;color:rgba(255,255,255,.4)">Медицинское изделие. Применение — по назначению специалиста.</div>'
LOGO=f'<div style="position:absolute;left:0;right:0;bottom:100px;text-align:center;filter:drop-shadow(0 0 20px rgba(243,130,33,.45))">{logo(64,ORANGE)}</div>'
keys=['neonatology','obstetrics','plastic_surgery','dermatology','geriatrics','surgery']
grid=''.join(f'<div style="display:inline-block;width:300px;height:300px;margin:10px">{glow_svg(art_paths(k),300,"p"+str(i),5)}</div>' for i,k in enumerate(keys))
P1=f'''{backdrop(31,60)}{kin("a",["Твоя","кожа","помнит"],110,100)}{kin("b",["всё."],230,150,accent_idx=(0,))}
<div style="position:absolute;left:40px;right:40px;top:430px;text-align:center">{grid}</div>{LOGO}{FOOT}{GRAIN}'''
P2=f'''{backdrop(32,60)}<div style="position:absolute;left:0;right:0;top:170px;text-align:center;font-family:'Inter Display';font-weight:700;font-size:250px;color:{ORANGE};text-shadow:0 0 60px rgba(243,130,33,.8),0 0 140px rgba(243,130,33,.4)">03:47</div>
<div style="position:absolute;left:280px;top:470px">{glow_svg(lineart.belly()["paths"],520,"q",5)}</div>
{kin("c",["Привет,","шрам."],1040,80,extra="font-family:Inter;font-style:italic;font-weight:400")}
<div style="position:absolute;left:0;right:0;top:1150px;text-align:center;font-size:32px;color:{ORANGE};font-weight:700;letter-spacing:.1em">#ПИСЬМОШРАМУ</div>{FOOT}{GRAIN}'''
P3=f'''{backdrop(33,70)}<div style="position:absolute;left:140px;top:120px">{glow_svg(lineart.butterfly()["paths"],800,"r",5)}</div>
{kin("d",["Есть","дети,","чья","кожа","хрупкая,"],860,64,extra="white-space:nowrap")}{kin("e",["как","крыло","бабочки."],950,92,accent_idx=(1,2),extra="white-space:nowrap")}
<div style="position:absolute;left:0;right:0;top:1110px;text-align:center;font-size:30px;color:#F2E6DA">25–31 октября · Неделя детей-бабочек</div>{LOGO}{GRAIN}'''
od=carousel('posters_tmp',[P1,P2,P3],'Постеры')
dst=os.path.join(OUT.replace('v6_campaign','v7_cinematic'),'posters'); os.makedirs(dst,exist_ok=True)
for i,n in enumerate(['poster_kozha_pomnit_vsyo','poster_0347_pismo_shramu','poster_krylo_babochki']):
    shutil.copy(os.path.join(od,f'slide{i+1}.png'),os.path.join(dst,n+'.png'))
shutil.rmtree(od); print('ok')
