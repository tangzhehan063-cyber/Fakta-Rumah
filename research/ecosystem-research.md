# Riset Ekosistem — Laporan (terverifikasi sebagian)

Tanggal riset: 24 Nov 2026. **Tidak ada yang diinstal atau diadopsi.** Semua rekomendasi menunggu review Anda.

## 0. Cara membaca laporan ini (tingkat bukti)

| Tanda | Arti |
|---|---|
| **[V-npm]** | Diverifikasi langsung dari registry npm hari ini (`npm view`): versi, lisensi, tanggal publish terakhir |
| **[V-file]** | Diverifikasi dengan membaca file sumber (mis. `LICENSE.md` dari paket Remotion, repo yang di-clone dangkal) |
| **[V-web]** | Dari hasil pencarian web (sumber sekunder atau cuplikan); belum dicek ke sumber primer |
| **[K]** | Pengetahuan saya, **belum diverifikasi**; harus diuji di pilot |

Keterbatasan jujur: jumlah bintang/aktivitas GitHub tidak saya ambil (API GitHub tidak terbuka untuk repo di luar sesi ini). "Aktivitas" saya ukur dari tanggal commit/publish terakhir. Beberapa repo hasil pencarian **tidak saya buka** (ditandai).

---

## 1. Temuan utama (ringkas)

1. **Remotion tetap kandidat host render terkuat**, dengan **satu syarat hukum yang harus Anda konfirmasi**: lisensi gratis hanya untuk individu, perusahaan for-profit ≤3 karyawan, atau nirlaba. Lisensi akan "sedikit berubah" di Remotion 5.0 **[V-file]**. Paket pendukung `@remotion/three/paths/noise/motion-blur/shapes` berlisensi MIT **[V-npm]**; `remotion`, `transitions`, `lottie` memakai lisensi Remotion **[V-npm]**.
2. **Three.js / R3F / drei: MIT, aktif** (three 0.187.0, publish 30 Okt 2026) **[V-npm]**. Cocok sebagai teknik per-shot, bukan default.
3. **GSAP kini gratis termasuk komersial dan semua plugin** (lisensi "no charge" sejak 30 Apr 2025, setelah akuisisi Webflow) **[V-web]**. Ia bukan OSI open-source dan melarang penggunaan di alat animasi visual no-code yang bersaing. Untuk render deterministik per-frame, nilai tambahnya terhadap `interpolate/spring` Remotion perlu dibuktikan, bukan diasumsikan.
4. **Skill resmi `remotion-dev/skills`** (commit terakhir 23 Nov 2026, 13 folder skill) **[V-file]**: kandidat *adapt* untuk pengetahuan teknis Remotion. **Tidak ada file LICENSE di root repo** dan `package.json` tidak mencantumkan lisensi **[V-file]**: status hukum penyalinan teksnya tidak jelas; memakainya sebagai skill terinstal sesuai petunjuk resmi Remotion tidak sama dengan menyalin isinya.
5. **`video-shotcraft` (Apache-2.0)** punya ratusan "kartu resep shot" dan pipeline Remotion, tetapi orientasinya **video promo produk web**. Berguna sebagai **perpustakaan teknik gerak/kamera untuk dipelajari**, bukan skill untuk dipasang **[V-file]**.
6. **Skill storyboard komunitas yang saya temukan hampir semuanya untuk memberi prompt ke generator video AI**, jadi tidak relevan dengan larangan Anda (reject; ide metodenya saja yang dicatat).
7. **Tidak ada library animasi yang menyelesaikan masalah utama Anda** (depth, detail, ilustrasi bergaya). Itu pekerjaan *ilustrasi prosedural* dan *komposisi/kamera*; library hanya mengurus gerak. Lihat §6.

---

## 2. A. Ekosistem Remotion

