# Шаг 16: техконтроль всех роликов календаря
import csv,glob,os,subprocess,json,sys
D='/home/user/CreateVideo/deliverables/yafho-silicare-instagram'; os.chdir(D)
def probe(v):
    j=json.loads(subprocess.run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',v],capture_output=True,text=True).stdout)
    vs=[s for s in j['streams'] if s['codec_type']=='video'][0]; a=[s for s in j['streams'] if s['codec_type']=='audio']
    I=P=None
    if a:
        e=subprocess.run(['ffmpeg','-hide_banner','-nostats','-i',v,'-af','ebur128=peak=true','-f','null','-'],capture_output=True,text=True).stderr.split('\n')
        Il=[l for l in e if l.strip().startswith('I:')]; Pl=[l for l in e if 'Peak:' in l]
        I=float(Il[-1].split()[1]) if Il else None; P=float(Pl[-1].split()[1]) if Pl else None
    return dict(file=v,w=vs['width'],h=vs['height'],codec=vs['codec_name'],pix=vs['pix_fmt'],fps=vs['r_frame_rate'],dur=round(float(j['format']['duration']),1),audio=a[0]['codec_name'] if a else '',lufs=I,tp=P,kb=os.path.getsize(v)//1024)
if __name__=='__main__':
    rows=list(csv.DictReader(open('MASTER/master_calendar.csv'))); vids=[]
    for r in rows:
        if os.path.isdir(r['file']): vids+=[(r['date'],v) for v in glob.glob(r['file']+'/*.mp4')]
    out=[]
    for d,v in sorted(vids): x=probe(v); x['date']=d; out.append(x)
    for x in out: print(x['date'],os.path.basename(x['file']),x['w'],x['h'],x['codec'],x['pix'],x['fps'],x['dur'],x['audio'] or 'NO AUDIO',x['lufs'],x['tp'])
    json.dump(out,open(sys.argv[1] if len(sys.argv)>1 else '/dev/null','w'),ensure_ascii=False,indent=1)
