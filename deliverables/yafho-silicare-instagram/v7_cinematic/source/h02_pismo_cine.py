from cinekit import *
from cine import *
from brand import ORANGE
import sfx, random, lineart
BABY = "M232 480 C206 430 208 370 228 338 L214 236 C211 214 240 208 244 230 L258 318 L264 200 C266 176 296 176 296 200 L293 312 L308 214 C312 190 340 193 337 216 L326 322 L348 256 C356 234 382 243 375 265 L350 365 C340 425 320 455 300 482"
paths = lineart.belly()['paths'] + [(BABY,0,'translate(232,236) scale(.36) rotate(-8 300 340)')]
# отдельные классы для ладошки
LINES=[(1.9,'Привет, шрам.',58),(4.0,'Ты появился в 03:47.',46),(6.6,'В ту минуту я впервые услышала её крик.',46),(10.2,'Я долго тебя стеснялась.',46),(12.6,'А теперь знаю: ты — дверь,',46),(14.4,'через которую она пришла в этот мир.',46)]
def typed(i,t,txt,size):
    chars=''.join(f'<span class="c{i}">{c if c!=" " else "&nbsp;"}</span>' for c in txt)
    return f'<div id="ln{i}" style="font-family:Inter;font-style:italic;font-size:{size+4}px;line-height:1.3;color:#F6EADF;margin-top:14px;text-shadow:0 0 18px rgba(255,180,120,.25)">{chars}</div>'
body = f'''<section id="h" class="clip" data-start="0" data-duration="1.9" data-track-index="1">{backdrop(4)}
<div id="clk" style="position:absolute;left:0;right:0;top:700px;text-align:center;font-family:'Inter Display';font-weight:700;font-size:260px;letter-spacing:-.02em;color:{ORANGE};text-shadow:0 0 60px rgba(243,130,33,.8),0 0 120px rgba(243,130,33,.4)">03:47</div>
<div id="clk2" style="position:absolute;left:0;right:0;top:1020px;text-align:center;font-size:34px;color:#cbb;letter-spacing:.3em">ТОТ САМЫЙ ДЕНЬ</div></section>
<section id="m" class="clip" data-start="1.9" data-duration="17.8" data-track-index="1">{backdrop(5)}<div class="lab2">◆ #ПисьмоШраму</div>
<div id="cam" style="position:absolute;left:190px;top:170px;width:700px;height:700px">{glow_svg(paths,700,"gb",4)}</div>
<div style="position:absolute;left:90px;right:90px;top:930px">{"".join(typed(i,t,txt,s) for i,(t,txt,s) in enumerate(LINES))}</div>
{kin("thx",["Спасибо."],1600,120,accent_idx=(0,))}</section>
<section id="e" class="clip" data-start="19.7" data-duration="6.3" data-track-index="1">{end_card("en","Шрам — это память.","Пусть она будет мягкой.","💌 Напишите письмо своему шраму<br><b style='color:#F38221'>#ПисьмоШраму</b>")}</section>'''
js = '''tl.from("#clk",{opacity:0,scale:1.6,filter:"blur(20px)",duration:.45,ease:"power3.out"},.1).fromTo("#clk",{scale:1},{scale:1.05,duration:.15,repeat:3,yoyo:true},.6).from("#clk2",{opacity:0,duration:.4},.8);''' + drift_js(0,26)
js += 'tl.fromTo("#gb .gi:not(:last-of-type)",{strokeDasharray:1,strokeDashoffset:1},{strokeDashoffset:0,duration:2.2,ease:"power2.inOut"},2.0);'
# ладошка = последние 3 пути класса gi; рисуем её позже — отдельной анимацией по индексам
js += 'const gi=[...document.querySelectorAll("#gb .gi")];const hand=gi.slice(-3),body=gi.slice(0,-3);'
js = js.replace('tl.fromTo("#gb .gi:not(:last-of-type)"','tl.fromTo(body')
js = js.replace("const gi=","")  # placeholder (перестраиваем ниже)
js = '''tl.from("#clk",{opacity:0,scale:1.6,filter:"blur(20px)",duration:.45,ease:"power3.out"},.1).fromTo("#clk",{scale:1},{scale:1.05,duration:.15,repeat:3,yoyo:true},.6).from("#clk2",{opacity:0,duration:.4},.8);''' + drift_js(0,26) + '''
const gi=[...document.querySelectorAll("#gb .gi")];const hand=gi.slice(-3),bod=gi.slice(0,-3);
tl.fromTo(bod,{strokeDasharray:1,strokeDashoffset:1},{strokeDashoffset:0,duration:2.2,ease:"power2.inOut"},2.0);
tl.fromTo(hand,{strokeDasharray:1,strokeDashoffset:1,opacity:0},{strokeDashoffset:0,opacity:1,duration:1.6,ease:"power2.out"},16.4);
tl.fromTo("#gb .ga",{strokeDasharray:1,strokeDashoffset:1,opacity:0},{strokeDashoffset:0,opacity:1,duration:1.2},3.6);
tl.fromTo("#cam",{scale:.96},{scale:1.05,duration:17,ease:"none"},2.0);'''
ev=[(.1,sfx.boom(.6)),(.6,sfx.heart(.9)),(1.4,sfx.heart(.8)),(1.85,sfx.whoosh(.6,.25))]
r=random.Random(2)
for i,(t,txt,s) in enumerate(LINES):
    step=.035; js+=f'tl.from(".c{i}",{{opacity:0,duration:.01,stagger:{step}}},{t});'
    if i: js+=f'tl.to("#ln{i-1}",{{opacity:.35,duration:.5}},{t});'
    for k in range(0,len(txt),2): ev.append((t+k*step, sfx.click(r.uniform(.12,.22))))
js+='tl.to("#ln5",{opacity:.35,duration:.5},16.6);'+slam_js('thx',17.6)
ev+=[(16.4,sfx.chime(880,.22,3)),(17.6,sfx.heart(.9)),(17.62,sfx.chime(1320,.15,3)),(18.4,sfx.riser(1.3,.25)),(19.7,sfx.boom(.8)),(20.3,sfx.chime(523,.2,3))]
f,fj=flash('fe',19.7); body+=f'<div class="clip" data-start="19.2" data-duration="1.4" data-track-index="7">{f}</div>'; js+=fj
js+=slam_js('ena',19.8,.1)+slam_js('enb',20.3,.1)+'tl.from("#enl",{opacity:0,scale:.9,duration:.7},21.0).from("#enc",{opacity:0,y:20,duration:.6},21.6);'
shots=cine_reel('m2_pismo_shramu_cinematic',26,body,js,'Письмо шраму',ev,pad=(98,146.8,196,246.9),check=(18.2,.9,5.5,12.0,23.5))
strip(shots,'kp/chk_m2.jpg'); print('ok')
