from gen_lib import TOP, dress, layers, page
S = []  # (filename, html)

def add(name, html):
    dark = 'fill dark' in html or 'background:#123A40;color' in html
    col = '#F5F1EA' if dark else '#0C1A1D'
    S.append((name, f'<div class="fill" style="color:{col}">{html}</div>'))

# ---------- POST 1 — HERO
add('p01_hero', f'''<div class="fill skinbg grain"></div>
<div class="ring" style="left:240px;top:420px;width:600px;height:600px;color:rgba(255,255,255,.35)"></div>
<div class="ring" style="left:160px;top:340px;width:760px;height:760px;color:rgba(255,255,255,.18)"></div>
{dress(330,510,420,'transform:rotate(-8deg)')}
{TOP('01','#0C1A1D')}
<div class="pad"><h1 class="h" style="font-size:132px;margin-top:70px"><span>Снимать —</span><span style="color:#fff">не ранить.</span></h1></div>
<div class="bot"><div class="body" style="font-size:30px;max-width:620px">Силиконовая пенная повязка <b>Silicare</b> для ран с умеренным и обильным экссудатом</div><div class="lab">yafho.com</div></div>''')

# ---------- POST 2 — CAROUSEL: 4 СЛОЯ (explainer)
LAY = [
 ('Слой 1 · контакт с кожей','Мягкий силикон','Бережно фиксируется на неповреждённой коже и не вклеивается в рану. Снятие — без вторичной травмы и лишней боли.'),
 ('Слой 2 · впитывание','Полиуретановая пена','Принимает экссудат и поддерживает влажную среду, в которой рана заживает.'),
 ('Слой 3 · удержание','Суперабсорбирующая подушка','Запирает жидкость внутри и не отдаёт её обратно — снижает риск мацерации краёв раны.'),
 ('Слой 4 · защита','Паропроницаемая ПУ-плёнка','Внешний барьер: защищает повязку снаружи и пропускает водяной пар — кожа «дышит».'),
]
add('p02_s1_cover', f'''<div class="fill dark"></div>
{layers(540,800,None,90,1.05)}
{TOP('02 · 1/6','#F5F1EA')}
<div class="pad"><div class="lab" style="color:#9FD3C5;margin-top:90px">Анатомия повязки</div><h1 class="h" style="font-size:96px;margin-top:28px"><span>4 слоя.</span><span style="color:#9FD3C5">Одна задача.</span></h1></div>
<div class="bot"><div class="body" style="font-size:28px;opacity:.7">Листайте, чтобы разобрать Silicare →</div></div>''')
for i,(lab,title,txt) in enumerate(LAY):
    add(f'p02_s{i+2}_layer{i+1}', f'''<div class="fill light"></div>
{layers(540,560,i,70,.95)}
{TOP(f'02 · {i+2}/6')}
<div class="pad" style="top:840px"><div class="lab" style="color:#E2573B">{lab}</div><h2 class="h" style="font-size:76px;margin-top:20px">{title}</h2><p class="body" style="margin-top:24px;font-size:32px;max-width:900px">{txt}</p></div>''')
add('p02_s6_summary', f'''<div class="fill mintbg grain"></div>
{TOP('02 · 6/6')}
<div class="pad" style="padding-top:220px">
<h2 class="h" style="font-size:84px"><span>Силикон держит кожу.</span><span>Пена держит влагу.</span><span style="color:#E2573B">Рана — в покое.</span></h2>
<div style="margin-top:80px;display:flex;flex-direction:column;gap:22px;font-size:32px">
<div>✓ Атравматичное снятие</div><div>✓ Влажная среда для заживления</div><div>✓ Запирает экссудат</div><div>✓ Паропроницаемая защита</div></div></div>
<div class="bot"><div class="body" style="font-size:28px">Спецификации и образцы — в директ</div><div class="lab">yafho.com</div></div>''')

