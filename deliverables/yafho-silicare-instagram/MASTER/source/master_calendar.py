# Шаг 11: единый мастер-календарь по всем версиям (v3…v12)
import os, csv, datetime as dt
from PIL import Image, ImageDraw, ImageFont
D='/home/user/CreateVideo/deliverables/yafho-silicare-instagram'; M=f'{D}/MASTER'
WD=['Пн','Вт','Ср','Чт','Пт','Сб','Вс']
# ключ -> (тип, название, рубрика, путь к материалу, превью, A/B-обложки)
A={
 'm1':('Reel','Манифест «Твоя кожа помнит всё»','Манифест','v7_cinematic/m1_manifest_cinematic','v7_cinematic/m1_manifest_cinematic/cover.png','m1_manifest'),
 'm2':('Reel','«Письмо шраму» (кино) + старт #ПисьмоШраму','🤱 Акушерство','v7_cinematic/m2_pismo_shramu_cinematic','v7_cinematic/m2_pismo_shramu_cinematic/cover.png','m2_pismo'),
 'm3':('Reel','«Тест на рисовой бумаге» (кино)','🦋 Дерматология','v7_cinematic/m3_risovaya_bumaga_cinematic','v7_cinematic/m3_risovaya_bumaga_cinematic/cover.png','m3_bumaga'),
 'm4':('Reel','«Персиковый тест» (кино)','🍑 Гериатрия','v7_cinematic/m4_persik_cinematic','v7_cinematic/m4_persik_cinematic/cover.png','m4_persik'),
 'm5':('Reel','«Тоньше лепестка» (кино)','👶 Неонатология','v7_cinematic/m5_lepestok_cinematic','v7_cinematic/m5_lepestok_cinematic/cover.png','m5_lepestok'),
 'e1':('Reel','«3-й день дома после кесарева» (телефон)','🤱 Акушерство','v9_series/e1_akusherstvo_3_den_doma','v9_series/e1_akusherstvo_3_den_doma/cover.png','e1_kesarevo'),
 'e2':('Reel','«Дневник ОРИТН» (телефон)','👶 Неонатология','v9_series/e2_neonatologiya_dnevnik_oritn','v9_series/e2_neonatologiya_dnevnik_oritn/cover.png','e2_oritn'),
 'e3':('Reel','«Шрам каждую неделю» (телефон)','✨ Пластика','v9_series/e3_plastika_shram_kazhduyu_nedelyu','v9_series/e3_plastika_shram_kazhduyu_nedelyu/cover.png','e3_shram'),
 'e4':('Reel','«Дети-бабочки» (телефон)','🦋 Дерматология','v9_series/e4_dermatologiya_deti_babochki','v9_series/e4_dermatologiya_deti_babochki/cover.png','e4_babochki'),
 'e5':('Reel','«POV: ты медсестра» (телефон)','🩺 Хирургия','v9_series/e5_hirurgiya_pov_medsestra','v9_series/e5_hirurgiya_pov_medsestra/cover.png','e5_medsestra'),
 'e6':('Reel','«Под лупой: линейка» (B2B)','📦 B2B','v9_series/e6_b2b_pod_lupoi_lineika','v9_series/e6_b2b_pod_lupoi_lineika/cover.png',''),
 'k1':('Reel','Кинетика: акушерство','🤱 Акушерство','v12_kinetic/k1_akusherstvo','v12_kinetic/k1_akusherstvo/cover.png',''),
 'k2':('Reel','Кинетика: неонатология','👶 Неонатология','v12_kinetic/k2_neonatologiya','v12_kinetic/k2_neonatologiya/cover.png',''),
 'k3':('Reel','Кинетика: пластика','✨ Пластика','v12_kinetic/k3_plastika','v12_kinetic/k3_plastika/cover.png',''),
 'k4':('Reel','Кинетика: дети-бабочки','🦋 Дерматология','v12_kinetic/k4_babochki','v12_kinetic/k4_babochki/cover.png',''),
 'k5':('Reel','Кинетика: хирургия','🩺 Хирургия','v12_kinetic/k5_hirurgiya','v12_kinetic/k5_hirurgiya/cover.png',''),
 'k6':('Reel','Кинетика: пролежни','🍑 Гериатрия','v12_kinetic/k6_geriatriya','v12_kinetic/k6_geriatriya/cover.png',''),
 'l1':('Reel','Под лупой №1: Wound Contact Layer','📦 Продукт','v11_pod_lupoi/l1_wcl','v11_pod_lupoi/l1_wcl/cover.png',''),
 'l2':('Reel','Под лупой №2: Scar Sheet','📦 Продукт','v11_pod_lupoi/l2_scar','v11_pod_lupoi/l2_scar/cover.png',''),
 'l3':('Reel','Под лупой №3: Nonwoven','📦 Продукт','v11_pod_lupoi/l3_nonwoven','v11_pod_lupoi/l3_nonwoven/cover.png',''),
 'l4':('Reel','Под лупой №4: Hydrogel','📦 Продукт','v11_pod_lupoi/l4_hydrogel','v11_pod_lupoi/l4_hydrogel/cover.png',''),
 'l5':('Reel','Под лупой №5: Hydrocolloid','📦 Продукт','v11_pod_lupoi/l5_hydrocolloid','v11_pod_lupoi/l5_hydrocolloid/cover.png',''),
 'l6':('Reel','Под лупой №6: CHG I.V. Fixation','📦 Продукт','v11_pod_lupoi/l6_chg','v11_pod_lupoi/l6_chg/cover.png',''),
 's1':('Reel','Кинетика «СТОП. Ты срываешь пластырь»','Манифест','v8_styles/s1_kinetic_type','v8_styles/s1_kinetic_type/cover.png',''),
 's3':('Reel','Бумажный коллаж','Манифест','v8_styles/s3_paper_collage','v8_styles/s3_paper_collage/cover.png',''),
 's4':('Reel','Под лупой: 5 слоёв Sili-Care','📦 Продукт','v8_styles/s4_macro_asmr','v8_styles/s4_macro_asmr/cover.png',''),
 'a1':('Карусель','«Её первый шрам»','🤱 Акушерство','v6_campaign/a1_ee_pervyi_shram','v6_campaign/a1_ee_pervyi_shram/slide1.png',''),
 'a3':('Карусель','«7 вещей после кесарева»','🤱 Акушерство','v6_campaign/a3_7_veshchei_posle_kesareva','v6_campaign/a3_7_veshchei_posle_kesareva/slide1.png',''),
 'b2':('Карусель','«2–3 слоя» для медсестёр ОРИТН ⚠ сверить цифру','👶 Неонатология','v6_campaign/b2_oritn_2_sloya','v6_campaign/b2_oritn_2_sloya/slide1.png',''),
 'c1':('Reel','«День 1 из 180» — старт сериала','✨ Пластика','v6_campaign/c1_den_1_iz_180','v6_campaign/c1_den_1_iz_180/cover.png',''),
 'c3':('Карусель','«Как носить пластину»','✨ Пластика','v6_campaign/c3_kak_nosit_plastinu','v6_campaign/c3_kak_nosit_plastinu/slide1.png',''),
 'd1':('Reel','«Хирург vs медсестра»','🩺 Хирургия','v6_campaign/d1_hirurg_vs_medsestra','v6_campaign/d1_hirurg_vs_medsestra/cover.png',''),
 'd2':('Карусель','«Шов зажил» (MARSI)','🩺 Хирургия','v6_campaign/d2_shov_zazhil','v6_campaign/d2_shov_zazhil/slide1.png',''),
 'eb':('Фото','Фото-манифест «Крыло бабочки» — старт недели БЭ','🦋 Дерматология','v6_campaign/e2_foto_manifest_babochka','v6_campaign/e2_foto_manifest_babochka/slide1.png',''),
 'ec':('Карусель','«Кто такие дети-бабочки» ⚠ ссылка на фонд','🦋 Дерматология','v6_campaign/e3_kto_takie_deti_babochki','v6_campaign/e3_kto_takie_deti_babochki/slide1.png',''),
 'f1':('Карусель','UGC «Нарисуем одной линией»','✍️ UGC','v6_campaign/f1_narisuem_odnoi_liniei','v6_campaign/f1_narisuem_odnoi_liniei/slide1.png',''),
 'f2':('Карусель','Итоги #ПисьмоШраму (заполнить работами)','✍️ UGC','v6_campaign/f2_shablon_itogi_pismo_shramu','v6_campaign/f2_shablon_itogi_pismo_shramu/slide1.png',''),
 'g1':('Reel','«Линейка Yafho за 30 секунд»','📦 B2B','v6_campaign/g1_katalog_za_30_sekund','v6_campaign/g1_katalog_za_30_sekund/cover.png',''),
 'ol':('Карусель','«Одна линия — 6 отделений»','📦 B2B','v5_platform/carousel_odna_liniya','v5_platform/carousel_odna_liniya/slide1.png',''),
 'pk':('Пост','Постер «Твоя кожа помнит всё»','Манифест','v7_cinematic/posters/poster_kozha_pomnit_vsyo.png','v7_cinematic/posters/poster_kozha_pomnit_vsyo.png',''),
 'p3':('Пост','Постер «03:47»','🤱 Акушерство','v7_cinematic/posters/poster_0347_pismo_shramu.png','v7_cinematic/posters/poster_0347_pismo_shramu.png',''),
}
C1=dt.date(2026,10,30)  # старт сериала «День 1 из 180»
for n in (7,14,21,30,45,60,90,120,150,180):
    p=f'v6_campaign/c2_overlei_serii/overlay_den_{n:03d}.png'
    A[f'c{n}']=('Reel',f'Сериал «День {n} из 180» (реальное видео + оверлей)','✨ Пластика',p,p,'')
