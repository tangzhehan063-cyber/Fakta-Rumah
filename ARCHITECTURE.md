# Proposal Arsitektur (Fase 1) — DRAFT untuk review

Tujuan: kerangka yang membuat video **beragam secara visual** namun **otomatis pada bagian mekanis**, tanpa mengunci style. Semua di bawah ini adalah usulan; tidak ada yang dibangun.

## 1. Prinsip (diturunkan dari audit repo lama)

| Pelajaran | Prinsip arsitektur |
|---|---|
| Kunci karakter membekukan hasil | **Tidak ada template video.** Unit produksi = *shot*, bukan "salin video lama". |
| Teknik menentukan tampilan | **Teknik adalah detail internal shot.** Engine tidak tahu apakah shot memakai SVG, Canvas atau R3F. |
| Gerbang dokumen bisa dilewati | **Gerbang berbasis artefak yang bisa diperiksa** (frame/klip hasil render + persetujuan tercatat di manifest). |
| Aturan bertumpuk | **Satu sumber kebenaran per topik**; engine membaca `identity/` bukan menyalinnya. |
| Kedip & ketidakdeterminan | **Shot = fungsi murni dari waktu.** Tidak ada `Math.random()` tanpa seed, tidak ada gerak berbasis jam. |
| Otomasi dulu, kreativitas hilang | **Otomatisasi hanya untuk langkah mekanis**; keputusan kreatif tetap lewat gerbang persetujuan. |

## 2. Lapisan

```
┌────────────────────────────────────────────────────────────┐
│ A. KONTEN        videos/<slug>/   brief → riset → naskah    │  manusia + Claude
│ B. DIREKSI       direction.md, storyboard (md + storyboard.json)│  manusia menyetujui
├────────────────────────────────────────────────────────────┤
│ C. IDENTITAS     identity/        spec (md) → tokens bila perlu│  dibaca B & D
├────────────────────────────────────────────────────────────┤
│ D. SHOT          videos/<slug>/src/shots/*.tsx                 │  kode kreatif per shot
│    - kontrak tipis (§3), teknik bebas per shot                 │
├────────────────────────────────────────────────────────────┤
│ E. ENGINE TIPIS  engine/  timeline, transisi, kamera-helper,   │  ditunda sampai pilot
│    audio-sync, caption                                         │
├────────────────────────────────────────────────────────────┤
│ F. RENDER HOST   Remotion (kandidat) / perender cadangan       │  
├────────────────────────────────────────────────────────────┤
│ G. PIPELINE      tools/ (CLI berbasis manifest): TTS, align,   │  Fase 5–6
│                  render, QA, paket rilis                       │
├────────────────────────────────────────────────────────────┤
│ H. QA            qa/ cek otomatis + tinjauan visual manusia     │
└────────────────────────────────────────────────────────────┘
```

Arah ketergantungan satu arah: A,B → D → E → F. G memanggil F. H membaca output F. **C tidak memiliki kode**; ia dibaca manusia dan (setelah disetujui) menjadi token (palet, easing, durasi) yang diimpor shot **secara opsional**.

## 3. Kontrak shot (satu-satunya "abstraksi" yang diusulkan, harus diuji di pilot)

Sebuah shot adalah komponen dengan masukan waktu dan tanpa efek samping:

```
Shot = {
  id:        string
  durationInFrames
  render:    (frame, fps, ctx) => Visual      // murni; tidak ada state tersembunyi
  notes:     { tujuan, teknik, kamera, alasan } // sinkron dengan storyboard
}
```

- Teknik bebas: SVG, Canvas, CSS 3D, R3F, PixiJS, atau campuran. 
- Kamera adalah **urusan shot**; engine hanya menyediakan *helper opsional* per teknik (mis. kamera R3F, "kamera 2.5D", transformasi perspektif layer 2D). Tidak ada kamera global default.
- Transisi antar shot adalah **shot kecil tersendiri** atau fungsi dua-shot, bukan preset tetap.
- Alasan kontrak ini sebesar ini: cukup untuk otomasi (durasi, urutan, QA frame), cukup kecil untuk tidak membatasi visual. **Jika pilot menunjukkan kontrak ini mengganggu, kita ubah.**

## 4. Struktur folder yang diusulkan setelah pilot (belum dibuat)