# ---------- POST 4 — MOIST, NOT WET
add('p04_balance', f'''<div class="fill light"></div>
{TOP('04')}
<div style="position:absolute;left:110px;top:300px;width:400px;height:400px;border-radius:50%;background:radial-gradient(circle at 35% 30%,#E6F5F0,#9FD3C5)"></div>
<div style="position:absolute;left:570px;top:300px;width:400px;height:400px;border-radius:50%;border:3px dashed #E2573B;background:repeating-linear-gradient(-45deg,rgba(226,87,59,.10) 0 10px,transparent 10px 22px)"></div>
<div style="position:absolute;left:110px;top:730px;width:400px;text-align:center"><div class="lab" style="color:#123A40">Влажная среда</div><div class="body" style="font-size:28px;margin-top:10px">условие заживления</div></div>
<div style="position:absolute;left:570px;top:730px;width:400px;text-align:center"><div class="lab" style="color:#E2573B">Мацерация</div><div class="body" style="font-size:28px;margin-top:10px">размокшие края раны</div></div>
<div class="pad" style="top:900px"><h2 class="h" style="font-size:92px"><span>Влажно.</span><span style="color:#E2573B">Но не мокро.</span></h2></div>
<div class="bot"><div class="body" style="font-size:26px;max-width:760px;opacity:.75">Silicare удерживает экссудат внутри, сохраняя баланс влаги у раны</div></div>''')

# ---------- POST 5 — CAROUSEL: ПОКАЗАНИЯ
IND = [('Пролежни','Для пациентов с ограниченной подвижностью, когда повязку меняют регулярно и кожа вокруг особенно уязвима.'),
       ('Венозные язвы голени','Длительное лечение, обильное отделяемое и хрупкая кожа вокруг раны — именно здесь важно атравматичное снятие.'),
       ('Раны с умеренным и обильным экссудатом','Суперабсорбирующий слой запирает жидкость и помогает держать края раны сухими.')]
add('p05_s1_cover', f'''<div class="fill" style="background:#123A40;color:#F5F1EA"></div>
{TOP('05 · 1/4','#F5F1EA')}
{dress(560,560,380,'transform:rotate(12deg)')}
<div class="pad"><div class="lab" style="color:#9FD3C5;margin-top:90px">Показания</div><h1 class="h" style="font-size:96px;margin-top:28px;max-width:640px"><span>Где Silicare</span><span>работает</span><span style="color:#9FD3C5">лучше всего</span></h1></div>
<div class="bot"><div class="body" style="font-size:28px;opacity:.7">3 клинические ситуации →</div></div>''')
for i,(t,txt) in enumerate(IND):
    add(f'p05_s{i+2}', f'''<div class="fill light"></div>
{TOP(f'05 · {i+2}/4')}
<div class="num" style="position:absolute;right:60px;top:110px;font-size:440px;color:#CDEBE2;line-height:1">0{i+1}</div>
<div class="pad" style="top:640px"><h2 class="h" style="font-size:82px;max-width:900px">{t}</h2><p class="body" style="margin-top:30px;max-width:880px">{txt}</p></div>
<div class="bot"><div class="body" style="font-size:22px;opacity:.55">Применение — по назначению и под контролем медицинского специалиста</div></div>''')

# ---------- POST 6 — QUOTE (nurse)
add('p06_quote', f'''<div class="fill dark grain"></div>
{TOP('06','#F5F1EA')}
<div style="position:absolute;left:80px;top:250px;width:920px;height:4px;background:linear-gradient(90deg,#E2573B 0 40%,#9FD3C5 40%)"></div>
<div class="pad" style="top:320px"><h2 class="h" style="font-size:78px;line-height:1.05"><span style="opacity:.55">Для медсестры</span><span style="opacity:.55">смена повязки — процедура.</span><span style="margin-top:36px">Для пациента —</span><span style="color:#E2573B">самая тяжёлая минута дня.</span></h2>
<p class="body" style="margin-top:60px;max-width:860px;color:#CDEBE2">Silicare создан, чтобы эта минута стала тише.</p></div>''')

