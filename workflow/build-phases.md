# Rencana Pembangunan — 6 Fase

Tiap fase punya **tujuan, hasil, gerbang keluar, dan apa yang sengaja tidak dilakukan**. Pindah fase hanya setelah gerbang keluar disetujui pemilik.

```
F1 Riset & arsitektur → F2 Referensi & identitas → F3 Core engine + pilot → F4 Evaluasi → F5 TTS + automasi → F6 Pipeline otomatis
   (sekarang)              (butuh referensi Anda)      (kode dimulai)         (keputusan)     (kembalikan yang lama)   (naskah → final)
```

## Fase 1 — Riset dan desain arsitektur (SEKARANG)
- **Hasil:** `PROPOSAL.md`, `ARCHITECTURE.md`, `research/ecosystem-research.md`, `research/repo-lama-audit.md`, `identity/reference-analysis-framework.md`, draf `identity/visual-identity.md`, `workflow/*`.
- **Gerbang keluar:** Anda menyetujui (a) arsitektur lapisan + kontrak shot (konsep), (b) shortlist teknologi untuk diuji di pilot, (c) keputusan terbuka (lihat bawah), (d) fakta channel yang diwarisi.
- **Tidak dilakukan:** instalasi, kode engine, analisis style final.

## Fase 2 — Analisis referensi & penetapan Visual Identity
- **Masukan:** referensi Anda (bertahap), plus referensi *anti*.
- **Pekerjaan:** analisis per referensi dengan framework (8 dimensi + 4 keranjang), lalu sintesis ke `visual-identity.md`. Frame uji (mockup statis) dibuat **setelah** analisis disetujui untuk kalibrasi, bukan sebelum.
- **Hasil:** `identity/references/*.md` + `visual-identity.md` v1 (parameter, status "kandidat"→"disetujui").
- **Gerbang keluar:** Anda menyatakan "ya, ini yang saya maksud" pada frame uji (≥4 dari 6 ya/hampir, lihat `pilot-plan.md` P0).
- **Risiko:** referensi terlalu sedikit → ulangi dengan referensi tambahan.
- **Tidak dilakukan:** engine, animasi.

## Fase 3 — Core visual engine dan pilot pendek
- **Syarat masuk:** gerbang Fase 2; keputusan lisensi Remotion; izin memasang dependency.
- **Pekerjaan:** setup minimal Remotion + render (harness, bukan engine); pilot P0→P1→P2 (lihat `pilot-plan.md`), membandingkan ≥2 teknik per shot kritis; ekstrak ke `engine/` hanya yang dipakai ≥2 kali; adaptasi `cek-mandiri` dan uji determinisme.
- **Hasil:** harness render, klip pilot, catatan teknik + biaya, `qa/checklist.md` awal.
- **Gerbang keluar:** Anda menonton klip pilot dan menilai style, gerak, dan kejelasan penjelasan.
- **Tidak dilakukan:** TTS otomatis, pipeline penuh, pustaka komponen besar.

## Fase 4 — Evaluasi kualitas, gerak, biaya, performa
- **Pengukuran:** kualitas visual (penilaian Anda per klip), motion (daftar prinsip), **biaya per detik video** (waktu kerja + jumlah baris kode), **waktu render per detik video**, stabilitas (determinisme), keterulangan (apakah kode shot bisa dipakai ulang tanpa membuat video seragam).
- **Keputusan:** teknik mana dipertahankan, host render final, kontrak shot (ubah/tetap), target produksi realistis (video per minggu), apakah karakter layak.
- **Hasil:** laporan evaluasi, `visual-identity.md` v2, keputusan arsitektur final.
- **Gerbang keluar:** persetujuan Anda atas laporan dan keputusan.
- **Tidak dilakukan:** menambah fitur baru; ini fase menilai.

## Fase 5 — Integrasikan kembali Gemini TTS dan automasi
- **Pekerjaan:** tulis ulang bersih alat TTS (adaptasi `gemini_tts.py`: model cadangan, chunking, hash-skip, kunci via environment), verifikasi model/harga/dukungan Indonesia dari dokumen resmi; alat align kata (adaptasi `align_teks.py`, bandingkan dengan alternatif); cek suara; mix & loudnorm; SRT; manifest `video.json`.
- **Hasil:** perintah CLI per langkah mekanis; satu video diproduksi dengan jalur audio otomatis.
- **Gerbang keluar:** VO dan sinkronisasi diterima Anda pada satu video nyata.
- **Pengecualian aturan terdokumentasi:** TTS Gemini diperbolehkan hanya untuk audio.

## Fase 6 — Pipeline otomatis naskah → video final
- **Pekerjaan:** orkestrator berbasis manifest yang menjalankan langkah mekanis berurutan dan berhenti di gerbang persetujuan; QA Q0–Q3 otomatis, Q4 (tinjauan visual) terjadwal; paket rilis (video, SRT, caption, cover); penyimpanan ke Drive jika dikehendaki.
- **Hasil:** dari naskah yang disetujui + storyboard yang disetujui → draf render lengkap + laporan QA.
- **Gerbang keluar:** dua video berturut-turut diproduksi lewat pipeline dengan intervensi manusia hanya pada gerbang.
- **Batas yang jujur:** keputusan visual tetap manusia/Claude + storyboard; otomasi penuh hanya untuk resep shot yang sudah terbukti.

## Keputusan yang harus diambil Anda di Fase 1 (daftar tunggal)

| # | Keputusan | Rekomendasi saya |
|---|---|---|
| 1 | Lisensi Remotion: apakah Anda individu / ≤3 karyawan, dan menerima risiko perubahan lisensi di v5.0? | Jika ya → lanjut Remotion; jaga kontrak shot bebas dari API Remotion (hedge) |
| 2 | Fakta channel yang diwarisi (1080×1920, 30 fps, Shorts, 50–70 dtk, audiens 35+, penutup "Follow…") masih berlaku? | Konfirmasi atau ganti; tulis di `channel.md` |
| 3 | Pengecualian TTS: Gemini TTS untuk audio, tidak untuk visual | Setujui, dicatat di CLAUDE.md |
| 4 | Pasang `remotion-dev/skills` saat Fase 3? | Ya, hanya Fase 3 |
| 5 | Naskah/topik repo lama boleh dipakai sebagai bahan pilot? | Boleh, dipilih bersama |
| 6 | Kebijakan Git: Claude tidak merge ke `main`; PR hanya atas permintaan | Usul dipertahankan |
