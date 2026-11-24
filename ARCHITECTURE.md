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
- `characters/` **ditunda sampai Anda memutuskan karakter diperlukan.**
Aturan tetap: kontrak shot §3; tidak ada template; teknik dipilih per shot.
