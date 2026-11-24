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
