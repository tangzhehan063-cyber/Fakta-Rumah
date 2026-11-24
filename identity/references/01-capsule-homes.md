# Referensi 01 — "3D Isometric Explainer Video Animation – Capsule Homes"

**File:** `3D Isometric Explainer Video Animation - Capsule Homes_1080p.mp4`
**Data teknis (ffprobe):** 1920×1080, **15 fps** (nilai kontainer; bisa hasil unggahan ulang), 42,3 dtk, ada audio (**tidak saya dengar**).
**Yang saya periksa:** 18 frame (1 frame / 2,4 dtk), 12 frame rapat (3 fps) pada 0–4 dtk, deteksi cut otomatis. **Tidak diperiksa:** audio/narasi, timing gerak di bawah 0,33 dtk, easing sebenarnya.

Tanda: **(O)** observasi langsung dari frame · **(I)** inferensi saya · warna diukur dari piksel (median-cut), bukan tebakan mata.

## Ringkasan isi (O)
Iklan produk: pasangan memilih rumah kapsul lewat tablet, melihat katalog (**"17 MODELS"**), mengunjungi model pajangan bersama konsultan berhoodie hijau, berjabat tangan, lalu memesan lewat situs di monitor. Tutup dengan logo + tombol URL pada kartu krem datar. Ini **iklan**, bukan penjelasan: informasi sangat sedikit, cerita emosional (ragu → tertarik → sepakat).

## A. Gaya visual
- **Bahasa bentuk (O):** semua tepi dibulatkan (bevel lembut) pada sofa, kursi, meja, tablet, monitor. Tidak ada sudut tajam. Bentuk "gemuk" dan sederhana.
- **Proporsi karakter (O):** kepala kecil, tungkai dan lengan panjang, ±6,5–7 kepala (perkiraan visual). Tangan besar dan sederhana (jari menyatu).
- **Wajah (O):** sangat disederhanakan (mata oval gelap kecil, hidung sebagai tonjolan, mulut minimal). Emosi dibaca dari **pose tubuh** (tangan di dagu = berpikir, tangan di pinggul), bukan ekspresi wajah.
- **Rambut & pakaian (O):** rambut massa pahatan padat; pakaian dengan tekstur sederhana (garis putih di baju biru, jahitan halus), tanpa kain realistis.
- **Outline (O):** **tidak ada** garis tepi. Bentuk dibaca dari shading.
- **Shading (O):** shading lunak dengan *bounce light* hangat (permukaan putih terlihat tersaput peach/krem), highlight lembut, bayangan panjang berwarna tidak terlalu gelap. (I) tampak seperti render GI (global illumination) lunak, bukan shading datar.
- **Material (O):** matte seperti tanah liat untuk kulit dan sofa; kayu dek dengan serat terlihat; kaca dengan pantulan di rumah; logam gelap pada rangka; kerikil/pasir bertekstur pada tanah di adegan rumah.
- **Palet terukur (O, dari 15 frame non-logo):** krem/peach dominan `#ece1d6` `#f6e8d8` `#f1e7dc` (±55%), krem gelap `#d1c7b6` `#af9d89`, cokelat tua `#635647`. Aksen: biru-abu baju `#8fa5b5`-an, hijau sage hoodie, **hijau hutan gelap merek** (layar tablet, pelat dasar) dan salmon/terakota pada tombol. Total palet terkendali, hangat, kontras rendah-menengah.
- **Cahaya (O):** satu arah cahaya hangat dari satu sisi dengan bayangan lembut memanjang; tidak ada kontras dramatis. Suasana siang lembut.
- **Ketidaksempurnaan/karakter artistik (O):** jari kadang menyatu, wajah dingin; tidak ada tekstur kuas atau grain. Bersih.

## B. Komposisi spasial & depth
- **Dunia (O):** *lantai krem tak terbatas* tanpa dinding, hanya set-piece yang relevan (sofa, kursi berlengan, meja kopi, karpet, tanaman). Ini **panggung bersih, bukan ruangan penuh**.
- **Lapisan (O):** depth dibangun dari: (1) overlap objek, (2) bayangan kontak di lantai, (3) **depth of field** pada adegan close-up (tangan di depan tablet buram), (4) skala figur. Foreground framing: tangan dan tablet besar menutupi sudut frame pada shot POV.
- **Perspektif (O/I):** shot lebar tampak **hampir ortografik / lensa panjang** (sofa dan kursi sama besar di depan dan belakang, garis sejajar). Shot dekat (tablet, tangan) memperlihatkan **konvergensi perspektif** jelas. (I) kamera berpindah antara lensa panjang dan lensa lebih normal sesuai shot.
- **Sudut kamera (O):** oblik tinggi (±35–50° ke bawah) pada shot lebar; ketinggian mata/POV bahu pada shot dekat; ada **tampak ¾ atas** model rumah.
- **Skala lingkungan (O):** model rumah diletakkan di tanah berkerikil berukuran "meja diorama" (isometrik mini) lalu karakter kecil di sampingnya: **perubahan skala** dipakai sebagai alat cerita.
- **Terasa:** volumetrik/spasial (bukan datar). Depth dicapai **tanpa lingkungan rumit**, cukup dengan cahaya, bayangan, dan DOF.

