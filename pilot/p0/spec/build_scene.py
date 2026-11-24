#!/usr/bin/env python3
"""P0 — deskripsi scene BERSAMA untuk dua jalur render (web/Three.js dan Blender).

Semua geometri dihitung di sini (numpy) dan diekspor sebagai mesh mentah, jadi kedua renderer menampilkan
BENTUK yang sama persis. Tekstur dibuat prosedural oleh assets/gen_textures.py (tanpa AI).
Satuan: meter. Sumbu: Y ke atas (Blender mengonversi sendiri).

Topik uji: "kolong wastafel dan pipa-U" (mekanisme + lingkungan sehari-hari, tanpa karakter).
"""
import json, math, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "scene.json")


# ---------------------------------------------------------------- util geometri
def rot_y(a):
    c, s = math.cos(a), math.sin(a)
    return np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]])

def rot_x(a):
    c, s = math.cos(a), math.sin(a)
    return np.array([[1, 0, 0], [0, c, -s], [0, s, c]])

def rot_z(a):
    c, s = math.cos(a), math.sin(a)
    return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])

def world_uv(P, N, tile):
    """UV proyeksi-kotak dari koordinat DUNIA agar kerapatan tekstur konsisten antar objek."""
    ax = np.argmax(np.abs(N), axis=1)
    uv = np.zeros((len(P), 2))
    for i in range(3):
        m = ax == i
        if i == 0: uv[m] = np.stack([P[m, 2], P[m, 1]], 1)
        if i == 1: uv[m] = np.stack([P[m, 0], P[m, 2]], 1)
        if i == 2: uv[m] = np.stack([P[m, 0], P[m, 1]], 1)
    return uv / tile

def pack(name, P, N, UV, F, mat):
    return {"name": name, "material": mat,
            "positions": np.round(P, 5).flatten().tolist(),
            "normals": np.round(N, 4).flatten().tolist(),
            "uvs": np.round(UV, 5).flatten().tolist(),
            "indices": F.flatten().astype(int).tolist()}

def rounded_box(name, size, radius, pos, mat, tile=0.5, rot=None, seg=5):
    hx, hy, hz = [s / 2 for s in size]
    r = min(radius, hx, hy, hz) * 0.999
    def axis_samples(h):
        a = [-h + r * i / seg for i in range(seg + 1)]
        b = [(h - r) + r * i / seg for i in range(seg + 1)]
        return np.array(a + b)
    P, N, F = [], [], []
    base = 0
    for axis, sign in [(0, 1), (0, -1), (1, 1), (1, -1), (2, 1), (2, -1)]:
        o = [i for i in range(3) if i != axis]
        H = [hx, hy, hz]
        u = axis_samples(H[o[0]]); v = axis_samples(H[o[1]])
        uu, vv = np.meshgrid(u, v, indexing="ij")
        p = np.zeros(uu.shape + (3,))
        p[..., o[0]] = uu; p[..., o[1]] = vv; p[..., axis] = sign * H[axis]
        flat = p.reshape(-1, 3)
        lim = np.array([hx - r, hy - r, hz - r])
        inner = np.clip(flat, -lim, lim)
        n = flat - inner
        n /= np.linalg.norm(n, axis=1, keepdims=True)
        vert = inner + n * r
        nu, nv = uu.shape
        idx = np.arange(nu * nv).reshape(nu, nv)
        tris = []
        for i in range(nu - 1):
            for j in range(nv - 1):
                a, b, c, d = idx[i, j], idx[i + 1, j], idx[i + 1, j + 1], idx[i, j + 1]
                tris += [[a, b, c], [a, c, d]]
        tris = np.array(tris)
        # pastikan arah luar
        fn = np.cross(vert[tris[:, 1]] - vert[tris[:, 0]], vert[tris[:, 2]] - vert[tris[:, 0]])
        out = (fn * n[tris[:, 0]]).sum(1) < 0
        tris[out] = tris[out][:, ::-1]
        P.append(vert); N.append(n); F.append(tris + base); base += len(vert)
    P = np.concatenate(P); N = np.concatenate(N); F = np.concatenate(F)
    R = np.eye(3) if rot is None else rot
    P = P @ R.T + np.array(pos); N = N @ R.T
    return pack(name, P, N, world_uv(P, N, tile), F, mat)

