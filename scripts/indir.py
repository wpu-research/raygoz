"""Açık veri setlerini data/raw/ altına indirir. Anahtar: .env içindeki ROBOFLOW_API_KEY."""
import os
from pathlib import Path

from dotenv import load_dotenv
from roboflow import Roboflow

KOK = Path(__file__).resolve().parents[1]
HAM = KOK / "data" / "raw"

# (klasör adı, workspace, proje, sürüm, dışa aktarım biçimi)
SETLER = [
    ("fastener", "railway-defects-osolv", "fastener-detection-7a3vn", 1, "yolov8"),
    ("kakashi", "kakashi-fmrs2", "rail-surface-defects-d9i8o", 7, "yolov8"),
    ("unal", "raildefectunal", "rail-defects-detection", 2, "yolov8"),
    ("rail_defect_cls", "defect-rexb3", "rail-defect", 2, "folder"),
]


def main():
    load_dotenv(KOK / ".env")
    rf = Roboflow(api_key=os.environ["ROBOFLOW_API_KEY"])
    HAM.mkdir(parents=True, exist_ok=True)
    for ad, ws, proje, surum, bicim in SETLER:
        hedef = HAM / ad
        if hedef.exists() and any(hedef.iterdir()):
            print(f"atlandı (var): {ad}")
            continue
        print(f"indiriliyor: {ad} ({ws}/{proje} v{surum}, {bicim})")
        rf.workspace(ws).project(proje).version(surum).download(bicim, location=str(hedef))


if __name__ == "__main__":
    main()
