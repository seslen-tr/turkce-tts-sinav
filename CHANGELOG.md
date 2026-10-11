# Değişiklikler

## 0.1.1 — belgeler

- README ve CHANGELOG koda göre güncellendi (kurulum, kullanım, API, düzen); kod davranışı değişmedi.

## 0.1.0 — ilk açık sürüm

- İlk yayın (PyPI: `turkce-tts-sinav`). Ayrıntılar ve sonuçlar README'de.
- Veri: 174 kaynaklı literatür vurgu örneği, 9.030 Vikisözlük vurgu kaydı (1.234 kesin, 7.796 yumuşak),
  11.108 Vikisözlük IPA okunuşu, 128 metin hazırlama örneği.
- Değerlendiriciler: `vurgu_sinavi`, `okunus_sinavi` (PER, incelik-duyarsız PER), `normalizasyon_sinavi` (WER).
- Komut satırı: `python -m turkce_tts_sinav [turkce-vurgu | turkce-normalize | son-hece | espeak]`.
