# Laporan Pilot P0 — Web (Three.js) vs Blender (bpy)

**Status:** hasil pengukuran dan penilaian, **bukan keputusan engine final**. Perangkat uji: container 4 vCPU, 15 GB RAM, **tanpa GPU** (Three.js memakai Chromium + SwiftShader di CPU; Blender memakai Cycles CPU). Hasil waktu akan sangat berbeda di mesin ber-GPU (belum diuji).

Gambar perbandingan: `eval/cmp_A.jpg` (S1, S2), `eval/cmp_B.jpg` (S3, S4), `eval/clip_strip.jpg` (klip 3 dtk; baris atas web, bawah Blender). Urutan dalam tiap pasangan: **web | blender**.

## 1. Apa yang diuji (sama untuk keduanya)
Satu scene "kolong wastafel + pipa-U" (mekanisme + lingkungan, tanpa karakter), geometri **identik** (mesh dihitung sekali dari `spec/build_scene.py`), tekstur prosedural identik (tanpa AI), kamera dan easing identik, 1080×1920. 4 still + 1 klip kamera 3 dtk (S1→S2). Aturan yang dijaga: tanpa karakter, tanpa AI, tanpa blok melayang. Alat terpasang: `three@0.187.0` (MIT), `bpy 5.3.0` (GPL-3.0). Tidak ada library lain.

## 2. Pengukuran (terukur, bukan penilaian)

| Ukuran | Web | Blender |
|---|---|---|
| Still 1080×1920 (S1/S2/S3/S4) | 20,3 / 26,2 / 25,5 / 27,0 dtk (MSAA×4 + AO + DOF) | 137,5 / 161,3 / 207,2 / 153,4 dtk (Cycles 64 spp + denoise) |
| Draf cepat | ±9–11 dtk (tanpa AO/DOF/MSAA) | ±7–10 dtk (0,4× skala, 16 spp) |
| Klip 90 frame @540×960 | **996 dtk** (11,1 dtk/frame) | **1.058 dtk** (11,8 dtk/frame, 16 spp) |
| Determinisme (render ulang frame yang sama) | **identik piksel** | **identik piksel** |
| Kedip temporal (turunan kedua luma, lebih kecil = lebih halus; mengandung gerak kamera yang sah) | 4,12 | 2,56 |
| Baris kode (render saja) | 200 (index.html 141 + render.mjs 59) | 197 |
| Kode bersama | build_scene.py 322 + gen_textures.py 154 (dipakai keduanya) | |
| Ukuran paket | `three` ± puluhan MB, Chromium sudah ada | `bpy` wheel **±427 MB** |

**Ekstrapolasi kasar (bukan pengukuran), video 45 dtk @30 fps = 1.350 frame, 1080×1920, CPU 4 inti:**
web ≈ 25 dtk/frame → **±9,4 jam**; Blender 16 spp ≈ 47 dtk/frame → **±17,6 jam**, Blender 64 spp ≈ 150–200 dtk/frame → **±56–75 jam**. Dengan GPU, keduanya jauh lebih cepat (besarannya tidak saya ukur). Bila diuji 15 fps (karakter referensi 01), biaya separuhnya.

## 3. Penilaian visual (penilaian saya dari frame yang saya lihat; skala 1–5)

| # | Kriteria | Web | Blender | Bukti |
|---|---|---|---|---|
| 1 | Komposisi vertikal 9:16 | 4 | 4 | kamera sama; kekurangan ada di penataan saya (plakat terpotong di S2) |
| 2 | Material | 3,5 | 4 | Blender memberi pantulan hangat yang konsisten; web lebih "bersih" tetapi datar |
| 3 | Cahaya & bayangan | 3 | **4,5** | Blender: bounce hangat dari kayu ke pipa/ubin, kontak bayangan lembut. Web: tidak ada GI; muncul **bercak terang dari lampu aksen** di dinding (S2/S3) yang terbaca seperti artefak |
| 4 | Depth | 3,5 | **4,5** | DOF Blender mulus dan benar; DOF web (BokehPass) kasar, ada **bidang kotak pucat** di sekitar kaca (S3) |
| 5 | Detail bertingkat | 3,5 | 3,5 | ditentukan isi scene, bukan renderer |
| 6 | Informasi di dalam dunia | 3,5 | 3,5 | plakat terbaca di keduanya; kawat penunjuk **tidak terlihat** di keduanya (tipis); teks 3D **belum diuji** |
| 7 | Kejelasan mekanisme tanpa karakter | 3,5 | 3,5 | sekat air (air di tekukan) terbaca; **proses/aliran belum diuji** |
| 8 | Gerak kamera & transisi | 3,5 | 4 | keduanya kontinu dan stabil; metrik kedip Blender lebih halus |
| 12 | Syarat mutlak §1b | lolos | lolos | keduanya terbaca sebagai set utuh, bukan diagram/slide/blok melayang. **Tetapi lihat §5: terlihat seperti render katalog furnitur** |