def lathe(name, profile, pos, mat, seg=48, tile=0.4, flip=False):
    prof = np.array(profile, float)
    # normal profil (2D): tegak lurus tangent, menghadap luar bila profil berjalan naik di sisi luar
    t = np.gradient(prof, axis=0)
    n2 = np.stack([t[:, 1], -t[:, 0]], 1)
    n2 /= (np.linalg.norm(n2, axis=1, keepdims=True) + 1e-9)
    if flip: n2 = -n2
    P, N = [], []
    for k in range(seg):
        a = 2 * math.pi * k / seg
        ca, sa = math.cos(a), math.sin(a)
        for (r, y), (nr, ny) in zip(prof, n2):
            P.append([r * ca, y, r * sa]); N.append([nr * ca, ny, nr * sa])
    P = np.array(P) + np.array(pos); N = np.array(N)
    m = len(prof); F = []
    for k in range(seg):
        k2 = (k + 1) % seg
        for i in range(m - 1):
            a, b = k * m + i, k * m + i + 1
            c, d = k2 * m + i + 1, k2 * m + i
            F += [[a, b, c], [a, c, d]]
    F = np.array(F)
    return pack(name, P, N, world_uv(P, N, tile), F, mat)

def tube(name, path, radius, mat, seg=16, tile=0.4, caps=True):
    path = np.array(path, float)
    T = np.gradient(path, axis=0)
    T /= np.linalg.norm(T, axis=1, keepdims=True)
    ref = np.array([0, 0, 1.0]) if abs(T[0, 2]) < 0.9 else np.array([1.0, 0, 0])
    P, N = [], []
    nrm = np.cross(T[0], ref); nrm /= np.linalg.norm(nrm)
    for i, (c, t) in enumerate(zip(path, T)):
        nrm = nrm - t * np.dot(nrm, t); nrm /= np.linalg.norm(nrm)   # transport frame
        bn = np.cross(t, nrm)
        for k in range(seg):
            a = 2 * math.pi * k / seg
            d = math.cos(a) * nrm + math.sin(a) * bn
            P.append(c + radius * d); N.append(d)
    P = np.array(P); N = np.array(N); n = len(path); F = []
    for i in range(n - 1):
        for k in range(seg):
            k2 = (k + 1) % seg
            a, b = i * seg + k, (i + 1) * seg + k
            c, d = (i + 1) * seg + k2, i * seg + k2
            F += [[a, c, b], [a, d, c]]
    if caps:
        for end, sgn in [(0, -1), (n - 1, 1)]:
            ci = len(P); P = np.vstack([P, path[end]]); N = np.vstack([N, sgn * T[end]])
            for k in range(seg):
                k2 = (k + 1) % seg
                a, b = end * seg + k, end * seg + k2
                F += [[ci, a, b]] if sgn > 0 else [[ci, b, a]]
    F = np.array(F)
    return pack(name, P, N, world_uv(P, N, tile), F, mat)

def plane(name, size, pos, mat, rot=None, uvscale=(1, 1)):
    w, h = size[0] / 2, size[1] / 2
    P = np.array([[-w, -h, 0], [w, -h, 0], [w, h, 0], [-w, h, 0]], float)
    N = np.tile([0, 0, 1.0], (4, 1))
    R = np.eye(3) if rot is None else rot
    P = P @ R.T + np.array(pos); N = N @ R.T
    UV = np.array([[0, 0], [uvscale[0], 0], [uvscale[0], uvscale[1]], [0, uvscale[1]]], float)
    return pack(name, P, N, UV, np.array([[0, 1, 2], [0, 2, 3]]), mat)

def fillet_path(pts, radius, steps=8):
    """polyline dengan tikungan membulat (kuadrat Bezier)."""
    pts = [np.array(p, float) for p in pts]
    out = [pts[0]]
    for i in range(1, len(pts) - 1):
        a, b, c = pts[i - 1], pts[i], pts[i + 1]
        da, dc = a - b, c - b
        ra = min(radius, np.linalg.norm(da) / 2); rc = min(radius, np.linalg.norm(dc) / 2)
        p0 = b + da / np.linalg.norm(da) * ra; p2 = b + dc / np.linalg.norm(dc) * rc
        for s in range(steps + 1):
            t = s / steps
            out.append((1 - t) ** 2 * p0 + 2 * (1 - t) * t * b + t ** 2 * p2)
    out.append(pts[-1])
    return np.array(out)

