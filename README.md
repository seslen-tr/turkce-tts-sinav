# turkce-tts-sinav

Türkçe G2P, sözcük vurgusu ve ses sentezi ön uçlarını ölçmek için **açık sınav verisi ve
değerlendirici**. Türkçe için bugüne kadar böyle ortak bir ölçüt yoktu. Sistemler ya hiç
ölçülmüyor ya da herkes kendi örnekleriyle ölçüyordu.

```python
from turkce_tts_sinav import vurgu_sinavi, okunus_sinavi

vurgu_sinavi(lambda sozcuk, ozel_kok: benim_sistemim.vurgulu_hece(sozcuk))  # 0'dan hece sırası ya da None
okunus_sinavi(lambda sozcuk: benim_sistemim.ipa(sozcuk))                    # IPA dizisi
```

```
python -m turkce_tts_sinav turkce-vurgu son-hece espeak
```

## Veri

| Dosya | İçerik | Kaynak |
|---|---|---|
| `vurgu_literatur.tsv` | Dilbilim literatüründe vurgusu verilmiş 135 sözcük ve çekimli biçim, her biri kaynağıyla. Tür etiketi: ek/kök kuralı, Sezer kuralı, sözlüksel, bağlamsız çözülemez | Inkelas & Orgun 2003; Inkelas 1999; Göksel & Kerslake 2005; Sezer 1981; Woodard 2015; Yawney 2018 |
| `vurgu_vikisozluk.tsv` | 9.030 sözcüğün vurgulu hecesi, **kesin / yumuşak** ayrımıyla | Vikisözlük (kaikki.org), CC BY-SA 4.0 |
| `okunus_vikisozluk.tsv` | 11.108 sözcüğün sesbirimsel IPA'sı | Vikisözlük (kaikki.org), CC BY-SA 4.0 |

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

## Sonuçlar

| Sistem | Literatür kural+Sezer | Vikisözlük kesin | Vikisözlük yumuşak | Okunuş PER |
|---|---|---|---|---|
| [turkce-vurgu](../turkce-vurgu) 0.1 | 120/123 (%97,6) | %97,2 ⚠ | %91,7 | %3,04 ⚠ |
| hep son hece | 21/123 (%17,1) | %0 | %100 | — |

⚠ **Sızıntı:** turkce-vurgu'nun istisna ve okunuş sözlükleri Vikisözlük'ten türetildiği için
bu sütunlar şişkin çıkar. Sözlükten bağımsız ölçümü (5 katlı çapraz doğrulama) turkce-vurgu'nun
kendi README'sinde bulunur. Vikisözlük'ten sözlük türeten her sistem bu uyarıyı taşımalıdır.

espeak-ng'yi ölçmek için `pip install phonemizer` ve sistemde espeak-ng gerekir. Başka bir
çalışma, espeak-ng'nin Vikisözlük'le yalnız %55 oranında aynı hecede vurgu yaptığını bildiriyor
([Ghostwriter-Dict](https://github.com/Prosincerity/Ghostwriter-Dict)).

## Katkı

Yeni kaynaklı örnek, düzeltme ya da sistem sonucu eklemek için PR açılabilir. Literatür
örneklerinde kaynak (yazar, yıl, sayfa ya da örnek numarası) zorunludur.

## Lisans

Kod MIT ([LICENSE](LICENSE)). `veri/` altındaki Vikisözlük türevi dosyalar CC BY-SA 4.0.
Literatür örnekleri kaynaklarına atıfla kısa alıntıdır.
