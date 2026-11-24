# Fakta Rumah

Repository produksi video explainer/edukasi. Dimulai dari nol (clean slate); tidak menyalin `Channel-Penjelasan`.

**Status: Fase 1 — riset dan desain arsitektur (menunggu review). Belum ada engine, belum ada video.**

## Peta dokumen (baca berurutan)

| # | Dokumen | Isi |
|---|---------|-----|
| 1 | [`PROPOSAL.md`](PROPOSAL.md) | Struktur repo, prinsip, status keputusan |
| 1b | [`ARCHITECTURE.md`](ARCHITECTURE.md) | Arsitektur berlapis, kontrak shot, manifest, QA, batas otomasi |
| 1c | [`workflow/build-phases.md`](workflow/build-phases.md) | Rencana 6 fase + keputusan terbuka |
| 2 | [`workflow/workflow.md`](workflow/workflow.md) | Alur produksi video, adaptif per kategori |
| 3 | [`workflow/categories.md`](workflow/categories.md) | Kategori konten: pertanyaan kunci & opsi (bukan template) |
| 4 | [`identity/reference-analysis-framework.md`](identity/reference-analysis-framework.md) | Cara membedah video/gambar referensi |
| 5 | [`identity/visual-identity.md`](identity/visual-identity.md) | Draft Visual Identity Spec (kerangka, belum final) |
| 6 | [`workflow/pilot-plan.md`](workflow/pilot-plan.md) | Rencana pilot untuk menguji style & kualitas animasi |
| 7 | [`research/ecosystem-research.md`](research/ecosystem-research.md) | Laporan riset: lisensi, kelebihan/kekurangan, rekomendasi |
| 8 | [`research/repo-lama-audit.md`](research/repo-lama-audit.md) | Audit read-only repo lama: masalah, yang layak dipertahankan |

## Struktur

```
CLAUDE.md        instruksi proyek (pendek)
identity/        visual identity + analisis referensi
workflow/        alur kerja, kategori, rencana pilot
templates/       brief, storyboard, analisis referensi
research/        riset tools/library/skills
videos/<slug>/   satu folder per video (brief → render)
engine/          KOSONG sampai pilot disetujui
assets/          KOSONG; hanya aset yang terbukti dipakai ulang
qa/              checklist & catatan review render
```
