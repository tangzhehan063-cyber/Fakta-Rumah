# Temuan: Cinematic Illusion untuk produksi CPU-only

**Tanggal:** 24 Nov 2026 · **Perangkat:** 4 vCPU, 15 GB RAM, tanpa GPU (Chromium + SwiftShader; Blender Cycles CPU) · **Status:** temuan dan usulan, **bukan keputusan**. Tidak ada library baru dipasang untuk benchmark ini (hanya `three`, `bpy`, Playwright yang sudah ada). Kode uji: `pilot/p0/bench/`.

Tingkat bukti: **[U]** diukur di container ini · **[V]** diverifikasi dari file repo · **[K]** pengetahuan saya, belum diuji · **[P]** penilaian visual saya dari frame.

## 1. Koreksi atas angka "±9 jam"
Angka itu ekstrapolasi saya dari pengaturan P0 yang **sengaja mahal** (shadow dinamis 4096 VSM, AO, DOF, MSAA×4, 1080×1920). Itu bukan batas bawaan 3D web.
- Repo lama merender video 58–59 dtk 1080×1920 dengan Remotion + Three.js dalam **9 mnt 11 dtk** (≈0,31 dtk/frame) dan "±20 mnt" untuk render penuh, dengan `--concurrency=4`, frame JPEG, ANGLE swangle **[V: STATUS.md, tools/produksi.sh, remotion.config.ts]**. Ia juga sudah "memanggang efek 2D berat ke PNG" **[V]**: prinsip cache yang sama dengan arah baru ini.
- Pengukuran saya pada scene P0 yang sama **[U]**:

| Varian Three.js (1080×1920, JPEG, per frame) | ms |
|---|---|
| V0 P0-final (shadow 4096 dinamis, AO, MSAA×4, DOF) | **17.432** |
| V1 shadow dihitung **sekali** (statis) | 5.632 |
| V2 + shadow 2048 | 5.017 |
| V3 + tanpa AO | 2.844 |
| V4 + tanpa DOF | 1.915 |
| V5 + tanpa MSAA | **1.287** |

Pelajaran: biaya terbesar bukan "3D" tetapi **efek yang dihitung ulang tiap frame padahal scene statis**. Shadow statis saja memangkas 3×; semua penghematan 13,5×.

## 2. Benchmark kompositing berlapis (setara biaya per-frame Remotion; Remotion sendiri belum dipasang) [U]
Chromium, 1080×1920, JPEG q90, layer RGBA ukuran penuh dengan transform perspektif 3D CSS:

| Konfigurasi | ms/frame |
|---|---|
| 1 latar saja | 154 (**lantai** = encode+screenshot) |
| 6 lapisan RGBA + perspektif 3D | 148 |
| 12 lapisan, tanpa blur | 210 |
| 12 lapisan + sapuan cahaya (gradien blend) | 223 |
| 12 lapisan + sapuan + 300 partikel (blur **dipanggang**) | **274** |
| 6 lapisan + blur CSS langsung pada 3 lapisan | 356 |
| 12 lapisan + blur langsung 6 lapisan + sapuan + partikel | 854 |
| idem, 4 worker paralel | 513 efektif (percepatan hanya 1,66×) |

Pelajaran: banyaknya lapisan hampir tidak memengaruhi biaya; **blur real-time** dan filter berat yang memengaruhi. Blur dipanggang ke beberapa tingkat lalu di-cross-fade (rack focus) menjaga biaya di ≈0,27 dtk/frame, setara angka repo lama. Paralelisme 4 inti tidak linear untuk isi yang berat.

## 3. Reproyeksi kedalaman (satu render 3D mahal dipakai ulang) [U][P]
Alur: render 3D mahal **sekali** (beauty 64 spp ±150 dtk) + peta kedalaman 16-bit (**0,5–1,1 dtk** lewat override material, murah) → mesh bidang berdisplasi di Three.js → kamera bergerak. Biaya per frame **≈340–400 ms** (540×960, termasuk screenshot PNG, belum dioptimalkan).

