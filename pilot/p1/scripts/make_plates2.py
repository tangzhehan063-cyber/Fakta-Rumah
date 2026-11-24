#!/usr/bin/env python3
"""Plat v2: dari render Blender per-LAPISAN (BACK bersih, MID, FG; objek lain tak terlihat kamera namun tetap membayangi).
Membuat versi blur (LOD) untuk rack focus dan menyimpan ke public/plates2/. Tanpa AI."""
import os, numpy as np
from PIL import Image, ImageFilter
HERE = os.path.dirname(os.path.abspath(__file__)); L = os.path.join(HERE, '../../p0/out/blender'); OUT = os.path.join(HERE, '../public/plates2')
os.makedirs(OUT, exist_ok=True)

def blur_rgba(im, r):
    a = np.asarray(im.convert('RGBA')).astype(np.float64); rgb = a[..., :3] * (a[..., 3:] / 255.0)
    pm = Image.fromarray(np.dstack([rgb, a[..., 3]]).astype(np.uint8), 'RGBA').filter(ImageFilter.GaussianBlur(r))
    b = np.asarray(pm).astype(np.float64); al = np.maximum(b[..., 3:], 1e-3) / 255.0
    return Image.fromarray(np.dstack([np.clip(b[..., :3] / al, 0, 255), b[..., 3]]).astype(np.uint8), 'RGBA')

for tag, cam in (('s1', 'S1_establish'), ('s2', 'S2_medium')):
    for lay in ('BACK', 'MID', 'FRONT'):
        im = Image.open(f'{L}/layers/{cam}_{lay}.png').convert('RGBA')
        if lay == 'BACK':
            im.convert('RGB').save(f'{OUT}/{tag}_{lay}.jpg', quality=93)
            if tag == 's2': im.convert('RGB').filter(ImageFilter.GaussianBlur(12)).save(f'{OUT}/{tag}_{lay}_blur.jpg', quality=93)
        else:
            im.save(f'{OUT}/{tag}_{lay}.png')
            if tag == 's2': blur_rgba(im, 10 if lay == 'MID' else 12).save(f'{OUT}/{tag}_{lay}_blur.png')
s4 = Image.open(f'{L}/S4_high_s48.png').convert('RGB'); s4.save(f'{OUT}/s4.jpg', quality=93); s4.filter(ImageFilter.GaussianBlur(14)).save(f'{OUT}/s4_blur.jpg', quality=93)
print('ok', sorted(os.listdir(OUT)))
