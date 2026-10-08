# Шаг 16: озвучка «немых» роликов v6 + выравнивание громкости всех роликов календаря.
# Один проход кодирования из исходника в git (многократное перекодирование AAC давало «плавающие» пики).
import sys, os, json, subprocess, tempfile, csv, glob
sys.path.insert(0,'/home/user/CreateVideo/projects/yafho-silicare-instagram'); import sfx
D='/home/user/CreateVideo/deliverables/yafho-silicare-instagram'; REPO='/home/user/CreateVideo'
TMP=tempfile.mkdtemp(dir='/tmp/claude-0/-home-user-CreateVideo/8f17faa1-693e-57ef-8190-9cf6a8124841/scratchpad')
BASE=sys.argv[1] if len(sys.argv)>1 else 'HEAD'   # коммит с исходными (необработанными) роликами
PAD=(110,164.8,220,277.2)
SILENT={
 'v6_campaign/c1_den_1_iz_180/c1_den_1_iz_180.mp4':(15,[(0,sfx.whoosh(.8,.25)),(.8,sfx.chime(523,.14,2.5)),(6.0,sfx.whoosh(.6,.2))]+[(6.4+3.2*(i/16)**.8,sfx.click(.2)) for i in range(16)]+[(9.7,sfx.chime(784,.16,2.5)),(11.0,sfx.whoosh(.9,.3)),(11.3,sfx.boom(.5)),(11.6,sfx.chime(659,.18,3))]),
 'v6_campaign/d1_hirurg_vs_medsestra/d1_hirurg_vs_medsestra.mp4':(15,[(0,sfx.whoosh(.6,.25)),(.6,sfx.chime(440,.14,2)),(4.2,sfx.whoosh(.6,.22)),(4.5,sfx.click(.3)),(10.2,sfx.whoosh(.9,.3)),(10.6,sfx.chime(659,.18,3)),(12.6,sfx.boom(.45))]),
 'v6_campaign/g1_katalog_za_30_sekund/g1_katalog_za_30_sekund.mp4':(34.5,[(0,sfx.whoosh(.7,.25)),(.6,sfx.chime(440,.15,2))]+sum([[(3.0+i*2.7-.15,sfx.whoosh(.45,.14)),(3.0+i*2.7+.3,sfx.chime([392,440,494,523,587,659,698,784,880,988][i],.1,1.6))] for i in range(10)],[])+[(30.0,sfx.whoosh(.9,.3)),(30.3,sfx.boom(.6)),(30.8,sfx.chime(659,.18,3))]),
}
def run(*a): return subprocess.run(a,check=True,capture_output=True,text=True)
os.chdir(D)
vids=sorted({v for r in csv.DictReader(open('MASTER/master_calendar.csv')) if os.path.isdir(r['file']) for v in glob.glob(r['file']+'/*.mp4')})
for v in vids:
    b=os.path.basename(v); src=f'{TMP}/src_{b}'; wav=f'{TMP}/{b}.wav'
    rel=os.path.relpath(os.path.join(D,v),REPO)
    with open(src,'wb') as f: subprocess.run(['git','-C',REPO,'show',f'{BASE}:{rel}'],stdout=f,check=True)
    if v in SILENT: dur,ev=SILENT[v]; sfx.mix(dur,ev,wav,PAD,.05)
    else: run('ffmpeg','-y','-i',src,'-vn','-ac','2','-ar','48000',wav)
    e=subprocess.run(['ffmpeg','-hide_banner','-i',wav,'-af','loudnorm=I=-15:TP=-3:LRA=11:print_format=json','-f','null','-'],capture_output=True,text=True).stderr
    m=json.loads(e[e.rindex('{'):e.rindex('}')+1])
    af=(f"loudnorm=I=-15:TP=-3:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}:"
        f"measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true,alimiter=limit=0.63:attack=2:release=50:level=disabled,aresample=48000")
    o=f'{TMP}/o_{b}'
    run('ffmpeg','-y','-i',src,'-i',wav,'-map','0:v','-map','1:a','-c:v','copy','-af',af,'-c:a','aac','-b:a','192k','-ar','48000','-shortest','-movflags','+faststart',o)
    os.replace(o,os.path.join(D,v)); print('ok',b,m['input_i'],flush=True)