| Item | Versi / tanggal | Lisensi | Kemampuan | Rekomendasi |
|---|---|---|---|---|
| **remotion** (core) | 4.0.546, 23 Nov 2026 [V-npm] | Lisensi Remotion (custom) [V-file] | Render deterministik per frame (React), Studio untuk preview, `interpolate`, `spring`, `Sequence`, still & video | **adopt (kandidat, menunggu konfirmasi lisensi)** |
| `@remotion/transitions` | 4.0.546 [V-npm] | Lisensi Remotion | `TransitionSeries`, preset fade/slide/wipe/flip/clock-wipe, timing linear/spring, presentasi kustom [V-web] | **adapt**: pakai sebagai mekanisme; transisi kreatif kita **buat kustom** (preset bawaan = rasa template) |
| `@remotion/three` | 4.0.546 [V-npm] | MIT | `ThreeCanvas` (butuh width/height eksplisit), `useVideoTexture`, kini juga `ThreeWebGPUCanvas` di dokumen terbaru [V-web] | **adapt per shot** |
| `@remotion/paths` | 4.0.546 | MIT | Ukur/animasikan SVG path (draw-on, titik di sepanjang path) [K] | **adopt (kandidat)** untuk shot SVG |
| `@remotion/noise` | 4.0.546 | MIT | Noise deterministik untuk gerak organik [K] | **adopt (kandidat)** |
| `@remotion/motion-blur` | 4.0.546 | MIT | Motion blur via sub-frame sampling [K] | **evaluasi di pilot** (biaya render naik) |
| `@remotion/shapes` | 4.0.546 | MIT | Primitif bentuk SVG [K] | reference only |
| `@remotion/lottie` | 4.0.546 | Lisensi Remotion | Memutar Lottie | **reject untuk sekarang** (aset Lottie dibuat di tool lain, bertentangan "visual dari kode") |
| **Skills `remotion-dev/skills`** | commit 23 Nov 2026 [V-file] | **Tidak ada LICENSE di repo** [V-file] | Skill: best-practices, create, markup, render, captions, studio, docs, upgrade, dll. | **adapt**: pasang hanya di Fase 3 setelah persetujuan, dipakai sebagai pengetahuan *teknis*; aturan visual tetap milik kita |
| Pola render/performa | — | — | Concurrency, codec, render per bagian (old repo sudah punya pola render per 15 dtk) [V-file repo lama] | **reference** + uji di pilot |

**Risiko khusus Remotion**
- *Lisensi (butuh keputusan Anda):* free untuk individu / ≤3 karyawan / nirlaba. Jika channel ini kelak dijalankan oleh badan usaha >3 karyawan, perlu Company License (harga: **belum terverifikasi**, sumber web saling bertentangan: "min. $100/bln" vs "mulai $500/bln"; cek `remotion.dev/pricing`). Perubahan lisensi di Remotion 5.0 perlu dibaca saat rilis.
- *Penguncian ke React/Chromium:* konsekuensinya render lambat dan setiap kode shot harus murni fungsi frame (pelajaran dari bug repo lama: `useFrame` R3F dan `Math.random()` menimbulkan kedip).
- **Hedge (usulan "orang luar"):** inti Remotion pada dasarnya = "halaman web deterministik yang di-screenshot per frame lalu di-encode ffmpeg". Jika lisensi/biaya jadi masalah, kontrak shot kita (lihat `ARCHITECTURE.md` §3) cukup tipis untuk dihosting oleh perender Playwright+ffmpeg buatan sendiri. Kita tidak membangunnya sekarang; kita hanya **menjaga kontrak shot tetap bebas dari API Remotion di dalam kode teknik**.

---

## 3. B. Ekosistem Three.js

