# Pilot P0 — Bake-off dua jalur render (web vs Blender)

**Status:** eksperimen sekali pakai. Kode di folder ini **bukan engine**; boleh dibuang. `engine/` tetap kosong.
**Aturan:** tidak ada AI untuk visual/aset/tekstur; tidak ada karakter; tidak ada blok melayang di latar datar; identitas visual tidak diubah. Hanya `three@0.187.0` (MIT) dan `bpy 5.3.0` (GPL-3.0) yang dipasang; tidak ada library lain.

## Prinsip kesetaraan (agar adil)
| Elemen | Cara dibuat sama |
|---|---|
| Geometri | `spec/build_scene.py` menghitung SEMUA mesh sekali (numpy) → `spec/scene.json`. Kedua renderer memuat mesh yang **identik**, termasuk normal dan UV |
| Tekstur | `assets/gen_textures.py` (numpy + Pillow, seed tetap, tanpa AI) → PNG yang sama dipakai keduanya |
| Material | satu daftar material (warna, roughness, metallic, opacity, emisi) |
| Kamera | koordinat bola (target, azimuth, elevasi, jarak, FOV, DOF) dan interpolasi easing yang **sama** |
| Cahaya | didefinisikan secara persepsi (key/fill/accent); **dikalibrasi manual** per renderer (lihat temuan: ini sendiri sebuah biaya) |
| Format | 1080×1920 (9:16), 30 fps |
| Topik | "kolong wastafel + pipa-U": mekanisme (sekat air) + lingkungan sehari-hari, tanpa karakter |

## Storyboard uji (sama untuk keduanya)
| Shot | Tujuan penonton | Kamera | Hal yang diuji |
|---|---|---|---|
| S1 establish | "Ini kolong wastafel; ada pipa di dalamnya" | oblik tinggi (30°), jarak jauh | komposisi vertikal, konteks ruangan, detail bertingkat |
| S2 medium | "Pipa membentuk huruf U dan ada air di sana" | oblik rendah (14°), DOF ringan | material, cahaya, DOF, informasi di dalam dunia (plakat) |
| S3 macro | "Air tertahan di tekukan" | hampir sejajar mata (4°), DOF kuat | material tembus pandang, kedalaman, penanda hangat |
| S4 high | pindah sudut: lebih tinggi untuk melihat rute pipa | oblik 42° | perpindahan angle, komposisi |
| C1 klip 3 dtk | S1 → S2 | dolly + orbit + turun, easing inOutCubic | gerak kamera kontinu, stabilitas antar-frame |

## Kriteria evaluasi (ditetapkan SEBELUM membandingkan)
Skala 1–5 per kriteria, ditambah catatan bukti.
1. Komposisi vertikal 9:16 (fokus, ruang, framing)
2. Material (kayu, ubin, keramik, kaca, air, logam terbaca berbeda dan berkarakter)
3. Cahaya dan bayangan (arah, kelembutan, bounce, kontak)
4. Depth (lapisan, DOF, occlusion)
5. Detail bertingkat (fokus kaya, periferi sederhana tanpa kosong)
6. Informasi di dalam dunia (plakat, penanda) terbaca tanpa seperti slide
7. Kejelasan mekanisme tanpa karakter (apakah sekat air terpahami)
8. Gerak kamera & transisi (kontinu, bebas flicker)
9. **Biaya**: waktu render per frame, waktu pengembangan, kompleksitas kode, jumlah kode per backend
10. **Reusable assets**: seberapa mudah aset/resep dipakai ulang dan diperluas
11. **Keterpeliharaan & fleksibilitas** (ketergantungan, risiko versi, lisensi, kemudahan debug)
12. **Syarat mutlak §1b**: tidak ada hasil yang terbaca sebagai diagram datar/slide/blok melayang

## Menjalankan ulang
```bash
python3 assets/gen_textures.py && python3 spec/build_scene.py
npm install                                   # three@0.187.0
node web/render.mjs stills final              # out/web/*.png
node web/render.mjs clip 0.5 3                # frames/web/*.png
/path/ke/venv/bin/python blender/render.py stills 64 1.0   # out/blender/*.png
/path/ke/venv/bin/python blender/render.py clip 16 0.5 3   # frames/blender/*.png
```
`bpy` dipasang di virtualenv terpisah (`pip install bpy==5.3.0`), di luar repo.
