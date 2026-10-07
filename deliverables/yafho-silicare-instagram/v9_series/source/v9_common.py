from stylekit import style_reel, SOUT
from kp import strip
V9 = SOUT.replace('v8_styles','v9_series')
def run(name, ep, dur, title, check, pad=(82.4,123.5,164.8), bg='#000'):
    shots = style_reel(name, dur, ep.body, ep.js, title, ep.ev, pad=pad, pad_amp=.04, check=check, bg=bg, outdir=V9)
    strip(shots, f'kp/chk_{name}.jpg', 2400)
    return shots
