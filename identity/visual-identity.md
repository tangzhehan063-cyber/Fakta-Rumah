# Visual Identity Specification — DRAFT v1 (Fase 2)

> **Status: DRAFT. Belum disetujui.** Sumber bukti: `identity/references/01…03` (tiga video yang Anda unggah). Anda belum menyatakan mana yang disukai. Setiap butir ditandai: **[B]** bukti kuat (muncul ≥2 referensi) · **[K]** kandidat (1 referensi) · **[?]** belum ada bukti, perlu keputusan Anda · **[M]** mandat langsung dari Anda.
> Aturan: butir tanpa bukti tidak ditulis sebagai fakta.

## 1. Arah visual keseluruhan
- **[M]** *Stylized illustrated animation*, bukan fotorealistis; dimensional, berlapis, berdetail relevan, kamera dirancang, animasi lancar. Teknologi tidak menentukan style.
- **[B]** Tampilan hipotetis: *dunia 3D yang kohesif dengan cahaya lembut berarah, permukaan matte bevel, tanpa outline*, dan informasi hidup di dalam dunia (01–03).
- **[?]** Tingkat kehangatan/mood dan kerapatan detail.

## 1b. Syarat mutlak kualitas visual **[M]**
**Gagal otomatis** bila terlihat seperti diagram datar top-down, susunan objek 1D/2D, slideshow, gambar statis dengan overlay beranimasi, foto dengan elemen kartun ditempel, objek 3D sederhana melayang di latar datar, atau animasi yang bergerak tetapi datar/murahan/terputus.
**Wajib:** setiap scene adalah satu lingkungan visual utuh (ilustrasi, objek, cahaya, perspektif, kamera, depth, animasi di dunia yang sama); komposisi spasial bermakna; depth meyakinkan; sudut kamera disengaja; staging kuat; animasi halus; terasa seperti shot animasi sungguhan.
**Dilarang tanpa persetujuan eksplisit:** foto/gambar nyata sebagai latar dengan elemen animasi di atasnya. **Dilarang sebagai default:** kamera overhead, layout datar, framing statis.
**Penilaian:** hanya dengan menonton render nyata.

## 2. Bahasa bentuk
- **[B]** Bentuk disederhanakan, dengan **tepi dibulatkan (bevel)** pada objek yang dekat kamera (01: konsisten; 03: sebagian); blok tajam pada massa jauh (02).
- **[K]** Siluet jelas: objek terbaca dari bentuk luarnya (01, 02).
- **[?]** Proporsi dan seberapa "gemuk/kartun".

## 3. Prinsip warna
- **[B]** Dunia berpalet terkendali; warna jenuh dihemat untuk **makna** (02 kuat; 01: hijau hutan sebagai merek).
- **[K]** Palet terukur 01: krem/peach `#ece1d6 #f6e8d8 #f1e7dc`, krem gelap `#d1c7b6 #af9d89`, cokelat `#635647`, aksen hijau hutan. 02: abu `#c8c9c8 #d4d2d0 #e0dfde`, hijau `#687f69 #88a893`, aksen per makna (oranye `#e1a139`, biru, cyan). 
- **[?]** Palet channel: hangat (01) atau netral (02)? Aturan turunan per kategori belum ada bukti.

## 4. Pendekatan ilustrasi dan rendering
- **[B]** Tanpa outline; volume dari shading lunak + occlusion di celah (01, 02, 03).
- **[K]** Material matte seperti tanah liat, dengan aksen kayu/kaca/logam (01).
- **[?]** Tingkat tekstur (grain, serat, imperfeksi).
- **Catatan:** dua dari tiga referensi tampak dibuat dengan render 3D offline (I; 03 pasti Blender). Ini berimplikasi teknis (§16).

## 5. Depth dan perspektif
- **[B]** Depth dibangun dari: **bayangan kontak + overlap + skala**; ditambah **DOF** pada close-up (01) dan **AO/fog** pada skala besar (02).
- **[B]** Ketiganya memakai sudut **oblik-tinggi**. **[?]** Apakah ini yang Anda inginkan (Anda juga melarang default overhead/isometrik).
- **[K]** Lensa panjang/ortografik pada shot lebar vs perspektif kuat pada close-up (01); perspektif nyata sepanjang video (02). **[?]** Pilihan lensa per jenis shot.

## 6. Desain lingkungan dan objek
- **[B]** Set dikurasi: hanya objek yang berfungsi (01), detail bertingkat menurut fokus (02).
- **[K]** Objek tematik bervolume penuh dengan beberapa warna (02), perangkat sebagai pemicu cerita (01).
- **[?]** Kerapatan lingkungan. Hindari lantai kosong luas tanpa alasan (lihat §15).

