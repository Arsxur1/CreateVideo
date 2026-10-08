import os, subprocess
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
D='/home/user/CreateVideo/deliverables/yafho-silicare-instagram'
OUT=f'{D}/v10_ab_covers'; os.makedirs(OUT,exist_ok=True)
FB='/usr/share/fonts/opentype/inter/InterDisplay-Black.otf'
if not os.path.exists(FB): FB='/usr/share/fonts/opentype/inter/InterDisplay-Bold.otf'
FM='/usr/share/fonts/opentype/inter/InterDisplay-SemiBold.otf'
if not os.path.exists(FM): FM='/usr/share/fonts/opentype/inter/Inter-SemiBold.otf'
OR=(243,130,33); WH=(255,255,255)
R=[ # name, video, t, [(variant, line1, line2, tag)]
 ('m1_manifest',f'{D}/v7_cinematic/m1_manifest_cinematic/m1_manifest_cinematic.mp4',4.6,[('A','Что помнит','твоя кожа?','вопрос'),('B','6 историй.','1 линия.','факт'),('C','Твоя кожа','помнит всё.','эмоция')]),
 ('m2_pismo',f'{D}/v7_cinematic/m2_pismo_shramu_cinematic/m2_pismo_shramu_cinematic.mp4',8.5,[('A','Что бы ты','сказала шраму?','вопрос'),('B','03:47.','Тот самый день.','факт'),('C','Привет,','шрам.','эмоция')]),
 ('m3_bumaga',f'{D}/v7_cinematic/m3_risovaya_bumaga_cinematic/m3_risovaya_bumaga_cinematic.mp4',6.4,[('A','Выдержит ли','лист?','вопрос'),('B','Кожа тонкая','как бумага','факт'),('C','Для них это','каждый день.','эмоция')]),
 ('m4_persik',f'{D}/v7_cinematic/m4_persik_cinematic/m4_persik_cinematic.mp4',8.4,[('A','Что пластырь','сделает с персиком?','вопрос'),('B','Сутки спустя:','кожица порвана','факт'),('C','Это кожа','вашей бабушки.','эмоция')]),
 ('m5_lepestok',f'{D}/v7_cinematic/m5_lepestok_cinematic/m5_lepestok_cinematic.mp4',6.2,[('A','Тоньше','лепестка?','вопрос'),('B','2–3 слоя','клеток','факт'),('C','Её первое','прикосновение.','эмоция')]),
 ('e1_kesarevo',f'{D}/v9_series/e1_akusherstvo_3_den_doma/e1_akusherstvo_3_den_doma.mp4',6.5,[('A','Больно смеяться','после кесарева?','вопрос'),('B','1 из 5 родов —','кесарево','факт'),('C','3 часа ночи.','3-й день дома.','эмоция')]),
 ('e2_oritn',f'{D}/v9_series/e2_neonatologiya_dnevnik_oritn/e2_neonatologiya_dnevnik_oritn.mp4',3.6,[('A','Почему кожа','краснеет?','вопрос'),('B','1 420 г.','День 12.','факт'),('C','Дневник мамы','недоношенной дочки','эмоция')]),
 ('e3_shram',f'{D}/v9_series/e3_plastika_shram_kazhduyu_nedelyu/e3_plastika_shram_kazhduyu_nedelyu.mp4',2.6,[('A','Как ухаживать','за шрамом?','вопрос'),('B','9 недель.','1 шрам.','факт'),('C','Я снимаю шрам','каждую неделю','эмоция')]),
 ('e4_babochki',f'{D}/v9_series/e4_dermatologiya_deti_babochki/e4_dermatologiya_deti_babochki.mp4',5.0,[('A','Кто такие','дети-бабочки?','вопрос'),('B','25–31','октября','факт'),('C','Мой сын —','«бабочка»','эмоция')]),
 ('e5_medsestra',f'{D}/v9_series/e5_hirurgiya_pov_medsestra/e5_hirurgiya_pov_medsestra.mp4',9.5,[('A','Кожа как бумага.','Что делать?','вопрос'),('B','Смена','12 часов','факт'),('C','POV:','ты медсестра','эмоция')]),
]
def fit(draw,text,font_path,max_w,start):
    s=start
    while s>40:
        f=ImageFont.truetype(font_path,s)
        if draw.textlength(text,font=f)<=max_w: return f
        s-=4
    return ImageFont.truetype(font_path,s)
