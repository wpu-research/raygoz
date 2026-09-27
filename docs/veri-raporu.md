# Veri raporu

_scripts/hazirla.py çıktısı. Tohum 42. Artırılmış kopyalar kaynak adına göre gruplanır, neredeyse aynı görüntüler (dHash ≤ 10/256) aynı kümeye toplanır; bölme kümelere göre 80/10/10. Doğrulama ve testte her kaynaktan tek kopya._

## yuzey (tespit)

Kaynak görüntü grubu: 1137 · benzerlik kümesi: 1118 · görüntü: eğitim 3793, doğrulama 112, test 113

Kutu (örnek) sayıları:

| Sınıf | Eğitim | Doğrulama | Test |
|---|---|---|---|
| squat | 209 | 10 | 15 |
| dokulme | 937 | 44 | 64 |
| pullanma | 201 | 10 | 7 |
| catlak | 409 | 13 | 14 |
| head_check | 785 | 49 | 35 |
| kirik | 371 | 9 | 7 |
| iz | 1155 | 20 | 16 |

## bilesen (tespit)

Kaynak görüntü grubu: 2420 · benzerlik kümesi: 2144 · görüntü: eğitim 2056, doğrulama 234, test 247

Kutu (örnek) sayıları:

| Sınıf | Eğitim | Doğrulama | Test |
|---|---|---|---|
| baglanti_eksik | 710 | 80 | 100 |
| tirfon_eksik | 79 | 8 | 4 |
| ek_kusurlu | 282 | 50 | 37 |
| baglanti_saglam | 1446 | 138 | 172 |
| ek_saglam | 398 | 39 | 44 |

## siniflandirma (görüntü düzeyi)

Kaynak görüntü grubu: 502 · benzerlik kümesi: 502

| Sınıf | Eğitim | Doğrulama | Test |
|---|---|---|---|
| catlak | 871 | 22 | 20 |
| dokulme | 1514 | 11 | 14 |
| kirik | 65 | 1 | 3 |
| korugasyon | 19 | 1 | 0 |
| pullanma | 749 | 8 | 8 |
| squat | 675 | 7 | 6 |

## Sızıntı kontrolü (scripts/sizinti.py)
Benzerlik kümelemesinden sonra, eğitimde neredeyse aynısı (dHash ≤ 10/256) bulunan görüntü oranı:

| Görev | Doğrulama | Test | Kümeleme öncesi test |
|---|---|---|---|
| yuzey | 3/112 | 3/113 (%2,7) | 11/114 (%9,6) |
| bilesen | 0/234 | 2/247 (%0,8) | 47/242 (%19,4) |
| siniflandirma | 0/50 | 0/51 | 0/51 |

Kalan birkaç eşleşme, çevrilmiş (flip) artırılmış kopyaların başka bir kaynağa benzemesinden. Kabul edildi.

## Uyarılar
- **Yüzey testi küçük** (113 görüntü): squat 15, pullanma 7, kırık 7 örnek → sınıf bazında metrikler gürültülü; güven aralığıyla raporlanmalı.
- **tirfon_eksik** testte 4 örnek → bu sınıf için test metriği anlamlı değil.
- **Sınıflandırma seti:** 4.939 görüntünün 502'si kaynak, gerisi artırılmış. **Korugasyon** toplam 20 örnek → faz 1'den çıkarıldı, saha verisi gerekiyor.
- Görüntüler Roboflow'da 640×640'a gerilmiş ve kontrast eşitlenmiş (kakashi). Saha görüntüsünde aynı ön işleme uygulanmalı ya da model bu varsayıma bağımlı kalmamalı.