Catatan warna: Blender memakai tone mapping AgX yang **menurunkan saturasi** aksen: oranye "hangat" berubah menjadi salmon/pink. Web (ACES) mempertahankan oranye. Ini bisa disetel di keduanya.

## 4. Biaya, reuse, keterpeliharaan (kriteria 9–11)

**Hal yang berhasil dan penting:** satu **deskripsi scene netral-renderer** (mesh + material + kamera + cahaya dalam JSON, geometri dihasilkan oleh Python) bisa dibaca oleh kedua renderer dengan ±200 baris masing-masing. Artinya aset/resep tidak terkunci pada satu engine, dan renderer bisa diganti tanpa membuang aset. Ini mendukung kontrak shot di `ARCHITECTURE.md` §3.

| Aspek | Web | Blender |
|---|---|---|
| Waktu sampai gambar pertama | cepat; tetapi **butuh banyak penyetelan** agar tidak terlihat murah (VSM, AO, DOF, env, kaca) | gambar pertama langsung enak dilihat; penyetelan lebih sedikit |
| Pencahayaan | harus **dipalsukan** (hemisfer, env, AO); lampu aksen menghasilkan artefak | GI sungguhan; kalibrasi kekuatan lampu tetap manual dan **berbeda satuan** antar-engine |
| Material tembus pandang | kaca/air via alpha (tanpa refraksi); transmission bawaan Three.js tampak keruh dan saya tinggalkan | alpha di Cycles bersih; refraksi sungguhan tersedia tetapi tidak dipakai agar adil |
| Teks dalam dunia | tekstur PNG di bidang (sama di keduanya). **3D text belum diuji** | sama |
| Pratinjau | **cepat dan interaktif** (modal besar untuk iterasi) | lambat (draf 7–10 dtk, final menit) |
| Integrasi dengan Remotion/caption/audio | alami (satu bahasa); **belum diuji** | lewat urutan frame lalu disusun (ffmpeg/Remotion); belum diuji |
| Risiko versi | three 0.187.0 MIT, aktif (publish Okt 2026) | **API Blender 5.x memberi peringatan deprecation** (`use_nodes` akan dihapus di 6.0); wheel terikat Python 3.13 |
| Lisensi | MIT | **GPL-3.0** untuk `bpy`; memakai sebagai alat render internal umumnya aman, tetapi **mendistribusikan kode yang meng-import `bpy`** punya implikasi GPL (perlu ditinjau bila kelak didistribusikan) [K, bukan nasihat hukum] |
| Skalabilitas ribuan objek (gaya MediaCraft) | instancing efisien [K, belum diuji] | instancing/Geometry Nodes kuat [K, belum diuji] |

## 5. Kelemahan dan hal yang **tidak** dibuktikan pilot ini (jujur)
1. **Scene uji terlihat seperti render katalog furnitur.** Belum ada karakter sinematik/direksi seperti Referensi 01/03 (cahaya jendela dramatis, kamera bercerita). Pilot menguji kemampuan *engine*, bukan kualitas art-direction.
2. **Palet belum "netral dengan aksen hangat"**: kayu menempati area luas sehingga scene condong cokelat/oranye (terutama di Blender karena bounce). Ini kesalahan penataan saya, bukan keterbatasan engine.
3. **Belum diuji:** reveal/proses berurutan (aliran air, pertumbuhan prosedural), instancing massal, teks 3D di dunia, transisi antar-scene, GPU, integrasi Remotion, Eevee (hanya Cycles), efek bloom/malam.
4. Penilaian 1–5 adalah **penilaian saya sendiri atas frame**. Penilaian Anda yang menentukan; lihat gambar `eval/*.jpg`.
5. Angka waktu hanya berlaku untuk 4 vCPU tanpa GPU. Ekstrapolasi video penuh adalah perkiraan kasar.
6. Metrik "kedip temporal" bukan bukti bebas flicker (tercampur gerak kamera).

