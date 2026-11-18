# RayGöz

Kaydedilmiş hat görüntülerinden **ray yüzey kusurlarını** (ezilme, dökülme, pullanma, çatlak vb.) ve **hat bileşeni kusurlarını** (eksik klips/tirfon, kusurlu ray eki) tespit edip işaretleyen ve raporlayan yazılım. Hedef: demiryolu/metro işletmecisine pilot. İç çatlaklar (ultrasonik/girdap akımı) kapsam dışıdır.

## Durum
Araştırma ve ilk deneyler tamamlandı: açık veri setleri indirildi, ortak sınıf şemasına eşlendi, YOLO11 / RT-DETR temel çizgileri eğitildi (sonuçlar `docs/deneyler.md`). Web arayüzü ve PDF/CSV rapor henüz yok; MVP planı `BRIEF.md` içinde.

## İçerik
- `BRIEF.md`: amaç, kapsam, kararlar, MVP ve kabul kriterleri. `CLAUDE.md`: proje kuralları.
- `arastirma/`: veri seti, literatür ve pazar araştırması.
- `configs/siniflar.yaml`: kaynak set sınıflarını RayGöz sınıflarına (UIC 712 kodlarıyla) eşleyen şema.
- `scripts/`: `indir.py` (Roboflow'dan veri), `hazirla.py` / `birlestir.py` (bölme, tekilleştirme), `egit.py` (eğitim), `sizinti.py`, `deneyler.sh`.
- `docs/`: `deneyler.md`, `veri-raporu.md`. `data/README.md`: veri setleri, lisanslar, ürüne girip girmeyeceği.

## Teknoloji
Python >= 3.12, `uv`; roboflow, numpy, pillow, pyyaml, python-dotenv; eğitim grubunda ultralytics (YOLO11, RT-DETR).

## Kurulum / çalıştırma
```bash
uv sync --group egitim
uv run python scripts/indir.py
uv run python scripts/hazirla.py
uv run python scripts/egit.py bilesen yolo11s.pt --epochs 100
```
Veri dosyaları ve `runs/` git dışıdır.

## Ortam değişkenleri
`ROBOFLOW_API_KEY` (`.env` içinde, değer paylaşılmaz).

## Lisans
Proje lisansı belirtilmemiş. Veri setleri çoğunlukla CC BY 4.0 (atıf zorunlu); Ultralytics AGPL-3.0 olduğundan ürün için ticari lisans/alternatif gerekir (`data/README.md`, `BRIEF.md`).
