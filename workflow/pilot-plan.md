# Rencana Pilot (E)

**Tujuan pilot:** menguji (1) apakah style yang diterjemahkan dari referensi benar-benar yang Anda maksud, dan (2) apakah kualitas animasi yang Anda inginkan **dapat dicapai lewat kode dengan biaya wajar**. Pilot **bukan** membangun engine dan **bukan** video siap tayang.

## Prasyarat
- ≥3 referensi dari pemilik, dianalisis dan keranjangnya disetujui.
- Keputusan awal: format/rasio, ada/tidaknya karakter.
- Riset ekosistem (`research/ecosystem-research.md`) disetujui sebagian: minimal tentang apa yang boleh dipakai untuk render/preview.

## Prinsip pilot
- Teknik **tidak** ditentukan di muka. Setiap eksperimen memilih teknik terbaik untuk tujuan visualnya; hasilnya dibandingkan.
- Tiap eksperimen **kecil, dibuang jika gagal**. Tidak ada kode yang otomatis menjadi engine.
- Penilaian dari **render yang ditonton**, oleh Anda.

## Fase

### P0 — Kalibrasi style (still frame, bukan animasi)
Dari analisis referensi, buat **4–6 frame uji** dari kode, mencakup variasi yang disengaja: 1 environment lebar, 1 objek close-up/detail, 1 komposisi dengan foreground framing, 1 kategori kontras (mis. mekanisme vs situasi sehari-hari). Opsional: 2 pendekatan teknik berbeda untuk shot yang sama.
- **Gerbang:** Anda menjawab per frame: "ya / hampir / tidak" + apa yang salah. Parameter identity direvisi.
- **Kriteria lulus:** ≥ 4 dari 6 frame "ya/hampir" dan kesalahannya bisa dinyatakan sebagai parameter.

### P1 — Uji gerak (3–4 klip, masing-masing 4–8 detik)
Konten dipilih untuk menguji hal yang berbeda:
1. **Mekanisme berurutan** (sebab-akibat jelas; staging, anticipation, follow-through).
2. **Pergerakan kamera melalui environment** (depth, parallax/perspektif bergerak).
3. **Transisi bermotivasi** antar dua shot (match cut atau serupa).
4. *(jika ada karakter)* **Aksi karakter ringan.** Ini uji kelayakan; bisa berujung keputusan "tanpa karakter".
- **Gerbang:** Anda menonton; saya mencatat biaya (jam kerja/jumlah kode) per klip.
- **Kriteria lulus:** motion hierarchy terbaca; Anda tidak melihat "objek muncul satu per satu"; biaya per detik dapat diterima untuk target produksi Anda.

### P2 — Mini-video (30–60 detik, satu topik nyata)
Jalankan **workflow penuh** (brief → riset → direction → script → storyboard → approval → produksi → QA) pada topik pendek. Ini menguji proses, bukan hanya visual.
- **Gerbang akhir:** pemilik menilai kesesuaian style, kejelasan penjelasan, dan kelayakan produksi berulang.

## Pilihan topik pilot
Idealnya topik yang punya **mekanisme + lingkungan sehari-hari** sekaligus (mis. sesuatu di rumah: cara kerja suatu perangkat rumah dan situasi pemakaiannya) sehingga menguji dua kategori. Topik diusulkan setelah referensi ada; bisa Anda pilih sendiri.

## Output pilot
1. `identity/visual-identity.md` v1 (parameter terisi, status disetujui).
2. Catatan teknik: apa yang berhasil untuk apa, dan biaya (ke `research/` atau `videos/pilot-*/notes.md`).
3. Keputusan arsitektur: apakah `engine/` perlu dan **hanya** untuk hal yang terbukti berulang.
4. `qa/checklist.md` dari temuan nyata.
5. Daftar "toolkit yang diadopsi" (dari riset), dengan bukti dipakai.

## Yang sengaja tidak dilakukan di pilot
Membangun engine/timeline generik, komponen "universal", pustaka aset besar, atau pipeline otomatis.

## Risiko pilot & mitigasi
| Risiko | Mitigasi |
|---|---|
| Referensi tidak cukup untuk menyimpulkan style | Minta 2–3 referensi tambahan + referensi *anti* |
| Hasil kode terasa "datar" lagi | P0 menguji depth secara eksplisit sebelum animasi; kriteria ≥3 layer terbaca |
| Biaya per detik terlalu tinggi | Dicatat sejak P1; bila tinggi, diskusikan trade-off (detail vs durasi, tipe shot yang lebih murah) |
| Satu teknik mendominasi karena kebiasaan | Eksperimen dwi-teknik di P0/P1 untuk shot yang sama |
