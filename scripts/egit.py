"""Tespit modeli eğitimi (temel çizgi). Kullanım: uv run python scripts/egit.py bilesen yolo11s.pt --epochs 100"""
import argparse
from pathlib import Path

import yaml
from ultralytics import RTDETR, YOLO

KOK = Path(__file__).resolve().parents[1]


def veri_yaml(gorev: str) -> str:
    """data.yaml'daki path'i bu makinenin yoluna göre yeniden yazar."""
    kaynak = KOK / "data/processed" / gorev / "data.yaml"
    y = yaml.safe_load(open(kaynak, encoding="utf-8"))
    y["path"] = str(kaynak.parent)
    hedef = kaynak.with_name("data.local.yaml")
    hedef.write_text(yaml.safe_dump(y, allow_unicode=True, sort_keys=False), encoding="utf-8")
    return str(hedef)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("gorev", choices=["yuzey", "bilesen", "yuzey_birlesik"])
    ap.add_argument("model", default="yolo11s.pt")
    ap.add_argument("--epochs", type=int, default=100)
    ap.add_argument("--imgsz", type=int, default=640)
    ap.add_argument("--batch", type=int, default=16)
    ap.add_argument("--patience", type=int, default=25)
    a = ap.parse_args()
    ad = f"{a.gorev}_{Path(a.model).stem}_{a.imgsz}"
    Sinif = RTDETR if "rtdetr" in a.model else YOLO
    m = Sinif(a.model)
    m.train(data=veri_yaml(a.gorev), epochs=a.epochs, imgsz=a.imgsz,
            batch=a.batch, patience=a.patience, project=str(KOK / "runs"), name=ad, exist_ok=True,
            seed=42, deterministic=True, workers=8, plots=True)
    # Kilitli test setinde değerlendirme
    en_iyi = Sinif(KOK / "runs" / ad / "weights" / "best.pt")
    r = en_iyi.val(data=veri_yaml(a.gorev), split="test",
                   project=str(KOK / "runs"), name=ad + "_test", exist_ok=True, plots=True)
    satirlar = [f"# {ad} — test", "", f"mAP@0.5: {r.box.map50:.3f} · mAP@0.5:0.95: {r.box.map:.3f}", "",
                "| Sınıf | Precision | Recall | mAP@0.5 |", "|---|---|---|---|"]
    for i, c in enumerate(r.box.ap_class_index):
        p, rc, ap50, _ = r.box.class_result(i)
        satirlar.append(f"| {r.names[int(c)]} | {p:.3f} | {rc:.3f} | {ap50:.3f} |")
    (KOK / "runs" / f"{ad}_test.md").write_text("\n".join(satirlar) + "\n", encoding="utf-8")
    print("\n".join(satirlar))


if __name__ == "__main__":
    main()
