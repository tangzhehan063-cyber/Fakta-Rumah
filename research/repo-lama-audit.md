# Audit Repo Lama `Channel-Penjelasan` (read-only)

Dasar: clone dangkal pada commit `55151c4` (23 Nov 2026), 324 commit, 1.143 file. Saya membaca README, CLAUDE.md (±16 KB), KEPUTUSAN.md, STATUS.md, daftar bagian WORKFLOW.md (1.028 baris), `tools/*`, struktur `remotion/`, dan dua gambar (still hook + contact sheet video #10). **Saya tidak membaca seluruh isi.** Tidak ada yang disalin ke repo ini.

Setiap temuan ditandai: **(F)** fakta dari file, **(I)** inferensi saya.

## 1. Apa yang sebenarnya ada

**Channel & produksi (F):** seri "fakta rumah", Bahasa Indonesia santai, audiens 35+, YouTube Shorts (platform utama), video vertikal **1080×1920**, naskah 50–70 dtk (±110–155 kata). ±24 video seri lama (#1–#24) + 2 video eksperimen "E1" (#01, #02). MP4 final disimpan di Google Drive, bukan Git.

**Tiga era visual yang bertumpuk (F):**
1. Origami (#1–#4) → diarsipkan.
2. "Editorial 3D / diorama kertas" (#5–#24): satu objek 3D besar per adegan, kartu teks terang, palet latar bergantian.
3. "E1 semi-realistis / architectural visualization" (#01–#02, 23 Nov): material prosedural, rumah 3D, kamera 3D. **Inilah yang sekarang Anda tolak.**

**Pipeline otomatis (F):** `tools/produksi.sh` (satu pintu: vo, words, sheet, final, bagian, srt, cover) → loudnorm −14 LUFS → SRT; gerbang checklist per video; Gemini TTS otomatis; timestamp kata tanpa Scribe; cek suara, cek kilau, pemindai API AI.

## 2. Masalah arsitektur (dengan bukti)

| # | Masalah | Bukti | Dampak |
|---|---|---|---|
| 1 | **Aturan bertumpuk tanpa pembersihan** | `CLAUDE.md` memuat blok "ARAH AKTIF: E1 menang atas semua aturan lama" lalu tetap memuat "ATURAN KAKU" era 3D (#1–#26) di file yang sama; ada catatan "alat lama tidak dipanggil E1 tapi sengaja tidak diubah" | Agen harus menebak aturan mana yang berlaku |
| 2 | **Aturan yang saling bertentangan** | "Claude merge sendiri ke main" (KEPUTUSAN 9 & 16 Nov) vs "Claude TIDAK merge sendiri" (E1); "Hemat token: cek gambar maks 1 sheet" vs kebutuhan QA visual; WORKFLOW.md (1.028 baris) berbeda versi dengan CLAUDE.md | Perilaku tidak dapat diprediksi |
| 3 | **"Kunci karakter" membekukan hasil** | Aturan: "mulai dari salinan `v08`", "yang diganti hanya data", "dilarang mengganti struktur adegan, tipografi, kartu", "kalau menyimpang, video dibuang" | **Sumber langsung kemonotonan**; bertentangan dengan tujuan Anda sekarang. Folder `remotion/src/v05…v24` = salinan berulang |
| 4 | **Teknik menentukan tampilan** | Satu objek 3D prosedural per adegan + kartu teks + kamera isometrik adalah *satu-satunya* kosakata (kit `Penjelasan`, `stage`) | Kesan "slide dengan objek 3D" (I; lihat contact sheet #10: tangga 3D + kartu judul + subtitle) |
| 5 | **Gerbang berbasis dokumen, bukan hasil** | `gerbang.mjs` memeriksa centang `[x]` di checklist | Bisa lolos tanpa menonton; "QC mata hanya dari 11 still, video penuh belum ditonton Claude" (STATUS) |
| 6 | **Pergantian arah tanpa evaluasi keluar** | E1 diganti dua kali dalam sehari (semi-realistis AI → 100% kode, 23 Nov) | Fondasi tidak sempat divalidasi |
| 7 | **Style diturunkan dari teks & aturan, bukan analisis referensi** | `style/referensi-visual/*` ada, tetapi aturan style ditulis sebagai larangan/ukuran ("objek ≥1/3 tinggi layar") | Aturan menutup alternatif |
| 8 | **Aset menggunung** | 720 file di `remotion/public`; 84 MB `.git` pada clone dangkal | Perlu kebijakan aset |
| 9 | **Hambatan lingkungan** | Wikimedia 429, Cloudflare memblokir sumber riset; foto dari user tanpa lisensi jelas | Pelajaran untuk pipeline aset |

## 3. Yang berhasil dan layak dipertahankan (setelah evaluasi)

| Komponen lama | Fungsi | Putusan | Catatan evaluasi |
|---|---|---|---|
| `gemini_tts.py` | Naskah → WAV via Gemini TTS; rantai model cadangan; potong per ≤900 karakter; hash-skip supaya kuota tidak terbuang; jalur cadangan `edge-tts` | **adapt (Fase 5)** | Pertahankan konsep (hash-skip, fallback, chunking). Tulis ulang bersih; verifikasi model/harga terbaru; kunci API lewat environment, tidak pernah di repo |
| `align_teks.py` | Timestamp kata tanpa API: ffmpeg `silencedetect` + DP; akurasi ±0,1–0,3 dtk | **adapt (Fase 5)** | Cukup untuk subtitle; **kurang untuk sinkron animasi halus**. Bandingkan dengan forced alignment (mis. Whisper lokal) saat Fase 5 |
| `cek_suara.py` | F0 median/p90, kata/dtk, loudness vs referensi VO yang diterima | **adapt (Fase 5)** | Lahir dari bug nyata (VO "berlagak"); ide bagus: kontrol kualitas suara = angka |
| `mix-audio.mjs` + loudnorm −14 LUFS dua-pass | Mix VO+SFX+musik, normalisasi | **adapt (Fase 5)** | |
| `cek-mandiri.mjs` | Pemindai kode visual dari API AI/jaringan | **adapt (Fase 3)** | Menegakkan aturan "tanpa AI generation" secara otomatis. Kecil dan bermanfaat |
| `cek_kilau.py` (nudge test) | Render dua kali dengan kamera digeser 0,0004 m; hitung piksel berbeda → deteksi z-fighting | **adapt untuk 3D saja** | Ide generalnya berlaku: **uji determinisme dan stabilitas dengan perturbasi** |
| `style/cek-bug.md` | Daftar bug visual dari kasus nyata (mis. `useFrame()` R3F dan `Math.random()` menyebabkan kedip; `<Sequence layout="none">` di `ThreeCanvas`) | **adapt**: pelajaran teknis saja | Pisahkan pelajaran teknis dari aturan layout |
| `produksi.sh` (satu pintu), render per bagian 15 dtk, SRT | Orkestrasi mekanis | **adapt (Fase 5–6)** sebagai CLI berbasis manifest | Perlu ditulis ulang sesuai kontrak data baru |
| Prinsip "visual = fungsi murni dari frame" (`e1-visual-kode.md`) | Determinisme | **adopt (prinsip)** | Sudah sesuai ide kita |
| Skill `script-writer` + `prompts/ScriptForge.md` | Penulisan naskah (ide → riset → script) | **evaluasi di Fase 5–6**; tidak diimpor sekarang | Belum saya baca isinya |
| `riset/` (tren, ide) dan `naskah/`, SRT, caption | Konten | **arsip referensi** | Naskah/topik boleh dipakai sebagai bahan pilot bila Anda mau |
| Struktur Drive `Fakta Rumah / E1 / #NN` | Penyimpanan hasil | **pertimbangkan Fase 6** | |
| `remotion/src/e1/look.tsx` (material prosedural) | Teknik tekstur prosedural | **reference only** | Berguna sebagai bahan belajar; **bukan style kita** |

## 4. Yang tidak dibawa

- `CLAUDE.md`, `WORKFLOW.md`, `KEPUTUSAN.md`, `STATUS.md` lama, skill `sutradara`, `breakdown`, `remotion-fitur`, aturan "Kunci Karakter", kit objek (`kit/objek`), 24 folder video (`v05…v24`), `arsip/origami`, `sampel-hyperframes`.
- **Alasan:** campuran aturan visual, workflow, dan teknik yang sudah bertentangan satu sama lain. Dari repo lama kita hanya mengambil *pelajaran dan alat mekanis*, bukan aturan.

## 5. Hal yang diwarisi sebagai fakta channel (perlu Anda konfirmasi ulang)

| Fakta | Sumber lama | Status |
|---|---|---|
| Nama seri "fakta rumah"; repo baru bernama Fakta-Rumah | README | konfirmasi |
| Bahasa Indonesia santai; audiens 35+ | CLAUDE.md | konfirmasi |
| YouTube Shorts utama, 1080×1920, 30 fps | CLAUDE.md / `produksi.sh` | konfirmasi (Anda mengatakan format akan "didefinisikan") |
| Durasi 50–70 dtk | KEPUTUSAN (23 Nov) | konfirmasi |
| Penutup "Follow buat fakta rumah berikutnya!" | CLAUDE.md | konfirmasi |
| Fakta wajib bersumber, tandai `[CEK]` | CLAUDE.md | usul dipertahankan |
| Persetujuan pemilik untuk: topik final, script, style, render batch besar, publish, merge ke `main` | CLAUDE.md | usul dipertahankan |

## 6. Catatan tentang dua gambar yang saya lihat

- `style/referensi-visual/01-…lentera…png`: objek 3D bermaterial dengan bayangan ranting lembut dan tipografi besar. Ini dulu disimpan sebagai referensi, tetapi **belum saya analisis dan bukan persetujuan style** (sesuai instruksi Anda).
- Contact sheet #10: tangga 3D bernuansa beige dengan kartu teks terang dan subtitle. Dugaan saya (I): ini contoh konkret keluhan "slide dengan objek 3D" — informasi dibawa kartu teks, objek hanya ilustrasi.

Jika Anda mau, gambar/video di `style/referensi-visual/` dan `referensi/moodboard/` bisa dianalisis ulang di Fase 2 **hanya bila Anda menunjuknya**.
