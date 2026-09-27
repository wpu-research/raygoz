# RayGöz — Proje brifi

_27 Eylül 2026 · Tezgâh prompt'undan üretildi, kullanıcı kararlarıyla güncellendi._

## Amaç
Tren ve metro hatlarında **kaydedilmiş** görüntü ve videolardan ray **yüzey kusurlarını** ve **hat bileşeni kusurlarını** otomatik tespit edip işaretleyen, raporlayan bir yazılım. Hedef: bir demiryolu/metro işletmecisine (öncelik Türkiye) pilot olarak sunulabilecek ürün.

## Kapsam düzeltmesi
Kamera yalnız yüzeyi görür. Ray başının **içindeki** enine çatlaklar (en tehlikeli kusurlar) ultrasonik ve girdap akımıyla bulunur; bu projenin kapsamı dışındadır. RayGöz'ün hedefi:
- **Ray yüzeyi:** yüzey çatlakları, ray başı yorulma çatlakları (head check), ezilme (squat), dökülme (spalling), dalgalanma (corrugation)
- **Hat bileşenleri:** eksik/kırık bağlantı elemanı (klips, cıvata), kırık/çatlak travers

Kusur sınıfları ve şiddet dereceleri, işletmecinin kullandığı katalogla (UIC 712 ve TCDD talimatları) eşleştirilecek — `arastirma/` sonucuna göre kesinleşir.

## Kullanıcı kararları (27.09.2026)
| Konu | Karar |
|---|---|
| Veri | Açık veri setleriyle başla; saha görüntüsü sonra |
| Hedef | Demiryolu işletmecisine ürün (pilot) |
| Platform | Kayıttan analiz, web arayüzü (canlı/edge yok) |
| Klasör | `~/Desktop/Urunler/RayGoz` |

Ürün hedefi nedeniyle: veri setlerinin **ticari kullanım lisansı** kontrol edilir; yalnız araştırma lisanslı setler ürün modelinde kullanılmaz (ön-eğitim/karşılaştırma için ayrı tutulur).

## MVP kapsamı
- Fotoğraf ve kısa video yükleme; videodan kare çıkarma
- Kusur tespiti (bbox ya da maske) + güven skoru
- İşaretli görsel çıktısı; kusur listesi (kare no, zaman, sınıf, skor)
- Rapor indirme: PDF ve CSV
- Web arayüzü: yükle → sonuç → indir

## Kapsam dışı (ilk sürüm)
Canlı/edge analiz · GPS ile otomatik hat haritalama · otomatik bakım önceliklendirme · donanım tasarımı · çoklu kamera · 3B · iç çatlaklar.

## Önerilen teknik yığın
- **Model:** Python + PyTorch. Temel çizgi: Ultralytics YOLO (tespit) ve bir segmentasyon modeli (U-Net / SegFormer). Az kusur örneği olan sınıflar için anomali tespiti (PatchCore vb.) değerlendirilir.
- **Backend:** FastAPI · **Arayüz:** ilk sürüm Streamlit ya da basit bir web sayfası · **Depolama:** yerel dosya + SQLite
- **Ortam:** `uv`, RTX 4070 (8 GB) ile yerel eğitim
- Lisans: kullanılan her model ağırlığının ve kütüphanenin ticari lisansı kontrol edilir (Ultralytics AGPL-3.0 — ürün için ticari lisans ya da alternatif gerekir).

## Kabul kriterleri (MVP)
Kesin değerler veri seti seçilince netleşir:
1. Seçilen test setinde hedef sınıflar için tespit geri çağırımı (recall) ≥ %70 ve yanlış alarm oranı ≤ %30 (başlangıç eşiği; işletmecinin "km başına yanlış alarm" beklentisine göre revize edilir).
2. 1 dakikalık 1080p video GPU'suz makinede ≤ 5 dk, GPU'lu makinede ≤ 1 dk içinde işlenir.
3. Arayüzden yükle → işaretli sonuç → PDF/CSV indir akışı uçtan uca çalışır.
4. Her tespit, kaynak kare ve zaman damgasına geri izlenebilir.

## İlk görevler (sıralı)
1. Araştırma: açık veri setleri + lisanslar, kusur kataloğu, rakipler, işletmeci beklentileri (`arastirma/`).
2. Veri setlerini indir, sınıfları ortak bir şemaya eşle, eğitim/doğrulama/test ayır.
3. Temel çizgi model: YOLO tespit + metrikler (mAP, sınıf bazında recall/precision).
4. Video işleme hattı: kare çıkarma, çift tespit birleştirme.
5. FastAPI + arayüz + PDF/CSV rapor.
6. Kabul kriterleri testi, sonuç raporu.
7. Pilot paketi: işletmeciye gidecek tek sayfa + demo.

## Başlamadan önce açık sorular
- İşletmeci hedefi: TCDD mi, bir metro işletmesi mi (hat tipi, hız, araç)?
- Saha görüntüsü ileride kimden, hangi kamerayla gelecek?
- Rapor hangi bakım sistemine aktarılacak (Excel, SAP PM, iç sistem)?

## Çalışma kuralları
Önce plan sun, onay bekle · küçük commit'ler · her adımda test ve metrik · gizli anahtarları koda yazma · veri setlerini ve model ağırlıklarını git'e koyma (`data/`, `models/`).