Kualitas terhadap kebenaran 3D (Blender, jalur kamera S1→S2 yang besar: dolly 3,9→2,1 m, tilt 16°):

| Posisi di jalur | Satu gambar (S1) | Dua keyframe di-crossfade | Empat keyframe, campur tetangga |
|---|---|---|---|
| 5% | 38,7 dB | 36,3 | 35,0 |
| 15% | 32,5 | 27,9 | 26,8 |
| 36% | 26,7 | 21,0 | 34,2 |
| 52% | 23,9 | 18,4 | 23,4 |
| 66% (tepat di keyframe) | 21,6 | 17,0 | **41,2** |
| 86% | 18,8 | 17,3 | 20,4 |

Penilaian visual:
- **Gerak kecil (≈ ≤10–15% dari jalur uji ini; setara dolly ≲0,3 m dari 3,9 m atau orbit ≲2–3°) nyaris tak dapat dibedakan dari 3D asli.** Ini persis jangkauan *slow push-in / parallax* dokumenter.
- **Gerak sedang**: olesan tekstur di tepi benda (dinding di belakang pipa "ditarik" seperti karet).
- **Gerak besar**: rusak. Memotong segitiga yang terentang menyisakan lubang besar.
- **Cross-fade dua keyframe berjauhan menghasilkan bayangan ganda** (terlihat jelas pada gambar `eval/b3_mix.jpg`). Keyframe lebih rapat memperbaiki di dekat keyframe, tetapi **di antara keyframe masih berbayang** (`eval/b3_keys.jpg`).
- Artinya: **"ilusi dari satu gambar" aman hanya dalam amplop gerak kamera yang sempit.** Untuk gerak besar butuh (a) 3D sungguhan, atau (b) plat berlapis (latar bersih tanpa objek depan, dirender terpisah) yang menyelesaikan disokulasi; (b) belum diuji.

## 4. Jawaban pemeriksaan repo (7 pertanyaan)
1. **Bagian yang benar-benar butuh 3D penuh.** Di repo ini: tidak ada yang *mutlak*. Yang butuh 3D nyata: perakitan/pembongkaran mekanisme, aliran/simulasi, dan reveal yang mengganti sisi benda atau gerak kamera di luar amplop di §3. (Repo lama punya `PilotSifon`: pipa-U dibongkar, air mengalir; itu contoh Mode C [V].)
2. **Bisa diganti teknik murah:** lingkungan statis, push-in/pan/parallax kecil, DOF (blur dipanggang, cross-fade), sapuan cahaya, partikel, kabut, plakat/teks sebagai bidang berperspektif, shadow dan AO statis (§1, §2).
3. **Kemampuan yang sudah ada.** Repo baru (P0): spesifikasi scene netral-renderer + generator mesh + tekstur prosedural, dua renderer, ekspor kedalaman, harness reproyeksi, benchmark. Repo lama (referensi; tidak diimpor): jalur Remotion 4.0.546 dengan R3F, transisi, motion-blur, caption; `produksi.sh` (render per bagian 15 dtk + concat, `--concurrency=4`), mix audio/loudnorm, TTS, align, cek suara **[V]**.
4. **Perlu didesain ulang:** asumsi "semuanya 3D" di P0; manifest shot (belum ada mode, plat, cache, amplop kamera); QA (perlu cek artefak ilusi: bayangan ganda, tarikan tekstur); pengaturan render P0.
5. **Apakah arsitektur mendukung beberapa pendekatan per shot?** Secara prinsip ya: kontrak shot §3 membuat teknik detail internal, dan kamera berbasis data (koordinat bola) sudah dipakai di semua uji. Secara implementasi **belum**: belum ada field mode, cache plat, atau kamera yang sama menggerakkan DOM, mesh kedalaman, dan R3F.
6. **Remotion sebagai lapisan kompositing utama.** Cocok sebagai *compositor + timeline + audio + caption + perender per-shot* (terbukti di repo lama dengan pola serupa [V]). Catatan: belum dipasang atau dites di repo baru; lisensi (≤3 karyawan gratis) perlu konfirmasi; **lantai biaya per frame ≈150 ms** (screenshot/encode 1080×1920) tidak bisa dihilangkan oleh kompositing apa pun [U].
7. **Arsitektur CPU-efisien terbaik:** lihat `ARCHITECTURE.md` §11.

