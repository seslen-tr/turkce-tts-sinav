# Değişiklikler

## Yayımlanmamış

- `normalizasyon.tsv`'ye isteğe bağlı dördüncü sütun: kaynak. Boşsa `turkce-normalize-testleri`; eski üç sütunlu
  satırlar olduğu gibi çalışır. Sonuç toplamın yanında kaynağa göre de verilir (`kaynaklar`).
- Beklenen sütununda birden çok doğru okunuş (`" | "` ile); en yakını sayılır. Mevcut veride değişiklik yok.
- `normalizasyon_sinavi(..., gevsek=True)`: büyük-küçük harf, noktalama ve kesme yok sayılır ("Beş'te." = "beşte").
- Bağımsız ikinci kaynak `bagimsiz-dorukdumlu`: 67 banka ve sigorta cümlesi
  ([tr-tts-norm-bench](https://github.com/dorukdumlu/tr-tts-norm-bench), MIT), birden çok doğru okunuşla
  (145 → 212 örnek). turkce-normalize 0.1.11 bu kaynakta 54/67, gevşek 60/67.

## 0.1.2 — metin hazırlama verisi güncel

- 20 beklenen okunuş turkce-normalize 0.1.4–0.1.7'nin bilinçli değişikliklerine göre güncellendi: harf harf okunan
  kısaltma bitişik ("te be me me" → "tebememe"; ses modeli ayrık harf adlarında ünlüleri yutuyordu), alan adı
  uzantısı "com" → "kom", "te re" → "tere", adresteki tek harf adıyla ("b tire c" → "be tire ce"), Roma rakamı
  okunur ("Henry VIII" → "Henry sekizinci"), sözcük içi tire okunmaz ("Ar-Ge" → "Ar Ge").
- Yeni grup "Yeni" (17 örnek): g / mg / ml, `.io`, "saat"siz noktalı saat (`06.45'te`, `10.00'a`), baştaki sıfır
  (`TR-042`), "dört" yumuşaması (`4'e`, `%14'ü`, `1.004'ü`), ekli Roma rakamı (`Bölüm III'te`, `Tip II`), para / yüzde
  / sıra / ondalık eki (`5 TL'ye`, `%5'i`, `3'üncü`, `3,5'e`), saat aralığı (`09:00-17:00`). 128 → 145 örnek.

## 0.1.1 — belgeler

- README ve CHANGELOG koda göre güncellendi (kurulum, kullanım, API, düzen); kod davranışı değişmedi.

## 0.1.0 — ilk açık sürüm

- İlk yayın (PyPI: `turkce-tts-sinav`). Ayrıntılar ve sonuçlar README'de.
- Veri: 174 kaynaklı literatür vurgu örneği, 9.030 Vikisözlük vurgu kaydı (1.234 kesin, 7.796 yumuşak),
  11.108 Vikisözlük IPA okunuşu, 128 metin hazırlama örneği.
- Değerlendiriciler: `vurgu_sinavi`, `okunus_sinavi` (PER, incelik-duyarsız PER), `normalizasyon_sinavi` (WER).
- Komut satırı: `python -m turkce_tts_sinav [turkce-vurgu | turkce-normalize | son-hece | espeak]`.
