from gen_lib import TOP, dress, layers, page
S=[]
def add(name, html, dark=False):
    S.append((name, f'<div class="fill" style="color:{"#F5F1EA" if dark else "#0C1A1D"}">{html}</div>'))
TAG = lambda t,bg,c='#0C1A1D': f'<div class="tag" style="background:{bg};color:{c}">{t}</div>'
T_EXP = TAG('#ПочемуТак','#9FD3C5')
T_NUM = TAG('#ВЦифрах','#E2573B','#fff')

# ===== 11 · POV «Будет больно?» (viral) 2 slides
add('v11_s1', f'''<div class="fill" style="background:#EDE7DE"></div>{TOP('11 · 1/2')}
<div class="lab" style="position:absolute;left:80px;top:200px;opacity:.6">POV: вы медсестра. Перевязка.</div>
<div class="bubble" style="position:absolute;left:80px;top:290px;background:#fff;box-shadow:0 10px 30px rgba(0,0,0,.08)">Будет больно?</div>
<div style="position:absolute;left:80px;top:440px;font-size:22px;opacity:.5">Пациентка, 81 год</div>
<div class="bubble" style="position:absolute;right:80px;top:560px;background:#0C1A1D;color:#F5F1EA;font-size:80px;letter-spacing:.1em;padding:20px 50px">• • •</div>
<div class="pad" style="top:900px"><h2 class="h" style="font-size:76px"><span>Самый честный ответ</span><span>зависит <span class="hl">не от вас.</span></span></h2></div>
<div class="bot"><div class="body" style="font-size:28px;opacity:.7">Листайте →</div></div>''')
add('v11_s2', f'''<div class="fill" style="background:#EDE7DE"></div>{TOP('11 · 2/2')}
<div class="bubble" style="position:absolute;left:80px;top:200px;background:#fff">Будет больно?</div>
<div class="bubble" style="position:absolute;right:80px;top:360px;background:#0C1A1D;color:#F5F1EA">Нет. Эта повязка на силиконе — она отпускает кожу.</div>
{dress(120,700,300,'transform:rotate(-10deg)')}
<div class="pad" style="top:1040px;padding-left:80px"><h2 class="h" style="font-size:64px"><span>Ответ зависит от того,</span><span style="color:#E2573B">что касается кожи.</span></h2></div>''')

# ===== 12 · Проблема в цифрах (proof) 4 slides
add('v12_s1', f'''<div class="fill dark"></div>{TOP('12 · 1/5','#F5F1EA')}
<div class="pad" style="top:200px">{T_NUM}<h1 class="h" style="font-size:118px;margin-top:40px"><span>Самая дорогая</span><span>минута</span><span style="color:#E2573B">в уходе за раной.</span></h1>
<p class="body" style="margin-top:50px;max-width:820px;opacity:.8">3 цифры, которые объясняют, почему смена повязки — это не мелочь.</p></div>
<div class="bot"><div class="body" style="font-size:28px;opacity:.6">Листайте →</div></div>''', True)
NUMS=[('40%','пациентов с хроническими ранами называют смену повязки <b>худшим</b> в жизни с раной','Price P. et al., Int Wound J, 2008 · опрос 2018 пациентов, 15 стран'),
      ('16%','взрослых пациентов реанимации получают повреждения кожи от медицинского клея (MARSI)','мета-анализ, J Wound Care, 2024 (объединённая частота у взрослых в ОРИТ)'),
      ('$26,8 млрд','в год — стоимость внутрибольничных пролежней только в США','Padula W. et al., Int Wound J, 2019')]
