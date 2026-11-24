# Kamus Kamera Isometrik — DRAFT

**Status:** draft dari pengamatan referensi dan benchmark yang pemilik nilai "oke". **Belum disetujui sebagai final.** Bukan keputusan style: dokumen ini hanya menamai dan mengukur gerak kamera.
Tingkat bukti: **[R]** terlihat di referensi (`identity/references/01–03`) · **[B]** dibangun dan diukur di benchmark (`pilot/p1`, `pilot/p1/README.md` bagian v3) · **[K]** pengetahuan umum, belum diuji.

## 1. Nama gayanya
- **Visual:** *isometric 3D explainer animation*: dunia diorama dilihat dari atas-miring, cahaya lunak, material tanpa outline (juga disebut *miniature/diorama world* atau *clay render*). Istilah industri tidak baku [K].
- **Kamera:** *orthographic camera choreography*: kamera ortografik (azimuth 45°, elevasi 35,264° untuk isometrik sejati) yang digerakkan dengan truck, zoom, dan orbit.

## 2. Ortografik vs perspektif (penentu rasa)
| | Ortografik (isometrik sejati) | Perspektif oblik tinggi |
|---|---|---|
| Garis sejajar | tetap sejajar | menyatu ke kejauhan |
| Ukuran benda | sama di depan dan belakang | mengecil di kejauhan |
| Geser kamera | benda dan latar bergeser **sama** (tanpa parallax) | benda dekat bergeser lebih jauh (parallax) |
| Zoom | hanya skala, tanpa perubahan perspektif | dolly mengubah perspektif |
| Sumber kedalaman | bayangan, oklusi, blur, **orbit** | + parallax dan skala |
Temuan referensi [R]: **MediaCraft memakai perspektif nyata** (bukan ortografik murni); **Capsule Homes** tampak hampir ortografik pada shot lebar dan berperspektif pada close-up; tutorial Blender membandingkan keduanya. Pilihan "ortografik murni atau oblik berperspektif" **belum diputuskan**.

## 3. Gerak dasar
| Gerak | Istilah | Efek di layar | Fungsi naratif (contoh) | Batas dan biaya di pipeline kita |
|---|---|---|---|---|
| **Kiri-kanan** | *truck* (geser lateral); *pan* bila kamera hanya berputar di tempat | adegan bergeser kaku | menyusuri ruang, memperkenalkan elemen satu per satu, menghubungkan dua benda | **[B]** satu plat overscan lebar (3240×2112 untuk frame 1080×1920) digeser di Remotion; tanpa artefak. Plat ±312 dtk render |
| **Naik-turun** | *pedestal* | adegan bergeser vertikal | mengikuti ketinggian (mis. dari wastafel ke pipa di bawah) | sama dengan truck; keuntungan: gerak kecil bisa dari plat yang sama |
| **Zoom in/out** | zoom ortografik (skala bidang pandang), bukan *dolly* | membesar/mengecil tanpa perubahan perspektif | memusatkan perhatian ke detail (in) atau memperlihatkan konteks (out) | **[B]** dibatasi **resolusi plat**: zoom 1,26× butuh plat 1361×2419 (BACK/MID/FRONT ±282 dtk); zoom lebih besar menaikkan biaya kuadratik |
| **Memutar** | *orbit* (*arc*); *turntable* bila benda yang diputar | sudut pandang berubah | membuka sisi yang tersembunyi, memberi kedalaman, memperlihatkan hubungan 3D | **[B]** keyframe tiap ≤2° (beauty + kedalaman 16-bit, ±97 dtk per keyframe) lalu reproyeksi; 41°→49° bersih; orbit besar belum diuji |
| **Fokus bergeser** | *rack focus* | lapisan depan/belakang bergantian tajam | mengarahkan mata dari satu elemen ke elemen berikutnya | **[B]** blur dipanggang per lapisan lalu cross-fade; murah |
| **Statis** | *locked-off* | tidak ada gerak kamera | memberi jeda, fokus ke gerak objek | gratis; gunakan sebagai pilihan sah |

## 4. Kombinasi (contoh resep; bukan template wajib)
| Resep | Urutan | Tujuan |
|---|---|---|
| **Reveal lateral** | truck pelan → berhenti pada elemen kunci | memperkenalkan sesuatu yang berada di luar frame |
| **Zoom ke detail** | zoom in + rack focus ke bagian mekanisme | menjelaskan bagian dalam |
| **Buka dan lihat** | orbit kecil sambil benda tetap | memperlihatkan sisi yang terhalang |
| **Konteks lalu detail** | frame lebar statis → zoom in → potong ke shot lain | dari gambaran besar ke penjelasan |
Setiap gerak harus punya tujuan; gerak tanpa tujuan tidak dipakai.

## 5. Aturan variasi (dari arahan pemilik)
Jangan zoom-in di setiap shot; jangan partikel di setiap shot; jangan sapuan cahaya di setiap shot; jangan DOF di setiap shot; jangan memakai kombinasi kamera yang sama berulang. Sebagian shot **harus statis**, sebagian lateral, sebagian macro, sebagian wide. Angka batas per video **belum ditetapkan** (usulan lama: push-in ≤30%, statis ≥15%, lateral ≥15%) dan menunggu persetujuan.

## 6. Pelajaran dari benchmark [B]
- Truck, pedestal, dan zoom pada kamera ortografik bersih dari **satu plat**; orbit butuh banyak keyframe. **Setiap derajat kebebasan kamera punya biaya plat sendiri**; rencanakan di storyboard.
- Dunia harus **melampaui frame** (lantai 6,4 m, dinding 4 m) agar isometrik tidak terbaca sebagai blok melayang di latar abu.
- Komposisi 9:16 pada isometrik menyisakan **dinding atas yang kosong**; turunkan target kamera dan isi dinding dengan elemen bermotivasi.
- Push-in sempit (1,26×) belum cukup membuat bagian dalam terbaca; pada 45° benda bisa terhalang panel depan.
- Render Remotion 12 dtk: **25,2 dtk** (CPU 4 inti); pabrik plat 3 shot: **18 menit** (Blender CPU).

## 7. Pertanyaan terbuka
1. Ortografik murni (isometrik sejati) atau oblik berperspektif seperti MediaCraft?
2. Rentang orbit: ±4° (aman, murah) atau lebih besar (butuh lebih banyak keyframe atau 3D penuh)?
3. Rentang zoom yang diinginkan (menentukan resolusi plat)?
4. Batas variasi per video (angka)?
5. Dunia/topik berikutnya yang dipakai untuk menguji kamera ini selain kamar mandi?