## 7. Prinsip karakter
- **[K]** Hanya 01 memiliki karakter: proporsi memanjang, wajah minimal, emosi lewat pose; berperan sebagai pengganti penonton. 02 menunjukkan visual kaya tanpa karakter.
- **[?]** Karakter wajib / opsional / dihindari? Biaya produksi **tinggi** (I). Tidak akan ada sistem karakter sebelum Anda memutuskan.

## 8. Bahasa kamera
- **[B]** Sedikit cut, **gerak kamera kontinu** yang menuju fokus cerita (01, 02).
- **[K]** Variasi: wide vignette → medium → POV/close-up dengan DOF → detail (01); sapuan panjang & push-in (02).
- **[K]** Transisi lewat objek (kamera masuk ke layar, kartu keluar jadi panel dunia) (01).
- **[?]** Kecepatan dan ritme untuk format Shorts.

## 9. Bahasa animasi
- **[K]** Objek muncul bertahap, bukan serentak (01 kartu, 02 pertumbuhan prosedural).
- **[K]** Gelembung/penanda muncul dengan skala (01). Pose karakter berganti halus.
- **[M]** Wajib punya anticipation, timing, follow-through, hierarki gerak, sebab-akibat (brief awal).
- **Belum diukur:** easing, durasi tepat (sampling saya terlalu jarang). Perlu analisis lebih rapat bila penting.

## 10. Pencahayaan dan shading
- **[B]** Cahaya lembut berarah, bayangan besar halus, occlusion di celah, tanpa outline.
- **[K]** Varian hangat dengan bounce peach (01); varian dramatis dengan patch cahaya jendela (03); varian malam dengan bloom titik putih (02).
- **[?]** Varian mana yang jadi dasar.

## 11. Komposisi scene
- **[K]** Fokus tunggal per shot; foreground framing pada close-up (01); label dan huruf 3D menempel pada bidang dunia (02).
- **[?]** Komposisi untuk 9:16 (semua referensi 16:9).

## 12. Prinsip penceritaan visual
- **[B]** Informasi **di dalam dunia**: teks 3D, label, layar perangkat (01, 02).
- **[K]** Warna-sebagai-data dengan reveal bergelombang (02); alur emosi lewat karakter (01).
- **[?]** Apakah caption/overlay 2D tetap dipakai.

## 13. Karakteristik yang harus dipertahankan (KANDIDAT inti)
H1 membumi · H2 cahaya lunak + matte + bevel + tanpa outline · H3 informasi dalam dunia · H4 dunia netral, warna untuk makna · H5 kamera kontinu bermotivasi · H6 reveal bertahap. *(Tabel bukti: `references/00-perbandingan.md` §3.)*

## 14. Karakteristik fleksibel
Sudut/lensa, kerapatan detail, suasana cahaya, skala, DOF, palet turunan.

## 15. Hal yang dihindari (KANDIDAT)
Daftar dari §1b ditambah: lantai kosong luas tanpa alasan, label berbaris ala slide, logo/watermark konstan, teks terpotong tanpa motivasi, blok/objek melayang di latar datar (kontra-contoh 02), steril ala visualisasi perkotaan.

## 16. Implikasi teknis untuk engine
Lihat `ARCHITECTURE.md` §10. Ringkas: tampilan yang tampak pada referensi (**GI lunak, bevel, DOF, AO, bayangan lembut, pertumbuhan prosedural, teks 3D dalam dunia**) hampir pasti membutuhkan **pipeline 3D**, bukan SVG/CSS/2D saja. Kesenjangan utama: **kualitas cahaya** dan **karakter beranimasi**.

## 17. Contoh penerapan per topik (ILUSTRASI, bukan keputusan)
| Topik | Ide penerapan | Bukti yang dipakai |
|---|---|---|
| Cara kerja sifon pipa-U | miniatur potongan pipa di dalam kamar mandi, air bergerak, kamera masuk ke dalam pipa | 03 (diorama potongan), 01 (set-piece), 02 (aliran) |
| Mitos "rumah tusuk sate sial" | set jalan dan rumah, karakter pengganti penonton, cahaya/bayangan, perbandingan dua rumah | 01 (karakter), 02 (warna makna) |
| Perbandingan KPR vs sewa | dua set bersisian, warna oranye vs biru bertumbuh | 02 (1995 vs 2005) |
| Sejarah bahan bangunan | satu bangunan tumbuh per era | 02 (pertumbuhan); **tidak ada referensi era** |
| Konsep abstrak (suku bunga) | tidak ada referensi; **jangan diisi** | — |

## Pertanyaan terbuka
Lihat bagian akhir laporan Fase 2 di `identity/references/00-perbandingan.md` §5 dan `workflow/build-phases.md`.

## Riwayat
- v0 kerangka · v1 diisi dari 3 referensi (kandidat, belum disetujui).