for i,(n,t,s) in enumerate(NUMS):
    add(f'v12_s{i+2}', f'''<div class="fill light"></div>{TOP(f'12 · {i+2}/5')}
<div class="num" style="position:absolute;left:70px;top:260px;font-size:{260 if len(n)<5 else 190}px;color:#E2573B;line-height:1;font-weight:500">{n}</div>
<div class="pad" style="top:620px"><p class="body" style="font-size:52px;line-height:1.18;font-weight:600;letter-spacing:-0.02em;max-width:900px">{t}</p></div>
<div class="bot"><div class="src">Источник: {s}</div></div>''')
add('v12_s5', f'''<div class="fill mintbg grain"></div>{TOP('12 · 5/5')}
<div class="pad" style="top:260px"><h2 class="h" style="font-size:96px"><span>Общий знаменатель&nbsp;—</span><span><span class="hl">кожа</span> вокруг раны.</span></h2>
<p class="body" style="margin-top:50px;max-width:880px">Боль, травма при снятии, мацерация — всё происходит в точке контакта повязки с кожей. Значит, и ключ к решению — там же.</p></div>
{dress(660,880,300,'transform:rotate(10deg)')}
<div class="bot"><div class="body" style="font-size:28px">Сохраните 📌</div></div>''')

# ===== 14 · Угадай (viral quiz) 3 slides
add('v14_s1', f'''<div class="fill" style="background:#E2573B"></div>{TOP('14 · 1/3','#fff')}
<div class="pad" style="top:200px;color:#fff"><div class="lab">Угадаете?</div><h1 class="h" style="font-size:88px;margin-top:30px"><span>Что пациенты</span><span>с хроническими ранами</span><span>называют самым тяжёлым?</span></h1>
<div style="margin-top:70px;display:flex;flex-direction:column;gap:22px">
<div class="chip" style="background:rgba(255,255,255,.18);color:#fff;font-size:38px;padding:22px 34px">A · Боль от самой раны</div>
<div class="chip" style="background:rgba(255,255,255,.18);color:#fff;font-size:38px;padding:22px 34px">B · Долгое лечение</div>
<div class="chip" style="background:rgba(255,255,255,.18);color:#fff;font-size:38px;padding:22px 34px">C · Смену повязки</div></div></div>
<div class="bot" style="color:#fff"><div class="body" style="font-size:28px">Ответ в комментарии — потом листайте →</div></div>''')
add('v14_s2', f'''<div class="fill dark"></div>{TOP('14 · 2/3','#F5F1EA')}
<div class="pad" style="top:220px"><div class="lab" style="color:#9FD3C5">Правильный ответ</div><h1 class="h" style="font-size:150px;margin-top:20px"><span class="hl">C.</span></h1>
<p class="body" style="margin-top:50px;font-size:54px;font-weight:600;line-height:1.15">Каждый 2–3-й пациент назвал смену повязки худшим в жизни с раной.</p>
<p class="body" style="margin-top:30px;opacity:.75">Не саму рану. Не сроки. Процедуру, которая должна помогать.</p></div>
<div class="bot"><div class="src">40,3% из 2018 пациентов · Price P. et al., Int Wound J, 2008</div></div>''', True)
add('v14_s3', f'''<div class="fill light"></div>{TOP('14 · 3/3')}
<div class="pad" style="top:200px"><h2 class="h" style="font-size:84px"><span>Почему?</span><span style="color:#E2573B">Повязку снимают</span><span style="color:#E2573B">вместе с кожей.</span></h2>
<p class="body" style="margin-top:50px;max-width:880px">Клей держится за клетки кожи крепче, чем они держатся друг за друга. Силиконовый контактный слой работает иначе — фиксирует и отпускает.</p></div>
{dress(620,860,320,'transform:rotate(-8deg)')}
<div class="bot"><div class="body" style="font-size:28px;max-width:520px">Отправьте коллеге, который угадал бы с первого раза</div></div>''')

