# Veri setleri, literatür, standartlar ve pazar

_27 Eylül 2026 · web araştırması. Lisanslar sayfadan elle doğrulanmalı; "doğrulanmadı" işaretliler özellikle._

## 1. Açık veri setleri
| Set | İçerik | Lisans / ticari |
|---|---|---|
| RSDDs (Gan vd.) | Type-I 67 görüntü 160×1000; Type-II 128 görüntü 55×1250; piksel maske. IEEE DataPort abonelik, dosyalar yüklenmemiş. https://ieee-dataport.org/documents/rsdds | Lisans yok → **ticari için kullanma** |
| NEU RSDDS-113 | 113 renkli + derinlik + maske (zip şifresi "neurail"). https://github.com/neu-rail-rsdds/rsdds | Lisans yok → belirsiz |
| Rail-5k | 1.100 etiketli (3648×2736) + ~4k etiketsiz; 13 sınıf (korugasyon, spalling, indentation, çatlak, bağlantı elemanı…); bbox + çatlak maske; uzun kuyruk. https://arxiv.org/abs/2106.14366 | Link/lisans bulunamadı; yazarlardan istenmeli |
| RailSem19 | Ray sahnesi segmentasyonu (ROI, ön-eğitim). https://openaccess.thecvf.com/content_CVPRW_2019/papers/WAD/Zendel_RailSem19_A_Dataset_for_Semantic_Rail_Scene_Understanding_CVPRW_2019_paper.pdf | CC-BY-NC 4.0 → **ticari değil** https://www.wilddash.cc/license/railsem19 |
| RFDD (bağlantı elemanı, Sci Data 2026) | 1.350 görüntü 2048×2021, 8.100+ örnek; Intact/Missing/Reversed/Displaced/Deformed/Fractured; maske. https://doi.org/10.57760/sciencedb.msdc.00071 · https://github.com/NIM-NMDC/RFDD | Makale CC BY-NC-ND; veri lisansı doğrulanmadı |
| Kaggle Railway Track Fault Detection (+ fastener) | Sınıflandırma, Bangladeş. https://www.kaggle.com/datasets/salmaneunus/railway-track-fault-detection · https://www.kaggle.com/datasets/ashikadnan/railway-track-fault-detection-dataset2fastener | "© Original Authors" → **ticari yok** |
| Roboflow: Rail Defects Detection (UNAL) | 207 görüntü; Squat, Head Checking, Corrugation, Spalling, Welding, Break Outs; bbox. https://universe.roboflow.com/raildefectunal/rail-defects-detection/dataset/2 | Doğrulanmadı |
| **Roboflow: Rail Defect** | ~4,9k; corrugation crack, flaking, putus, spalling, squat. https://universe.roboflow.com/defect-rexb3/rail-defect | CC BY 4.0 görünüyor, doğrulanmadı |
| Roboflow: Rail-Surface-defects (Kakashi) | spalling, squat, breaks, chipping. https://universe.roboflow.com/kakashi-fmrs2/rail-surface-defects-d9i8o | CC BY 4.0 görünüyor, doğrulanmadı |
| Roboflow: Railway Surface Defect / 1.5m | 46 görüntü; Spalling, Squat, Wheel Burn. https://universe.roboflow.com/ray-obj-detection/railway-surface-defect-detection | CC BY 4.0 görünüyor, doğrulanmadı |
| **Roboflow: Fastener Detection** | ~2,6k; Missing Fastener, Missing Dogscrew, Defective Joint, Good Fasteners, Good Joint. https://universe.roboflow.com/railway-defects-osolv/fastener-detection-7a3vn | Doğrulanmadı (RFD-DETR makalesi kendi setini CC BY 4.0 diyor) |
| DeepCrack (ön-eğitim) | https://github.com/yhlleo/DeepCrack | Ticari olmayan → **ticari yok** |
| Crack500 (ön-eğitim) | https://github.com/fyangneil/pavement-crack-detection | Lisans yok → belirsiz |

Konu dışı: RailFOD23 (katener yabancı cisim), MRSDI (yöntem adı, veri seti değil), awesome-railway-datasets (nokta bulutu).