## C. Kamera
- **Cut hanya 2 kali** (3,4 dtk dan 7,4 dtk, deteksi otomatis). Sisanya **gerak kamera kontinu** dan transisi lewat objek (O):
  - tablet di tangan → kamera masuk ke layar → kartu foto keluar menjadi panel 3D di dunia (I: berdasarkan urutan frame 6–9; transisi tepatnya tidak terlihat di sampling saya);
  - monitor → kursor 3D besar → kartu penutup.
- **Jenis shot (O):** wide vignette (0–3 dtk), medium two-shot (3–7), POV bahu + extreme close-up tablet/tangan (7–17), wide showroom (17–26), detail kursor (±36), end card.
- **Gerak (I):** lembut (push-in/pull-back, sedikit orbit). Kecepatan tepatnya tidak bisa saya ukur dengan sampling ini.
- **Motivasi (O):** kamera mengikuti fokus cerita (tablet → hasil layar → dunia).

## D. Lingkungan & objek
- Set-piece **dikurasi**, bukan dekorasi penuh; tiap objek punya fungsi (sofa = tempat ragu, tablet = pemicu, rumah = tujuan).
- Objek dibangun sebagai **volume utuh dengan bevel**, bukan bidang tempel.
- Layar tablet/monitor menampilkan **foto/halaman web nyata sebagai tekstur layar** (O): foto **di dalam perangkat dalam dunia**, bukan latar. (Catatan: ini kasus yang Anda larang kecuali disetujui eksplisit; di sini foto berfungsi sebagai konten layar dalam dunia 3D.)
- Teks dan angka **eksis di dalam dunia**: "17 MODELS" sebagai huruf 3D ekstrusi hijau gelap berdiri di tanah; kartu foto sebagai panel tipis bersudut bulat dengan pelat dasar hijau.

## E. Karakter
- 3 karakter (pasangan + konsultan). Desain: lihat bagian A. Peran: **pengganti penonton** (mereka bimbang, tertarik, memutuskan).
- Gerak karakter (O dari frame): siklus jalan (0–1 dtk), diam-bergerak (tangan ke dagu, ke pinggul, bahu naik), menunjuk, mengetuk layar, berjabat tangan. (I) tampak animasi keyframe atau mocap yang dibersihkan; **sekunder** (rambut) sangat halus.
- Interaksi dengan objek: jari menyentuh layar, tangan memegang tablet.
- **Biaya (I):** bagian paling mahal dari referensi ini.

## F. Animasi & gerak
- **Gelembung pikiran** muncul dengan skala membesar dari kecil, berisi model isometrik mini (O: tahap "terbentuk" terlihat di frame 5–6 dari strip rapat).
- Objek muncul bertahap (kartu bertumpuk → satu kartu), tidak semua sekaligus (O).
- Hierarki: karakter bergerak sedikit; fokus tetap pada objek kunci (layar). (I)
- Timing/easing: **tidak bisa dinilai** dari sampling saya (3 fps maksimum). Perlu pemotongan lebih rapat jika Anda ingin analisis ini.
- **Catatan frame rate:** sumber 15 fps. Jika benar, gerakan terasa halus karena konten gerak lembut dan motion blur (I; tidak terlihat jelas di frame statis). Perlu dikonfirmasi apakah ini target Anda.

## G. Penceritaan & editing
- Struktur: masalah ragu → petunjuk (tablet) → katalog → kunjungan → keputusan → ajakan.
- Informasi diangkut oleh **dunia** (layar perangkat, huruf 3D, kartu) dan perilaku karakter, bukan oleh overlay.
- Ritme: panjang per shot (2 cut dalam 42 dtk) dengan banyak **perubahan di dalam shot**.
- Terhadap narasi: tidak diketahui (audio tidak saya dengar).

## Apa yang membuat referensi ini menarik (I, berbasis bukti di atas)
1. Dunia hangat dan kohesif: satu palet, satu arah cahaya, material matte → semuanya terasa "satu set".
2. Kehadiran **objek bervolume dengan bevel**, bukan bentuk datar.
3. **DOF dan foreground framing** pada close-up memberi kesan sinematik.
4. Karakter sederhana yang tetap hidup lewat pose.
5. **Transisi lewat objek** menggantikan cut.

## Keranjang (KANDIDAT, menunggu review Anda; belum ada pernyataan suka/tidak dari Anda untuk video ini)
| ✅ Mungkin suka | ❌ Mungkin tidak | 🔧 Perlu disesuaikan | 🎬 Khusus video tertentu |
|---|---|---|---|
| bevel lembut, cahaya hangat, palet terkendali, transisi lewat objek, DOF pada close-up, teks 3D dalam dunia | lantai krem kosong terlalu bersih (jika Anda mau lingkungan lebih kaya)? | karakter: biaya tinggi, putuskan perlu/tidak | adegan iklan produk, layar perangkat |

**Risiko terhadap syarat mutlak Anda:** shot lebar dengan lantai krem kosong dan sedikit objek bisa terbaca sebagai "objek di latar datar" bila lingkungannya terlalu minim. Dalam video ini terselamatkan oleh bayangan kontak, skala figur, dan kamera yang bergerak. Perlu keputusan Anda: apakah tingkat "set minimal" ini cukup?