S0=dt.date(2026,10,12)
WEEKS=[ # 7 слотов Пн..Вс; None = пауза
 ('Неделя 1 · «Кожа помнит»: манифест и персик',['m1','k6','a1','s4','m4','k1','a3']),
 ('Неделя 2 · Акушерство и неонатология',['m2','e1','m5','k2','b2','e2','eb']),
 ('Неделя 3 · Неделя БЭ (25–31.10) + старт пластики',['m3','e4','ec','k4','c1','e3','l2']),
 ('Неделя 4 · Хирургия и медсёстры',['k5','e5','d1','d2','c7','l1','f1']),
 ('Неделя 5 · B2B: клиники и дистрибьюторы',['e6','l6','ol','g1','c14','l3','f2']),
 ('Неделя 6 · Манифест-2 и продукты',['s1','l4','s3','c3','c21','l5','pk']),
 ('Неделя 7 · Повтор победителей A/B',['k3',None,'p3',None,None,'c30',None]),
]
rows=[]
for w,(title,slots) in enumerate(WEEKS):
    for i,k in enumerate(slots):
        if not k: continue
        d=S0+dt.timedelta(days=w*7+i); rows.append((d,w,title,k))
for n in (45,60,90,120,150,180):
    rows.append((C1+dt.timedelta(days=n-1),99,'Дальше: сериал «День N из 180» (выходит ровно в день N)',f'c{n}'))
