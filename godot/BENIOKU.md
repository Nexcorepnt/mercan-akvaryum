# Mercan Akvaryum 3D (Godot denemesi)

Mercan Akvaryum'un gerçek 3D sürümü için ilk deneme. Godot 4.7.2 ile yapıldı.

## Nasıl açılır (Windows)
1. https://godotengine.org/download/windows/ adresinden **Godot 4.7.2**'yi indir (standart sürüm, .NET değil). Kurulum gerekmez, zip'i açıp exe'yi çalıştır.
2. Godot açılınca **İçe Aktar** düğmesine bas, bu klasördeki `project.godot` dosyasını seç.
3. Proje açılınca sağ üstteki **▶ (Oynat)** düğmesine bas veya F5.
4. Editörü Türkçe yapmak için: Editör > Editör Ayarları > Arayüz > Editör > Dil: Türkçe.

## Kontroller
- Fareyle sürükle: kamerayı döndür
- Fare tekerleği: yakınlaş / uzaklaş
- Telefonda: tek parmakla döndür, iki parmakla yakınlaş

## İçerik
- `assets/models/`: Blender'dan aktarılan 3D balık ve süs modelleri (.glb)
- `assets/tex/sand_albedo.webp`: kum dokusu (Blender'da ~yarım milyon taneden)
- `shaders/`: balık yüzme dalgası, su ışığı (kostik), kum dalgaları, bitki dalgalanması
- `scripts/`: sahne kurulumu, balık davranışı, kamera
