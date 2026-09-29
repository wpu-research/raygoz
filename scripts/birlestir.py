"""data/processed/yuzey -> data/processed/yuzey_birlesik.

squat, dokulme, pullanma tek 'yuzey_hasari' sınıfında birleşir; diğerleri aynen kalır.
Bölme birebir aynıdır (aynı dosyalar), sonuçlar deney 2 ile doğrudan karşılaştırılabilir.
"""
import shutil
from pathlib import Path

import yaml

KOK = Path(__file__).resolve().parents[1] / "data" / "processed"
BIRLES = {"squat", "dokulme", "pullanma"}


def main():
    kaynak, hedef = KOK / "yuzey", KOK / "yuzey_birlesik"
    eski = yaml.safe_load(open(kaynak / "data.yaml", encoding="utf-8"))["names"]
    eski = [eski[i] for i in sorted(eski)]
    yeni = ["yuzey_hasari"] + [c for c in eski if c not in BIRLES]
    esle = {i: (0 if c in BIRLES else yeni.index(c)) for i, c in enumerate(eski)}
    shutil.rmtree(hedef, ignore_errors=True)
    for b in ("train", "val", "test"):
        (hedef / "labels" / b).mkdir(parents=True)
        (hedef / "images").mkdir(exist_ok=True)
        (hedef / "images" / b).symlink_to((kaynak / "images" / b).resolve(), target_is_directory=True)
        for f in (kaynak / "labels" / b).glob("*.txt"):
            satirlar = [f"{esle[int(s.split()[0])]} {' '.join(s.split()[1:])}" for s in f.read_text().splitlines() if s.strip()]
            (hedef / "labels" / b / f.name).write_text("".join(x + "\n" for x in satirlar))
    (hedef / "data.yaml").write_text(yaml.safe_dump(
        {"path": str(hedef), "train": "images/train", "val": "images/val", "test": "images/test",
         "names": dict(enumerate(yeni))}, allow_unicode=True, sort_keys=False), encoding="utf-8")
    print("sınıflar:", yeni)


if __name__ == "__main__":
    main()