# проверки
for d,w,t,k in rows:
    if 'c2_overlei' in A[k][3]: assert abs((d-(C1+dt.timedelta(days=int(k[1:])-1))).days)<=1,(k,d)
miss=[k for _,_,_,k in rows if not os.path.exists(f'{D}/{A[k][3]}')]
assert not miss, miss
used={k for *_,k in rows}
# MD
last=max(r[0] for r in rows)
L=[f'# Мастер-календарь Yafho · Instagram ({S0:%d.%m.%Y} → {last:%d.%m.%Y})','',
 'Один план вместо пяти: собраны все готовые материалы v3…v12. Где у одной идеи есть несколько версий, в план идёт сильнейшая (кино v7 вместо плоских v5/v6, телефон v9 вместо пилота s2). Остальные лежат в резерве.','',
 '**Ритм:** 6–7 публикаций в неделю. Пн — главный Reel недели, Вт/Чт — короткие (телефон, кинетика), Ср/Вс — карусели и сохраняемое, Сб — «Под лупой». Пятница — сериал «День N из 180», как только он стартует.','',
 '**Обложки:** у ролика с меткой 🅰🅱 есть 3 варианта в `v10_ab_covers/` — порядок теста описан в его README.','',
 '**Ключевые даты:** 25–31.10 — неделя буллёзного эпидермолиза · 30.10 — старт сериала «День 1 из 180» · 02.11 — начало B2B-блока.','']