## 5. Model biaya (perkiraan dari pengukuran di atas; 3 menit = 5.400 frame @30 fps, 1 worker)
| Strategi untuk seluruh video | Per frame | Total |
|---|---|---|
| 3D web berat (P0 final) | 17,4 dtk | ≈ 26 jam |
| Blender Cycles 16 spp 1080p | ≈ 47 dtk (ekstrapolasi) | ≈ 70 jam |
| 3D web dihemat (V5) | 1,3 dtk | ≈ 1,9 jam |
| Kompositing berlapis, blur dipanggang | 0,27 dtk | ≈ 24 menit |
| Campuran realistis: 60% kompositing + 25% 3D hemat + 15% reproyeksi | ≈ 0,57 dtk | **≈ 51 menit** + biaya sekali pakai pabrik plat (mis. 30 plat × 150 dtk ≈ 75 menit) |

Ini model, bukan janji. Biaya sebenarnya bergantung pada mix shot dan jumlah revisi; keuntungan terbesar: **revisi tidak mengulang plat**, hanya shot yang berubah.

## 6. Batas temuan
- Remotion belum diuji langsung; angka kompositing memakai Chromium mentah sebagai pengganti.
- Reproyeksi diuji pada satu scene (interior); hasil bisa berbeda untuk lanskap/kota.
- Plat berlapis dengan latar bersih, light groups (relighting), kabut/dust/light-rays, rack focus nyata, dan efek air **belum diuji**; klaimnya di dokumen ini hanya usulan [K].
- Penilaian visual adalah penilaian saya; Anda yang menentukan.

## 7. Benchmark Remotion (P1, 24 Nov) [U]
Detail dan cara ulang: `pilot/p1/README.md`. Ringkas: composisi 12 dtk 3 shot (lateral parallax, push-in + rack focus, statis + atmosfer) dirender **3,0–4,1× durasi** (35,7 dtk render-only pada concurrency 3), video **60 dtk dalam 177 dtk (2,96×)**, RAM puncak 1,6–3,5 GB, CPU rata-rata 1,6–2,4 dari 4 inti, PSNR encode 44,7–45 dB, **0 kegagalan dari 9 render**, keluaran **identik byte-per-byte** di semua concurrency. Ini memperbarui model biaya §5: kompositing berlapis **≈0,10 dtk/frame di dalam Remotion (≈3 menit per menit video)**. Cacat visual komposisi benchmark dicatat jujur di README P1 (rack focus yang salah rancang, larut berbayang ganda, irisan kedalaman bergerigi).

### 7b. P1 v2: perbaikan visual dan aturan pembuatan plat [U][P]
Detail: `pilot/p1/README.md` (bagian Versi 2). Render Remotion v2 **33,8 dtk** untuk 12 dtk (c=3), RAM 2,4 GB; biaya render tidak naik dibanding v1. Plat per-lapisan dari Blender (**≈3,3–4 menit per shot**, sekali) menghilangkan robekan tepi pada parallax. Empat aturan dipelajari dari kesalahan sendiri (urutan kedalaman, objek bersama permukaan, oklusi lapisan subjek, faktor parallax berdekatan). Koreksi determinisme: v2 tidak byte-identik antar-concurrency (2/360 frame berbeda ≤2 level); v1 identik.
