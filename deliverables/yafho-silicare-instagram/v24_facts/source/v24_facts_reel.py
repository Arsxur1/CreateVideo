# Шаг 38: ролик «Наука ухода» в стиле «ФАКТЫ» (1080×1920)
from factkit import *
from stylekit import style_reel, SOUT, kick
from kp import strip
import sfx
OUT=SOUT.replace('v8_styles','v24_facts'); W,H=1080,1920
def sec(id,s,d,inner): return f'<section id="{id}" class="clip" data-start="{s}" data-duration="{d}" data-track-index="1">{inner}</section>'
T0=3.6; FD=6.0; TF=T0+5*FD; TQ=TF+4.6; TE=TQ+6.6; DUR=round(TE+4.2,1)
body=''; js=''; ev=[]
chips=''.join(f'<span class="cc" style="display:inline-block;margin:0 14px 16px 0;padding:16px 30px;border-radius:40px;background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.16);{F};font-weight:900;font-size:46px;color:{INKW}">{b}</span>' for b,*_ in FACTS)
body+=sec('c0',0,T0,bg(W,H,0)+top(W,'НАУКА УХОДА',170)+
  f'<div id="c1" style="position:absolute;left:58px;top:420px;{F};font-weight:900;font-size:230px;line-height:.86;letter-spacing:-0.05em;{GRAD}">5 фактов</div>'
  f'<div id="c2" style="position:absolute;left:64px;right:64px;top:650px;{F};font-weight:800;font-size:72px;line-height:1.05;color:{INKW}">о повязках, которые<br>стоит знать <span style="color:{OR}">до выписки</span></div>'
  f'<div style="position:absolute;left:64px;right:64px;top:960px">{chips}</div>')
js+='tl.from("#c1",{scale:1.6,opacity:0,filter:"blur(14px)",duration:.5,ease:"power4.out"},.05).from("#c2",{opacity:0,y:30,duration:.4},.5).from("#c0 .cc",{opacity:0,y:20,scale:.8,duration:.3,stagger:.12,ease:"back.out(2)"},1.0);'
ev+=[(.05,kick(.9)),(.5,sfx.whoosh(.4,.15))]+[(1.0+k*.12,sfx.click(.25)) for k in range(5)]
for i,(big,tgt,fmt,st,src,gr,kind) in enumerate(FACTS):
    t=T0+i*FD; sid=f'f{i}'; pre,suf=fmt.split('|')
    body+=sec(sid,t,FD,fact(W,H,f'ФАКТ {i+1:02d} / 05',big,st,src,gr,extra(kind,W),v=i,bid=f'n{i}',top_y=170,num_y=330,
                 big_px=340 if len(big)<=3 else 290,stat_y=700,extra_y=960 if kind!='steps' else 980,foot_y=1400))
    js+=f'tl.from("#{sid} .fx-n",{{scale:1.5,opacity:0,filter:"blur(16px)",duration:.45,ease:"power4.out",transformOrigin:"0% 50%"}},{t+.05});'
    if tgt>2: js+=f'const o{i}={{v:0}};tl.to(o{i},{{v:{tgt},duration:1.1,ease:"power2.out",onUpdate:()=>{{document.getElementById("n{i}").textContent="{pre}"+Math.round(o{i}.v)+"{suf}"}}}},{t+.05});'
    js+=f'tl.from("#{sid} .fx-s",{{opacity:0,y:30,duration:.45,ease:"power3.out"}},{t+.9});'
    if kind=='bars': js+=f'tl.from("#{sid} .br",{{scaleX:0,duration:.8,stagger:.3,ease:"power2.out"}},{t+1.6});'
    elif kind in('d16','d40'): js+=f'tl.from("#{sid} .d{kind}off",{{opacity:0,duration:.4}},{t+1.5}).from("#{sid} .d{kind}on",{{scale:0,duration:.25,stagger:.03,ease:"back.out(3)"}},{t+1.8});'
    elif kind=='press': js+=f'tl.from("#{sid} .fx-x",{{opacity:0,y:20,duration:.4}},{t+1.5}).from("#{sid} .paon,#{sid} .pbon",{{scale:0,duration:.25,stagger:.06,ease:"back.out(3)"}},{t+1.9});'
    elif kind=='steps': js+=f'tl.from("#{sid} .stp",{{opacity:0,x:-30,duration:.35,stagger:.3}},{t+1.6});'
    js+=f'tl.from("#{sid} .fx-f",{{opacity:0,y:16,duration:.4}},{t+2.6});'
    ev+=[(t+.05,kick(.85)),(t+.9,sfx.whoosh(.4,.12)),(t+1.7,sfx.chime([523,587,659,698,784][i],.1,1.6))]
    if tgt>2: ev+=[(t+.1+k*.09,sfx.click(.12)) for k in range(10)]