```
engine/
  core/        timeline & kontrak shot, util waktu (frame-pure helpers)
  camera/      helper kamera per teknik (r3f, 2.5D, 2D-perspective)   ← hanya jika terbukti dipakai ≥2 shot
  transitions/ transisi kustom yang terbukti berguna
  audio/       sinkron kata→frame, caption
tools/         CLI mekanis (TTS, align, qa, render, package) — kode adaptasi dari repo lama
qa/            checklist + cek otomatis + log
assets/        hanya aset terbukti dipakai ulang; kebijakan: aset kecil di Git, besar di Drive + manifest
```

Aturan: folder baru dibuat hanya saat ada kode nyata yang pindah ke sana setelah dipakai di ≥2 video/klip.

## 5. Manifest video (dasar otomasi Fase 6)

Satu berkas `videos/<slug>/video.json` menjadi "paspor" yang dibaca semua alat:

```
{
  "slug", "title", "category": ["how-it-works", ...],
  "format": {"w":1080,"h":1920,"fps":30},
  "status": {
     "brief":"approved|draft", "script":"...", "direction":"...", "storyboard":"...", "final":"..."
  },
  "approvals": [{ "gate":"storyboard", "by":"owner", "at":"...", "ref":"commit/sha" }],
  "audio": { "vo":"out/vo.wav", "words":"out/words.json", "engine":"gemini-tts@model" },
  "shots": [{ "id","start","end","technique","entry":"src/shots/xxx.tsx" }],
  "qa":   { "last_run":"...", "results":{...} }
}
```

Pipeline Fase 6 hanya bergerak maju jika status gerbang yang relevan `approved`. Itu menggantikan checklist `[x]` lama dengan sesuatu yang bisa diperiksa mesin **dan** dicocokkan dengan artefak (mis. storyboard.json yang disetujui punya hash).

## 6. QA bertingkat

| Level | Apa | Otomatis? |
|---|---|---|
| Q0 Keamanan/aturan | Pemindai API AI/jaringan di kode visual (adaptasi `cek-mandiri`) | ya |
| Q1 Determinisme | Render frame sama dua kali → hash sama; uji perturbasi kecil (adaptasi ide `cek_kilau`) | ya |
| Q2 Struktur | Durasi per shot sesuai manifest; semua frame berhasil; tidak ada frame kosong | ya |
| Q3 Audio | Loudness, F0/laju bicara vs profil suara yang disetujui (adaptasi `cek_suara`) | ya |
| Q4 Visual | Contact sheet + klip pendek per shot, **ditonton** oleh Claude dan pemilik | **tidak**; wajib manusia/Claude melihat render |
| Q5 Identitas | Checklist anti-pola di `identity/` diperiksa terhadap render | semi |

Ketentuan: Claude **tidak menyatakan "selesai"** tanpa melihat frame/klip hasil (Q4). Biaya token Q4 dipangkas lewat *sampling frame yang cerdas* (frame di awal/akhir shot, puncak gerak, titik transisi), bukan dengan melewatkan Q4.

## 7. Otomasi: apa yang bisa dan tidak (jujur)

| Bisa otomatis penuh | Semi-otomatis (Claude + persetujuan) | Tetap manual/kreatif |
|---|---|---|
| TTS, align, mix audio, loudnorm, render per bagian, SRT, paket rilis, QA Q0–Q3, upload ke Drive | Riset, naskah, draft direction, storyboard.json, penulisan kode shot | Memilih metafora visual, menilai estetika, persetujuan gerbang |

**Titik risiko yang harus dikatakan terus terang:** "naskah → video final tanpa campur tangan" untuk visual berkualitas tinggi dan beragam *belum realistis*. Target Fase 6 yang masuk akal: **naskah disetujui → sistem membangun semua langkah mekanis dan menghasilkan draf render + laporan QA**, sementara keputusan visual melewati storyboard yang disetujui. Otomasi shot-level murni (tanpa manusia) hanya mungkin untuk **resep shot yang sudah terbukti**, setelah ada pustaka resep dari video-video sebelumnya.

## 8. Teknologi (usulan, ditentukan ulang di Fase 3 setelah pilot)

