# Синтез саунд-дизайна без внешних сервисов (numpy -> WAV)
import numpy as np, wave
SR = 44100
rng = np.random.default_rng(7)
def _t(d): return np.arange(int(d*SR))/SR
def lp(x, cutoff):
    n = 101; k = np.sinc(2*cutoff/SR*(np.arange(n)-(n-1)/2)); k *= np.hamming(n); k /= k.sum()
    return np.convolve(x, k, mode='same')
def hp(x, cutoff): return x - lp(x, cutoff)
def env(n, a, r):
    e = np.ones(n); A=int(a*SR); R=int(r*SR)
    if A: e[:A] = np.linspace(0,1,A)
    if R: e[-R:] *= np.linspace(1,0,R)
    return e
def pad(d, freqs=(110,164.8,220,277.2), amp=.06):
    t=_t(d); x=sum(np.sin(2*np.pi*f*t)+.6*np.sin(2*np.pi*f*1.003*t+1)+.25*np.sin(2*np.pi*2*f*t) for f in freqs)
    x*= (1+.15*np.sin(2*np.pi*.25*t)); x=lp(x,1800)
    return amp*x/len(freqs)*env(len(t),2.5,2.5)
def whoosh(d=.9, amp=.35):
    n=int(d*SR); w=rng.standard_normal(n); lo=lp(w,400); hi=lp(w,3500)
    m=np.linspace(0,1,n); x=lo*(1-m)+hi*m*.7; e=np.sin(np.pi*np.linspace(0,1,n))**2
    return amp*x*e/np.abs(x).max()
def boom(amp=.7):
    t=_t(1.6); x=np.sin(2*np.pi*(48+30*np.exp(-t*8))*t)*np.exp(-t*2.6); c=hp(rng.standard_normal(len(t)),2000)*np.exp(-t*60)*.3
    return amp*(x+c)
def chime(f=880, amp=.22, d=2.2):
    t=_t(d); x=np.sin(2*np.pi*f*t)+.45*np.sin(2*np.pi*2.01*f*t)+.2*np.sin(2*np.pi*3.02*f*t)
    return amp*x*np.exp(-t*2.2)*env(len(t),.004,.05)
def heart(amp=.8):
    def thump(): t=_t(.22); return np.sin(2*np.pi*52*t)*np.exp(-t*22)
    a=thump(); out=np.zeros(int(.6*SR)); out[:len(a)]+=a; out[int(.24*SR):int(.24*SR)+len(a)]+=.7*a
    return amp*out
def tear(d=.55, amp=.5):
    n=int(d*SR); w=hp(rng.standard_normal(n),1500); g=(rng.random(n//200+1)>.45).repeat(200)[:n]*1.0
    g=lp(g,300); return amp*w*g*np.linspace(1,.3,n)
def click(amp=.25):
    t=_t(.03); return amp*(hp(rng.standard_normal(len(t)),3000)*np.exp(-t*300)+.5*np.sin(2*np.pi*2200*t)*np.exp(-t*200))
def riser(d=1.5, amp=.25):
    t=_t(d); w=hp(rng.standard_normal(len(t)),800)*(t/d)**2; s=np.sin(2*np.pi*(200+600*(t/d)**2)*t)*(t/d)**2*.4
    return amp*(w*.5+s)
def mix(dur, events, out, pad_chord=None, pad_amp=.06):
    L=np.zeros(int(dur*SR)+SR)
    if pad_chord: p=pad(dur,pad_chord,pad_amp); L[:len(p)]+=p
    for t,snd in events:
        i=int(t*SR); L[i:i+len(snd)]+=snd[:max(0,len(L)-i)]
    L=L[:int(dur*SR)]; L/=max(1,np.abs(L).max()/.9)
    st=np.stack([L, np.roll(L,int(.012*SR))*.96],1)
    with wave.open(out,'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((st*32767).astype('<i2').tobytes())
    return out
