# turkce-tts-sinav

> **English:** Open test data and evaluator for Turkish G2P, lexical stress and TTS text normalization: 174 stress examples from the linguistic literature, ~9,000 Wiktionary stress entries, ~11,000 Wiktionary IPA transcriptions and 128 normalization cases, with ready-made scorers.

Türkçe G2P, sözcük vurgusu ve ses sentezi ön uçlarını ölçmek için **açık sınav verisi ve
değerlendirici**. Türkçe için bugüne kadar böyle ortak bir ölçüt yoktu. Sistemler ya hiç
ölçülmüyor ya da herkes kendi örnekleriyle ölçüyordu.

```python
from turkce_tts_sinav import normalizasyon_sinavi, okunus_sinavi, vurgu_sinavi

vurgu_sinavi(lambda sozcuk, ozel_kok: benim_sistemim.vurgulu_hece(sozcuk))  # 0'dan hece sırası ya da None
okunus_sinavi(lambda sozcuk: benim_sistemim.ipa(sozcuk))                    # IPA dizisi
normalizasyon_sinavi(lambda metin: benim_sistemim.normalize(metin))         # okunuşa hazır metin
```

```
python -m turkce_tts_sinav turkce-vurgu turkce-normalize son-hece espeak
```

## Kurulum

```
pip install turkce-tts-sinav                      # bağımlılığı yok, Python 3.9+
pip install turkce-vurgu turkce-normalize         # hazır sistemleri komut satırından ölçmek için
```

Komut satırı sistem adı verilmezse `turkce-vurgu` ve `son-hece` (hep son hece, taban çizgisi) ölçülür.
`espeak` için `pip install phonemizer` ve sistemde espeak-ng gerekir.

## Değerlendiriciler

| İşlev | Sistemden beklenen | Döndürdüğü |
|---|---|---|
| `vurgu_sinavi(sistem)` | `sistem(sozcuk, ozel_kok)` → vurgulu hecenin 0'dan sırası, vurgusuz sözcükte `None` | `literatur` (türe göre doğru/toplam), `vikisozluk_kesin`, `vikisozluk_yumusak`, `yanlislar` |
| `okunus_sinavi(sistem)` | `sistem(sozcuk)` → IPA (vurgu işareti yok sayılır) | `tam`, `per`, `per_incelik_duyarsiz`, `sozcuk` |
| `normalizasyon_sinavi(sistem)` | `sistem(metin)` → okunuşa hazır metin | `tam`, `wer`, `ornek`, `yanlislar` |

Hepsi `yaz=False` ile sessiz çalışır. Hece, Türkçe yazım hecesidir (`heceler()`); IPA çıktısı veren
sistemler `ipa_vurgu_hecesi(ipa)` ile vurgu sınavına bağlanır. Vikisözlük'te özel ad olan sözcük
sisteme büyük harfle başlayarak, küçük harfli hâli de `ozel_kok` olarak verilir; literatür
örneklerinde `ozel_kok` kaynaktaki özel ad köküdür (yoksa boş).

## Veri