- Bahasa: TypeScript untuk shot/engine; Python untuk alat audio/QA (sebagaimana repo lama), keduanya kecil.
- Host render: Remotion (menunggu konfirmasi lisensi, lihat `research/ecosystem-research.md`).
- Dependensi: ditambahkan satu per satu dengan catatan alasan di `research/`.
- Lingkungan: node_modules dan keluaran render di `.gitignore`; MP4/WAV tidak di Git.

## 9. Keamanan & kepatuhan

- Kunci API (Gemini) hanya lewat environment; tidak ada di repo, log, atau manifest.
- Pemindai Q0 memastikan aturan "tanpa AI generation untuk visual".
- Pengecualian terdokumentasi: **Gemini TTS untuk suara** (Anda sudah menyatakan akan diintegrasikan kembali di Fase 5).
- Aset pihak ketiga (foto, SFX): catat sumber dan lisensi di manifest; tolak aset tanpa lisensi jelas (pelajaran dari foto "asal-usul tidak diketahui" di repo lama).

---

# 10. Evaluasi teknik terhadap referensi (Fase 2) — USULAN, belum keputusan

Dasar: `identity/references/01…03`. Tingkat bukti: **[O]** terlihat di referensi · **[K]** pengetahuan saya, **belum diuji** · **[V]** diverifikasi di Fase 1 (`research/ecosystem-research.md`).

## 10.1 Apa yang sebenarnya dibutuhkan referensi (daftar kebutuhan visual)
1. Cahaya lunak berarah dengan **bounce/GI** terasa hangat [O 01].
2. **Bayangan** besar lembut + **ambient occlusion** di celah [O 01, 02, 03].
3. Bentuk **bevel** pada objek [O 01].
4. **DOF** pada close-up dan foreground framing [O 01].
5. **Instansiasi massal** (ribuan gedung/pohon) + animasi pertumbuhan prosedural [O 02].
6. **Teks 3D dan label menempel pada bidang dunia** [O 01, 02].
7. **Kamera kontinu** dengan perspektif nyata dan transisi lewat objek [O 01, 02].
8. *(opsional)* **Karakter berrig** dengan pose dan gerak [O 01].
9. Layar perangkat sebagai tekstur dinamis di dalam dunia [O 01].

## 10.2 Pendekatan, kemampuan, batas
| Pendekatan | Yang bisa direproduksi | Batas | Biaya produksi | Reuse | Performa | Cocok untuk engine kita? |
|---|---|---|---|---|---|---|
| **SVG / CSS** | Layer 2D, parallax datar, UI dan label, teks | Tidak bisa GI/AO/bevel volumetrik; "depth" palsu → mendekati **gagal otomatis** bila jadi dasar scene | rendah | tinggi | baik (filter SVG berat) | **Pelengkap saja** (tekstur UI, tipografi); bukan dasar dunia |
| **Canvas 2D** | Tekstur prosedural, grain, UI dinamis di layar perangkat | Sama dengan di atas | rendah-sedang | tinggi | baik | **Pelengkap** (tekstur untuk objek 3D) |
| **2.5D (kartu di ruang 3D)** | Parallax dan kamera nyata dari ilustrasi 2D | Tidak ada volume sejati; objek tidak bisa diputar | sedang | sedang | baik | **Scene tertentu** (latar jauh, siluet); bukan dasar |
| **Three.js / R3F** (real-time WebGL) [V: MIT] | Cahaya + bayangan lunak (PCSS/VSM), AO, DOF, bloom, tone mapping, instancing ribuan objek, teks 3D, kamera perspektif/ortografik, transisi kamera | **GI sejati tidak ada** (bounce hangat harus dipalsukan: cahaya isi, hemisfer, AO tersimpan); karakter berrig butuh aset; render per frame di Chromium headless **lambat** [K] | tinggi untuk "tampak mahal", sedang untuk "tampak bersih" | tinggi (resep) | sedang | **Kandidat inti untuk dunia spasial** |
| **SDF/raymarch shader "clay renderer"** [K, ide saya, belum diuji] | Bevel alami (smooth-min), **bayangan lunak dan AO analitik**, tampilan clay yang sangat dekat dengan 01–03, deterministik | Skala scene terbatas (ribuan objek berat), karakter sulit, pengembangan shader mahal | tinggi di awal, rendah per objek sederhana | sedang | tergantung GPU | **Kandidat pilot** (khusus objek hero/miniatur) |
| **Pra-bake pencahayaan lewat kode** [K, ide saya] | Hitung AO/bounce offline (ray tracing sederhana) → simpan sebagai tekstur/vertex color → tampilkan di Three.js real-time | Statis (benda yang bergerak butuh cara lain); pengembangan alat | sedang | tinggi | sangat baik saat render | **Kandidat pilot** (menutup kesenjangan GI) |
| **Blender headless via Python (bpy)** [K] | Persis tampilan referensi (Eevee/Cycles, GI, DOF, bevel, rigging, geometry nodes); **dikendalikan kode** | Toolchain berat (aplikasi GPL, keluaran bebas dipakai [K]), render offline lambat tanpa GPU, perlu menginstal di sini/di mesin Anda, dua bahasa (TS + Python), bukan "stack web" | tinggi di awal; render-time besar | tinggi | offline | **Opsi strategis yang perlu keputusan Anda** (lihat 10.4) |
| **GSAP** [V: lisensi "no charge"] | Timeline, easing, morph/motion-path untuk elemen 2D | Tidak menyelesaikan pencahayaan/volume; harus bisa di-*seek* per frame | rendah | tinggi | baik | **Opsional** |
| **Remotion** [V] | Host render per frame, komposisi, audio, caption, transisi | Lisensi (bersyarat); render lambat bila isi WebGL berat | rendah | tinggi | sedang | **Inti sebagai host** (bersyarat) |
| **Sistem prosedural kustom** | Pertumbuhan/reveal bertahap (02), penyebaran pohon/gedung, aliran garis putus-putus | Harus dibuat | sedang | tinggi | baik | **Inti** (ini yang paling berharga dan khas) |

