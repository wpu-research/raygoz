"""data/raw -> data/processed/{yuzey,bilesen,siniflandirma}.

- Poligon etiketleri kutuya çevrilir, sınıflar configs/siniflar.yaml'a göre eşlenir.
- Roboflow artırılmış kopyaları kaynak adına göre gruplanır ("<ad>_jpg.rf.<hash>").
  Gruplar 80/10/10 yeniden bölünür; doğrulama ve testte her gruptan yalnız bir kopya kalır.
- Sınıf dağılımı docs/veri-raporu.md'ye yazılır.
"""
import random
import re
import shutil
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
import yaml
from PIL import Image

KOK = Path(__file__).resolve().parents[1]
HAM, CIKTI = KOK / "data" / "raw", KOK / "data" / "processed"
SEMA = yaml.safe_load(open(KOK / "configs" / "siniflar.yaml", encoding="utf-8"))
TOHUM = 42
BENZERLIK_ESIK = 10  # dHash bit farkı (256 üzerinden); altı = aynı sahne
ORAN = (0.8, 0.1, 0.1)
IMG = (".jpg", ".jpeg", ".png")


def kaynak_adi(dosya: str, set_adi: str) -> str:
    m = re.match(r"(.+?)_(jpg|jpeg|png)\.rf\.[0-9a-f]+", dosya, re.I)
    return f"{set_adi}:{m.group(1) if m else Path(dosya).stem}"


def satir_kutu(satir: str):
    p = satir.split()
    if len(p) < 5:
        return None
    s, v = int(p[0]), list(map(float, p[1:]))
    if len(v) == 4:
        return s, v
    xs, ys = v[0::2], v[1::2]
    x0, x1, y0, y1 = max(min(xs), 0), min(max(xs), 1), max(min(ys), 0), min(max(ys), 1)
    if x1 <= x0 or y1 <= y0:
        return None
    return s, [(x0 + x1) / 2, (y0 + y1) / 2, x1 - x0, y1 - y0]


def dhash(p: Path, n: int = 16) -> np.ndarray:
    g = np.asarray(Image.open(p).convert("L").resize((n + 1, n)), dtype=np.int16)
    return (g[:, 1:] > g[:, :-1]).flatten()


def kumele(gruplar: dict) -> dict:
    """Neredeyse aynı görüntüleri (ardışık video kareleri) aynı kümeye toplar (union-find)."""
    anahtarlar = sorted(gruplar)
    H = np.stack([dhash(gruplar[k][0][0]) for k in anahtarlar])
    ata = list(range(len(anahtarlar)))

    def bul(i):
        while ata[i] != i:
            ata[i] = ata[ata[i]]
            i = ata[i]
        return i

    for i in range(len(anahtarlar)):
        yakin = np.nonzero((H[i + 1:] != H[i]).sum(1) <= BENZERLIK_ESIK)[0] + i + 1
        for j in yakin:
            ata[bul(int(j))] = bul(i)
    return {k: anahtarlar[bul(i)] for i, k in enumerate(anahtarlar)}


def bol(gruplar: dict) -> dict:
    kume = kumele(gruplar)
    kumeler = sorted(set(kume.values()))
    random.Random(TOHUM).shuffle(kumeler)
    n = len(kumeler)
    a, b = int(n * ORAN[0]), int(n * (ORAN[0] + ORAN[1]))
    atama = {c: ("train" if i < a else "val" if i < b else "test") for i, c in enumerate(kumeler)}
    bol.son_kume_sayisi = n
    return {k: atama[kume[k]] for k in gruplar}


