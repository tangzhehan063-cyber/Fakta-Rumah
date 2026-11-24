# Visual Reference Analysis Framework (B)

Tujuan: mengubah "saya suka yang ini" menjadi parameter konkret yang bisa diterjemahkan ke kode, tanpa meniru referensi mentah.

## Aturan analisis
1. **Dilarang label kosong** ("stylized", "flat", "2D", "3D", "clean", "modern") tanpa penjelasan terukur. Setiap label harus diikuti bukti yang bisa dicek di frame.
2. **Bukti berbasis frame.** Setiap temuan menyebut timestamp/frame atau bagian gambar. Untuk video: ambil frame di interval teratur + frame di momen transisi + klip gerak pendek. Saya melihat frame statis; untuk motion saya menganalisis rangkaian frame (timing diperkirakan dari jarak frame), jadi angka timing bersifat perkiraan dan ditandai demikian.
3. **Pisahkan observasi dari inferensi.** "Outline ±3px warna lebih gelap dari fill" = observasi. "Mungkin dibuat dengan stroke di atas fill" = inferensi.
4. **Selalu tutup dengan 4 keranjang** (lihat bagian 3). Tanpa pemisahan ini, analisis tidak boleh dipakai ke Identity Spec.
5. **Tidak ada keputusan teknologi** di analisis. Tanya "apa yang terlihat", bukan "bagaimana membuatnya di SVG/Three".
6. **Kalau tidak yakin, tanya pemilik** (mis. "bagian mana dari klip ini yang Anda suka?"). Referensi sering disukai karena satu hal, bukan keseluruhan.

## 1. Input per referensi (diisi pemilik, singkat)
- Tautan/file, durasi, bagian mana yang relevan (timestamp).
- "Yang saya suka" dan "yang tidak" dalam kata-kata bebas, sependek apa pun.
- Dipakai untuk kategori apa (jika terpikir).

## 2. Dimensi analisis

Setiap dimensi dijawab konkret. Contoh "pertanyaan ukur" ada di kolom kanan.

### A. Bentuk & objek
| Dimensi | Pertanyaan ukur |
|---|---|
| Bahasa bentuk | Dominan membulat/bersudut/organik? Apakah tepi dibulatkan konsisten (radius relatif)? |
| Proporsi | Rasio dilebih-lebihkan atau realistis? Objek "tebal/pendek" atau ramping? |
| Siluet | Apakah objek dikenali dari siluet saja? Seberapa sederhana siluetnya? |
| Detail | Jumlah tingkat detail (primer/sekunder/tersier)? Apa yang dipilih untuk didetailkan vs dihilangkan? Apakah detail menjelaskan fungsi atau hanya dekorasi? |
| Konsistensi | Apakah semua objek memakai bahasa bentuk sama? |

### B. Garis, warna, shading
| Dimensi | Pertanyaan ukur |
|---|---|
| Outline | Ada/tidak? Tebal relatif terhadap objek? Warna: hitam, atau turunan fill? Tebal bervariasi? |
| Shading | Tanpa shading / cel (jumlah band) / gradien halus / tekstur / grain? Arah cahaya konsisten? |
| Bayangan | Cast shadow ada? Keras/lembut? Ambient occlusion/contact shadow? Warna bayangan (hitam vs warna jenuh)? |
| Palet | Perkiraan nilai warna (hex), jumlah warna dominan, rasio 60/30/10, suhu, saturasi, kontras nilai (value). |
| Tekstur | Ada grain/noise/halftone/paper? Seberapa kuat? |
| Cahaya | Sumber tunggal/banyak? Rim light? Glow? Atmosfer (kabut, volumetric)? |