| Item | Versi / tanggal | Lisensi | Kemampuan | Rekomendasi |
|---|---|---|---|---|
| **three** | 0.187.0, 30 Okt 2026 [V-npm] | MIT [V-npm] | Kamera, cahaya, geometri, `MeshToonMaterial`, `OutlineEffect` (khusus WebGLRenderer), `ToonOutlinePassNode` untuk WebGPU [V-web], shader kustom | **adapt per shot** |
| **@react-three/fiber** | 9.8.2 [V-npm] | MIT | Three.js deklaratif (React 19) | adapt per shot |
| **@react-three/drei** | 10.7.9 [V-npm] | MIT | Helper (kamera, teks, environment) | **reference/adapt**: ambil per-helper, jangan seluruh paket |
| **postprocessing** (pmndrs) | 6.39.6 [V-npm] | **Zlib** (permisif) | Efek pasca-proses (outline, DOF, bloom, SSAO) | **evaluasi di pilot** untuk DOF & outline stylized |
| three-custom-shader-material | 6.4.0, publish terakhir Okt 2025 [V-npm] | MIT | Memodifikasi material bawaan dengan shader kustom | reference |
| troika-three-text | 0.53.1 [V-npm] | MIT | Teks SDF di 3D | reference |
| three-mesh-bvh | 0.9.18 [V-npm] | MIT | Raycast/BVH cepat | reference only |

**Catatan style:** three.js tidak otomatis = CGI. Tampilan "ilustrasi" di 3D dicapai lewat material toon/matcap, outline, shading terkuantisasi, tekstur prosedural, dan **tanpa** pencahayaan fisik realistis **[K, uji di pilot]**. Old repo membuktikan 3D prosedural *bisa* dibangun lewat kode, tetapi hasil akhirnya (arsitektur semi-realistis) justru yang Anda tolak sekarang; jadi 3D di sini **hanya dipakai bila lebih jelas untuk shot tertentu**.

---

## 4. C. SVG, Canvas, CSS, dan library gerak 2D

| Item | Versi / tanggal | Lisensi | Kemampuan | Rekomendasi |
|---|---|---|---|---|
| **GSAP** | 3.15.1, 11 Nov 2026 [V-npm] | "Standard no-charge" (bukan OSI) [V-npm]; gratis komersial + semua plugin sejak 30 Apr 2025 [V-web] | Timeline, easing kaya, MotionPath, MorphSVG, SplitText | **adapt opsional per shot**; butuh bukti bisa di-*seek* deterministik per frame [K]; larangan: alat animasi visual no-code yang bersaing |
| **PixiJS** | 8.23.0, 20 Nov 2026 [V-npm] | MIT | Render 2D WebGL: banyak layer, filter, mask | **kandidat** bila SVG/Canvas tak cukup untuk layer berdetail banyak |
| **anime.js** | 4.5.0 [V-npm] | MIT | Animasi ringan | reference only (Remotion + `interpolate` cukup) |
| **motion** | 14.14.0 [V-npm] | MIT | Animasi UI | reject (berorientasi real-time/UI, bukan per frame) |
| **Rive** (`@rive-app/canvas`) | 2.55.1, 23 Nov 2026 [V-npm] | MIT (runtime) | Animasi berrig/state machine | **reference only**: aset dibuat di editor Rive [K], bertentangan "visual dari kode" |
| **lottie-web** | 5.13.0, Mei 2025 [V-npm] | MIT | Memutar Lottie | reject (alasan sama) |
| **paper.js** | 0.17.0 [V-npm] | MIT | Grafik vektor di Canvas, operasi boolean path | reference (boolean path berguna untuk siluet/potongan) |
| **Two.js** | 0.8.24 [V-npm] | MIT | Render 2D multi-backend | reference only |
| **p5** | 2.4.0 [V-npm] | **LGPL-2.1** | Creative coding | **reference only** (LGPL: hindari tertaut ke kode kita) |
| **matter-js** | 0.20.0, Jun 2024 [V-npm] | MIT | Fisika 2D | reference (stale; simulasi bisa ditulis sendiri) |
| **flubber** | 0.4.2, 2022 [V-npm] | MIT | Morph path | reference (stale; kecil) |
| **d3-ease** | 3.0.2 [V-npm] | BSD-3 | Fungsi easing | **adopt (kandidat)**: kecil, murni |
| **svg-path-properties** | 2.2.0 [V-npm] | ISC | Panjang/titik path | reference |
| **Theatre.js** | core 0.7.2 Apache-2.0, **studio AGPL-3.0**, publish terakhir Mei 2024 [V-npm] | beda | Timeline editor visual | **reject** (studio AGPL; stale) |