def densify(path, step=0.012):
    path = np.array(path); res = [path[0]]
    for a, b in zip(path[:-1], path[1:]):
        L = np.linalg.norm(b - a); n = max(1, int(L / step))
        for k in range(1, n + 1): res.append(a + (b - a) * k / n)
    return np.array(res)

# ---------------------------------------------------------------- materials
MATERIALS = {
    # nama: baseColor / tekstur, roughness, metallic, dsb.
    "floor_tile":   {"map": "floor_tile.png",  "color": "#ffffff", "roughness": 0.38, "metallic": 0.0},
    "wall_plaster": {"map": "plaster.png",     "color": "#ffffff", "roughness": 0.92, "metallic": 0.0},
    "subway_tile":  {"map": "subway_tile.png", "color": "#ffffff", "roughness": 0.18, "metallic": 0.0},
    "wood":         {"map": "wood.png",        "color": "#d8c6b4", "roughness": 0.55, "metallic": 0.0},
    "wood_dark":    {"map": "wood.png",        "color": "#b9a08a", "roughness": 0.6,  "metallic": 0.0},
    "counter":      {"map": "stone.png",       "color": "#ffffff", "roughness": 0.30, "metallic": 0.0},
    "ceramic":      {"color": "#f2f1ee", "roughness": 0.08, "metallic": 0.0},
    "pvc":          {"color": "#e7e4dc", "roughness": 0.45, "metallic": 0.0},
    "chrome":       {"color": "#c9ccd0", "roughness": 0.16, "metallic": 1.0},
    "glass":        {"color": "#dcebf2", "roughness": 0.05, "metallic": 0.0, "opacity": 0.20},
    "water":        {"color": "#3f8cc0", "roughness": 0.03, "metallic": 0.0, "opacity": 0.85},
    "accent_warm":  {"color": "#e8792b", "roughness": 0.4,  "metallic": 0.0, "emissive": "#e8792b", "emissive_strength": 0.6},
    "plate":        {"map": "label.png", "color": "#ffffff", "roughness": 0.35, "metallic": 0.0},
    "bottle_a":     {"color": "#6f8f8a", "roughness": 0.35, "metallic": 0.0},
    "bottle_b":     {"color": "#d9c9a8", "roughness": 0.4,  "metallic": 0.0},
    "bucket":       {"color": "#7d8a99", "roughness": 0.5,  "metallic": 0.0},
    "cap":          {"color": "#3c3f44", "roughness": 0.4,  "metallic": 0.0},
}

