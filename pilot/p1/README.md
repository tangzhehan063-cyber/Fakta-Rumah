# Pilot P1 — Benchmark kompositor Remotion (eksperimen, bukan migrasi)

**Status:** eksperimen terisolasi. `pilot/p0/` dan dokumen lain tidak diubah. Hanya `remotion@4.0.546`, `@remotion/cli@4.0.546`, `react`/`react-dom` 19.3.1 yang dipasang di folder ini. Remotion memakai Chromium headless yang sudah ada (`--browser-executable`), tanpa unduhan tambahan.

## Isi benchmark (12 dtk, 1080×1920, 30 fps, 360 frame)
Tiga shot yang **sengaja berbeda** (aturan variasi): **A** tracking lateral + parallax kedalaman (4 bidang, tanpa zoom/partikel); **B** push-in lambat + rack focus (blur LOD cross-fade) + satu sapuan cahaya; **C** kamera statis + kabut tipis + debu dalam berkas cahaya. Potong keras A→B, larut B→C. Plat berasal dari render P0 (beauty + kedalaman, `scripts/make_plates.py`, tanpa AI). Semua gerak deterministik (tanpa `Math.random`).

## Hasil (container 4 vCPU, tanpa GPU, 15 GB RAM)
| Pengukuran | c=1 | c=2 | c=3 | c=4 |
|---|---|---|---|---|
| Render 12 dtk, **tanpa bundling** | 48,7 dtk | 38,8 dtk | **35,7 dtk** | 36,3 dtk |
| RAM puncak (seluruh pohon proses) | 1,6 GB | 2,2 GB | 2,8 GB | 3,3 GB |
| CPU rata-rata / puncak (dari 4 inti) | 1,63 / 2,76 | 2,26 / 3,54 | 2,36 / 3,82 | 2,44 / 3,90 |
| Bundling (sekali) | 4,0 dtk | | | |
| Render + bundling | 54,8 | 44,3 | — | 39,3 |

- **Kecepatan:** 0,10 dtk/frame pada c=3–4 ≈ **3× durasi video**. Percepatan berhenti di c=3 (bagian encode/stitch ffmpeg serial).
- **Uji panjang 60 dtk (1.800 frame, c=3):** **177,4 dtk** (2,96× durasi), RAM puncak 2,9 GB (naik pelan 2,3→2,9 GB selama render; tidak ada pertumbuhan tak terbatas teramati, namun hanya 1 menit yang diuji), CPU rata-rata 2,45 inti.
- **Kualitas encode:** H.264 CRF 18, frame JPEG q90. PSNR frame video vs still PNG tanpa kompresi video: **44,7–45,0 dB** (transparan). Berkas 12 dtk: 4,5 MB.
- **Stabilitas:** 9 render, **0 kegagalan**. Tujuh keluaran 12 dtk (c=1…4, dengan/tanpa bundling) **identik byte-per-byte** (md5). Pada video 60 dtk frame ke-360 = frame ke-1080 (identik), tanpa frame hitam (blackdetect).

## Penilaian visual (jujur; Anda yang menilai: `eval/bench12.mp4`, `eval/bench12_sheet.jpg`)
Infrastruktur lolos; **hasil visual belum mencapai level sinematik** dan memiliki cacat desain pada komposisi benchmark (bukan pada performa):
1. **Rack focus saya salah rancang:** pada awal shot B seluruh frame sempat kabur (tak ada lapisan yang fokus).
2. **Larut B→C menghasilkan citra ganda** (dua kamera berbeda saling menumpuk). Itu tepat jenis transisi tanpa alasan kreatif yang tidak Anda inginkan; harus diganti transisi bermotivasi.
3. **Parallax dari irisan kedalaman** meninggalkan tepi bergerigi/berganda di benda dekat (mis. bibir wastafel), terlihat jika diperhatikan. Aman hanya untuk gerak kecil; plat latar bersih belum dipakai.
4. **Kabut dan debu terlalu halus** untuk dinilai pada ukuran contact sheet; belum saya nilai.
5. Isi tetap satu ruangan; palet masih condong cokelat kayu (belum netral + aksen terkendali).

## Batas
Hanya gambar + CSS/SVG (Mode A/B sederhana). **Belum diuji di dalam Remotion:** Three.js/`@remotion/three` (Mode B kedalaman, Mode C), efek WebGL, audio, caption, transisi bawaan. Video 60 dtk bukan multi-menit.

## Menjalankan ulang
```bash
npm install && python3 scripts/make_plates.py          # butuh render P0 di ../p0/out/blender
CH=/opt/pw-browsers/chromium_headless_shell-1243/chrome-headless-shell-linux64/chrome-headless-shell
npx remotion bundle src/index.ts --out-dir=out/bundle
python3 bench/measure.py r_c3 -- npx remotion render out/bundle Bench12 out/r_c3.mp4 --browser-executable=$CH --concurrency=3 --image-format=jpeg --jpeg-quality=90 --crf=18
```
