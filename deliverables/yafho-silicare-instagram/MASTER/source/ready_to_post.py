# Шаг 17: пакет «Готово к публикации» — папка на каждый день
# По умолчанию кладёт только тексты и обложки (медиа остаются на своих местах в репозитории).
# С флагом --with-media OUT_DIR копирует и сами ролики/слайды — для загрузки с телефона/компьютера.
import csv, os, shutil, sys, glob, re
D='/home/user/CreateVideo/deliverables/yafho-silicare-instagram'; os.chdir(D)
media_out=sys.argv[sys.argv.index('--with-media')+1] if '--with-media' in sys.argv else None
OUT=media_out or 'READY_TO_POST'
cal={r['date']:r for r in csv.DictReader(open('MASTER/master_calendar.csv'))}
cap=list(csv.DictReader(open('MASTER/captions.csv')))
if os.path.isdir(OUT) and not media_out: shutil.rmtree(OUT)
idx=['# Готово к публикации','','Папка на каждый день. Порядок публикации:','1. Откройте `post.txt` и скопируйте подпись (хэштеги уже внутри).','2. Загрузите медиа из пути `media` в `post.txt` (или из этой папки, если пакет собран с `--with-media`).','3. Reels: обложка — `cover.jpg` (вариант A теста; B/C лежат рядом для смены через 72 ч). «Обрезка в профиле» — проверить.','4. «Расширенные настройки → Специальные возможности» → вставьте alt-текст.','5. Сразу после публикации — первый комментарий из `post.txt`.','6. Сторис дня — см. `stories.txt` (если есть).','',
     '| Дата | Папка | Формат | Публикация | ⚠ |','|---|---|---|---|---|']
ST={'12.10':'st01','13.10':'st02','16.10':'st03','19.10':'st04','20.10':'st05','22.10':'st06','25.10':'st07','26.10':'st08','30.10':'st09','02.11':'st10','04.11':'st11','05.11':'st12','09.11':'st13','10.11':'st14','12.11':'st15','16.11':'st16','19.11':'st17','22.11':'st18'}
AB={'m1_manifest_cinematic':'m1_manifest','m2_pismo_shramu_cinematic':'m2_pismo','m3_risovaya_bumaga_cinematic':'m3_bumaga','m4_persik_cinematic':'m4_persik','m5_lepestok_cinematic':'m5_lepestok','e1_akusherstvo_3_den_doma':'e1_kesarevo','e2_neonatologiya_dnevnik_oritn':'e2_oritn','e3_plastika_shram_kazhduyu_nedelyu':'e3_shram','e4_dermatologiya_deti_babochki':'e4_babochki','e5_hirurgiya_pov_medsestra':'e5_medsestra'}
for c in cap:
    r=cal[c['date']]; p=c['file']; slug=os.path.basename(p.rstrip('/')).replace('.png','')
    d=f"{OUT}/{c['date']}_{slug}"; os.makedirs(d,exist_ok=True)
    media=sorted(glob.glob(p+'/*.mp4')) or sorted(glob.glob(p+'/slide*.png'),key=lambda s:int(re.findall(r'\d+',os.path.basename(s))[0])) or [p]
    txt=[f"{r['weekday']} {c['date']} · {r['format']} · {r['title']}",'',f"media: {', '.join(media)}",'','=== ПОДПИСЬ ===',c['caption'],'','=== ПЕРВЫЙ КОММЕНТАРИЙ ===',c['first_comment'] or '—','','=== ALT-ТЕКСТ ===',c['alt_text']]
    if 'c2_overlei' in p: txt+=['','=== КАК СОБРАТЬ ВЫПУСК ===','1. Снять 7 с видео рубца: тот же ракурс и свет, что в прошлых выпусках, без ретуши (письменное согласие пациентки).','2. В CapCut/InShot положить PNG-оверлей поверх видео на всю длину (у оверлея прозрачный фон).','3. Экспорт 1080×1920, 30 к/с. Подпись — выше, в блоке «ПОДПИСЬ».']
    if c['check']: txt+=['','=== ⚠ ПРОВЕРИТЬ ДО ПУБЛИКАЦИИ ===',c['check']]
    open(f'{d}/post.txt','w').write('\n'.join(txt)+'\n')
    if slug in AB:
        for v in 'ABC': shutil.copy(f'v10_ab_covers/{AB[slug]}_{v}.jpg',f'{d}/cover_{v}.jpg')
        shutil.copy(f'{d}/cover_A.jpg',f'{d}/cover.jpg')
    elif os.path.exists(p+'/cover.png'):
        from PIL import Image; Image.open(p+'/cover.png').convert('RGB').save(f'{d}/cover.jpg',quality=88)
    dm=c['date'][8:10]+'.'+c['date'][5:7]
    if dm in ST:
        s=glob.glob(f'v13_stories/{ST[dm]}_*.png')[0]
        open(f'{d}/stories.txt','w').write(f'Сторис дня: {s}\nНастройки стикера — v13_stories/README.md, строка {ST[dm]}.\n+ репост публикации в сторис со стикером-ссылкой.\n')
    if media_out:
        for i,m in enumerate(media): shutil.copy(m,f'{d}/{i+1:02d}_{os.path.basename(m)}')
    idx.append(f"| {r['weekday']} {dm} | `{os.path.basename(d)}` | {r['format']} | {r['title']} | {'⚠' if c['check'] else ''} |")
open(f'{OUT}/README.md','w').write('\n'.join(idx)+'\n')
print('folders',len(cap),'->',OUT)
