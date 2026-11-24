# Rencana Pilot (E)

**Tujuan pilot:** menguji (1) apakah style yang diterjemahkan dari referensi benar-benar yang Anda maksud, dan (2) apakah kualitas animasi yang Anda inginkan **dapat dicapai lewat kode dengan biaya wajar**. Pilot **bukan** membangun engine dan **bukan** video siap tayang.

## Revisi Fase 2 — Usulan Pilot Fase 3 (berdasarkan referensi 01–03)

> Menggantikan rincian P0–P2 di bawah **bila Anda menyetujui**. Belum final; bergantung pada jawaban atas pertanyaan terbuka di `identity/references/00-perbandingan.md` §5.

**Prinsip:** menguji *kualitas tampilan* dan *biaya*, bukan engine. Setiap eksperimen kecil dan boleh dibuang. Penilaian dari **render yang ditonton**.

### P0 — Look-dev "bake-off" (still 4–6 frame)
Satu set yang sama (mis. sudut ruang rumah dengan cahaya jendela + satu objek mekanis) dibangun lewat 2–3 teknik: (a) Three.js real-time, (b) Three.js + pra-bake cahaya, (c) SDF clay untuk objek hero, (d) *opsional* Blender headless. Dibandingkan dengan Referensi 01/03 (cahaya, bevel, depth).
**Lulus:** Anda memilih teknik yang "terasa satu dunia", bukan datar; kekurangan dapat dinyatakan sebagai parameter.

### P1 — Gerak kamera + reveal (klip 6–8 dtk)
Kamera kontinu dengan DOF melewati set; **reveal prosedural** (objek tumbuh/terbentuk berurutan seperti Ref 02) yang membuat sebab-akibat terbaca. **Lulus:** terasa shot animasi sungguhan; tidak ada "objek muncul satu per satu" tanpa sebab.

### P2 — Informasi di dalam dunia (klip 6–8 dtk)
Teks 3D dan label yang hidup di dalam perspektif dunia, plus layar perangkat dengan tekstur dinamis. **Lulus:** terbaca jelas dan tidak seperti slide/overlay.

### P3 — Uji kelayakan karakter (hanya jika Anda memutuskan karakter)
Karakter sederhana berpose + siklus jalan 3–4 dtk. Keputusan **go / no-go** berdasarkan biaya dan tampilan.

### P4 — Mini-video 30–60 dtk (workflow penuh)
Satu topik rumah nyata yang memuat **mekanisme + lingkungan sehari-hari** sekaligus. Hanya setelah P0–P2 lulus.

### Metrik yang dicatat sejak P0
Waktu kerja per detik video, waktu render per detik video, determinisme (render ganda identik), ukuran file, dan penilaian Anda (ya / hampir / tidak) per klip.

### Syarat masuk
Jawaban Anda atas pertanyaan terbuka; keputusan lisensi Remotion (bila dipakai); izin memasang dependency (dan, bila Blender dipertimbangkan, izin memasangnya).

---

## Prasyarat (versi awal, Fase 1)
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