# ---------------------------------------------------------------- scene
def build(nm=False):
    objs = []
    add = objs.append
    # ruang: lantai + dua dinding (sudut ruangan, potongan)
    add(rounded_box("floor", (2.8, 0.08, 2.8), 0.01, (0, -0.04, 0), "floor_tile", tile=1.2))
    add(rounded_box("wall_back", (2.8, 2.5, 0.10), 0.01, (0, 1.25, -1.25), "wall_plaster", tile=1.4))
    add(rounded_box("wall_left", (0.10, 2.5, 2.8), 0.01, (-1.25, 1.25, 0), "wall_plaster", tile=1.4))
    add(plane("backsplash", (2.4, 1.15), (0, 0.575 + 0.02, -1.198), "subway_tile", uvscale=(2.4 / 1.2, 1.15 / 1.2)))
    add(rounded_box("skirting", (2.8, 0.09, 0.012), 0.004, (0, 0.045, -1.194), "ceramic", tile=1.0))

    # lemari kolong (terbuka, satu pintu terbuka) — pusat di x=-0.25
    cx, cz = -0.25, -0.92
    W, D, H, t = 0.95, 0.56, 0.78, 0.022
    add(rounded_box("cab_left",  (t, H, D), 0.004, (cx - W / 2 + t / 2, 0.08 + H / 2, cz), "wood", tile=0.6))
    add(rounded_box("cab_right", (t, H, D), 0.004, (cx + W / 2 - t / 2, 0.08 + H / 2, cz), "wood", tile=0.6))
    add(rounded_box("cab_bottom", (W, t, D), 0.004, (cx, 0.08 + t / 2, cz), "wood", tile=0.6))
    add(rounded_box("cab_plinth", (W, 0.08, D - 0.06), 0.004, (cx, 0.04, cz - 0.02), "wood_dark", tile=0.6))
    add(rounded_box("cab_top_rail", (W - 2 * t, 0.05, t), 0.004, (cx, 0.08 + H - 0.025, cz + D / 2 - t / 2), "wood", tile=0.6))
    # pintu kiri terbuka ±105° (engsel di tepi kiri-depan)
    door_w, door_h = W / 2 - 0.004, H - 0.03
    hinge = np.array([cx - W / 2 + 0.002, 0.08 + 0.015 + door_h / 2, cz + D / 2])
    R = rot_y(math.radians(105))
    local_center = np.array([door_w / 2, 0, 0.012])
    add(rounded_box("door_left", (door_w, door_h, 0.02), 0.004, hinge + R @ local_center, "wood", tile=0.6, rot=R))
    # meja marmer/batu
    add(rounded_box("counter", (W + 0.06, 0.04, D + 0.04), 0.008, (cx, 0.08 + H + 0.02, cz + 0.01), "counter", tile=0.8))

    # wastafel (vessel) di atas meja
    sink_x, sink_z, sink_y = cx, cz + 0.04, 0.08 + H + 0.04
    prof = [(0.0, 0.0), (0.12, 0.0), (0.2, 0.03), (0.215, 0.10), (0.222, 0.115), (0.205, 0.118), (0.195, 0.105),
            (0.17, 0.035), (0.0, 0.028)]
    add(lathe("sink", prof, (sink_x, sink_y, sink_z), "ceramic", seg=64, tile=0.5))
    # keran
    fx, fz = sink_x, sink_z - 0.28
    add(lathe("faucet_base", [(0, 0), (0.028, 0), (0.026, 0.035), (0.016, 0.04), (0.0, 0.04)],
              (fx, sink_y, fz), "chrome", seg=32))
    spout = fillet_path([(fx, sink_y + 0.035, fz), (fx, sink_y + 0.20, fz), (fx, sink_y + 0.20, fz + 0.12),
                         (fx, sink_y + 0.16, fz + 0.15)], 0.05)
    add(tube("faucet_spout", densify(spout, 0.008), 0.011, "chrome", seg=16))

    # pipa pembuangan (bidang x-y di z = pz); tikungan-U di bawah
    pz = cz + 0.04
    x0 = sink_x
    xu = x0 + 0.095      # pusat U
    r_u = 0.095
    y_top, y_bend = (0.88 if nm else 0.80), 0.36
    pipe_r = 0.034
    # bagian atas (opak): dari lubang wastafel turun ke awal U
    top = densify(np.array([[x0, y_top, pz], [x0, y_bend, pz]]), 0.01)
    # U (kaca): setengah lingkaran
    ang = np.linspace(math.pi, 2 * math.pi, 28)
    ubend = np.array([[xu + r_u * math.cos(a), y_bend + r_u * math.sin(a), pz] for a in ang])
    # sisi kanan naik lalu belok ke dinding (opak)
    xr = xu + r_u
    out = fillet_path([[xr, y_bend, pz], [xr, 0.55, pz], [xr, 0.55, -1.19]], 0.06)
    out = densify(out, 0.01)
    add(tube("pipe_top", top, pipe_r, "pvc", seg=24))
    add(tube("pipe_out", out, pipe_r, "pvc", seg=24))
    glass_path = np.vstack([np.array([[x0, y_bend + 0.0001, pz]]), ubend, np.array([[xr, y_bend + 0.0001, pz]])])
    glass_path = densify(np.vstack([[x0, y_bend + 0.12, pz], [x0, y_bend, pz], ubend, [xr, y_bend, pz], [xr, y_bend + 0.12, pz]]), 0.008)
    add(tube("pipe_glass", glass_path, pipe_r, "glass", seg=32, caps=False))
    # air (segel): dari muka air kiri ke muka air kanan lewat U
    lvl = y_bend + 0.075
    water_path = densify(np.vstack([[x0, lvl, pz], [x0, y_bend, pz], ubend, [xr, y_bend, pz], [xr, lvl, pz]]), 0.006)
    add(tube("water", water_path, pipe_r - 0.0045, "water", seg=28))
    # kolar sambungan
    for name, y in [("collar_a", y_bend + 0.14), ("collar_b", 0.55 - 0.0)]:
        xx = x0 if name == "collar_a" else xr
        add(rounded_box(name, (0.085, 0.032, 0.085), 0.012, (xx, y, pz), "chrome", tile=0.3))
    # flens dinding
    add(rounded_box("wall_flange", (0.11, 0.11, 0.012), 0.005, (xr, 0.55, -1.192), "chrome", tile=0.3))

    # penanda aksen hangat: dua kolar di garis air + kawat penunjuk ke plakat dinding
    def collar(cx_, cy_, cz_, rr=0.041):
        c = np.array([[cx_ + rr * math.cos(a), cy_, cz_ + rr * math.sin(a)] for a in np.linspace(0, 2 * math.pi, 49)])
        return c
    add(tube("marker_collar_l", collar(x0, lvl, pz), 0.0055, "accent_warm", seg=10, caps=False))
    add(tube("marker_collar_r", collar(xr, lvl, pz), 0.0055, "accent_warm", seg=10, caps=False))
    leader = fillet_path([[x0 - 0.041, lvl, pz], [-0.34, 0.50, -1.02], [-0.36, 0.585, -1.17]], 0.05)
    add(tube("marker_leader", densify(leader, 0.01), 0.0030, "accent_warm", seg=8))
    # plakat enamel pada dinding belakang (informasi DI DALAM dunia)
    add(rounded_box("plate_body", (0.43, 0.185, 0.012), 0.006, (-0.50, 0.60, -1.186), "wood_dark", tile=0.5))
    add(plane("plate_face", (0.40, 0.155), (-0.50, 0.60, -1.1795), "plate"))

    # isi lemari (detail bertingkat): botol dan ember
    add(lathe("bottle_a", [(0, 0), (0.038, 0), (0.04, 0.02), (0.04, 0.16), (0.018, 0.2), (0.015, 0.23), (0, 0.23)],
              (cx - 0.33, 0.08 + t, cz - 0.1), "bottle_a", seg=32))
    add(lathe("cap_a", [(0, 0), (0.017, 0), (0.017, 0.03), (0, 0.03)], (cx - 0.33, 0.08 + t + 0.23, cz - 0.1), "cap", seg=24))
    add(lathe("bottle_b", [(0, 0), (0.03, 0), (0.032, 0.015), (0.032, 0.12), (0.014, 0.16), (0.012, 0.18), (0, 0.18)],
              (cx - 0.25, 0.08 + t, cz - 0.17), "bottle_b", seg=32))
    add(lathe("cap_b", [(0, 0), (0.013, 0), (0.013, 0.025), (0, 0.025)], (cx - 0.25, 0.08 + t + 0.18, cz - 0.17), "cap", seg=24))
    add(lathe("bucket", [(0, 0), (0.11, 0), (0.135, 0.22), (0.14, 0.225), (0.128, 0.225), (0.105, 0.012), (0, 0.012)],
              (1.0, 0.0, -0.2), "bucket", seg=48))
    return objs


