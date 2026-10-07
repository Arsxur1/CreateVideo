from gen_lib import dress, layers, page
B = lambda c: f'<div class="brand" style="position:absolute;left:90px;top:110px;color:{c}">Yafho <i>· Silicare</i></div>'
S = [
f'''<div class="fill dark" style="color:#F5F1EA"><div class="fill dark"></div>{B('#F5F1EA')}
<div class="pad" style="top:420px;padding:0 90px"><div class="lab" style="color:#9FD3C5">Опрос</div><h1 class="h" style="font-size:96px;margin-top:30px"><span>Что важнее всего</span><span>при выборе</span><span style="color:#9FD3C5">повязки?</span></h1></div>
<div style="position:absolute;left:90px;right:90px;top:1180px;height:300px;border:2px dashed rgba(245,241,234,.35);border-radius:30px;display:grid;place-items:center;font-size:26px;opacity:.6">[ место для стикера «Опрос»: Снятие без боли / Впитываемость ]</div></div>''',
f'''<div class="fill" style="color:#0C1A1D"><div class="fill light"></div>{B('#0C1A1D')}
{layers(540,760,0,60,1.2)}
<div class="pad" style="top:1130px;padding:0 90px"><div class="lab" style="color:#E2573B">Тест</div><h2 class="h" style="font-size:80px;margin-top:20px"><span>Какой слой касается</span><span>кожи пациента?</span></h2></div>
<div style="position:absolute;left:90px;right:90px;top:1460px;height:260px;border:2px dashed rgba(12,26,29,.3);border-radius:30px;display:grid;place-items:center;font-size:26px;opacity:.6">[ стикер «Викторина»: Пена / Силикон ✓ / Плёнка ]</div></div>''',
f'''<div class="fill" style="color:#0C1A1D"><div class="fill skinbg grain"></div>{B('#0C1A1D')}
{dress(330,480,420,'transform:rotate(-8deg)')}
<div class="pad" style="top:1080px;padding:0 90px"><h2 class="h" style="font-size:104px"><span>Образцы</span><span style="color:#fff">для вашей клиники</span></h2><p class="body" style="margin-top:30px">Напишите нам — пришлём Silicare на оценку</p></div>
<div style="position:absolute;left:90px;right:90px;top:1600px;height:150px;border:2px dashed rgba(12,26,29,.35);border-radius:30px;display:grid;place-items:center;font-size:26px;opacity:.6">[ стикер «Ссылка» → yafho.com ]</div></div>''',
]
open('stories/index.html','w').write(page(S,1080,1920,'Yafho stories'))