## 10.3 Rekomendasi sementara (untuk ditinjau)
- **Inti:** (1) *Kontrak shot murni-waktu* (tetap dari §3), (2) **Remotion** sebagai host jika lisensi lolos, (3) **Three.js/R3F** sebagai teknik spasial utama, (4) **sistem prosedural kustom** (scatter, growth/reveal, kamera, rig cahaya) sebagai nilai khas channel.
- **Opsional per shot:** SVG/CSS/Canvas untuk tekstur UI/tipografi, 2.5D untuk latar jauh, GSAP untuk elemen 2D, postprocessing (DOF/AO/bloom).
- **Harus dibandingkan di pilot, bukan diputuskan sekarang:** (a) Three.js real-time langsung, (b) Three.js + **pra-bake cahaya**, (c) **SDF clay** untuk objek hero, (d) **Blender headless** (jika Anda izinkan).
- **Alternatif jika kesenjangan kualitas cahaya tak tertutup:** pindah sumber render ke Blender headless dan menjadikan Remotion hanya host untuk teks/caption/audio. Kontrak shot dibuat agar sebuah shot bisa berupa "urutan frame dari renderer lain" tanpa mengubah pipeline lain.

## 10.4 Satu hal yang menurut saya sedang terlewat
Dua dari tiga referensi Anda hampir pasti dibuat dengan **render 3D offline** (03 pasti Blender [O]). Tampilan GI lunak, DOF, dan bevel bersih itu mudah di sana dan **mahal di web real-time**. Jika kita memilih stack web karena kebiasaan, bisa saja kita mengulang pola repo lama: stack menentukan tampilan. Karena Anda menekankan "visual dibuat melalui kode", Blender via Python adalah *kode*, tetapi mengubah pilihan alat. **Ini keputusan Anda**, bukan saya.