**Teknik (belum diuji; semua [K])** yang akan dibandingkan di pilot, per tujuan visual:
- **2.5D**: ilustrasi 2D berlapis sebagai bidang di ruang 3D dengan kamera perspektif sungguhan → parallax dan perspektif asli, biaya jauh di bawah 3D penuh.
- **CSS 3D transforms / perspective** dan **SVG** (mask, clipPath, `feTurbulence`/`feDisplacementMap`/blur untuk tekstur dan DOF palsu) — waspadai biaya filter SVG di Chromium headless.
- **Canvas 2D / WebGL fragment shader** untuk tekstur prosedural, grain, cahaya & bayangan stylized, SDF 2D.
- **Bayangan stylized**: contact shadow + cast shadow keras/lembut bergantung style, dapat dibangun sebagai layer terpisah.
- **Kamera simulasi** untuk layer 2D: dolly/orbit lewat transform perspektif per layer, rack focus lewat blur per kedalaman.

---

## 5. D. Skill Claude dan repo GitHub

| Kandidat | Isi | Lisensi | Aktivitas | Pengalaman bukti | Rekomendasi |
|---|---|---|---|---|---|
| **remotion-dev/skills** | Skill Remotion resmi (13 folder) | Tidak ada LICENSE di repo [V-file] | Commit 23 Nov 2026 | Di-clone, daftar dibaca; isi `SKILL.md` belum dibaca penuh | **adapt** (Fase 3) |
| **Vincentwei1021/video-shotcraft** | Skill + pustaka: ±124 kartu resep shot (README menyebut 150 shot di galeri; angkanya tak konsisten), template "Ink Press", sound design & sumber SFX (Freesound), pipeline 6 tahap, `shot-polish` (alat QC perbandingan) | **Apache-2.0** [V-file] | Commit 21 Nov 2026; repo ±44 MB | Di-clone; SKILL.md dibaca sebagian (bahasa campuran Mandarin) | **reference only** untuk kosakata gerak/kamera (adaptasi resep individual diperbolehkan dengan atribusi Apache-2.0); **reject** template Ink Press dan aturan estetikanya (video promo produk). Alat `sfx-source` layak dilihat di Fase 5 |
| **aicontentskills/ai-video-storyboard-skill** | Rencana shot + prompt untuk generator video AI | README/agregator: MIT; **tidak ada file LICENSE di root** [V-file] | Commit 9 Apr 2026 | Dibaca bagian awal | **reject** (untuk generator AI). Ide dicatat: *konsistensi antar shot lebih penting daripada satu shot sempurna* |
| H4pplness/storyboard-skill, smixs/visual-skills, SallyRS/video-director (basis HyperFrames), bluzir/claude-code-design, calesthio/OpenMontage | Muncul di hasil pencarian | tidak diperiksa | tidak diperiksa | **Tidak dibuka** | **belum dievaluasi**. `video-director` berbasis HyperFrames, yang sudah Anda tolak di repo lama; yang lain berkesan untuk prompt generator AI [V-web] |
| Skill di sesi ini `directing-stickman-videos`, `social-video-scriptwriting` | — | tidak dievaluasi | — | — | stickman = **reject** untuk style; `social-video-scriptwriting` kandidat *reference* untuk naskah (Fase 5/6) |

**Kesimpulan D:** tidak ada skill yang cocok langsung untuk "storytelling visual explainer ber-style sendiri". Kita **tidak perlu memasang skill komunitas**; kita perlu (a) skill Remotion resmi untuk hal teknis, dan (b) *membuat* proses direksi/storyboard kita sendiri (sudah dirancang di `workflow/`). Pencarian lanjutan (GitHub) bisa dilakukan jika Anda ingin; saya hanya melakukan 1 pencarian skill luas.