# ---------- POST 8 — CAROUSEL B2B
add('p08_s1', f'''<div class="fill mintbg"></div>
{TOP('08 · 1/3')}
<div class="pad" style="padding-top:260px"><div class="lab" style="color:#E2573B">Для бизнеса</div><h1 class="h" style="font-size:104px;margin-top:28px"><span>Дистрибьюторам</span><span>и клиникам</span></h1>
<p class="body" style="margin-top:40px;max-width:820px">Yafho — производитель силиконовых раневых покрытий. Работаем напрямую.</p></div>
{dress(640,900,300,'transform:rotate(-14deg)')}''')
add('p08_s2', f'''<div class="fill light"></div>
{TOP('08 · 2/3')}
<div class="pad" style="padding-top:220px"><h2 class="h" style="font-size:80px">Что вы получаете</h2>
<div style="margin-top:70px;display:grid;gap:40px">
<div style="display:flex;gap:30px"><div class="num" style="font-size:64px;color:#E2573B;width:90px">01</div><div><div style="font-size:38px;font-weight:700">Образцы для оценки</div><div class="body" style="font-size:28px;opacity:.7">Протестируйте в отделении до закупки</div></div></div>
<div style="display:flex;gap:30px"><div class="num" style="font-size:64px;color:#E2573B;width:90px">02</div><div><div style="font-size:38px;font-weight:700">Полная спецификация</div><div class="body" style="font-size:28px;opacity:.7">Состав, размеры, регистрационные документы</div></div></div>
<div style="display:flex;gap:30px"><div class="num" style="font-size:64px;color:#E2573B;width:90px">03</div><div><div style="font-size:38px;font-weight:700">Прямые поставки</div><div class="body" style="font-size:28px;opacity:.7">От производителя, без лишних звеньев</div></div></div>
<div style="display:flex;gap:30px"><div class="num" style="font-size:64px;color:#E2573B;width:90px">04</div><div><div style="font-size:38px;font-weight:700">Линейка решений</div><div class="body" style="font-size:28px;opacity:.7">Пенные повязки, контактные слои, нетканые повязки</div></div></div>
</div></div>''')
add('p08_s3', f'''<div class="fill dark"></div>
{TOP('08 · 3/3','#F5F1EA')}
<div class="pad" style="padding-top:240px"><h2 class="h" style="font-size:84px"><span>Три шага</span><span style="color:#9FD3C5">до поставки</span></h2>
<div style="margin-top:90px;display:flex;flex-direction:column;gap:0">
<div style="border-left:3px solid #9FD3C5;padding:0 0 60px 40px"><div class="lab" style="color:#9FD3C5">Шаг 1</div><div style="font-size:42px;font-weight:700;margin-top:10px">Напишите в директ</div></div>
<div style="border-left:3px solid #9FD3C5;padding:0 0 60px 40px"><div class="lab" style="color:#9FD3C5">Шаг 2</div><div style="font-size:42px;font-weight:700;margin-top:10px">Получите образцы и КП</div></div>
<div style="border-left:3px solid #E2573B;padding:0 0 0 40px"><div class="lab" style="color:#E2573B">Шаг 3</div><div style="font-size:42px;font-weight:700;margin-top:10px">Согласуем поставку</div></div></div></div>
<div class="bot"><div class="lab">yafho.com</div></div>''')

# ---------- POST 9 — CTA
add('p09_cta', f'''<div class="fill skinbg grain"></div>
{TOP('09')}
{dress(150,380,330,'transform:rotate(-10deg)')}{dress(430,520,330,'transform:rotate(6deg)')}{dress(640,330,300,'transform:rotate(18deg)')}
<div class="pad" style="top:920px"><h2 class="h" style="font-size:88px"><span>Проверьте сами.</span><span style="color:#fff">До закупки.</span></h2></div>
<div class="bot"><div class="body" style="font-size:30px">Образцы Silicare для клиник — по запросу в директ</div></div>''')

open('stills/index.html','w').write(page([h for _,h in S],1080,1350,'Yafho Silicare stills'))
open('stills/names.txt','w').write('\n'.join(n for n,_ in S))
print(len(S))