sheet=[]
for name,vid,t,vars_ in R:
    tmp=f'/tmp/claude-0/-home-user-CreateVideo/8f17faa1-693e-57ef-8190-9cf6a8124841/scratchpad/bg_{name}.png'
    os.makedirs(os.path.dirname(tmp),exist_ok=True)
    subprocess.run(['ffmpeg','-loglevel','error','-y','-ss',str(t),'-i',vid,'-frames:v','1',tmp],check=True)
    bg=Image.open(tmp).convert('RGB').resize((1080,1920))
    row=[]
    for v,l1,l2,tag in vars_:
        im=bg.copy()
        if v=='B': im=ImageEnhance.Brightness(im.filter(ImageFilter.GaussianBlur(10))).enhance(.55)
        elif v=='C': im=ImageEnhance.Brightness(im).enhance(.7)
        else: im=ImageEnhance.Brightness(im.filter(ImageFilter.GaussianBlur(4))).enhance(.6)
        # зона текста: сильное размытие с мягкими краями, чтобы текст ролика не спорил с обложкой
        m=Image.new('L',im.size,0); dm=ImageDraw.Draw(m)
        for yy in range(620,1380): dm.line([(0,yy),(1080,yy)],fill=int(255*min(1,(380-abs(yy-1000))/120)))
        im=Image.composite(ImageEnhance.Brightness(im.filter(ImageFilter.GaussianBlur(22))).enhance(.8),im,m)
        ov=Image.new('RGBA',im.size,(0,0,0,0)); d=ImageDraw.Draw(ov)
        # градиент снизу/сверху для читаемости
        for y in range(700,1300): d.line([(0,y),(1080,y)],fill=(0,0,0,int(190*(1-abs(y-1000)/300))))
        im=Image.alpha_composite(im.convert('RGBA'),ov); d=ImageDraw.Draw(im)
        f1=fit(d,l1,FB,960,150); f2=fit(d,l2,FB,960,150)
        y=1000-(f1.size+f2.size+20)//2
        if v=='A':
            for txt,f,col in ((l1,f1,WH),(l2,f2,OR)):
                w=d.textlength(txt,font=f); d.text(((1080-w)/2,y),txt,font=f,fill=col); y+=f.size+20
        elif v=='B':
            for i,(txt,f) in enumerate(((l1,f1),(l2,f2))):
                w=d.textlength(txt,font=f); x=(1080-w)/2
                if i==1: d.rounded_rectangle([x-24,y-6,x+w+24,y+f.size+18],radius=14,fill=OR)
                d.text((x,y),txt,font=f,fill=WH); y+=f.size+30
        else:
            for txt,f,col in ((l1,f1,WH),(l2,f2,WH)):
                w=d.textlength(txt,font=f); x=(1080-w)/2
                d.text((x+4,y+4),txt,font=f,fill=(0,0,0)); d.text((x,y),txt,font=f,fill=col); y+=f.size+20
            d.rectangle([440,y+20,640,y+32],fill=OR)
        im=im.convert('RGB'); p=f'{OUT}/{name}_{v}.jpg'; im.save(p,quality=92); row.append(im)
    sheet.append(row)
# лист сравнения (в сетке профиля видна зона 4:5: y 285..1635)
W=270; H=480
S=Image.new('RGB',(W*3+40,(H+10)*len(sheet)),(20,20,20))
for r,row in enumerate(sheet):
    for c,im in enumerate(row): S.paste(im.resize((W,H)),(c*(W+20),r*(H+10)))
S.save(f'{OUT}/ab_contact_sheet.jpg',quality=85)
print('ok',len(sheet)*3)
