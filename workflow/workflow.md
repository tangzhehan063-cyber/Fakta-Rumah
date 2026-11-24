# Workflow Video (D)

Ringan, berurutan, tapi tidak kaku. Tahap boleh digabung untuk video pendek; yang tidak boleh dilewati hanya **gerbang persetujuan** (⛔).

```
Brief → Riset → Visual Direction → Script → Storyboard → ⛔Approval → Produksi → Render & QA
```

Semua artefak disimpan di `videos/<slug>/`.

## 1. Brief → `brief.md` (template: `templates/brief.md`)
Isi: topik, kategori (boleh hybrid), tujuan penonton ("setelah menonton, penonton harus bisa ___"), durasi, format, sudut pandang/hook, apa yang *tidak* dibahas.
Aturan: kategori **harus** ditetapkan di sini; ia menentukan pertanyaan di tahap berikut (lihat `categories.md`). Info kurang → tanya pemilik.

## 2. Riset & analisis konten → `research.md`
- Fakta & mekanisme diverifikasi dengan sumber. Mekanisme yang salah = video gagal, seindah apa pun visualnya.
- Output: informasi utama; konsep sulit (yang paling mungkin disalahpahami); *visual opportunity* (bagian yang lebih mudah dipahami lewat gambar daripada kata); *storytelling opportunity*; bagian yang butuh demonstrasi; miskonsepsi umum.

## 3. Visual Direction → `direction.md`
- Mulai dari: "Visual apa yang paling membuat konsep sulit tadi dipahami?" bukan "teknik apa yang tersedia?".
- Jika arah belum jelas: **tawarkan 2–3 konsep yang benar-benar berbeda** (beda metafora/dunia visual/kamera, bukan beda warna), masing-masing dengan thumbnail-level sketsa atau frame uji. Pemilik memilih; yang ditolak dicatat singkat.
- Direction harus patuh pada `identity/visual-identity.md` (bahasa visual channel), namun bebas dalam komposisi dan teknik.
- Pilih teknik per shot di sini, bukan sebelumnya.

## 4. Script → `script.md`
Disusun dari alur informasi dan storytelling. Visual tidak boleh memaksa naskah, dan naskah tidak boleh menugaskan visual yang tidak masuk akal. Tandai titik "tunjukkan, jangan ceritakan".

## 5. Visual Design & Storyboard → `storyboard.md` (template: `templates/storyboard.md`)
Per shot: tujuan (apa yang dipahami penonton), visual & environment, komposisi & hierarki fokus, kamera (jenis shot, sudut, gerak + **alasan**), motion (apa bergerak, urutan, timing kasar), transisi (+ alasan kreatif), teknik yang dipakai, risiko produksi.
Untuk shot yang berisiko secara visual: buat **frame uji** (satu still dari kode) sebelum approval.

## 6. ⛔ Approval
Pemilik meninjau direction + storyboard bila ada keputusan kreatif besar (style baru, metafora utama, ada/tidaknya karakter, kamera utama). Perubahan kecil tidak perlu gerbang.

## 7. Produksi → `src/`
Implementasi sesuai storyboard. Jika ada penyimpangan kreatif, hentikan dan kembali ke storyboard. Iterasi dengan render pendek (klip/frame), bukan menebak dari kode. Komponen baru boleh ekstrak ke `engine/` atau `assets/` hanya setelah dipakai ≥2 video.

## 8. Render & QA
> Syarat mutlak kualitas ada di `identity/visual-identity.md` §1b. Shot yang melanggarnya dinyatakan gagal, apa pun status kodenya.
 → `out/`, `qa/`
Tonton render aktual. Checklist ada di `qa/checklist.md` (dibuat saat pilot): keterbacaan, fokus, depth, timing, kontinuitas spasial, kesesuaian dengan identity, akurasi fakta, audio sinkron. Temuan dicatat; hanya perbaiki yang terlihat di render.

## Perubahan aturan
Aturan baru → ubah dokumen ini (atau `identity/`), bukan menambah file baru. Kalau dua dokumen bertentangan, perbaiki salah satunya.