## 6. Kandidat library untuk jalur web (**belum dipasang; butuh persetujuan Anda**)
| Kandidat | Fungsi | Lisensi (diverifikasi npm) | Manfaat | Risiko/catatan |
|---|---|---|---|---|
| `postprocessing` (pmndrs) 6.39.6 | efek pasca-proses lebih matang (SSAO/DOF/bloom) | Zlib | memperbaiki artefak DOF dan AO | satu dependency tambahan |
| `n8ao` 2.1.0 | ambient occlusion berkualitas tinggi | ISC | AO lebih halus dan stabil | satu dependency |
| `three-gpu-pathtracer` 0.0.28 | **path tracing di browser** (GI sungguhan) | MIT | berpotensi menutup kesenjangan cahaya web vs Blender | **pra-1.0**, butuh GPU WebGL2 (tidak bisa dites di container ini), tidak dijamin deterministik |
| `three-mesh-bvh` 0.9.18 | percepatan raycast (dipakai pathtracer) | MIT | dependensi pathtracer | — |

## 7. Rekomendasi (belum final; menunggu penilaian visual Anda)
**Jalur paling masuk akal untuk engine jangka panjang: hibrida dengan deskripsi scene netral-renderer sebagai pusat.**
- **Renderer kualitas-akhir untuk shot spasial: Blender (bpy)**, karena memberi cahaya, DOF, dan material yang paling dekat dengan Referensi 01–03 dengan penyetelan paling sedikit.
- **Jalur web (Three.js) dipertahankan sebagai pratinjau cepat dan untuk shot yang cukup dengan kualitas web**, serta sebagai tempat integrasi Remotion (teks, caption, audio, assembly).
- **Aset dan resep ditulis sekali** (mesh generator, material, kamera, cahaya) dalam format netral; tidak ada aset yang terkunci pada satu engine.

**Syarat sebelum menjadikannya keputusan final** (dilakukan di P1, lihat bawah):
1. Biaya render memenuhi target produksi Anda. Pada CPU 4 inti, Blender kualitas penuh **terlalu lambat** untuk video penuh; perlu GPU, render terdistribusi, atau kompromi (resolusi/spp/fps).
2. Blender lolos uji **reveal prosedural, instancing massal, teks 3D, dan transisi**.
3. Alur Blender→Remotion/ffmpeg→audio berjalan mulus.
4. Tinjauan implikasi lisensi GPL bila kode didistribusikan.

**Jika biaya Blender tidak dapat diterima**, alternatif: jalur web + `three-gpu-pathtracer`/`postprocessing`/`n8ao` (butuh persetujuan dan GPU), atau menurunkan target visual (cahaya lebih sederhana).

## 8. Usulan P1 (menunggu persetujuan)
1. **Reveal/proses berurutan**: air mengisi pipa dan sekat air terbentuk; pertumbuhan prosedural (lemari/pipa "dirakit").
2. **Teks 3D di dunia** (huruf berbayang di dinding/lantai) tanpa tempelan datar.
3. **Instancing massal** (mis. 2.000 ubin/benda) untuk mengukur skalabilitas.
4. **Transisi antar-scene** lewat objek (kamera masuk ke dalam pipa menuju scene berikutnya).
5. **Perbaikan palet** (netral + aksen hangat) dan **art-direction cahaya** (cahaya jendela seperti Ref 03).
6. Uji **15 fps vs 30 fps** (karakter gerak referensi 01) dan estimasi biaya.
7. Uji jalur Blender di mesin ber-GPU (jika Anda punya).
