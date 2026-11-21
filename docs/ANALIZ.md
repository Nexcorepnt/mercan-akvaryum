# Mercan Akvaryum — Rakip Analizi ve v5 Tasarım Kararları

_Kasım 2026 · Google Play çıkışı öncesi_

## 1. İncelenen oyunlar

| Oyun | Tür | Çekirdek döngü | Para birimleri | Öne çıkan fikir |
|---|---|---|---|---|
| **FishVille** (Zynga, 2009–2012) | Gerçek zamanlı akvaryum | Yumurta al → besle → büyüt → sat | Sand Coins (oyunla) + Sand Dollars (seviye/ödeme) | 3 büyüme evresi, 15 balıklık başlangıç tankı, 350 altın + 5 premium ile başlangıç; seviye atlayınca premium para |
| **Fishdom** (Playrix) | Match-3 + dekorasyon | Bölüm oyna → altın → balık/süs al → tank yıldızı | Altın + elmas | Tank "3 yıldız" hedefi; balıklar günlük besleyince altın verir; temizlikten düşen altın/elmas |
| **Tap Tap Fish AbyssRium** | Idle / clicker | Dokun → canlılık → balık/mercan aç → seviyelendir | Canlılık (tek ana kaynak) | Her balık ve mercan pasif kaynak üretir; seviye atladıkça üretim artar; rahatlatıcı müzik |
| **Fish Tycoon 2** | Üretim / ticaret | Üret → sat → mağazayı/tankı geliştir | Para + premium | 400+ tür; önce yaygın türleri satıp tankı geliştirme tavsiyesi |
| **Chillquarium** (2024–2026) | Cozy idle | Paket aç → büyüt → **sat ya da sergile** | Para + premium (mobil) | Satmak veya tutup bilet geliri almak arasında seçim; nadir ve ultra nadir renk varyantları; 156+ tür koleksiyonu |
| **Fish Paradise** | Dekorasyon + sosyal | Balık yetiştir, "serbest bırak" ile altın | Altın + premium | Yüzlerce mercan/yapı; hediyeleşme |

## 2. Ortak kalıplar

1. **İki katmanlı ekonomi.** Neredeyse hepsinde oyunla kazanılan yumuşak para (altın) ve az bulunan premium para (elmas/inci/sand dollar) var. Premium para seviye atlama, başarım ve günlük ödüllerden de damla damla gelir.
2. **Pasif gelir.** Fishdom ve AbyssRium'da balıklar zamanla kaynak üretir; Chillquarium bunu "sat ya da sergile" kararına çevirir. Bu, oyuncuya her balıkta küçük bir strateji verir.
3. **Tank değeri / yıldızı.** Fishdom'un 3 yıldızlı tankı, süs almaya somut bir hedef verir.
4. **Koleksiyon ve nadirlik.** Chillquarium'un altın/gökkuşağı varyantları ve garanti eşiği oyuncuyu geri getirir. Mercan Akvaryum'da bu zaten var (13 nadir varyant).
5. **Zaman atlama.** Premium para çoğunlukla "beklemeyi atla" için harcanır.
6. **Rahatlatıcı sunum.** Yumuşak müzik, sakin renkler, ceza yok (çevrimdışıyken ölüm yok).

## 3. Mercan Akvaryum'un durumu (v4)

- ✅ Güçlü: Blender'la işlenmiş 2.5D grafikler, nadir varyantlar, koleksiyon, görevler, başarımlar, temalar.
- ⚠️ Zayıf: Tek para birimi (altın) → premium satın alma ya da ödüllü reklam için yer yok.
- ⚠️ Büyüme süreleri test için çok kısa (1–10 dk) → mobilde içerik çok hızlı tükenir.
- ⚠️ Süslerin oyuna etkisi yok, sadece görsel.
- ⚠️ Arayüz emoji tabanlı → Android cihazlarda emoji görünümü değişir, profesyonel durmaz.

## 4. v5 kararları