| Dosya | İçerik | Kaynak |
|---|---|---|
| `vurgu_literatur.tsv` | Dilbilim literatüründe vurgusu verilmiş 174 sözcük ve çekimli biçim, her biri kaynağıyla. Tür etiketi: ek/kök kuralı (90), Sezer kuralı (33), sözlüksel (43), bağlamsız çözülemez (8) | Inkelas & Orgun 2003; Inkelas 1999; Göksel & Kerslake 2005; Sezer 1981; Woodard 2015; Yawney 2018 |
| `vurgu_vikisozluk.tsv` | 9.030 sözcüğün vurgulu hecesi, **kesin / yumuşak** ayrımıyla | Vikisözlük (kaikki.org), CC BY-SA 4.0 |
| `okunus_vikisozluk.tsv` | 11.108 sözcüğün sesbirimsel IPA'sı | Vikisözlük (kaikki.org), CC BY-SA 4.0 |
| `normalizasyon.tsv` | 128 metin hazırlama örneği: sayı, tarih, saat, para, IBAN, telefon, kısaltma, Roma rakamı, kesir, aralık, e-posta, koordinat | [turkce-normalize](https://github.com/seslen-tr/turkce-normalize) testleri, MIT |

Dosyalar paketle birlikte `turkce_tts_sinav/veri/` altında gelir.

**Kesin ve yumuşak.** Vikisözlük'ün Türkçe okunuş şablonu, vurgu belirtilmezse son heceyi
kendiliğinden işaretler. Bu yüzden:
- **Kesin:** son hece dışındaki işaretler editörün elle yazdığı güvenilir bilgidir (1.234 sözcük).
- **Yumuşak:** son hece işaretleri editörün de olabilir, şablonun varsayılanı da (7.796 sözcük).
  Örneğin özel adlarda şablon varsayılanı Sezer kuralıyla çelişir (erzinCAN / ERzincan).

**Okunuş.** Sesbirimsel yazım ince k/g'yi her zaman işaretlemez (git → /ɡit/). Bu yüzden ayrıca
**incelik-duyarsız** ses hata oranı da verilir.

## Ölçüler

| Bölüm | Ölçü |
|---|---|
| Vurgu, literatür | doğru / toplam, türe göre; asıl ölçü "kural + Sezer" (bağlamsız çözülemeyen örnekler hariç) |
| Vurgu, Vikisözlük | kesin ve yumuşak alt kümelerde doğruluk |
| Okunuş | tam eşleşme oranı, PER (ses hata oranı; düzenleme uzaklığı / ses sayısı), incelik-duyarsız PER |
| Metin hazırlama | tam eşleşme oranı, WER (sözcük hata oranı) |

## Sonuçlar

| Sistem | Literatür kural+Sezer | Vikisözlük kesin | Vikisözlük yumuşak | Okunuş PER |
|---|---|---|---|---|
| [turkce-vurgu](https://github.com/seslen-tr/turkce-vurgu) 0.1 | 120/123 (%97,6) | %97,2 ⚠ | %91,7 | %3,04 ⚠ |
| hep son hece | 21/123 (%17,1) | %0 | %100 | — |

**Metin hazırlama:** [turkce-normalize](https://github.com/seslen-tr/turkce-normalize) 0.1 → 128/128. ⚠ Örnekler onun
testlerinden derlendiği için bu bağımsız bir ölçüm değildir; başka sistemlerin
karşılaştırılması için konmuştur. Bağımsız örnek katkıları bu yüzden özellikle değerlidir.

⚠ **Sızıntı:** turkce-vurgu'nun istisna ve okunuş sözlükleri Vikisözlük'ten türetildiği için
bu sütunlar şişkin çıkar. Sözlükten bağımsız ölçümü (5 katlı çapraz doğrulama) turkce-vurgu'nun
kendi README'sinde bulunur. Vikisözlük'ten sözlük türeten her sistem bu uyarıyı taşımalıdır.

espeak-ng'yi ölçmek için `pip install phonemizer` ve sistemde espeak-ng gerekir. Başka bir
çalışma, espeak-ng'nin Vikisözlük'le yalnız %55 oranında aynı hecede vurgu yaptığını bildiriyor
([Ghostwriter-Dict](https://github.com/Prosincerity/Ghostwriter-Dict)).

## Testler

```
python -m unittest discover -s tests     # ya da: pytest -q (CI'daki gibi, Python 3.9 ve 3.12)
```

## Kardeş projeler

Ölçülen sistemler [turkce-vurgu](https://github.com/seslen-tr/turkce-vurgu) ve
[turkce-normalize](https://github.com/seslen-tr/turkce-normalize),
[seslen-tts](https://github.com/seslen-tr/seslen-tts) ses modelinin metin ön ucudur. Diğerleri:
[turkce-duygu](https://github.com/seslen-tr/turkce-duygu) · [turkce-uslup](https://github.com/seslen-tr/turkce-uslup) ·
[turkce-plbert](https://github.com/seslen-tr/turkce-plbert)

## Katkı

Yeni kaynaklı örnek, düzeltme ya da sistem sonucu eklemek için PR açılabilir. Literatür
örneklerinde kaynak (yazar, yıl, sayfa ya da örnek numarası) zorunludur.

## Lisans

Kod MIT ([LICENSE](LICENSE)). `turkce_tts_sinav/veri/` altındaki Vikisözlük türevi dosyalar CC BY-SA 4.0.
Literatür örnekleri kaynaklarına atıfla kısa alıntıdır.