## 10.5 Arsitektur engine awal (pembaruan §3–§4, tetap tidak dibangun)
Tambahan modul *kandidat* (dibuat hanya jika terbukti dipakai ≥2 kali):
- `world/` penyusun dunia dan set-piece, aturan "membumi" (bayangan kontak).
- `light/` preset rig cahaya sebagai **data** (arah, warna, kekerasan bayangan), bukan kode per shot.
- `camera/` kamera kontinu: jalur, fokus, DOF, ortografik↔perspektif.
- `reveal/` koreografer reveal bertahap (stagger, gelombang, urutan sebab-akibat).
- `worldtext/` teks/label yang menempel pada bidang dunia (SDF/ekstrusi).
- `scatter/` instansiasi massal.
- ~~`characters/`~~ **dibatalkan**: pemilik menghindari karakter (keputusan #3).
Aturan tetap: kontrak shot §3; tidak ada template; teknik dipilih per shot.

## 10.6 Persyaratan yang diturunkan dari keputusan pemilik
- **Sadar-rasio:** format (`9:16` sekarang, `16:9` kelak) hidup di manifest `video.json`. Komponen shot menerima ukuran kanvas dan tidak meng-hardcode 1080×1920. Komposisi per rasio dipikirkan di storyboard (satu shot boleh punya framing berbeda per rasio).
- **Pilot memuat dua jalur render** (stack web dan Blender-Python) untuk set uji yang sama, dengan kontrak shot yang sama (shot dapat berupa urutan frame dari renderer lain).
- **Tanpa karakter:** tidak ada kebutuhan rigging; prioritas pindah ke cahaya, material berkarakter, kamera, dan reveal prosedural.

---

# 11. Arsitektur "Cinematic Illusion" — arah baru (kompositor Remotion: usulan resmi bersyarat; lihat `workflow/build-phases.md`)

Dasar: arahan pemilik (produksi dokumenter berdurasi menit pada CPU-only; persepsi 3D, bukan 3D penuh) dan `research/illusion-findings.md`. Prinsip: **pisahkan pembuatan dunia yang mahal (sekali) dari kompositing yang murah (berulang).** Mengganti §10.3 sebagai arah utama; §3 (kontrak shot murni-waktu) tetap.

## 11.1 Dua mesin, satu kontrak
```
                    ┌───────────────────────────────┐
  spesifikasi dunia │  PABRIK PLAT (mahal, sekali)  │  cache berbasis hash
  (JSON + generator)│  Blender/Three.js kualitas    │  cache/plates/<hash>/
  ─────────────────►│  beauty, kedalaman, topeng    │
                    │  objek/lapisan, plat latar    │
                    │  bersih, (lightgroups)        │
                    └───────────────┬───────────────┘
                                    │ plat + metadata
                    ┌───────────────▼───────────────┐
  storyboard + mode │  KOMPOSITOR (murah, per frame)│  Remotion
  per shot ────────►│  bidang berkedalaman, kamera, │  → frame JPEG/segmen
                    │  efek cahaya/atmosfer/blur LOD│  → ffmpeg
                    └───────────────────────────────┘
```
- **Pabrik plat:** dari spesifikasi dunia (sama dengan format P0) menghasilkan *plat*: beauty, peta kedalaman 16-bit (0,5–1,1 dtk per plat [U]), topeng per objek/lapisan, **plat latar bersih** tanpa objek depan (untuk menutup disokulasi), dan blur LOD (mis. 0/4/12 px). Kunci cache = hash(spesifikasi + kamera + pengaturan). Revisi narasi/waktu/kamera-dalam-amplop **tidak** memicu render ulang plat.
- **Kompositor:** adegan multi-bidang. Setiap bidang punya z, topeng, LOD blur, dan efek (cahaya, kabut). Kamera berbasis data (koordinat bola, sama seperti P0) menggerakkan semua bidang lewat satu fungsi: DOM/CSS-3D untuk bidang datar, mesh kedalaman Three.js untuk parallax kedalaman, R3F untuk geometri sederhana (Mode C).
- **Kontrak shot** (perluasan §3): `{ id, mode: A|B|C|D, plates: [...], camera: {plan, envelope}, effects: [...], purpose }`. Teknik tetap detail internal shot.

## 11.2 Empat mode produksi (per shot, bukan per video)
| Mode | Isi | Teknik | Biaya terukur/perkiraan | Catatan |
|---|---|---|---|---|
| **A Cinematic 2D** | citra statis berlapis, kamera kecil, cahaya, atmosfer | lapisan + CSS-3D + blur LOD | ≈ 0,15–0,3 dtk/frame [U] | **Foto arsip/gambar nyata hanya dengan persetujuan eksplisit per kasus** (syarat mutlak §1b); tanpa AI |
| **B Cinematic 2.5D** | lingkungan/objek dengan kedalaman, reveal | plat dari 3D + peta kedalaman + bidang perspektif | ≈ 0,35–0,4 dtk/frame [U] | **amplop gerak kamera sempit** (§11.4) |
| **C 3D prosedural** | mekanisme bergerak, perakitan, sisi berbeda | Three.js hemat (shadow statis, tanpa AO/DOF/MSAA real-time) | ≈ 1,3 dtk/frame [U] | AO/DOF boleh **dipanggang** atau ditambahkan di kompositor |
| **D 3D penuh** | simulasi, perubahan struktur besar, gerak kamera besar | Blender (pra-render) atau 3D web | ≈ 17 dtk (web berat) – ±47 dtk+ (Cycles 16 spp) per frame [U/ekstrapolasi] | pengecualian; di-cache per shot |

## 11.3 Sistem keputusan teknik per shot (usulan)
Pertanyaan berurutan, ambil mode termurah yang lolos:
1. Apakah ada **gerak benda** atau perubahan sisi (perakitan, aliran, simulasi)? Ya → C (atau D bila simulasi). Tidak → lanjut.
2. **Kamera bergerak melewati amplop 2.5D?** Ya → C/D, atau bagi menjadi dua plat + transisi bermotivasi. Tidak → lanjut.
3. Apakah butuh **kedalaman nyata** (parallax kuat, orbit kecil)? Ya → B. Tidak → A.
4. Efek tambahan hanya bila **punya tujuan naratif** (lihat 11.5).

**Anggaran variasi (usulan, dicek otomatis di storyboard):** per video, push-in ≤ 30% shot; ≥ 15% shot statis; ≥ 15% lateral/tracking; partikel ≤ 35%; sapuan cahaya ≤ 25%; DOF aktif ≤ 40%; tidak ada dua shot berurutan dengan kombinasi kamera+efek identik. Angka bisa diubah pemilik; tujuannya mencegah repetisi.

## 11.4 Amplop kamera untuk 2.5D (dari data §3 findings [U][P])
Dari satu plat: PSNR ≥ 32 dB hingga ≈15% jalur uji (dolly ≲0,3 m dari 3,9 m; orbit ≲2–3°); turun cepat sesudahnya. Keputusan sementara: **amplop B = ±8–10% dolly dan ±3° orbit/tilt per plat**; gerak lebih besar memakai plat tambahan dan transisi bermotivasi (bukan cross-fade polos, yang menghasilkan bayangan ganda), atau Mode C/D. Amplop harus dikalibrasi ulang dengan plat berlapis (belum diuji).

## 11.5 Toolkit ilusi (status)
| Kapabilitas | Teknik | Status |
|---|---|---|
| Push-in, pan, tilt, tracking kecil | transform bidang + mesh kedalaman | **terbukti** dalam amplop [U] |
| Orbit ilusi / perspective shift | mesh kedalaman, plat berlapis | terbukti sempit; berlapis **belum diuji** |
| Parallax dan multi-plane | z per bidang (CSS-3D) | **terbukti murah** [U] |
| Blur fokus / rack focus | blur LOD dipanggang + cross-fade | murah [U: 0,27 dtk]; kualitas visual **belum dinilai** |
| Sapuan cahaya, highlight bergerak | overlay gradien + blend, topeng | murah [U]; kualitas **belum dinilai** |
| Relighting (cahaya jendela bergeser) | *light groups* di Blender → kompositing intensitas | [K] **belum diuji** |
| Kabut, debu, berkas cahaya | lapisan prosedural berkedalaman + topeng | [K] belum diuji |
| Partikel halus | canvas/DOM | murah [U]; aturan: hanya bila beralasan |
| Material (logam, kaca, air) | sapuan cahaya, refleksi dipanggang, tekstur bergerak | [K] belum diuji |
| Handheld micro-motion | noise deterministik (`@remotion/noise`, MIT) | [K] sangat selektif |

## 11.6 Performa dan operasional
- **Tiga tingkat pratinjau:** (1) contact sheet still dari kompositor ×0,25; (2) animatic 540p 15 fps; (3) final. Hanya (3) memicu render penuh.
- **Render per shot + cache frame** (shot yang tidak berubah dilewati), digabung ffmpeg, seperti pola render-per-bagian repo lama [V].
- **Anggaran biaya per shot** dicatat di manifest (mode, ms/frame terukur, jumlah plat).
- Hindari blur real-time dan filter berat; pakai LOD dipanggang. Paralelisme 4 worker hanya ±1,7× pada isi berat [U]; rancang agar isi murah.
- Resolusi sadar-rasio (9:16 sekarang, 16:9 kelak) di manifest.

## 11.7 QA tambahan untuk ilusi
Selain Q0–Q5 (§6): **Q6 artefak ilusi** — cek tarikan tekstur di tepi benda, bayangan ganda, lubang disokulasi, pop antar-keyframe, di frame-frame kritis; **Q7 variasi** — pemeriksaan anggaran variasi §11.3; **Q8 persepsi** — tinjauan visual manusia/Claude terhadap klip (wajib; kode berjalan bukan bukti lulus).

## 11.8 Yang perlu didesain ulang dari keadaan sekarang
Spesifikasi dunia P0 → masukan pabrik plat; kontrak shot → tambah `mode/plates/envelope`; renderer web P0 → profil "hemat" sebagai bawaan; Blender → pabrik plat (bukan perender video penuh); QA → Q6–Q8; manifest `video.json` → tambah mode, plat, anggaran.

## 11.9 Aturan pembuatan plat (dipelajari di P1 v2, diuji) [U][P]
1. **Lapisan mengikuti urutan kedalaman dari kamera**, bukan fungsi benda. Contoh: pipa di dalam lemari berada di lapisan tengah di belakang cangkang lemari (FRONT), bukan di depannya.
2. **Benda yang berdiri di atas permukaan satu lapisan dengan permukaan itu** (botol + dasar lemari); jika tidak, permukaan di depan benda menutupinya dengan bayangan kontak.
3. **Objek di luar lapisan dibuat tak terlihat kamera tetapi tetap membayangi/memantulkan cahaya** (`visible_camera=False` di Cycles): pencahayaan konsisten dan lapisan di belakang lengkap (tanpa lubang disokulasi).
4. **Faktor parallax antar-lapisan berdekatan** (mis. 0,5/0,68/0,85) agar garis kontak tidak meluncur; kedalaman terasa dari skala push-in dan blur latar/depan.
5. **Rack focus = bobot ketajaman per kedalaman** (selalu ada lapisan yang tajam); blur dipanggang per lapisan (LOD) lalu cross-fade.
6. **Transisi:** potong yang disembunyikan oleh lepas-fokus lebih aman daripada larut antar-kamera (yang menghasilkan citra ganda).
7. Biaya pabrik plat ≈3,3–4 menit per shot (3 lapisan, 48 spp, CPU 4 inti); biaya Remotion ≈33,8 dtk per 12 dtk.

## 11.10 Kamera isometrik/ortografik (dipelajari di P1 v3) [U][P]
1. **Truck, pedestal, dan zoom pada kamera ortografik = transformasi kaku 2D tanpa parallax.** Cukup **satu plat overscan** yang digeser/diskalakan di Remotion; tanpa artefak. Resolusi plat harus setara kerapatan piksel pada zoom akhir (mis. 600 px/m untuk frame penuh; 1008 px/m untuk zoom 1,26×).
2. **Zoom dibatasi resolusi plat:** zoom lebih besar memerlukan plat berpiksel lebih banyak (biaya Blender naik kuadratik).
3. **Orbit memerlukan sudut pandang baru:** pakai keyframe tiap ≤2° (beauty + kedalaman 16-bit, ±97 dtk per keyframe pada 1080×1920) lalu reproyeksi mesh kedalaman ortografik; campur dua keyframe terdekat; rentangkan piksel pinggir (padding 6%) agar tidak ada lubang di tepi. Hasil bersih pada ±4° dari pusat.
4. **Dunia harus melampaui frame:** lantai/dinding diperluas (6,4 m, tinggi 4 m) agar isometrik tidak terbaca sebagai blok diorama melayang di latar abu.
5. **Setiap derajat kebebasan kamera punya biaya plat sendiri:** truck = 1 plat lebar; zoom = plat resolusi lebih tinggi; orbit = N keyframe. Rencanakan di storyboard.
6. **Komposisi vertikal 9:16 pada isometrik** menyisakan area dinding atas yang besar; atur target kamera lebih rendah dan isi dinding dengan elemen bermotivasi.