# ===== 15 · Миф «рана должна дышать» (explain) 4 slides
add('v15_s1', f'''<div class="fill skinbg grain"></div>{TOP('15 · 1/4')}
<div class="pad" style="top:220px">{T_EXP}<h1 class="h" style="font-size:112px;margin-top:40px"><span>«Пусть рана</span><span>подышит</span><span>и подсохнет»</span></h1>
<div class="h" style="font-size:150px;margin-top:40px;color:#fff">— миф.</div></div>
<div class="bot"><div class="body" style="font-size:28px">Разбираемся →</div></div>''')
add('v15_s2', f'''<div class="fill light"></div>{TOP('15 · 2/4')}
<div class="num" style="position:absolute;left:70px;top:200px;font-size:240px;color:#9FD3C5;line-height:1">1962</div>
<div class="pad" style="top:520px"><h2 class="h" style="font-size:66px">Джордж Винтер закрыл одни раны плёнкой, а другие оставил на воздухе.</h2>
<p class="body" style="margin-top:36px">Под плёнкой, во влажной среде, новый эпителий нарастал примерно вдвое быстрее. Сухая корка — не защита, а преграда для заживления.</p></div>
<div class="bot"><div class="src">Winter G.D., Nature, 1962 · эксперимент на коже домашней свиньи</div></div>''')
add('v15_s3', f'''<div class="fill dark"></div>{TOP('15 · 3/4','#F5F1EA')}
<div class="pad" style="top:240px"><h2 class="h" style="font-size:96px"><span>Но есть подвох:</span><span style="color:#E2573B">лишняя влага</span><span style="color:#E2573B">тоже вредит.</span></h2>
<p class="body" style="margin-top:50px;max-width:880px;opacity:.85">Если экссудат остаётся у раны, края размокают — это мацерация. Кожа вокруг слабеет, и рана может расти.</p></div>
<div style="position:absolute;left:80px;right:80px;bottom:150px;height:24px;border-radius:12px;background:linear-gradient(90deg,#C99577 0%,#9FD3C5 40%,#9FD3C5 60%,#E2573B 100%)"></div>
<div style="position:absolute;left:80px;right:80px;bottom:90px;display:flex;justify-content:space-between;font-size:22px;opacity:.75"><span>сухо — корка</span><span style="color:#9FD3C5">оптимально</span><span style="color:#E2573B">мокро — мацерация</span></div>''', True)
add('v15_s4', f'''<div class="fill mintbg grain"></div>{TOP('15 · 4/4')}
{layers(540,470,None,60,.9)}
<div class="pad" style="top:820px"><h2 class="h" style="font-size:72px"><span>Задача повязки —</span><span>держать <span class="hl">баланс</span>.</span></h2>
<p class="body" style="margin-top:30px;font-size:32px">В Silicare пена поддерживает влажную среду у раны, а суперабсорбент забирает излишек и запирает его внутри.</p></div>''')

