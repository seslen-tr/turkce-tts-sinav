# -*- coding: utf-8 -*-
"""
TÜRKÇE TTS SINAVI — Türkçe G2P / vurgu / ses sentezi ön uçlarını ölçmek için açık veri ve değerlendirici.

    from turkce_tts_sinav import vurgu_sinavi, okunus_sinavi
    vurgu_sinavi(lambda sozcuk, ozel_kok: benim_sistemim.vurgulu_hece(sozcuk))
    okunus_sinavi(lambda sozcuk: benim_sistemim.ipa(sozcuk))

Bölümler (veri/):
  vurgu_literatur.tsv   dilbilim literatüründe vurgusu verilmiş 135 örnek (kaynaklı)
  vurgu_vikisozluk.tsv  9.030 Vikisözlük sözcüğü; "kesin" (son hece dışı, editör yazmış) ve
                        "yumusak" (son hece; şablon varsayılanı olabilir) ayrımıyla
  okunus_vikisozluk.tsv 11.108 Vikisözlük sözcüğünün sesbirimsel IPA'sı
  normalizasyon.tsv     128 metin hazırlama örneği (sayı, tarih, saat, para, kısaltma, Roma rakamı…)
Hece: Türkçe yazım hecesi (her ünlü bir hece; iki ünlü arasındaki tek ünsüz sonraki heceye,
birden çoksa sonuncusu). Vurgulu hece 0'dan sayılır; vurgusuz sözcük (mi, de) için None.
"""
from __future__ import annotations

import re
import unicodedata
from collections import Counter
from pathlib import Path
from typing import Callable

VERI = Path(__file__).resolve().parent / "veri"
UNLU = set("aeıioöuüâîû")
_BUYUK_UNLU = set("AEIİOÖUÜÂÎÛ")
_IPA_UNLU = set("aeiɯoøuyɛɑæœ")


def kucuk(s: str) -> str:
    return unicodedata.normalize("NFC", s.replace("I", "ı").replace("İ", "i")).lower()


def heceler(w: str) -> list[int]:
    """Yazım hecelerinin başladığı harf konumları (küçük harfli sözcükte)."""
    u = [i for i, c in enumerate(w) if c in UNLU]
    if not u:
        return [0]
    bas = [0]
    for onceki, simdi in zip(u, u[1:]):
        bas.append(simdi if simdi - onceki == 1 else simdi - 1)
    return bas


def ipa_vurgu_hecesi(ipa: str) -> int | None:
    """IPA'daki ˈ işaretinden önceki hece sayısı (ünlü sayısı) — espeak vb. çıktısını sınava bağlar."""
    if "ˈ" not in ipa:
        return None
    return sum(1 for c in ipa.split("ˈ")[0] if c in _IPA_UNLU)


def _satirlar(ad: str) -> list[list[str]]:
    return [s.split("\t") for s in (VERI / ad).read_text(encoding="utf-8").splitlines() if s and not s.startswith("#")]


def literatur() -> list[dict]:
    """Kaynaklı örnekler: sözcük (küçük), beklenen hece, tür, kaynak, özel kök."""
    sonuc = []
    for p in _satirlar("vurgu_literatur.tsv"):
        ornek, tur, kaynak = p[0], p[1], p[2]
        w = kucuk(ornek)
        i = next(j for j, c in enumerate(ornek) if c in _BUYUK_UNLU)
        sonuc.append({"sozcuk": w, "beklenen": max(k for k, b in enumerate(heceler(w)) if b <= i),
                      "tur": tur, "kaynak": kaynak, "ozel_kok": p[3] if len(p) > 3 else "", "ornek": ornek})
    return sonuc