### C. Ruang: perspektif, kamera, depth
| Dimensi | Pertanyaan ukur |
|---|---|
| Perspektif | Orthographic, 1-/2-/3-point, fisheye, "dipalsukan" dengan layer? Titik hilang di mana? |
| Sudut kamera | Eye-level/low/high/overhead/3-4? Berubah antar shot atau tetap? |
| Depth | Berapa layer yang terbaca (foreground/mid/background)? Dengan apa depth dibangun: skala, overlap, atmospheric perspective, blur, parallax, bayangan? |
| Komposisi | Pusat vs aturan sepertiga vs asimetris; ruang negatif; garis penuntun; framing foreground. |
| Lingkungan | Apakah ada latar yang bercerita, atau hanya warna polos/gradien? Kepadatan detail latar vs fokus. |

### D. Karakter (jika ada)
Proporsi (tinggi kepala), kompleksitas wajah, mata/mulut/ekspresi, rig (sendi, bagian tubuh terpisah), gaya gerak (squash & stretch, overshoot), seberapa sering karakter muncul, apakah *perlu* untuk komunikasi.

### E. Motion
| Dimensi | Pertanyaan ukur |
|---|---|
| Timing | Durasi gerak tipikal (ms): masuk, jeda, keluar. Tempo (cepat-tajam / lambat-halus). |
| Easing | Linier, ease-in-out, overshoot/spring, snap? Apakah easing berbeda per jenis elemen? |
| Prinsip | Anticipation, follow-through, overlapping action, squash-stretch, arc: ada? di mana? |
| Hierarki | Apa yang bergerak duluan? Apakah elemen sekunder menahan diri? Berapa elemen bergerak bersamaan? |
| Kamera | Jenis gerakan (dolly/pan/push-in/orbit/parallax), kecepatan, motivasi. |
| Motion pada kondisi diam | Ada gerak ambient (napas, kibaran)? Seberapa halus? |

### F. Transisi & editing
Jenis transisi (cut/match cut/wipe/objek-ke-objek/kamera menembus), motivasi kreatifnya, durasi shot rata-rata, ritme (konstan/bervariasi), hubungan cut dengan narasi, penggunaan hold untuk memberi napas.

### G. Penyampaian informasi
Bagaimana informasi dikomunikasikan: lewat gambar, label, angka, narasi saja? Bagaimana teks diperlakukan (jenis huruf, posisi, kapan muncul)? Apakah visual *membuktikan* klaim atau hanya menemaninya? Bagaimana konsep sulit disederhanakan?

### H. Apa yang membuatnya menarik
Satu paragraf, jujur: 3–5 hal spesifik yang menahan perhatian. (Ini penentu apa yang harus dipertahankan.)

## 3. Empat keranjang (wajib)
| Keranjang | Pertanyaan | Isi |
|---|---|---|
| ✅ **Suka** | Apa yang harus masuk ke identitas channel? | Parameter konkret |
| ❌ **Tidak suka** | Apa yang harus dihindari? | Parameter konkret |
| 🔧 **Perlu disesuaikan** | Cocok tapi tidak bisa ditiru mentah: terlalu mirip sumber, terlalu mahal, tidak cocok bahasa/budaya channel | Versi adaptasi + alasan |
| 🎬 **Khusus video tertentu** | Menarik tapi hanya untuk kategori/konten tertentu | Tag kategori |

## 4. Terjemahan ke implementasi (setelah pemilik menyetujui keranjang)
Untuk tiap item ✅/🔧: tulis sebagai **parameter** + **cara memverifikasi di render**. Contoh bentuk (bukan isi final):

> Outline: tebal ≈ 2–3% tinggi objek, warna = fill digelapkan 35% + sedikit hue shift, tebal konstan. Verifikasi: tebal tampak sama pada dua skala objek.

Hasil akhirnya diringkas di `visual-identity.md`. Detail mentah tetap di `identity/references/<nama>.md`.

## 5. Uji kalibrasi (anti-salah-tafsir)
Setelah analisis, saya membuat **frame uji** dari kode yang merepresentasikan parameter. Pemilik menilai: "ini yang saya maksud?" Jika tidak, analisis direvisi, bukan kodenya ditambal. Frame uji adalah bahasa bersama; kata-kata saja mudah salah paham.

## Template
`templates/reference-analysis.md`