def tespit(gorev: str) -> dict:
    siniflar = list(SEMA[gorev]["siniflar"])
    idx = {s: i for i, s in enumerate(siniflar)}
    hedef = CIKTI / gorev
    shutil.rmtree(hedef, ignore_errors=True)
    gruplar = defaultdict(list)
    for set_adi, esleme in SEMA[gorev]["eslemeler"].items():
        ad_listesi = yaml.safe_load(open(HAM / set_adi / "data.yaml"))["names"]
        for bolum in ("train", "valid", "test"):
            for g in sorted((HAM / set_adi / bolum / "images").iterdir()):
                if g.suffix.lower() not in IMG:
                    continue
                etiket = HAM / set_adi / bolum / "labels" / (g.stem + ".txt")
                kutular = []
                if etiket.exists():
                    for satir in etiket.read_text().splitlines():
                        k = satir_kutu(satir)
                        if not k:
                            continue
                        yeni = esleme.get(ad_listesi[k[0]])
                        if yeni:
                            kutular.append((idx[yeni], k[1]))
                gruplar[kaynak_adi(g.name, set_adi)].append((g, kutular))
    bolumler = bol(gruplar)
    sayim = {b: Counter() for b in ("train", "val", "test")}
    goruntu = Counter()
    for grup, ogeler in gruplar.items():
        b = bolumler[grup]
        if b != "train":
            ogeler = ogeler[:1]
        for g, kutular in ogeler:
            (hedef / "images" / b).mkdir(parents=True, exist_ok=True)
            (hedef / "labels" / b).mkdir(parents=True, exist_ok=True)
            ad = f"{grup.replace(':', '__')}__{g.stem[-8:]}{g.suffix.lower()}"
            shutil.copy2(g, hedef / "images" / b / ad)
            (hedef / "labels" / b / (Path(ad).stem + ".txt")).write_text(
                "".join(f"{s} {' '.join(f'{v:.6f}' for v in k)}\n" for s, k in kutular))
            goruntu[b] += 1
            for s, _ in kutular:
                sayim[b][siniflar[s]] += 1
    (hedef / "data.yaml").write_text(yaml.safe_dump(
        {"path": str(hedef), "train": "images/train", "val": "images/val", "test": "images/test",
         "names": dict(enumerate(siniflar))}, allow_unicode=True, sort_keys=False))
    return {"siniflar": siniflar, "sayim": sayim, "goruntu": goruntu, "grup": len(gruplar), "kume": bol.son_kume_sayisi}


def siniflandirma() -> dict:
    hedef = CIKTI / "siniflandirma"
    shutil.rmtree(hedef, ignore_errors=True)
    gruplar = defaultdict(list)
    for set_adi, esleme in SEMA["siniflandirma"]["eslemeler"].items():
        for bolum in ("train", "valid", "test"):
            for klasor in sorted((HAM / set_adi / bolum).iterdir()):
                yeni = esleme.get(klasor.name)
                if not (klasor.is_dir() and yeni):
                    continue
                for g in sorted(klasor.iterdir()):
                    if g.suffix.lower() in IMG:
                        gruplar[kaynak_adi(g.name, set_adi)].append((g, yeni))
    bolumler = bol(gruplar)
    sayim = {b: Counter() for b in ("train", "val", "test")}
    for grup, ogeler in gruplar.items():
        b = bolumler[grup]
        if b != "train":
            ogeler = ogeler[:1]
        for g, sinif in ogeler:
            d = hedef / b / sinif
            d.mkdir(parents=True, exist_ok=True)
            shutil.copy2(g, d / f"{grup.replace(':', '__')}__{g.stem[-8:]}{g.suffix.lower()}")
            sayim[b][sinif] += 1
    return {"sayim": sayim, "grup": len(gruplar), "kume": bol.son_kume_sayisi}


def tablo(sayim, siniflar):
    s = "| Sınıf | Eğitim | Doğrulama | Test |\n|---|---|---|---|\n"
    for c in siniflar:
        s += f"| {c} | {sayim['train'][c]} | {sayim['val'][c]} | {sayim['test'][c]} |\n"
    return s


def main():
    r = {g: tespit(g) for g in ("yuzey", "bilesen")}
    c = siniflandirma()
    md = ["# Veri raporu", "", "_scripts/hazirla.py çıktısı. Tohum 42. Artırılmış kopyalar kaynak adına göre gruplanır, neredeyse aynı görüntüler (dHash ≤ 10/256) aynı kümeye toplanır; bölme kümelere göre 80/10/10. Doğrulama ve testte her kaynaktan tek kopya._", ""]
    for g, v in r.items():
        md += [f"## {g} (tespit)", "",
               f"Kaynak görüntü grubu: {v['grup']} · benzerlik kümesi: {v['kume']} · görüntü: eğitim {v['goruntu']['train']}, doğrulama {v['goruntu']['val']}, test {v['goruntu']['test']}", "",
               "Kutu (örnek) sayıları:", "", tablo(v["sayim"], v["siniflar"])]
    cl = sorted(set().union(*[set(x) for x in c["sayim"].values()]))
    md += ["## siniflandirma (görüntü düzeyi)", "", f"Kaynak görüntü grubu: {c['grup']} · benzerlik kümesi: {c['kume']}", "", tablo(c["sayim"], cl)]
    (KOK / "docs").mkdir(exist_ok=True)
    (KOK / "docs" / "veri-raporu.md").write_text("\n".join(md), encoding="utf-8")
    print("\n".join(md))


if __name__ == "__main__":
    main()