def vurgu_sinavi(sistem: Callable[[str, str], int | None], yaz: bool = True) -> dict:
    """sistem(sozcuk, ozel_kok) → vurgulu hece. sozcuk Vikisözlük'te özel adsa büyük harfle başlar.
    Döner: {"literatur": {tür: (doğru, toplam)}, "vikisozluk_kesin": (d, t), "vikisozluk_yumusak": (d, t)}."""
    lit: dict[str, list[int]] = {}
    yanlis = []
    for o in literatur():
        t = sistem(o["sozcuk"], o["ozel_kok"])
        lit.setdefault(o["tur"], [0, 0])
        lit[o["tur"]][1] += 1
        if t == o["beklenen"]:
            lit[o["tur"]][0] += 1
        elif o["tur"] != "belirsiz":
            yanlis.append((o["ornek"], t, o["kaynak"]))
    kesin, yumusak = [0, 0], [0, 0]
    for w, v, n, guven in _satirlar("vurgu_vikisozluk.tsv"):
        k = kucuk(w)
        t = sistem(w if w[:1].isupper() else k, k if w[:1].isupper() else "")
        hedef = kesin if guven == "kesin" else yumusak
        hedef[1] += 1
        hedef[0] += t == int(v)
    sonuc = {"literatur": {k: tuple(v) for k, v in lit.items()}, "vikisozluk_kesin": tuple(kesin),
             "vikisozluk_yumusak": tuple(yumusak), "yanlislar": yanlis}
    if yaz:
        print("VURGU")
        for tur in ("kural", "sezer", "sozluk", "belirsiz"):
            if tur in lit:
                d, t = lit[tur]
                print(f"  literatür {tur:9s} {d:4d} / {t:4d}  %{100 * d / t:.1f}")
        olcu = [lit[t] for t in ("kural", "sezer") if t in lit]
        d, t = sum(x[0] for x in olcu), sum(x[1] for x in olcu)
        print(f"  literatür kural+sezer {d} / {t}  %{100 * d / t:.1f}")
        print(f"  Vikisözlük kesin (son hece dışı) {kesin[0]} / {kesin[1]}  %{100 * kesin[0] / kesin[1]:.1f}")
        print(f"  Vikisözlük yumuşak (son hece)    {yumusak[0]} / {yumusak[1]}  %{100 * yumusak[0] / yumusak[1]:.1f}")
    return sonuc


def _fonemler(ipa: str) -> list[str]:
    s = unicodedata.normalize("NFC", ipa).replace("͡", "").replace("ˈ", "").replace("ˌ", "").replace(".", "")
    s = s.translate(str.maketrans({"g": "ɡ", "r": "ɾ", "ɛ": "e", "ɑ": "a", "æ": "e"})).replace(" ", "")
    return re.findall(r"dʒ|tʃ|.ː|.", s)


def _uzaklik(a: list[str], b: list[str]) -> int:
    onceki = list(range(len(b) + 1))
    for i, x in enumerate(a, 1):
        simdi = [i]
        for j, y in enumerate(b, 1):
            simdi.append(min(onceki[j] + 1, simdi[j - 1] + 1, onceki[j - 1] + (x != y)))
        onceki = simdi
    return onceki[-1]


def okunus_sinavi(sistem: Callable[[str], str], yaz: bool = True) -> dict:
    """sistem(sozcuk) → IPA (vurgu işareti olabilir, yok sayılır). Ölçüler: tam eşleşme, PER (ses hata
    oranı) ve incelik-duyarsız PER (Vikisözlük'ün sesbirimsel yazımı ince k/g'yi her zaman işaretlemez)."""
    tam = top = hata = hata_i = 0
    incelik = str.maketrans({"c": "k", "ɟ": "ɡ", "l": "ɫ"})
    for w, ipa in _satirlar("okunus_vikisozluk.tsv"):
        a, b = _fonemler(sistem(w)), _fonemler(ipa)
        top += len(b)
        h = _uzaklik(a, b)
        hata += h
        hata_i += _uzaklik([x.translate(incelik) for x in a], [x.translate(incelik) for x in b])
        tam += h == 0
    n = len(_satirlar("okunus_vikisozluk.tsv"))
    sonuc = {"tam": tam / n, "per": hata / top, "per_incelik_duyarsiz": hata_i / top, "sozcuk": n}
    if yaz:
        print("OKUNUŞ")
        print(f"  tam eşleşme %{100 * sonuc['tam']:.1f} · PER %{100 * sonuc['per']:.2f} · "
              f"incelik-duyarsız PER %{100 * sonuc['per_incelik_duyarsiz']:.2f}  ({n} sözcük)")
    return sonuc


def normalizasyon_sinavi(sistem: Callable[[str], str], yaz: bool = True) -> dict:
    """sistem(metin) → okunuşa hazır metin. Ölçü: tam eşleşme (boşluk farkı yok sayılır) ve
    sözcük hata oranı (WER)."""
    tam = hata = top = 0
    yanlis = []
    for girdi, beklenen, grup in _satirlar("normalizasyon.tsv"):
        cikti = " ".join(sistem(girdi).split())
        a, b = cikti.split(), beklenen.split()
        h = _uzaklik(a, b)
        hata += h
        top += len(b)
        tam += h == 0
        if h:
            yanlis.append((girdi, cikti, beklenen))
    n = len(_satirlar("normalizasyon.tsv"))
    sonuc = {"tam": tam / n, "wer": hata / top, "ornek": n, "yanlislar": yanlis}
    if yaz:
        print("METİN HAZIRLAMA")
        print(f"  tam eşleşme {tam} / {n}  %{100 * tam / n:.1f} · WER %{100 * hata / top:.2f}")
    return sonuc
