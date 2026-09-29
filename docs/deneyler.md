# Deney kayıtları

Her deney: tarih · görev · model · veri sürümü (hazirla.py, tohum 42, benzerlik kümeli bölme) · ana metrikler · not · lisans durumu.
Metrikler **kilitli test setinde**. Eğitim makinesi: ofis (RTX 3080 Ti 12 GB, WSL2). Çıktılar: `runs/` (git dışı).

| # | Tarih | Görev | Model | Epoch (en iyi) | Süre | Test mAP@0.5 | mAP@0.5:0.95 | Lisans |
|---|---|---|---|---|---|---|---|---|
| 1 | 27.09.2026 | bilesen | YOLO11s, 640 | 83 (48) | 15 dk | **0,871** | 0,569 | AGPL — yalnız araştırma |
| 2 | 27.09.2026 | yuzey | YOLO11s, 640 | 93 (72) | 29 dk | **0,540** | 0,258 | AGPL — yalnız araştırma |
| 3 | 29.09.2026 | yuzey | YOLO11s, **1024** | — | ~1 sa* | 0,513 | 0,240 | AGPL — yalnız araştırma |
| 4 | 29.09.2026 | yuzey | **YOLO11m**, 640 | — | ~1 sa | 0,524 | 0,274 | AGPL — yalnız araştırma |
| 5 | 29.09.2026 | yuzey_birlesik | YOLO11s, 640 | 105 (78) | ~25 dk | 0,432 | 0,191 | AGPL — yalnız araştırma |
| 6 | 29.09.2026 | yuzey | **RT-DETR-l**, 640 | 54 (29) | 1,7 sa | **0,572** | **0,292** | Ultralytics uygulaması AGPL; mimari Apache (resmî depo) |

\* Deney 3 sırasında ofis makinesi uykuya geçti; gerçek süre ~1 saat.

## 1 · bilesen · YOLO11s
| Sınıf | Test örnek | Precision | Recall | mAP@0.5 |
|---|---|---|---|---|
| baglanti_eksik | 100 | 0,935 | **0,880** | 0,936 |
| tirfon_eksik | 4 | 0,339 | 1,000 | 0,702 |
| ek_kusurlu | 37 | 1,000 | 0,708 | 0,885 |
| baglanti_saglam | 172 | 0,879 | 0,849 | 0,885 |
| ek_saglam | 44 | 0,870 | 0,914 | 0,946 |

- **Eksik bağlantı elemanı: kabul kriterini geçiyor** (recall 0,88, precision 0,94 ≥ 0,70).
- Kusurlu ek: precision yüksek, recall 0,71 — sınırda.
- Eksik tirfon: testte 4 örnek → metrik anlamsız; precision 0,34 çok yanlış alarm veriyor olabilir, daha fazla veri gerekli.

## 2 · yuzey · YOLO11s
| Sınıf | Test örnek | Precision | Recall | mAP@0.5 |
|---|---|---|---|---|
| squat | 15 | 0,360 | 0,333 | 0,281 |
| dokulme | 64 | 0,545 | 0,453 | 0,431 |
| pullanma | 7 | 0,247 | 0,429 | 0,278 |
| catlak | 14 | 0,673 | 0,429 | 0,585 |
| head_check | 35 | 0,516 | 0,457 | 0,554 |
| kirik | 7 | 0,923 | 1,000 | 0,995 |
| iz | 16 | 0,545 | 0,812 | 0,655 |

- **Faz 1 sınıfları (squat, dökülme, pullanma) kabul kriterinin altında** (recall 0,33–0,45).
- Karışıklık matrisi: ana hata **kaçırma** — squat %67, pullanma %57, dökülme %45 arka plan sayılmış. Sınıflar arası karışma az; tek belirgin karışma çatlak → iz (%43).
- Kırık %100 ama testte 7 örnek; güvenilir değil.
- Sebep adayları: az kaynak görüntü (~1.100), üç farklı kaynaktan farklı kamera/çözünürlük, 640×640'a gerilmiş görüntülerde küçük kusurların kaybolması.

## 3–6 · yüzey karşılaştırması (recall, test)
| Sınıf (test örnek) | #2 YOLO11s 640 | #3 1024 | #4 YOLO11m | #6 RT-DETR-l |
|---|---|---|---|---|
| squat (15) | 0,333 | — | — | **0,533** |
| dokulme (64) | **0,453** | — | — | 0,283 |
| pullanma (7) | **0,429** | — | — | 0,286 |
| catlak (14) | 0,429 | — | — | **0,641** |
| head_check (35) | **0,457** | — | — | 0,371 |
| **mAP@0.5** | 0,540 | 0,513 | 0,524 | **0,572** |

Deney 5 (birleşik sınıf) test: yuzey_hasari P 0,291 / R 0,333 / mAP50 0,302; head_check 0,114'e düştü.

### Sonuçlar
- **Çözünürlük (#3) ve model büyüklüğü (#4) işe yaramadı** → darboğaz model değil, **veri**.
- **Sınıf birleştirme (#5) kötüleştirdi:** üç farklı kaynaktan gelen, görünüşü çok farklı kusurlar tek sınıfta toplanınca model ortak bir desen bulamıyor; head check bile bozuldu. Birleştirme fikri bırakıldı.
- **RT-DETR (#6) en iyisi** (+3 puan mAP50, +3,4 puan mAP50-95); squat ve çatlakta belirgin iyi, dökülme ve head check'te daha kötü. Ürün yolu için Apache lisanslı mimari olması avantaj.
- **Faz 1 yüzey sınıflarının hiçbiri kabul kriterini (recall ≥ 0,70) geçmiyor.** Açık verideki tavan ~0,55–0,60 mAP50 görünüyor.

## Sonraki denemeler (öncelik sırasıyla)
1. ~~Çözünürlük 1024~~ · ~~YOLO11m~~ · ~~sınıf birleştirme~~ · ~~RT-DETR karşılaştırması~~ — yapıldı (#3–#6).
2. **Kaynak bazında değerlendirme:** test sonuçlarını kakashi / unal kaynaklarına ayır — alan farkı (kamera, çözünürlük) ne kadar etkili?
3. **PatchCore** anomali katmanı (3. aşama): sağlam ray görüntüleriyle (eğitimde 1.367 arka plan görüntüsü) eğit, kaçırılan kusurları yakalıyor mu?
4. **Saha verisi:** asıl sıçrama işletmecinin kendi görüntüleriyle olur; pilot sözleşmesinde veri paylaşımı ve etiketleme planı.
