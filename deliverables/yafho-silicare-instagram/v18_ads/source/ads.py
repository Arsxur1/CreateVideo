# Шаг 18: рекламные версии 4:5 и 1:1 из лучших Reels
import subprocess, os
D='/home/user/CreateVideo/deliverables/yafho-silicare-instagram'; OUT=f'{D}/v18_ads'
ADS={'m4_persik':'v7_cinematic/m4_persik_cinematic/m4_persik_cinematic.mp4',
     'm1_manifest':'v7_cinematic/m1_manifest_cinematic/m1_manifest_cinematic.mp4',
     'k5_hirurgiya':'v12_kinetic/k5_hirurgiya/k5_hirurgiya.mp4',
     'e6_b2b_lineika':'v9_series/e6_b2b_pod_lupoi_lineika/e6_b2b_pod_lupoi_lineika.mp4'}
Y45={'m4_persik':110,'m1_manifest':285,'k5_hirurgiya':285,'e6_b2b_lineika':285}  # верх окна 4:5 (безопасная зона 285..1635)
def run(*a): subprocess.run(a,check=True,capture_output=True)
for k,v in ADS.items():
    src=f'{D}/{v}'
    # 4:5 — кадрирование по безопасной зоне
    run('ffmpeg','-y','-i',src,'-vf',f'crop=1080:1350:0:{Y45[k]}','-c:v','libx264','-crf','18','-preset','slow','-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart',f'{OUT}/{k}_4x5.mp4')
    # 1:1 — ролик целиком по высоте, по бокам размытый и затемнённый он же
    fc='[0:v]split[a][b];[a]scale=1080:1080:force_original_aspect_ratio=increase,crop=1080:1080,boxblur=40:2,eq=brightness=-0.12[bg];[b]scale=-2:1080[fg];[bg][fg]overlay=(W-w)/2:0'
    run('ffmpeg','-y','-i',src,'-filter_complex',fc,'-c:v','libx264','-crf','18','-preset','slow','-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart',f'{OUT}/{k}_1x1.mp4')
    print('ok',k,flush=True)
# Версии с обязательным предупреждением (≥5% площади кадра) — для стран, где закон о рекламе медизделий этого требует
from PIL import ImageFont
FB='/usr/share/fonts/opentype/inter/InterDisplay-Bold.otf'
L1,L2='ИМЕЮТСЯ ПРОТИВОПОКАЗАНИЯ.','НЕОБХОДИМА КОНСУЛЬТАЦИЯ СПЕЦИАЛИСТА'
for k in ADS:
    for fmt,h in (('4x5',1350),('1x1',1080)):
        bh=int(h*0.07)+1  # полоса 7% высоты = 7% площади (с запасом к 5%)
        fs=int(bh*0.34)
        while ImageFont.truetype(FB,fs).getlength(L2)>1000: fs-=1
        g=int(fs*0.25); y1=f'h-{bh}+({bh}-{2*fs+g})/2'
        dt=lambda t,y: f"drawtext=fontfile={FB}:text='{t}':fontsize={fs}:fontcolor=0x2B2B2B:x=(w-text_w)/2:y={y}"
        vf=f"drawbox=x=0:y=ih-{bh}:w=iw:h={bh}:color=white@1:t=fill,{dt(L1,y1)},{dt(L2,y1+f'+{fs+g}')}"
        run('ffmpeg','-y','-i',f'{OUT}/{k}_{fmt}.mp4','-vf',vf,'-c:v','libx264','-crf','18','-preset','slow','-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart',f'{OUT}/{k}_{fmt}_warn.mp4')
    print('warn',k,flush=True)