def build_scene(nm=False):
    objs = build(nm)
    # kamera: koordinat bola di sekitar target (derajat). Rasio 9:16.
    cams = {
        "S1_establish": {"target": [-0.26, 0.50, -0.92], "az": 33, "el": 30, "dist": 3.9, "fov": 30, "dof": None},
        "S2_medium":    {"target": [-0.15, 0.42, -0.92], "az": 24, "el": 14, "dist": 2.1, "fov": 30, "dof": {"focus": 2.1, "fstop": 2.8}},
        "S3_macro":     {"target": [-0.15, 0.40, -0.90], "az": 8,  "el": 4,  "dist": 0.85, "fov": 30, "dof": {"focus": 0.85, "fstop": 1.8}},
        "S4_high":      {"target": [-0.15, 0.40, -0.92], "az": 22, "el": 42, "dist": 2.3, "fov": 30, "dof": {"focus": 2.3, "fstop": 4.0}},
    }
    # keyframe tambahan untuk uji "reproyeksi berkeyframe" (jalur kamera S1->S2 pada u=0.33 dan u=0.66)
    a, b = cams["S1_establish"], cams["S2_medium"]
    for nm, u in (("K1_third", 0.33), ("K2_twothird", 0.66)):
        l = lambda p, q: p + (q - p) * u
        cams[nm] = {"target": [l(x, y) for x, y in zip(a["target"], b["target"])], "az": l(a["az"], b["az"]), "el": l(a["el"], b["el"]),
                    "dist": l(a["dist"], b["dist"]), "fov": 30, "dof": None}
    scene = {
        "units": "m", "up": "y", "format": {"width": 1080, "height": 1920, "fps": 30},
        "materials": MATERIALS, "objects": objs, "cameras": cams,
        "lights": {
            # persepsi, bukan satuan fisik: dikalibrasi manual di tiap renderer
            "key":     {"type": "sun", "dir_from": [0.55, 0.75, 0.55], "color": "#fff1de", "strength": 1.0, "softness": 0.5},
            "fill":    {"type": "hemi", "sky": "#dbe3ea", "ground": "#8c867c", "strength": 0.55},
            "accent":  {"type": "point", "pos": [-0.18, 0.62, -0.78], "color": "#ffb066", "strength": 0.6, "radius": 0.15},
        },
        "background": "#cfd3d6",
        "clip": {"name": "C1_push", "from": "S1_establish", "to": "S2_medium", "seconds": 3, "ease": "inOutCubic"},
    }
    return scene


