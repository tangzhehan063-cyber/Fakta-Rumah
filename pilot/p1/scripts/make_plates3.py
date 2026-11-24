#!/usr/bin/env python3
"""Plat isometrik v3 -> public/iso/ (Remotion) dan ../p0/bench/iso/ (reproyeksi orbit). Tanpa AI."""
import os, numpy as np
from PIL import Image, ImageFilter
HERE = os.path.dirname(os.path.abspath(__file__)); B = os.path.join(HERE, '../../p0/out/blender'); OUT = os.path.join(HERE, '../public/iso'); ORB = os.path.join(HERE, '../../p0/bench/iso')
os.makedirs(OUT, exist_ok=True); os.makedirs(ORB, exist_ok=True)
def blur_rgba(im, r):
    a = np.asarray(im.convert('RGBA')).astype(np.float64); rgb = a[..., :3] * (a[..., 3:] / 255.0)
    pm = Image.fromarray(np.dstack([rgb, a[..., 3]]).astype(np.uint8), 'RGBA').filter(ImageFilter.GaussianBlur(r))
    b = np.asarray(pm).astype(np.float64); al = np.maximum(b[..., 3:], 1e-3) / 255.0
    return Image.fromarray(np.dstack([np.clip(b[..., :3] / al, 0, 255), b[..., 3]]).astype(np.uint8), 'RGBA')
Image.open(f'{B}/ISO_A_s48.png').convert('RGB').save(f'{OUT}/A.jpg', quality=92)
for lay, r in (('BACK', 14), ('MID', 12), ('FRONT', 14)):
    im = Image.open(f'{B}/layers/ISO_B_{lay}.png').convert('RGBA')
    if lay == 'BACK':
        im.convert('RGB').save(f'{OUT}/B_BACK.jpg', quality=93); im.convert('RGB').filter(ImageFilter.GaussianBlur(r)).save(f'{OUT}/B_BACK_blur.jpg', quality=93)
    else:
        im.save(f'{OUT}/B_{lay}.png'); blur_rgba(im, r).save(f'{OUT}/B_{lay}_blur.png')
for k in (41, 43, 45, 47, 49):
    Image.open(f'{B}/ISO_O{k}_s48.png').convert('RGB').save(f'{ORB}/beauty_{k}.png')
    v = np.asarray(Image.open(f'{B}/depth_ISO_O{k}.png')).astype(np.uint32)
    Image.fromarray(np.dstack([(v >> 8) & 255, v & 255, np.zeros_like(v)]).astype(np.uint8), 'RGB').save(f'{ORB}/depth_{k}_packed.png')
print('ok', sorted(os.listdir(OUT)))