### Ekonomi
| Sistem | Karar |
|---|---|
| **İnci (💎 premium)** | Başlangıç 5 inci. Kaynak: seviye atlama (+2/+3), başarım rozetleri (2/5/15), günlük girişin 7. günü (+5), tank yıldızları, 3. günlük görev (+1). İleride Google Play satın alma / ödüllü reklam buraya bağlanabilir. |
| **İnci harcama** | Anında büyütme (kalan 10 dk başına 1 inci), Nadir Yumurta (8 inci, garanti nadir), Otomatik Yemlik (24 saat, 6 inci), özel inci süsleri. |
| **Sergi geliri** | Olgun balıklar dakikada altın biriktirir (satış değerinin ~%0,6'sı/dk, güzellik çarpanıyla). Balığın üstünde para kesesi belirir; dokununca ya da **Topla** ile toplanır. Çevrimdışı gelir en fazla 8 saat birikir. |
| **Güzellik puanı** | Her süs ve tema güzellik puanı verir. Gelir çarpanı: 1 + puan/400 (en fazla ×2,5). 50 / 150 / 400 puanda tank yıldızı ve inci ödülü. |
| **Büyüme süreleri** | 3 dk (Neon) → 180 dk (Köpekbalığı). Açlık süresi türe göre uzar (en az 10 dk, büyümenin yarısı), böylece uzun süreli balıklarda sürekli besleme gerekmez. |
| **Satış/XP** | Satış ≈ maliyet × 1,6 + dakika × 3; XP ≈ 4 + dakika × 0,9 (uzun süreli balık hep daha kârlı). |
| **Topla menüsü** | "Gelirleri topla" ve "Olgunları sat" iki ayrı seçenek (yanlışlıkla satışı önler). |

### Arayüz
- Emoji yerine özel **SVG ikon seti** (altın, inci, yıldız, balık, yem, sünger, kese, çanta, defter, ayar…).
- Koyu **"derin deniz camı"** teması: yarı saydam lacivert paneller, turkuaz vurgu, altın para çipleri, yuvarlak **Fredoka** yazı tipi.
- Üst bar: seviye rozeti + dairesel XP halkası, altın / inci çipleri, güzellik yıldızları, defter ve ayarlar.
- Ses, müzik, kayıt, yardım ve yeni oyun tek bir **Ayarlar** penceresinde.
- Alt menü: yüzen cam kapsül, seçili araç parlar.
- Mağaza kartlarında nadirlik renk kenarı (yaygın → efsanevi) ve fiyat çipi.
- **Açılış ekranı**: logo + "Dokun ve başla" (aynı zamanda telefonda sesi açar).

### Grafik
- Kumda hareketli ışık ağı (caustics), arka planda bulanık derinlik katmanı, ön planda bokeh partiküller.
- Blender'da 3D logo; Google Play için 512×512 uygulama ikonu ve 1024×500 tanıtım görseli (`store/`).

## Kaynaklar
- FishVille: https://en.wikipedia.org/wiki/FishVille · https://www.gamezebo.com/walkthroughs/fishville-walkthrough/ · https://adamnash.blog/2009/12/24/fishville-economics-points-experience-levels-part-3/
- Fishdom: https://Www.wikipedia.org/wiki/Fishdom · https://apps.apple.com/us/app/fishdom/id664575829
- AbyssRium: https://reefbuilders.com/2016/12/12/we-played-abyssarium-for-two-weeks-heres-what-happened/ · https://thewhitepube.co.uk/games/tap-tap-fish
- Fish Tycoon 2: https://apps.apple.com/us/app/-/id1194725957
- Chillquarium: https://sourceforge.net/app/chillquarium/ · https://www.pocketgamer.com/chillquarium/announcement/ · https://gamepur.com/?p=598634
- Ekonomi tasarımı: https://unity.com/resources/game-economy-design-guide
- Google Play görselleri: https://support.google.com/googleplay/android-developer/answer/9866151 · https://developer.android.com/google-play/resources/icon-design-specifications