LAYER_MID = ("pipe_", "water", "collar_", "wall_flange", "marker_", "bottle_", "cap_", "cab_bottom", "cab_plinth")   # isi lemari (kedalaman tengah)
LAYER_BACK = ("floor", "wall_", "backsplash", "skirting", "plate_")                        # latar
# sisanya = FRONT: cangkang lemari (sisi, meja, pintu, wastafel, keran) dan ember (paling dekat kamera)

def layer_of(name):
    if name.startswith(LAYER_MID): return "MID"
    if name.startswith(LAYER_BACK): return "BACK"
    return "FRONT"

def neutral(scene):
    """Palet netral: kayu abu-oak, lemari antrasit; aksen hangat hanya dari penanda dan sedikit cahaya."""
    m = scene["materials"]
    m["wood"] = {"map": "wood_gray.png", "color": "#e4ded4", "roughness": 0.55, "metallic": 0.0}
    m["wood_dark"] = {"color": "#34373b", "roughness": 0.5, "metallic": 0.0}
    m["floor_tile"]["color"] = "#ffffff"
    L = scene["lights"]
    L["accent"].update({"strength": 0.0, "color": "#ffd3a4"})
    m["accent_warm"]["emissive_strength"] = 0.2
    scene["cameras"]["S2_medium"].update({"target": [-0.36, 0.45, -0.92], "dist": 2.5, "az": 20, "el": 13})
    L["key"]["color"] = "#fff8f0"
    L["fill"].update({"sky": "#dfe5ea", "ground": "#8b8c8c"})
    for o in scene["objects"]: o["layer"] = layer_of(o["name"])
    return scene

if __name__ == "__main__":
    s = build_scene(len(sys.argv) > 1 and sys.argv[1] == "neutral")
    if len(sys.argv) > 1 and sys.argv[1] == "neutral":
        OUT = os.path.join(HERE, "scene_neutral.json"); s = neutral(s)
    with open(OUT, "w") as f:
        json.dump(s, f, separators=(",", ":"))
    tri = sum(len(o["indices"]) // 3 for o in s["objects"])
    print("objek:", len(s["objects"]), "segitiga:", tri, "ukuran:", round(os.path.getsize(OUT) / 1e6, 2), "MB")
