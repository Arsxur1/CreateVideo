from phonekit import *
from v9_common import run
ep=Ep()
days=[1,7,14,21,30,45,60,90,120]
def tile(i):
    k=i/8; r=int(205+28*k); g=int(80+110*k); b=int(95+85*k)
    return f'radial-gradient(ellipse 70% 18% at 50% 52%,rgb({r},{g},{b}) 0%,rgb({min(255,r+10)},{min(255,g+25)},{min(255,b+25)}) 45%,transparent 70%),linear-gradient(160deg,#E8C2A6,#D6A584)'
gallery(ep,0,4.2,'21:14','Шрам 📸',[(f'День {d}',tile(i)) for i,d in enumerate(days)])
ep.body+=f'<div class="clip" data-start="0" data-duration="4.2" data-track-index="2">{caption("hc","Я фотографирую свой шрам<br><span style=\"color:#F38221\">каждую неделю.</span>",1420)}<div style="position:absolute;left:0;right:0;top:1640px;text-align:center;font-size:24px;color:#777">иллюстрация</div></div>'
ep.js+='tl.from("#hc",{opacity:0,y:30,duration:.4},.6);'
ans=f'В практических рекомендациях {hl("силиконовые пластины и гели")} — первая линия ухода за рубцами.<br><br>Начинают на {hl("полностью зажившей коже")} и по рекомендации хирурга. Носят долго и регулярно — {hl("месяцами")}.'
search(ep,4.2,7.6,'21:20','как ухаживать за шрамом после операции',['…после маммопластики','…после абдоминопластики'],ans,'Meaume et al., 2014; памятки NHS',step=.055)
lockscreen(ep,11.8,4.6,'08:00','Понедельник, 6 неделя',[('НАПОМИНАНИЯ','Надеть силиконовую пластину ✨','Сегодня — 12 часов'),('СООБЩЕНИЯ','Хирург · Анна В.','Как шов? Пришлите фото в пятницу 🙂'),('НАПОМИНАНИЯ','Неделя 6 — фото шрама 📸','Тот же свет, тот же ракурс')],step=.8)
endcard(ep,16.4,4.6,'Хирург отвечает за шов.','Следующие полгода&nbsp;— за&nbsp;вами.','📺 Смотрите наш сериал «День 1 из 180»<br>🏥 Клиникам пластической хирургии — образцы в директ')
run('e3_plastika_shram_kazhduyu_nedelyu',ep,21.0,'Шрам каждую неделю',check=(2.5,1.0,9.8,14.5,19.0),pad=(87.3,130.8,174.6))
print('ok')
