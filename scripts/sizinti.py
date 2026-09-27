"""Eğitim ile test/doğrulama arasında neredeyse aynı görüntü sızıntısını dHash ile arar."""
import sys
from pathlib import Path

import numpy as np
from PIL import Image

KOK = Path(__file__).resolve().parents[1] / "data" / "processed"


def dhash(p: Path, n: int = 16) -> np.ndarray:
    g = np.asarray(Image.open(p).convert("L").resize((n + 1, n)), dtype=np.int16)
    return (g[:, 1:] > g[:, :-1]).flatten()


def main(gorev: str, esik: int = 10):
    kok = KOK / gorev
    resimler = (lambda b: sorted((kok / "images" / b).glob("*"))) if (kok / "images").exists() \
        else (lambda b: sorted((kok / b).rglob("*.*")))
    tr = resimler("train")
    H = np.stack([dhash(p) for p in tr])
    for b in ("val", "test"):
        ogeler = resimler(b)
        sizan = 0
        for p in ogeler:
            d = (H != dhash(p)).sum(1)
            if d.min() <= esik:
                sizan += 1
        print(f"{gorev}/{b}: {sizan}/{len(ogeler)} görüntünün eğitimde neredeyse aynısı var (dHash mesafe <= {esik}/256)")


if __name__ == "__main__":
    for g in sys.argv[1:]:
        main(g)
