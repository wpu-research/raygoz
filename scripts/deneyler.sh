#!/bin/bash
cd ~/raygoz && export PATH=$HOME/.local/bin:$PATH
E="uv run python scripts/egit.py"
$E yuzey yolo11s.pt --epochs 120 --imgsz 1024 --batch 8 > runs/d3.log 2>&1
$E yuzey yolo11m.pt --epochs 120 > runs/d4.log 2>&1
$E yuzey_birlesik yolo11s.pt --epochs 120 > runs/d5.log 2>&1
$E yuzey rtdetr-l.pt --epochs 120 --batch 8 > runs/d6.log 2>&1
echo BITTI > runs/deneyler.done
