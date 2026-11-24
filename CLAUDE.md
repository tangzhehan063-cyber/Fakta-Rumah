# Fakta Rumah — instruksi proyek

Repo ini memproduksi video explainer. Visual dibuat lewat kode. **Tidak ada** AI image/video generation atau API AI eksternal **untuk visual**. Pengecualian yang disetujui pemilik: Gemini TTS untuk suara (Fase 5). Fase proyek: lihat `workflow/build-phases.md`.

## Sumber kebenaran
- Workflow: `workflow/workflow.md`
- Visual identity: `identity/visual-identity.md` (status DRAFT sampai pemilik menyetujui; jangan perlakukan isinya sebagai final)
- Kategori konten: `workflow/categories.md` (opsi, bukan template wajib)

Jika dokumen bertentangan, berhenti dan tanyakan. Jangan menambah aturan baru ke file lain; ubah dokumen sumbernya.

## Aturan keras
1. Jangan memilih style final sendiri. Style berasal dari referensi pemilik yang sudah dianalisis (`identity/references/`).
2. Teknik (SVG/Canvas/CSS/Three.js/Remotion/dll.) dipilih SETELAH visual direction, per shot. Tidak ada default teknik, default kamera (top-down, isometric, front, centered), atau default kategori (breakdown).
3. Jangan menyalin aturan, workflow, atau kode dari repo lama (`Channel-Penjelasan`) tanpa evaluasi; lihat `research/repo-lama-audit.md`.
3b. Jangan koding produksi sebelum storyboard disetujui pemilik jika ada keputusan kreatif besar.
4. QA = menonton hasil render (frame/klip), bukan hanya membaca kode. Jangan klaim "selesai" tanpa melihat render.
5. Jangan membuat abstraksi/komponen reusable sebelum dipakai di ≥2 video nyata. `engine/` dan `assets/` tetap kosong sampai pilot disetujui.
6. Kode/skill/aturan dari luar: adopt/adapt/reference/reject dicatat di `research/`. Jangan instal atau adopsi tanpa persetujuan.
7. Repo lama `Channel-Penjelasan` hanya referensi baca-saja. Jangan impor workflow, skill, atau aturan visualnya.

## Gaya kerja
- Kalau brief kurang jelas, tanya. Kalau arah visual belum jelas, tawarkan beberapa konsep yang benar-benar berbeda.
- Bahasa dokumen & komunikasi: Indonesia.
- Setiap shot wajib punya alasan (tujuan, komposisi, kamera).