cur=None
for d,w,t,k in sorted(rows):
    if t!=cur:
        L+=['',f'## {t}','','| Дата | Формат | Публикация | Рубрика | Файл | Обложки |','|---|---|---|---|---|---|']; cur=t
    ty,name,rub,path,_,ab=A[k]
    bold='**' if dt.date(2026,10,25)<=d<=dt.date(2026,10,31) else ''
    L.append(f'| {bold}{WD[d.weekday()]} {d:%d.%m}{bold} | {ty} | {name} | {rub} | `{path}` | {"🅰🅱 "+ab if ab else ""} |')
res=[k for k in A if k not in used]
L+=['','## Резерв (готово, но не в сетке)','']+[f'- `{A[k][3]}` — {A[k][1]}' for k in res]+[
 '- `v8_styles/s2_phone_3_nochi` — пилот, его заменил e1 (v9)',
 '- `v5_platform/reel_manifest_kozha_pomnit.mp4`, `v3_peach/reel_persikovyi_test.mp4`, `v6_campaign/a2_pismo_shramu`, `v6_campaign/b1_lepestok`, `v6_campaign/e1_test_risovaya_bumaga` — плоские версии, их заменили кино-ролики m1–m5',
 '- `v1/`, `v2/` — первые наброски: в ленту не идут, годятся для сторис',
 '','## До публикации — чек-лист',
 '- [ ] Ссылка на фонд-партнёр для детей-бабочек (e4, ec, k4, m3) — до 20.10',
 '- [ ] Сверить неонатальную цифру «2–3 слоя» (b2, m5, обложка m5_B) — до 19.10, иначе b2 снять',
 '- [ ] Акушер проверяет «7 вещей после кесарева» (a3) и e1 — до 15.10',
 '- [ ] Назначение Reco Dressing Kit (в план не включён до ответа)',
 '- [ ] Конструкция CHG I.V. Fixation (l6) сверена с каталогом — до 06.11',
 '- [ ] Согласия пациентов на реальные видео сериала «День N из 180» — до 30.10',
 '- [ ] Звук прослушан на телефоне (громкость проверена только по метрике)',
 '','## Метрики по неделям',
 '| Что смотрим | Где | Цель |','|---|---|---|',
 '| Досмотр первых 3 с | Reels-инсайты | > 60% |','| Репосты / охват | Reels | > 1% |','| Сохранения | карусели | > 2% |',
 '| Директ «КАТАЛОГ» / «ЛУПА» | директ | считать по кодовому слову |','| CTR из профиля по обложкам A/B/C | профиль | выбрать тип-победитель к неделе 7 |']
open(f'{M}/MASTER_CALENDAR.md','w').write('\n'.join(L)+'\n')
with open(f'{M}/master_calendar.csv','w',newline='') as f:
    wr=csv.writer(f); wr.writerow(['date','weekday','week','format','title','rubric','file','ab_covers'])
    for d,w,t,k in sorted(rows): ty,name,rub,path,_,ab=A[k]; wr.writerow([d.isoformat(),WD[d.weekday()],t,ty,name,rub,path,ab])
# визуальная сетка
TW,TH=180,320; F='/usr/share/fonts/opentype/inter/InterDisplay-Bold.otf'
f1=ImageFont.truetype(F,22); f2=ImageFont.truetype(F,16)
G=Image.new('RGB',(60+7*(TW+10),60+len(WEEKS)*(TH+70)),(18,18,18)); g=ImageDraw.Draw(G)
for i,wd in enumerate(WD): g.text((60+i*(TW+10)+TW/2-12,20),wd,font=f1,fill=(243,130,33))
for w,(title,slots) in enumerate(WEEKS):
    y=60+w*(TH+70); g.text((60,y),title,font=f1,fill=(230,230,230))
    for i,k in enumerate(slots):
        x=60+i*(TW+10); d=S0+dt.timedelta(days=w*7+i)
        g.text((x,y+32),f'{d:%d.%m}',font=f2,fill=(160,160,160))
        if not k: g.rectangle([x,y+56,x+TW,y+56+TH-30],outline=(60,60,60)); continue
        im=Image.open(f'{D}/{A[k][4]}').convert('RGB'); im.thumbnail((TW,TH-30))
        G.paste(im,(x+(TW-im.width)//2,y+56))
        g.text((x+4,y+56+TH-56),A[k][0],font=f2,fill=(243,130,33))
G.save(f'{M}/calendar_preview.jpg',quality=85)
print('rows',len(rows),'reserve',len(res))
