# Proposal Repository — Tahap 0

## 1. Diagnosis singkat masalah repo lama (sebagai hipotesis)

Saya belum membaca `Channel-Penjelasan`. Dari deskripsi Anda, pola kegagalannya kemungkinan:

| Gejala | Penyebab struktural yang mungkin | Pencegahan di repo ini |
|---|---|---|
| Instruksi bertumpuk, workflow bertentangan | Aturan ditambahkan di banyak file/skill setiap ada keluhan | Satu sumber kebenaran per topik; CLAUDE.md hanya menunjuk, tidak menduplikasi |
| Visual berulang tidak sesuai | Style ditebak dari teks, bukan dari referensi; teknik (SVG/top-down) menentukan style | Style hanya berasal dari analisis referensi; teknik dipilih belakangan |
| Semua video mirip | Template/komponen generik dibuat dini | Tidak ada komponen reusable sebelum terbukti dipakai ≥2 video |
| "Selesai" tapi hasil salah | QA membaca kode, bukan menonton | QA wajib melihat frame/klip hasil render |

Catatan: ini tebakan terdidik. Kalau Anda mau, saya baca repo lama hanya untuk mengonfirmasi, tanpa mengimpor apa pun.

## 2. Prinsip desain repo

1. **Dokumen sebelum kode.** Kode lahir dari storyboard yang disetujui.
2. **Satu sumber kebenaran per topik.** Tidak ada aturan visual di tempat selain `identity/`.
3. **Identitas ≠ template.** Identitas = bahasa visual (palet, cara membentuk objek, cahaya, ritme gerak). Template = layout tetap. Kita hanya punya yang pertama.
4. **Teknik mengikuti shot.** Setiap shot memilih teknik sendiri; video boleh memadukan beberapa teknik.
5. **Minimal sampai terbukti perlu.** Folder `engine/` dan `assets/` sengaja kosong.

## 3. Struktur folder (A)

```
fakta-rumah/
├── CLAUDE.md                         instruksi proyek (pendek, menunjuk dokumen lain)
├── README.md                         peta dokumen
├── PROPOSAL.md                       dokumen ini
│
├── identity/                         "Seperti apa channel ini terlihat"
│   ├── reference-analysis-framework.md   cara membedah referensi
│   ├── visual-identity.md                Visual Identity Spec (DRAFT)
│   └── references/                       satu analisis per referensi + file/tautan referensi
│
├── workflow/                         "Bagaimana video dibuat"
│   ├── workflow.md                       8 tahap, ringan
│   ├── categories.md                     kategori konten + opsi pendekatan
│   └── pilot-plan.md                     rencana pilot
│
├── templates/                        brief.md, storyboard.md, reference-analysis.md
├── research/                         ecosystem-research.md + catatan per kandidat
│
├── videos/<slug>/                    "Satu folder per video"
│   ├── brief.md
│   ├── research.md                       fakta, sumber, konsep sulit
│   ├── direction.md                      konsep visual (+ alternatif yang ditolak)
│   ├── script.md
│   ├── storyboard.md                     shot-by-shot
│   ├── src/                              kode produksi video ini
│   └── out/                              render (di-gitignore bila besar)
│
├── engine/        KOSONG — diisi hanya setelah pilot disetujui
├── assets/        KOSONG — hanya aset yang sudah dipakai ≥2 video
└── qa/            checklist QA + log review render
```

Pemetaan ke 11 pemisahan yang Anda minta: project instructions → `CLAUDE.md`; workflow → `workflow/`; visual identity → `identity/`; content category → `workflow/categories.md`; visual direction & storyboard → `videos/<slug>/`; animation system, production components → `engine/` (ditunda); reusable assets → `assets/` (ditunda); render → `videos/<slug>/out`; QA → `qa/`.

**Sengaja tidak ada:** folder `skills/`, folder per kategori, library komponen, config sistem. Skill baru ditambahkan hanya jika satu langkah workflow terbukti berulang dan sulit diikuti tanpa skill.

## 4. Keputusan yang saya butuhkan dari Anda

1. **Referensi visual.** Ini penghalang terbesar. Tanpa 3–6 referensi (video/gambar/channel), `visual-identity.md` tetap kerangka kosong. Bisa tautan YouTube, file, atau gambar.
2. **Bahasa & format video.** Bahasa narasi (Indonesia?), rasio (16:9 / 9:16 / keduanya), durasi tipikal.
3. **Narasi/suara.** Voiceover dari mana (rekaman sendiri, TTS)? Ini memengaruhi workflow timing. (Catatan: "tanpa external AI API" saya baca sebagai larangan untuk visual; TTS perlu Anda tegaskan.)
4. **Riset ekosistem.** Setujukah saya menjalankan riset web terverifikasi (versi lisensi, aktivitas repo) sebagai langkah berikutnya, sebelum instalasi apa pun?
5. **Repo lama.** Boleh saya baca (read-only) untuk mengambil aset/dokumen yang layak? Default saya: tidak, sampai Anda tunjuk.

## 5. Risiko yang perlu Anda sadari (tantangan)

- **Ekspektasi vs. batasan "visual lewat kode".** Kualitas "ilustrasi berdimensi, detail, ekspresif" dari kode murni sangat bergantung pada *seberapa banyak kerja ilustrasi manual-kode* per shot. Ini mahal. Pilot akan mengukur biaya nyata per detik video sebelum kita berjanji soal volume produksi.
- **Karakter (jika ada) adalah elemen tersulit.** Animasi karakter ekspresif dari kode jauh lebih mahal daripada objek/lingkungan. Keputusan "ada karakter atau tidak" sebaiknya diambil dari referensi, bukan diasumsikan.
- **Mengontrol style lewat teks itu rapuh.** Itulah sebabnya framework referensi mengubah selera menjadi parameter terukur (lihat `identity/`), dan pilot menjadikan gambar render sebagai alat kalibrasi, bukan deskripsi.
- **Hal yang mungkin diabaikan semua orang:** menguji style pada *kategori terberat dan teringan sekaligus* (pilot memakai dua shot kontras), karena style yang hanya bekerja untuk satu jenis konten akan runtuh saat channel melebar.
