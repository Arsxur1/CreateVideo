from cinekit import *
from cine import *
import sfx
SEG=[('neonatology','Неонатология','первое','прикосновение.'),('obstetrics','Акушерство','самый','счастливый день.'),
     ('plastic_surgery','Пластическая хирургия','каждый','шов.'),('dermatology','Дерматология','каждое','касание.'),
     ('geriatrics','Гериатрия','каждую','перевязку.'),('surgery','Хирургия','даже','зажившую рану.')]
H=2.8; D=3.1
body = f'<section id="hk" class="clip" data-start="0" data-duration="{H}" data-track-index="1">{backdrop(1)}{kin("k1",["Твоя","кожа","помнит"],600,124)}{kin("k2",["всё."],900,210,accent_idx=(0,))}</section>'
js = slam_js('k1',.1,.22) + slam_js('k2',.95) + drift_js(0,30)
ev = [(.1,sfx.click(.5)),(.32,sfx.click(.5)),(.54,sfx.click(.5)),(.95,sfx.boom(.8))]
f,fj = flash('fl0', .95); body += f'<div class="clip" data-start="0" data-duration="{H}" data-track-index="7" id="flc0">{f}</div>'; js += fj
notes=[660,740,880,990,1108,1320]
for i,(k,lab,w1,w2) in enumerate(SEG):
    t=round(H+i*D,2)
    body += f'''<section id="s{i}" class="clip" data-start="{t}" data-duration="{D}" data-track-index="1">{backdrop(i+2)}
<div class="lab2">◆ {lab}</div>
<div id="cam{i}" style="position:absolute;left:115px;top:300px;width:850px;height:850px">{glow_svg(art_paths(k),850,"g"+str(i),stroke=4)}</div>
{kin("t"+str(i)+"a",["Кожа","помнит"],1260,64,color="#F2E6DA")}{kin("t"+str(i)+"b",(w1+" "+w2).split(),1350,100,accent_idx=tuple(range(1,len((w1+" "+w2).split()))))}</section>'''
    js += draw_js('g'+str(i), t+.05, 1.5, t+1.2, .7) + f'tl.fromTo("#cam{i}",{{scale:.94}},{{scale:1.06,duration:{D},ease:"none"}},{t});' + slam_js(f't{i}a', t+.35, .1) + slam_js(f't{i}b', t+.9, .12)
    ev += [(t-.25, sfx.whoosh(.8,.3)), (t+1.25, sfx.chime(notes[i],.18))]
TE = round(H+len(SEG)*D,2); DUR = round(TE+4.6,1)
body += f'<section id="end" class="clip" data-start="{TE}" data-duration="{DUR-TE}" data-track-index="1">{end_card("e","Кожа помнит всё.","Пусть помнит заботу.","Неонатология · Акушерство · Пластика<br>Дерматология · Гериатрия · Хирургия")}</section>'
f,fj = flash('fl1', TE); body += f'<div class="clip" data-start="{TE-0.5}" data-duration="1.5" data-track-index="7">{f}</div>'; js += fj
js += slam_js('ea', TE+.1, .1) + slam_js('eb', TE+.6, .12) + f'tl.from("#el",{{opacity:0,scale:.9,duration:.7}},{TE+1.3}).from("#ec",{{opacity:0,y:20,duration:.6}},{TE+1.9});'
ev += [(TE-1.4, sfx.riser(1.4,.3)), (TE, sfx.boom(.9)), (TE+.6, sfx.chime(440,.2,3)), (TE+.62, sfx.chime(660,.15,3))]
shots = cine_reel('m1_manifest_cinematic', DUR, body, js, 'Кожа помнит — манифест', ev, check=(1.6, 4.5, 8.0, 17.5, 20.5, TE+2.5))
strip(shots, 'kp/chk_m1.jpg'); print('ok', DUR)
