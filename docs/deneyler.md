# Deney kayıtları

Her deney: tarih · görev · model · veri sürümü (hazirla.py, tohum 42, benzerlik kümeli bölme) · ana metrikler · not · lisans durumu.
Metrikler **kilitli test setinde**. Eğitim makinesi: ofis (RTX 3080 Ti 12 GB, WSL2). Çıktılar: `runs/` (git dışı).

| # | Tarih | Görev | Model | Epoch (en iyi) | Süre | Test mAP@0.5 | mAP@0.5:0.95 | Lisans |
|---|---|---|---|---|---|---|---|---|
| 1 | 27.09.2026 | bilesen | YOLO11s, 640 | 83 (48) | 15 dk | **0,871** | 0,569 | AGPL — yalnız araştırma |
| 2 | 27.09.2026 | yuzey | YOLO11s, 640 | 93 (72) | 29 dk | **0,540** | 0,258 | AGPL — yalnız araştırma |

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

## Sonraki denemeler (öncelik sırasıyla)
1. **yuzey, daha yüksek çözünürlük:** imgsz 1024 (küçük kusurlar gerilmede kayboluyor olabilir).
2. **yuzey, daha büyük model:** YOLO11m.
3. **Sınıf birleştirme:** squat + dökülme + pullanma → tek "yüzey hasarı" sınıfı (işletmeci için önce "burada kusur var" demek, tipini ikinci aşamada sınıflandırıcıya bırakmak). Recall'ı ne kadar yükselttiğini ölç.
4. **RT-DETR (Apache) karşılaştırması** — ürün adayı lisans.
5. **PatchCore** anomali katmanı (3. aşama) — kaçırılan kusurları yakalar mı?