# ===== 17 · Насколько это помогает (proof) 4 slides
add('v17_s1', f'''<div class="fill dark"></div>{TOP('17 · 1/4','#F5F1EA')}
<div class="pad" style="top:200px">{T_NUM}<div class="lab" style="margin-top:50px;opacity:.7">Профилактика пролежней силиконовой пеной</div>
<h1 class="h" style="font-size:230px;margin-top:20px;color:#9FD3C5">Вдвое</h1><h2 class="h" style="font-size:72px">меньше пролежней?</h2>
<p class="body" style="margin-top:40px;opacity:.8">Что на самом деле говорит крупнейший обзор исследований — честно, с оговорками →</p></div>''', True)
add('v17_s2', f'''<div class="fill light"></div>{TOP('17 · 2/4')}
<div class="pad" style="top:180px"><div class="lab" style="color:#E2573B">Cochrane, 2024 · 18 исследований · 5903 пациента</div>
<h2 class="h" style="font-size:60px;margin-top:20px">Частота пролежней у пациентов группы риска</h2></div>
<div style="position:absolute;left:80px;right:80px;top:500px">
<div style="font-size:30px;font-weight:600">Без повязки</div><div style="margin-top:14px;height:110px;width:900px;background:#C99577;border-radius:14px;display:flex;align-items:center;padding-left:30px;font-size:44px;font-weight:700;color:#fff">100%</div>
<div style="font-size:30px;font-weight:600;margin-top:50px">С силиконовой пенной повязкой</div><div style="margin-top:14px;height:110px;width:450px;background:#9FD3C5;border-radius:14px;display:flex;align-items:center;padding-left:30px;font-size:44px;font-weight:700">≈50%</div></div>
<div class="pad" style="top:900px"><p class="body" style="font-size:28px">Относительный риск 0,50 (95% ДИ 0,33–0,77). Достоверность доказательств авторы оценивают как низкую — нужны новые исследования.</p></div>
<div class="bot"><div class="src">Patton D. et al. Dressings and topical agents for preventing pressure ulcers. Cochrane, 2024. Данные по классу силиконовых пенных повязок, не по конкретному бренду.</div></div>''')
CH=[('Проблема','Хрупкая кожа, давление, экссудат','#E2573B'),('Причина','Травма при снятии и мацерация краёв','#E2573B'),('Механизм','Силикон отпускает кожу · пена держит влагу · суперабсорбент запирает излишек','#123A40'),('Результат','Меньше вторичной травмы и боли при перевязке','#2E8C79')]
rows=''.join(f'<div style="display:flex;gap:30px;align-items:flex-start;padding:30px 0;border-top:2px solid rgba(12,26,29,.1)"><div class="lab" style="width:220px;color:{c};padding-top:10px">{a}</div><div style="font-size:40px;font-weight:600;line-height:1.2;flex:1">{b}</div></div>' for a,b,c in CH)
add('v17_s3', f'''<div class="fill light"></div>{TOP('17 · 3/4')}
<div class="pad" style="top:180px"><h2 class="h" style="font-size:76px">Как это работает</h2><div style="margin-top:50px">{rows}</div></div>''')
add('v17_s4', f'''<div class="fill" style="background:#123A40"></div>{TOP('17 · 4/4','#F5F1EA')}
<div class="pad" style="top:220px"><h2 class="h" style="font-size:76px"><span>Для клиник —</span><span style="color:#9FD3C5">меньше осложнений.</span><span style="margin-top:30px">Для дистрибьюторов&nbsp;—</span><span style="color:#E2A857">продукт, который решает</span><span style="color:#E2A857">измеримую проблему.</span></h2></div>
<div class="bot"><div class="body" style="font-size:30px">Образцы и спецификация — в директ</div><div class="lab">yafho.com</div></div>''', True)

# ===== 18 · Ключ (opportunity)
key = '''<div style="position:absolute;left:250px;top:330px;width:580px;height:300px">
<div style="position:absolute;left:0;top:0;width:300px;height:300px;border-radius:90px;background:linear-gradient(145deg,#ECFAF5,#9FD3C5);box-shadow:0 40px 80px -30px rgba(0,0,0,.6)"><div style="position:absolute;inset:70px;border-radius:50px;background:#0C1A1D"></div></div>
<div style="position:absolute;left:280px;top:115px;width:300px;height:70px;border-radius:0 20px 20px 0;background:linear-gradient(180deg,#ECFAF5,#9FD3C5)"></div>
<div style="position:absolute;left:470px;top:180px;width:40px;height:70px;background:#9FD3C5;border-radius:0 0 10px 10px"></div>
<div style="position:absolute;left:530px;top:180px;width:40px;height:50px;background:#9FD3C5;border-radius:0 0 10px 10px"></div></div>'''
add('v18_key', f'''<div class="fill dark grain"></div>{TOP('18','#F5F1EA')}{key}
<div class="pad" style="top:760px"><h2 class="h" style="font-size:80px"><span>Проблема на миллиарды</span><span>решается в точке</span><span style="color:#9FD3C5">толщиной в один слой.</span></h2>
<p class="body" style="margin-top:36px;opacity:.8;font-size:32px">Силиконовый контакт — ключ к перевязке без лишней травмы. Для рынка — возможность.</p></div>''', True)

open('v2s/index.html','w').write(page([h for _,h in S],1080,1350,'Yafho v2 stills'))
open('v2s/names.txt','w').write('\n'.join(n for n,_ in S)+'\n')
print(len(S))
