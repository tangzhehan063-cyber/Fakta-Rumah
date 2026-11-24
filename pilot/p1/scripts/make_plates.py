#!/usr/bin/env python3
"""Membuat plat berlapis untuk benchmark dari render P0 (beauty + kedalaman). Deterministik, tanpa AI.
Plat = latar penuh + irisan kedalaman (alpha berbulu) + versi blur (LOD) untuk rack focus.
Pakai: python3 scripts/make_plates.py   (butuh pilot/p0/out/blender/*.png)"""
import os, numpy as np
from PIL import Image, ImageFilter
HERE = os.path.dirname(os.path.abspath(__file__)); P0 = os.path.join(HERE, '../../p0/out/blender'); OUT = os.path.join(HERE, '../public/plates')
os.makedirs(OUT, exist_ok=True)

def depth(name):
    return np.asarray(Image.open(f'{P0}/depth_{name}.png')).astype(np.float64) / 65535.0 * 8.0 + 1.0

def blur_rgba(im, r):
    a = np.asarray(im).astype(np.float64); rgb = a[..., :3] * (a[..., 3:] / 255.0)
    pm = Image.fromarray(np.dstack([rgb, a[..., 3]]).astype(np.uint8), 'RGBA').filter(ImageFilter.GaussianBlur(r))
    b = np.asarray(pm).astype(np.float64); al = np.maximum(b[..., 3:], 1e-3) / 255.0
    return Image.fromarray(np.dstack([np.clip(b[..., :3] / al, 0, 255), b[..., 3]]).astype(np.uint8), 'RGBA')

def build(tag, beauty_file, depth_name, cuts, blur_lod):
    img = Image.open(f'{P0}/{beauty_file}').convert('RGB'); z = depth(depth_name)
    qs = np.quantile(z, cuts)
    img.save(f'{OUT}/{tag}_bg.jpg', quality=93)
    if blur_lod: img.filter(ImageFilter.GaussianBlur(blur_lod)).save(f'{OUT}/{tag}_bg_blur.jpg', quality=93)
    names = []
    for i in range(len(qs) - 1):
        lo, hi = qs[i], qs[i + 1]
        m = ((z >= lo) & (z < hi if i < len(qs) - 2 else z <= hi)).astype(np.float32)
        m = np.asarray(Image.fromarray((m * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(2.2)), np.float32)
        rgba = Image.fromarray(np.dstack([np.asarray(img), m]).astype(np.uint8), 'RGBA')
        rgba.save(f'{OUT}/{tag}_L{i}.png'); names.append(f'{tag}_L{i}')
        if blur_lod: blur_rgba(rgba, blur_lod).save(f'{OUT}/{tag}_L{i}_blur.png')
    print(tag, 'zbands(m):', [round(float(q), 2) for q in qs])

build('s1', 'S1_establish_s64.png', 'S1_establish', [0, 0.30, 0.65, 1.0], 0)
build('s2', 'S2_medium_s64.png', 'S2_medium', [0, 0.30, 0.65, 1.0], 14)
build('s4', 'S4_high_s64.png', 'S4_high', [0, 1.0], 0)
