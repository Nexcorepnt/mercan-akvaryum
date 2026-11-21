# 🐠 Mercan Akvaryum

FishVille tarzında, tarayıcıda çalışan 2.5D akvaryum oyunu. Balık yumurtası al, besle, büyüt, sat; akvaryumu temizle ve süsle.

**Oyna:** `index.html` dosyasını tarayıcıda aç (tek dosya, internet gerekmez).

## Klasörler

| Yol | İçerik |
|---|---|
| `index.html` | Oynanabilir oyun (derlenmiş, sprite'lar gömülü) |
| `src/index.template.html` | Oyunun kaynak kodu (HTML + CSS + JS). Düzenlemeler burada yapılır |
| `assets/sprites/` | Blender'da işlenmiş balık sprite sheet'leri (`*_sheet.webp`) ve konum bilgileri (`*_meta.json`) |
| `blender/fish.py` | Balıkları (ve nadir renk varyantlarını) prosedürel olarak modelleyip render eden Blender betiği |
| `blender/decor.py` | Süsleri 3D modelleyip render eden Blender betiği (`d_*` sprite'ları) |
| `tools/build.py` | Sprite'ları, yazı tipini ve logoyu şablona gömüp `index.html` üretir |
| `tools/store_assets.py` | Logo, Google Play ikonu (512) ve tanıtım görseli (1024×500) üretir |
| `blender/logo.py` | 3D logo ve mağaza görselleri için yüksek çözünürlüklü balık renderları |
| `store/` | Google Play görselleri: `icon-512.png`, `feature-1024x500.png`, `logo.png` |
| `docs/ANALIZ.md` | Rakip oyun analizi ve v5 tasarım kararları |

## Geliştirme

```bash
# 1) Kaynağı düzenle: src/index.template.html
# 2) Derle:
python3 tools/build.py
```

### Balıkları yeniden render etmek (Blender 5.0)

```bash
python3.11 -m venv bvenv && ./bvenv/bin/pip install bpy pillow
./bvenv/bin/python blender/fish.py all 12 300 40     # tür(ler) kare genişlik örnekleme
python3 tools/build.py
```

Tek tür için: `./bvenv/bin/python blender/fish.py koi,betta 12 300 40` · nadir varyant: `koi_r`

Süsler: `./bvenv/bin/python blender/decor.py all 48 200` (tür(ler) örnekleme piksel/birim)

## Özellikler

- **v5:** derin deniz camı arayüzü, SVG ikonlar, gömülü Fredoka yazı tipi, açılış ekranı, ayarlar penceresi
- **v5 ekonomi:** inci (premium), sergi geliri, güzellik puanı ve tank yıldızları, anında büyütme, nadir yumurta, otomatik yemlik
- **v5 çiftleşme:** aynı türden iki yetişkin eşleşir, flört eder, yumurta bırakır; eşleşmiş balıklar korunur
- 13 balık türü + 13 nadir renk varyantı (Blender ile 3D, 12 karelik yüzme animasyonu); deniz atı ve denizanasının kendine özgü hareketi
- Koleksiyon albümü (26 kart), günlük 3 görev, günlük giriş serisi, 9 başarım × 3 rozet
- 4 akvaryum teması (Okyanus, Tatlı Su, Mercan Resifi, Gece) ve akvaryum büyütme
- 21 süs (16'sı Blender'da 3D işlenmiş), seviye sistemi, XP ve altın ekonomisi
- Yosun temizleme, temizlik göstergesi ve ödülü
- Yatay ekran (telefonda otomatik döndürme)
- Kayıt: tarayıcı + Claude hesabı (yayınlanan sürümde) + yedek kod