## 2. Literatür
- İyileştirilmiş YOLOv8 varyantları RSDDs benzeri setlerde %94–97 mAP@0.5 (küçük setler, şişkin olabilir): https://www.sciencedirect.com/science/article/abs/pii/S0263224124018074 · https://ieeexplore.ieee.org/document/10689418/ · https://www.mdpi.com/1424-8220/24/11/3579
- RSD-YOLO (YOLOv11n): https://academics.erytis.com/index.php/AJET/article/view/528
- RFD-DETR (bağlantı elemanı, RT-DETR tabanlı): https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0331513
- Anomali: FS-RSDD RSDDs'de 95,2 / 99,1 ROC; görüntü düzeyinde PatchCore daha iyi https://pmc.ncbi.nlm.nih.gov/articles/PMC10536558/ · Rail-PatchCore https://link.springer.com/article/10.1007/s10489-025-06294-8
- Görüntüleme: Network Rail PLPR 0,8 mm'de bir görüntü https://www.newcivilengineer.com/latest/cameras-strapped-to-trains-help-network-rail-fix-tracks-in-record-time-12-02-2019/ · line-scan 30 km/h'te 0,25 mm/piksel, 120 km/h'te 1 mm/piksel https://link.springer.com/article/10.1007/s41064-025-00355-w
- **Çıkarım:** telefon/drone ile yavaş çekim bağlantı elemanı ve travers için yeterli olabilir; head check ince çatlakları ≤ 0,5 mm/piksel + kontrollü aydınlatma ister.

## 3. Standartlar
- UIC 712 kodları: 2223 head checking · 227 squat · 2221 shelling. https://www.sciencedirect.com/science/article/pii/S235214652200549X — yerini IRS 70712 almış görünüyor.
- EN 16729-3:2018: kusur tanımlama ve NDT yöntemi uygunluğu; değerlendirme kriterleri kapsam dışı.
- TCDD: hat bakım genel emirleri (ör. 105) var, okunamadı. **TCDD'nin kusur kataloğu işletmeciden istenmeli.**

## 4. Pazar
- MERMEC V-CUBE (0–200 km/h, 50+ kusur tipi) https://www.mermecgroup.com/inspect/track-inspection/524/track-inspection-v-cube.php
- ENSCO TCIS / RSIS, KLD Labs https://www.ensco.com/rail
- Loram Aurora https://loram.com/inspection-and-optimization/inspection-services/tie-inspection-services/aurora/
- Plasser "measurement as a service" https://www.plassertheurer.com/en/infrastructure/measuring-and-inspection/measurement-as-a-service
- Fugro RILA (lidar + video) · Sperry, Nordco (ultrason, kapsam dışı)
- Girişimler: RailPod, InspectRail, D-Rail, KONUX (CB Insights)
- Türkiye: TCDD Teknik T-rail (geometri, profil, korugasyon ölçümü) https://www.tcddteknik.com.tr/hizmet/olcum-hizmetleri · TCDD–TÜBİTAK OTMİ (araç muayenesi) · Fırat Üniv. (İ. Aydın, M. Karaköse) https://github.com/ilhanaydintr/RailDefectDetection
- **Yerli ticari görsel ray yüzey sistemi bulunamadı.** Fiyatlar açıklanmamış.

## 5. Tedarik ve pilot
- 2019/12 sayılı Genelge: kamu verisi yalnız kurum sistemlerinde ya da kurum kontrolündeki yerli sağlayıcıda → **on-prem / yerli bulut zorunluya yakın**. https://cbddo.gov.tr/sss/bilgi-iletisim-guvenligi/
- Kanıt metriği: km başına aday ve doğrulama oranı (PLPR'de mil başına ~20 aday, %30–35 doğrulanıyor — forum kaynağı).
- Beklenen çıktı: kilometre konumu, şiddet, güven skoru, işaretli görüntü, REST API; SAP PM gibi EAM'e aktarım.
- Pilot sözleşmesine **operatör verisi üzerinde eğitim hakkı** yazılmalı.
