# Riset Ekosistem — Rencana & Shortlist Awal

> **PENTING:** Shortlist di bawah berasal dari pengetahuan saya, **belum diverifikasi** (versi, lisensi terkini, status maintenance, tautan). Tahap riset terverifikasi belum dijalankan. Tidak ada yang diinstal. Rekomendasi masih **hipotesis**.

## 1. Metode (saat riset dijalankan)
Untuk tiap kandidat: buka repo/dokumen resmi, catat lisensi (baca file LICENSE), tanggal commit terakhir, jumlah kontributor, dependency utama, ukuran. Uji kecil di folder terisolasi **hanya** untuk kandidat yang lolos shortlist dan atas persetujuan Anda.

Format catatan per kandidat:

| Kolom | Isi |
|---|---|
| Nama & link | |
| Kategori | library / engine / skill / contoh / workflow |
| Kemampuan | |
| Kelebihan / kekurangan | |
| Lisensi | (baca dari repo; penting untuk penggunaan komersial) |
| Dependency & risiko | |
| Duplikasi dengan sistem kita? | |
| Konflik style? | |
| Potensi integrasi | |
| Rekomendasi | adopt / adapt / reference only / reject |

## 2. Prinsip: OUR STYLE, THEIR TECHNIQUES
- Kita mengambil **mekanisme** (cara kamera, easing, masking, render), bukan **tampilan** atau aturan visual mereka.
- Skill/prompt eksternal yang mengandung aturan style = *reference only* kecuali isinya dapat dipisah dari aturan style.
- Menambah dependency butuh alasan tertulis dan persetujuan.

## 3. Area riset

| Area | Pertanyaan yang ingin dijawab |
|---|---|
| **A. Remotion** | Best practices; transisi; timeline; optimasi render (concurrency, codec); preview & frame-grab untuk visual QA; lisensi Remotion (ada ketentuan komersial; **wajib dicek**); alternatif non-React |
| **B. Three.js** | Kamera, cahaya, render bergaya (toon/outline/post-processing); shader; geometri prosedural; bagaimana membuat tampilan "ilustrasi" bukan CGI; performa render offline |
| **C. 2D: SVG/Canvas/CSS** | Teknik depth: layered parallax, perspektif palsu (transform 3D CSS), masking, morphing path, motion path, bayangan stylized, simulasi kamera; library gerak (mis. GSAP, anime.js, Rive/Lottie, paper.js/Two.js, PixiJS, p5.js) |
| **D. Skills & repo komunitas** | Storyboard, sinematografi, motion design, Remotion skills, creative coding, visual QA |
| **E. Pipeline pendukung** | Render frame→video (ffmpeg), sinkron audio, pembuatan voiceover (jika diizinkan), subtitle/caption, pembandingan frame (visual regression) |
| **F. Teknik lintas disiplin** | Animasi tradisional (12 prinsip), sinematografi film/animasi, teknik motion graphics, ilustrasi teknis/penjelasan, "paper-craft"/diorama, shader sebagai ilustrasi, SDF 2D, procedural noise untuk tekstur |

## 4. Shortlist awal (belum diverifikasi)

| Kandidat | Kategori | Hipotesis kegunaan | Hipotesis rekomendasi | Hal yang harus dicek |
|---|---|---|---|---|
| **Remotion** | framework render video (React) | Timeline, render frame deterministik, bisa memuat SVG/Canvas/Three/CSS | **adopt (kandidat kuat)** sebagai *host* render saja | Lisensi/komersial; kecocokan dengan teknik non-React; performa render |
| **@remotion/three** (react-three-fiber di Remotion) | integrasi | Bila shot membutuhkan 3D bergaya | adapt, per shot | Stabilitas, performa render |
| **Three.js** | engine 3D | Kamera/cahaya/geometri; tampilan toon dengan outline/post-processing | adapt, per shot (opsi, bukan wajib) | Cara menghindari kesan CGI |
| **GSAP** | animasi | Timeline, easing kaya, MotionPath, morph | reference/adapt | **Lisensi** (ketentuan berubah; cek), sinkron dengan render frame deterministik |
| **PixiJS / Canvas 2D** | render 2D | Banyak layer, filter, mask, performa | adapt bila SVG kurang | Integrasi dengan Remotion |
| **SVG + filter/mask/CSS 3D transforms** | teknik | Layer berlapis, perspektif palsu | adopt sebagai teknik | Batas performa filter |
| **Rive / Lottie** | runtime animasi | Karakter berrig | reference/adapt (jika karakter) | Alur pembuatan aset; cocok dengan "visual dari kode"? |
| **ffmpeg** | pipeline | Encode, gabung audio | adopt | – |
| **Skills Remotion resmi / komunitas** | skill | Praktik terbaik Remotion untuk Claude | reference only → adapt bagian teknis | Konflik aturan visual; isi apa adanya |
| **Repo "storyboard"/sinematografi di GitHub** | workflow | Kosakata shot, metode storyboard | reference only | Cari dulu; belum tahu kandidat spesifik |
| **Skill internal `directing-stickman-videos`** (ada di sesi ini) | skill | Metode storyboard/direksi | **reject untuk style**, reference untuk metode | Gaya stickman bertentangan dengan arah Anda |

Catatan: nama/link spesifik repo komunitas **belum saya cantumkan** karena belum dicari; mengarang tautan akan merusak kepercayaan dokumen ini.

## 5. Hal yang mungkin terlewat (perspektif luar)
- **Tool terbaik bisa jadi bukan "animation library", tapi *ilustrasi prosedural*:** fungsi yang menghasilkan bentuk berdetail (noise, SDF, generative texture) menjawab "detail tanpa menggambar manual" lebih baik daripada library animasi.
- **Pelajaran dari domain lain:** compositing film (layer + depth map + defocus), *paper cut-out/diorama* (depth murah tapi kaya), *technical illustration* (cutaway), *2.5D* (kartu bidang di ruang 3D dengan kamera nyata). 2.5D patut diuji karena memberi parallax & perspektif asli dari ilustrasi 2D.
- **Deterministic rendering** (setiap frame murni fungsi dari waktu) menentukan apakah kita bisa QA frame per frame; ini syarat teknis utama untuk host apa pun.

## 6. Keputusan yang diminta
Setujukah saya menjalankan riset terverifikasi (web) untuk area A–F, menghasilkan dokumen kandidat dengan lisensi/link/rekomendasi, **tanpa instalasi apa pun**?
