# Veri setleri

Veri dosyaları git'e girmez. Her set için kaynak, lisans ve ticari kullanım durumu burada tutulur. Ayrıntı: `../arastirma/veri-literatur-pazar.md`.

Lisanslar 27.09.2026'da set sayfalarından doğrulandı. CC BY 4.0: ticari kullanım serbest, **atıf zorunlu** (rapor ve ürün belgelerinde kaynak gösterilecek).

| Set | Görev | Görüntü | Sınıflar | Lisans | Ürüne girer mi |
|---|---|---|---|---|---|
| [Fastener Detection](https://universe.roboflow.com/railway-defects-osolv/fastener-detection-7a3vn) (railway defects) | Nesne tespiti | 2.571 | Defective Joint, Good Fasteners, Good Joint, Missing Dogscrew, Missing Fastener | CC BY 4.0 ✓ | Evet |
| [Rail Defect](https://universe.roboflow.com/defect-rexb3/rail-defect) (Defect) | **Sınıflandırma** (bbox yok) | 4.939 | crack, corrugation, flaking, putus, spalling (+1) | CC BY 4.0 ✓ | Evet — görüntü düzeyi sınıflandırıcı için |
| [Rail-Surface-defects](https://universe.roboflow.com/kakashi-fmrs2/rail-surface-defects-d9i8o) (Kakashi) | Nesne tespiti | 337 kaynak (v7: 4.156, artırılmış) | breaks, chipping, Cracks, Flaking, Rails (+4) | CC BY 4.0 ✓ | Evet |
| [Rail Defects Detection](https://universe.roboflow.com/raildefectunal/rail-defects-detection) (RailDefectUNAL) | Nesne tespiti | 207 kaynak (v2: 496) | Head - Checks, RCF, Spalling | CC BY 4.0 ✓ | Evet |
| RFDD | Segmentasyon | 1.350 | Intact, Missing, Reversed, Displaced, Deformed, Fractured | Belirsiz | Hayır (iç kıyaslama) |
| Rail-5k | Tespit + maske | 1.100 | 13 sınıf | Belirsiz | Hayır (yazar izni gerekir) |
| RSDDs / NEU RSDDS-113 | Segmentasyon | 67+128 / 113 | yüzey kusuru | Lisans yok | Hayır |
| RailSem19 | Sahne segmentasyonu | — | ray, travers… | CC-BY-NC 4.0 | Hayır |

**Not:** Artırılmış (augmented) sürümlerdeki görüntü sayıları şişkin. Test seti yalnız **kaynak görüntülerden** kurulur; aynı kaynağın artırılmış kopyası eğitim ve testte birlikte bulunmaz.

İndirme için Roboflow API anahtarı gerekir: `RayGoz/.env` içinde `ROBOFLOW_API_KEY=...` (git'e girmez).