fl=''.join(f'<div class="rf" style="display:flex;align-items:center;gap:24px;margin-top:26px"><span style="width:22px;height:22px;border-radius:50%;background:{RED};box-shadow:0 0 18px {RED}"></span><span style="{F};font-weight:800;font-size:54px;color:{INKW}">{x}</span></div>' for x in RED_FLAGS)
body+=sec('rq',TF,TQ-TF,bg(W,H,1)+top(W,'ВАЖНО',170)+
  f'<div id="r1" style="position:absolute;left:58px;top:330px;{F};font-weight:900;font-size:170px;line-height:.9;letter-spacing:-0.04em;color:{RED}">Сразу<br>к врачу,</div>'
  f'<div style="position:absolute;left:64px;top:660px;{F};font-weight:800;font-size:60px;color:{INKW}">если:</div><div style="position:absolute;left:64px;top:740px">{fl}</div>'
  f'<div id="r2" style="position:absolute;left:64px;right:64px;top:1260px">{glass("Повязка не лечит инфекцию и не заменяет осмотр врача.<br>Признаки — общие рекомендации NHS.",pad="18px 26px",r=24)}</div>')
js+=f'tl.from("#r1",{{scale:1.4,opacity:0,duration:.4,ease:"power4.out"}},{TF+.05}).from("#rq .rf",{{opacity:0,x:-30,duration:.3,stagger:.25}},{TF+.7}).from("#r2",{{opacity:0,duration:.4}},{TF+2.0});'
ev+=[(TF+.05,kick(.9))]+[(TF+.7+k*.25,sfx.click(.25)) for k in range(4)]
qs=''.join(f'<div class="q" style="display:flex;gap:26px;align-items:baseline;margin-top:{0 if k==0 else 34}px"><span style="{M};font-size:34px;color:{OR}">{k+1:02d}</span><span style="{F};font-weight:800;font-size:50px;line-height:1.15;color:{INKW}">{q}</span></div>' for k,q in enumerate(QUESTIONS))
body+=sec('qq',TQ,TE-TQ,bg(W,H,0)+top(W,'ЧЕК-ЛИСТ',170)+
  f'<div id="q1" style="position:absolute;left:58px;top:320px;{F};font-weight:900;font-size:140px;line-height:.92;letter-spacing:-0.04em;{GRAD}">5 вопросов</div>'
  f'<div style="position:absolute;left:64px;top:470px;{F};font-weight:800;font-size:64px;color:{INKW}">врачу при выписке</div>'
  f'<div style="position:absolute;left:64px;right:64px;top:620px;padding:50px;border-radius:40px;background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.14)">{qs}</div>')
js+=f'tl.from("#q1",{{scale:1.4,opacity:0,duration:.4,ease:"power4.out"}},{TQ+.05}).from("#qq .q",{{opacity:0,x:-30,duration:.35,stagger:.6}},{TQ+.7});'
ev+=[(TQ+.05,kick(.9))]+[(TQ+.7+k*.6,sfx.click(.3)) for k in range(5)]
body+=sec('ee',TE,DUR-TE,bg(W,H,1)+
  f'<div id="e1" style="position:absolute;left:0;right:0;top:520px;text-align:center">{logo(130,OR,True)}</div>'
  f'<div id="e2" style="position:absolute;left:64px;right:64px;top:820px;text-align:center;{F};font-weight:900;font-size:80px;line-height:1.05;color:{INKW}">Напишите<br><span style="{GRAD}">«ПАМЯТКА»</span><br>— пришлём PDF</div>'
  f'<div id="e3" style="position:absolute;left:64px;right:64px;top:1200px;text-align:center;{F};font-weight:700;font-size:38px;color:{SUB}">📌 Сохраните · покажите на приёме</div>'
  f'<div style="position:absolute;left:80px;right:80px;top:1440px;text-align:center;font-size:22px;line-height:1.5;color:{SUB}">Источники — в подписи к ролику. Не является медицинской консультацией.<br>Медицинские изделия. Применение — по назначению специалиста.</div>')
js+=f'tl.from("#e1",{{opacity:0,scale:.8,duration:.5}},{TE+.1}).from("#e2",{{opacity:0,y:30,duration:.5}},{TE+.6}).from("#e3",{{opacity:0,duration:.4}},{TE+1.2});'
ev+=[(TE,sfx.whoosh(.9,.3)),(TE+.1,sfx.boom(.5)),(TE+.6,sfx.chime(659,.18,3))]
chk=(T0+3.4,2.5,T0+FD+3.4,T0+2*FD+3.4,T0+3*FD+3.4,T0+4*FD+3.4,TF+3,TQ+5,TE+2.5)
shots=style_reel('nauka_fakty_reel',DUR,body,js,'Наука ухода — факты',ev,pad=(110,164.8,220,277.2),pad_amp=.03,check=chk,bg=BG,outdir=OUT)
strip(shots,'kp/chk_fakty.jpg',3000); print('ok',DUR)
