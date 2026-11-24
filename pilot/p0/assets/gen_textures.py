#!/usr/bin/env python3
"""Tekstur prosedural untuk P0 (numpy + Pillow). Tanpa AI. Seed tetap => hasil deterministik.
Tekstur yang sama dipakai kedua renderer (web dan Blender)."""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "tex")
os.makedirs(OUT, exist_ok=True)
rng = np.random.default_rng(7)
S = 1024


def noise(size, cells, seed_off=0):
    r = np.random.default_rng(100 + seed_off + cells)
    a = r.random((cells, cells)).astype(np.float32)
    im = Image.fromarray((a * 255).astype(np.uint8)).resize((size, size), Image.BICUBIC)
    return np.asarray(im, dtype=np.float32) / 255.0


def fbm(size, seed_off=0, octaves=(4, 8, 16, 32, 64), weights=(0.5, 0.3, 0.2, 0.12, 0.08)):
    acc = np.zeros((size, size), np.float32)
    for i, (c, w) in enumerate(zip(octaves, weights)):
        acc += w * noise(size, c, seed_off + i)
    acc -= acc.min(); acc /= acc.max()
    return acc


def hexrgb(h):
    h = h.lstrip("#"); return np.array([int(h[i:i + 2], 16) for i in (0, 2, 4)], np.float32) / 255


def save(arr, name):
    Image.fromarray((np.clip(arr, 0, 1) * 255).astype(np.uint8)).save(os.path.join(OUT, name))


def floor_tile():
    n = 4  # 4x4 ubin per 1.2 m => ubin 0.3 m
    img = np.zeros((S, S, 3), np.float32)
    base = hexrgb("#9b968e")
    f = fbm(S, 1)
    cell = S // n
    grout = hexrgb("#6f6b64")
    for i in range(n):
        for j in range(n):
            tint = 1 + (rng.random() - 0.5) * 0.10
            warm = (rng.random() - 0.5) * 0.04
            c = base * tint + np.array([warm, 0, -warm * 0.5])
            y0, y1, x0, x1 = i * cell, (i + 1) * cell, j * cell, (j + 1) * cell
            img[y0:y1, x0:x1] = c
    # variasi mikro dan "awan" batu
    img *= (0.93 + 0.14 * f)[..., None]
    speck = noise(S, 256, 9)
    img *= (0.97 + 0.06 * speck)[..., None]
    g = 6
    for k in range(n + 1):
        p = k * cell
        img[max(0, p - g):p + g, :] = grout
        img[:, max(0, p - g):p + g] = grout
    # tepi ubin sedikit lebih terang (bevel)
    save(img, "floor_tile.png")


def subway():
    cols, rows = 4, 8
    cw, ch = S // cols, S // rows
    img = np.zeros((S, S, 3), np.float32)
    base = hexrgb("#e4e7e5")
    grout = hexrgb("#b9b8b1")
    img[:] = grout
    f = fbm(S, 3)
    g = 3
    for r in range(rows):
        off = (cw // 2) if r % 2 else 0
        for c in range(-1, cols + 1):
            x0 = c * cw + off; x1 = x0 + cw
            y0, y1 = r * ch, (r + 1) * ch
            tint = 1 + (rng.random() - 0.5) * 0.045
            col = base * tint + np.array([-0.005, 0.0, 0.005])
            xs0, xs1 = max(0, x0 + g), min(S, x1 - g)
            if xs1 <= xs0: continue
            tile = np.ones((y1 - y0 - 2 * g, xs1 - xs0, 3), np.float32) * col
            # gradasi kaca (tepi lebih gelap)
            yy = np.linspace(-1, 1, tile.shape[0])[:, None]
            xx = np.linspace(-1, 1, tile.shape[1])[None, :]
            edge = 1 - 0.05 * (np.maximum(np.abs(yy), np.abs(xx)) ** 4)
            img[y0 + g:y1 - g, xs0:xs1] = tile * edge[..., None]
    img *= (0.97 + 0.05 * f)[..., None]
    save(img, "subway_tile.png")


def plaster():
    f = fbm(S, 4, octaves=(3, 6, 12, 48, 128), weights=(0.3, 0.3, 0.2, 0.15, 0.2))
    base = hexrgb("#d6d2ca")
    img = base[None, None, :] * (0.94 + 0.1 * f)[..., None]
    # tahi lembap halus di bawah (tak kentara)
    save(img, "plaster.png")


def wood():
    # papan kayu horizontal; serat memanjang
    r = np.random.default_rng(11)
    img = np.zeros((S, S, 3), np.float32)
    base = hexrgb("#97724f"); dark = hexrgb("#6b4d35")
    planks = 4
    ph = S // planks
    for p in range(planks):
        y0, y1 = p * ph, (p + 1) * ph
        tint = 1 + (r.random() - 0.5) * 0.18
        # serat: noise dengan skala anisotropik (diregangkan horizontal)
        a = r.random((ph // 6, 8)).astype(np.float32)
        g = np.asarray(Image.fromarray((a * 255).astype(np.uint8)).resize((S, ph), Image.BICUBIC), np.float32) / 255
        b = np.asarray(Image.fromarray((r.random((ph // 2, 3)) * 255).astype(np.uint8)).resize((S, ph), Image.BICUBIC), np.float32) / 255
        t = 0.6 * g + 0.4 * b
        ring = 0.5 + 0.5 * np.sin(t * 22 + np.linspace(0, 6, ph)[:, None])
        mix = (0.55 * t + 0.45 * ring)[..., None]
        img[y0:y1] = (dark[None, None] * (1 - mix) + base[None, None] * mix) * tint
        img[y0:y0 + 3] *= 0.55  # celah papan
    save(img, "wood.png")


def stone():
    f = fbm(S, 5, octaves=(4, 10, 40, 160), weights=(0.35, 0.3, 0.2, 0.15))
    base = hexrgb("#8f9392")
    veins = np.clip(np.sin(fbm(S, 6, octaves=(3, 6, 12), weights=(0.6, 0.3, 0.1)) * 14) ** 6, 0, 1)
    img = base[None, None] * (0.9 + 0.18 * f)[..., None]
    img = img * (1 - 0.18 * veins[..., None]) + 0.08 * veins[..., None]
    sp = noise(S, 400, 8)
    img *= (0.95 + 0.1 * sp)[..., None]
    save(img, "stone.png")


def label():
    W, H = 1290, 510
    im = Image.new("RGB", (W, H), (37, 40, 44))
    d = ImageDraw.Draw(im)
    # bingkai tipis
    d.rounded_rectangle([14, 14, W - 15, H - 15], 22, outline=(232, 121, 43), width=6)
    bold = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    reg = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    f1 = ImageFont.truetype(bold, 118)
    f2 = ImageFont.truetype(reg, 62)
    d.text((60, 55), "SEKAT AIR", font=f1, fill=(244, 213, 168))
    d.text((60, 215), "Air yang tertahan di tekukan", font=f2, fill=(226, 226, 222))
    d.text((60, 295), "pipa menutup jalur bau", font=f2, fill=(226, 226, 222))
    d.text((60, 375), "dari saluran pembuangan.", font=f2, fill=(226, 226, 222))
    im.save(os.path.join(OUT, "label.png"))


if __name__ == "__main__":
    for fn in (floor_tile, subway, plaster, wood, stone, label):
        fn()
    print("tekstur ->", OUT, sorted(os.listdir(OUT)))
