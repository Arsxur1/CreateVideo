# Шаг 37: «Наука ухода» — карусель в стиле «ФАКТЫ» (1080×1350)
import os, shutil, glob
from factkit import *
from kp import _dir, _snap
from gen_lib import page
OUT='/home/user/CreateVideo/deliverables/yafho-silicare-instagram/v24_facts/posters'; os.makedirs(OUT,exist_ok=True)
W,H=1080,1350; N=9
S=[]
chips=''.join(f'<span style="display:inline-block;margin:0 14px 16px 0;padding:16px 30px;border-radius:40px;background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.16);{F};font-weight:900;font-size:44px;color:{INKW}">{b}</span>' for b,*_ in FACTS)
S.append(bg(W,H,0)+top(W,'НАУКА УХОДА · 2026')+
  f'<div style="position:absolute;left:58px;top:250px;{F};font-weight:900;font-size:220px;line-height:.86;letter-spacing:-0.05em;{GRAD}">5 фактов</div>'
  f'<div style="position:absolute;left:64px;right:64px;top:470px;{F};font-weight:800;font-size:66px;line-height:1.05;color:{INKW}">о повязках, которые<br>стоит знать <span style="color:{OR}">до выписки</span></div>'
  f'<div style="position:absolute;left:64px;right:64px;top:720px">{chips}</div>'
  f'<div style="position:absolute;left:64px;right:64px;top:930px;font-size:30px;line-height:1.4;color:{SUB}">Каждая цифра — с источником и честной пометкой,<br>насколько уверены учёные.</div>'
  f'<div style="position:absolute;right:64px;bottom:80px;{M};font-size:28px;color:{OR}">ЛИСТАЙТЕ →</div>')
for i,(big,tgt,fmt,st,src,gr,kind) in enumerate(FACTS):
    ey={'bars':720,'d16':720,'d40':720,'press':720,'steps':740}[kind]
    S.append(fact(W,H,f'ФАКТ {i+1:02d} / 05',big,st,src,gr,extra(kind,W),v=i,num_y=170,stat_y=480,extra_y=ey,foot_y=1110,
             big_px=300 if len(big)<=3 else 260))
fl=''.join(f'<div style="display:flex;align-items:center;gap:22px;margin-top:22px"><span style="width:20px;height:20px;border-radius:50%;background:{RED};box-shadow:0 0 18px {RED}"></span><span style="{F};font-weight:800;font-size:46px;color:{INKW}">{t}</span></div>' for t in RED_FLAGS)
S.append(bg(W,H,1)+top(W,'ВАЖНО')+
  f'<div style="position:absolute;left:58px;top:180px;{F};font-weight:900;font-size:150px;line-height:.9;letter-spacing:-0.04em;color:{RED}">Сразу<br>к врачу,</div>'
  f'<div style="position:absolute;left:64px;top:470px;{F};font-weight:800;font-size:54px;color:{INKW}">если:</div><div style="position:absolute;left:64px;top:540px">{fl}</div>'
  f'<div style="position:absolute;left:64px;right:64px;top:1020px">{glass("Повязка не лечит инфекцию и не заменяет осмотр врача.<br>Признаки — общие рекомендации NHS.",pad="18px 26px",r=24)}</div>')
qs=''.join(f'<div style="display:flex;gap:26px;align-items:baseline;margin-top:{0 if k==0 else 28}px"><span style="{M};font-size:30px;color:{OR}">{k+1:02d}</span><span style="{F};font-weight:800;font-size:44px;line-height:1.15;color:{INKW}">{q}</span></div>' for k,q in enumerate(QUESTIONS))
S.append(bg(W,H,0)+top(W,'ЧЕК-ЛИСТ')+
  f'<div style="position:absolute;left:58px;top:170px;{F};font-weight:900;font-size:120px;line-height:.92;letter-spacing:-0.04em;{GRAD}">5 вопросов</div>'
  f'<div style="position:absolute;left:64px;top:300px;{F};font-weight:800;font-size:56px;color:{INKW}">врачу при выписке</div>'
  f'<div style="position:absolute;left:64px;right:64px;top:420px;padding:44px;border-radius:36px;background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.14)">{qs}</div>'
  f'<div style="position:absolute;left:64px;top:1150px;{F};font-weight:800;font-size:36px;color:{INKW}">📌 Сохраните · покажите на приёме</div>')
src=''.join(f'<div style="display:flex;gap:18px;margin-top:20px"><span style="{M};font-size:22px;color:{OR}">[{k+1}]</span><span style="font-size:25px;line-height:1.4;color:{SUB}">{s}</span></div>' for k,s in enumerate(SOURCES))
S.append(bg(W,H,1)+top(W,'ИСТОЧНИКИ')+f'<div style="position:absolute;left:64px;right:64px;top:180px">{src}</div>'
  f'<div style="position:absolute;left:64px;right:64px;top:930px;{F};font-weight:900;font-size:64px;line-height:1.05;color:{INKW}">Напишите <span style="{GRAD}">«ПАМЯТКА»</span><br>— пришлём PDF</div>'
  f'<div style="position:absolute;left:64px;right:64px;bottom:60px;font-size:20px;color:{SUB}">Медицинские изделия. Применение — по назначению специалиста. Не является медицинской консультацией.</div>')
d=_dir('v24_facts_posters')
open(os.path.join(d,'index.html'),'w').write(page(S,W,H,'Наука ухода — факты'))
shots=_snap(d,[i+.5 for i in range(len(S))])[:len(S)]
for f in glob.glob(f'{OUT}/*.png'): os.remove(f)
for i,sh in enumerate(shots): shutil.copy(sh,f'{OUT}/fact_{i+1:02d}.png')
from PIL import Image
G=Image.new('RGB',(5*432+40,2*540+10),(20,20,20))
for i,sh in enumerate(shots): G.paste(Image.open(sh).convert('RGB').resize((432,540)),((i%5)*442,(i//5)*550))
G.save(f'{OUT}/../posters_sheet.jpg',quality=88); print('ok',len(shots))
