from cinekit import *
from cine import *
from brand import ORANGE
import sfx, random, lineart
r=random.Random(5)
fib=''.join(f'<path d="M{r.randint(0,400)} {r.randint(0,560)} q{r.randint(-40,40)} {r.randint(-20,20)} {r.randint(30,140)} {r.randint(-12,12)}" stroke="rgba(150,95,40,.35)" stroke-width="1.4" fill="none"/>' for _ in range(70))
POLY="2% 40%,14% 8%,28% 30%,42% 2%,58% 26%,72% 0%,88% 24%,99% 46%,90% 70%,97% 96%,76% 80%,58% 100%,40% 78%,22% 98%,6% 76%"
def paper(x,y,id,torn=False):
    hole=''
    if torn:
        hole=f'''<div id="{id}g" style="position:absolute;left:0%;top:12%;width:100%;height:50%;opacity:0;background:radial-gradient(ellipse at center,rgba(255,250,235,1) 0%,rgba(255,220,160,.7) 35%,transparent 70%);filter:blur(18px)"></div>
<div id="{id}h" style="position:absolute;left:8%;top:22%;width:84%;height:30%;opacity:0;clip-path:polygon({POLY});background:#FFFDF6;box-shadow:0 0 40px #fff"></div>'''
    return f'''<div id="{id}" style="position:absolute;left:{x}px;top:{y}px;width:400px;height:560px">
<div style="position:absolute;inset:-60px;border-radius:40px;background:radial-gradient(ellipse at center,rgba(255,190,120,.45),transparent 70%);filter:blur(30px)"></div>
<div style="position:absolute;inset:0;border-radius:8px;background:radial-gradient(ellipse at 50% 45%,#FFF1DA 0%,#F8D7A8 55%,#E2AE72 100%)"></div>
<svg viewBox="0 0 400 560" style="position:absolute;inset:0;width:100%;height:100%">{fib}</svg>{hole}</div>'''
PL=f'<div id="tp" style="position:absolute;left:150px;top:780px;width:360px;height:120px;transform:rotate(-10deg);border-radius:60px;background:linear-gradient(180deg,#5A4A3C,#3A2E25);box-shadow:inset 0 2px 0 rgba(255,220,180,.25)"><div style="position:absolute;left:120px;top:20px;width:120px;height:80px;border-radius:12px;background:#2B221B"></div></div>'
MESH=f'<div id="tm" style="position:absolute;left:600px;top:730px;width:320px;height:240px;transform:rotate(6deg);border-radius:14px;background-color:rgba(70,45,25,.85);background-image:radial-gradient(circle,rgba(255,236,200,.95) 5px,transparent 5.8px);background-size:22px 22px"></div>'
body=f'''<section id="s1" class="clip" data-start="0" data-duration="10.6" data-track-index="1">{backdrop(11)}
{paper(110,560,"pl",True)}{paper(570,560,"pr")}{PL}{MESH}
{kin("k1",["Эта","бумага","—"],180,84)}{kin("k2",["как","кожа","ребёнка-бабочки."],290,70,accent_idx=(2,))}
{kin("k3",["Снимаем","пластырь…"],230,84,extra="opacity:0")}{kin("k4",["Снимаем","силикон."],230,84,accent_idx=(1,),extra="opacity:0")}
<div id="lL" style="position:absolute;left:90px;top:1180px;width:440px;text-align:center;font-size:34px;font-weight:700;color:#FF6B4A;opacity:0;text-shadow:0 0 20px rgba(255,80,60,.6)">Обычный пластырь</div>
<div id="lR" style="position:absolute;left:550px;top:1180px;width:440px;text-align:center;font-size:34px;font-weight:700;color:{ORANGE};opacity:0;text-shadow:0 0 20px rgba(243,130,33,.6)">Силикон — лист цел</div></section>
<section id="s2" class="clip" data-start="10.6" data-duration="5.0" data-track-index="1">{backdrop(12)}
<div id="bfw" style="position:absolute;left:140px;top:420px;width:800px;height:800px">{glow_svg(lineart.butterfly()["paths"],800,"bf",4.5)}</div>
{kin("k5",["Для","детей-бабочек","это","не","эксперимент."],180,70)}{kin("k6",["Это","каждая","перевязка."],1360,100,accent_idx=(1,2))}</section>
<section id="s3" class="clip" data-start="15.6" data-duration="6.4" data-track-index="1">{backdrop(13)}
<div id="d1" style="position:absolute;left:0;right:0;top:420px;text-align:center;font-family:'Inter Display';font-weight:800;font-size:170px;line-height:1;color:{ORANGE};text-shadow:0 0 60px rgba(243,130,33,.7)">25–31</div>
<div id="d2" style="position:absolute;left:0;right:0;top:600px;text-align:center;font-family:'Inter Display';font-weight:800;font-size:96px;color:#fff">октября</div>
<div id="d3" style="position:absolute;left:90px;right:90px;top:760px;text-align:center;font-size:40px;color:#F2E6DA;line-height:1.4">Неделя осведомлённости<br>о буллёзном эпидермолизе</div>
<div id="d4" style="position:absolute;left:90px;right:90px;top:960px;text-align:center;font-size:44px;color:#fff;font-weight:700">Поделитесь этим видео 🦋</div>
<div id="d5" style="position:absolute;left:90px;right:90px;top:1050px;text-align:center;font-size:28px;color:#aaa">[ссылка на фонд-партнёр]</div>
<div id="d6" style="position:absolute;left:0;right:0;top:1200px;text-align:center;filter:drop-shadow(0 0 24px rgba(243,130,33,.45))">{logo(100,ORANGE)}</div></section>'''
js=drift_js(0,22)+'''tl.from(["#pl","#pr"],{opacity:0,scale:.92,duration:.8,stagger:.15},.05);'''+slam_js('k1',.15,.1)+slam_js('k2',.55,.12)+'''
tl.to(["#k1","#k2"],{opacity:0,duration:.3},2.3);
tl.from("#tp",{y:-900,rotation:-50,opacity:0,duration:.5,ease:"power3.out"},2.6).from("#tm",{y:-900,rotation:40,opacity:0,duration:.5,ease:"power3.out"},3.2);
tl.to("#k3",{opacity:1,duration:.01},4.5);'''+slam_js('k3',4.5,.1)+'''
tl.to("#tp",{y:-700,x:-80,rotation:-50,duration:.55,ease:"power4.in"},5.0).to("#tp",{opacity:0,duration:.2},5.5);
tl.to(["#plh","#plg"],{opacity:1,duration:.08},5.32).fromTo("#plg",{scale:.6},{scale:1.3,duration:1.2,ease:"power2.out"},5.32);
tl.fromTo("#pl",{x:0},{x:14,duration:.04,repeat:7,yoyo:true},5.32).to("#lL",{opacity:1,duration:.4},6.0);
tl.to("#k3",{opacity:0,duration:.3},7.2).to("#k4",{opacity:1,duration:.01},7.4);'''+slam_js('k4',7.4,.1)+'''
tl.to("#tm",{y:-700,rotation:-6,duration:1.3,ease:"power2.inOut"},7.9).to("#tm",{opacity:0,duration:.3},9.1).to("#lR",{opacity:1,duration:.4},9.2);
tl.fromTo("#pr",{filter:"brightness(1)"},{filter:"brightness(1.25)",duration:.6,repeat:1,yoyo:true},9.2);'''
js+=draw_js('bf',10.7,1.6,11.0,1.2)+'tl.fromTo("#bfw",{scaleX:1},{scaleX:.82,duration:.35,repeat:7,yoyo:true,ease:"sine.inOut"},12.3).to("#bfw",{y:-260,duration:3.0,ease:"power1.in"},12.6);'+slam_js('k5',10.8,.08)+slam_js('k6',12.8,.12)
js+='tl.from("#d1",{opacity:0,scale:1.4,filter:"blur(16px)",duration:.5,ease:"power3.out"},15.7).from("#d2",{opacity:0,y:20,duration:.4},16.1).from(["#d3","#d4","#d5"],{opacity:0,y:20,duration:.5,stagger:.35},16.6).from("#d6",{opacity:0,duration:.6},18.0);'
f,fj=flash('ft',5.32,'#FFF6E6'); body+=f'<div class="clip" data-start="5" data-duration="1" data-track-index="7">{f}</div>'; js+=fj
f2,fj2=flash('fe',15.6); body+=f'<div class="clip" data-start="15.2" data-duration="1" data-track-index="6">{f2}</div>'; js+=fj2
ev=[(.15,sfx.click(.4)),(.55,sfx.boom(.5)),(2.6,sfx.click(.5)),(3.2,sfx.click(.5)),(4.5,sfx.whoosh(.5,.2)),
    (5.15,sfx.tear(.6,.75)),(5.32,sfx.boom(.6)),(7.4,sfx.whoosh(.5,.2)),(9.2,sfx.chime(880,.2,2.5)),
    (10.5,sfx.whoosh(.9,.3)),(11.0,sfx.chime(1108,.15,3)),(11.4,sfx.chime(1320,.12,3)),(12.8,sfx.heart(.7)),
    (14.2,sfx.riser(1.4,.25)),(15.6,sfx.boom(.85)),(16.1,sfx.chime(659,.18,3))]
shots=cine_reel('m3_risovaya_bumaga_cinematic',22,body,js,'Тест на рисовой бумаге',ev,pad=(103.8,155.6,207.7,261.6),check=(6.4,1.2,3.8,9.8,13.5,17.5))
strip(shots,'kp/chk_m3.jpg'); print('ok')