---

## 6. E. Hal yang dilewatkan banyak orang (hasil riset + analisis)

1. **Tidak ada "library untuk depth dan detail".** Library gerak hanyalah 20% masalah; 80% adalah *produksi ilustrasi*. Pertanyaan riset yang lebih penting: *bagaimana menghasilkan ilustrasi berdetail dari kode secara efisien*, misalnya generator prosedural (noise, scatter/instansiasi, SDF, gradient map toon) dan **pustaka resep bentuk milik sendiri**. Ini akan jadi pusat Fase 3, bukan memilih library animasi.
2. **Deterministik per frame adalah syarat keras untuk QA.** Semua kandidat dinilai dengan satu tes: bisa dirender dua kali dengan hasil identik? (old repo kehilangan banyak waktu pada kedip akibat ketidakdeterminan).
3. **Teknik terbaik per kasus mungkin campuran:** 2.5D untuk lingkungan, SVG untuk diagram bermotivasi, R3F hanya untuk objek yang perlu diputar/ditembus. Pilot harus membandingkan, bukan memutuskan di muka.
4. **Kekeliruan umum:** menganggap kendala "tanpa AI generation" berarti "tanpa detail". Detail yang kaya bisa dihasilkan prosedural, tetapi biayanya ada di waktu desain tiap resep. Biaya ini diukur di pilot (Fase 4).

---

## 7. Audio / TTS (relevan untuk Fase 5)

| Item | Bukti | Catatan |
|---|---|---|
| **Gemini TTS** (dipakai repo lama) | Skrip lama memakai model `gemini-2.5-flash-preview-tts`, `gemini-3.1-flash-tts-preview`, `gemini-2.5-pro-preview-tts`; VO Indonesia sudah dihasilkan (suara "Achernar") [V-file repo lama]. Harga 2.5 Flash TTS: $0,50/M token input dan $10/M token output audio, tanpa free tier; 3.1 disebut punya free tier; semua *preview* [V-web, sumber pihak ketiga, belum resmi] | **Verifikasi ulang di Fase 5** (halaman resmi Gemini API). Dukungan Bahasa Indonesia terbukti dari penggunaan lama, bukan dari dokumen |
| edge-tts, ElevenLabs | Repo lama punya jalur cadangan edge-tts; ElevenLabs disebut "hemat kredit" | Putuskan di Fase 5 |
| Sinkronisasi kata | Repo lama: `align_teks.py` (ffmpeg silencedetect + DP, akurasi ±0,1–0,3 dtk) tanpa API | **adapt**, lihat `research/repo-lama-audit.md` |

---

## 8. Shortlist rekomendasi (untuk keputusan Anda)

| Keputusan | Rekomendasi |
|---|---|
| Host render | **Remotion** (jika lisensi lolos); jaga kontrak shot bebas dari API Remotion |
| Teknik 3D | `three` + `@react-three/fiber` via `@remotion/three`, per shot saja |
| Teknik 2D/2.5D | SVG + CSS 3D + Canvas, ditambah **PixiJS bila perlu**; **keputusan lewat pilot, bukan sekarang** |
| Gerak | `interpolate/spring` Remotion + `d3-ease`; **GSAP opsional** jika terbukti perlu (MorphSVG/MotionPath) |
| Skill | `remotion-dev/skills` di Fase 3 saja; tidak ada skill komunitas dipasang |
| Ditolak | Lottie, Rive, motion, Theatre.js (AGPL), p5 (LGPL), skill storyboard untuk generator AI, HyperFrames |
| Referensi saja | video-shotcraft, paper, matter-js, flubber, Two.js |

**Tidak ada instalasi besar dilakukan atau diusulkan sebelum Fase 3 dan persetujuan Anda.**
