# Fakta Rumah

Repository produksi video explainer/edukasi. Dimulai dari nol; tidak menyalin `Channel-Penjelasan`.

**Status: setelah reset (24 Nov 2026).** Arah visual Fase 2–3 dihapus; pilot dipulihkan; bahasa kamera didokumentasikan sebagai draft. **Tidak ada engine, tidak ada keputusan style final.**

Seluruh pekerjaan sebelum reset tetap ada di riwayat Git (commit `8b0267d`); pulihkan bagian tertentu dengan `git checkout 8b0267d -- <path>`.

Pilot dipulihkan dari commit `8b0267d` atas permintaan pemilik (hasil benchmark dinilai "oke"): `pilot/p0` (scene bersama + dua renderer + bench) dan `pilot/p1` (benchmark Remotion v1–v3, video di `pilot/p1/eval`). Plat besar dan `node_modules` tidak ikut (dapat dibuat ulang).

## Yang dipertahankan
| Dokumen | Isi |
|---|---|
| [`CLAUDE.md`](CLAUDE.md) | Aturan proyek |
| [`PROPOSAL.md`](PROPOSAL.md), [`ARCHITECTURE.md`](ARCHITECTURE.md) | Proposal struktur dan arsitektur Fase 1 (versi sebelum arah ilusi/isometrik) |
| [`workflow/`](workflow/) | Alur kerja, kategori, rencana fase dan pilot versi Fase 1 |
| [`identity/reference-analysis-framework.md`](identity/reference-analysis-framework.md) | Cara membedah referensi |
| [`identity/references/`](identity/references/) | 3 video referensi pemilik dan analisis 01–03 |
| [`identity/kamus-kamera.md`](identity/kamus-kamera.md) | **Kamus kamera isometrik (draft)**: truck, zoom, orbit, pedestal, biaya, aturan variasi |
| [`identity/visual-identity.md`](identity/visual-identity.md) | Kerangka kosong + syarat mutlak kualitas dari pemilik (§1b) |
| [`research/ecosystem-research.md`](research/ecosystem-research.md), [`research/repo-lama-audit.md`](research/repo-lama-audit.md) | Riset ekosistem dan audit repo lama |
| [`templates/`](templates/) | Template brief, storyboard, analisis referensi |
