# -*- coding: utf-8 -*-
"""python -m turkce_tts_sinav [turkce-vurgu | son-hece | espeak] — hazır sistemleri sınavdan geçirir."""
import sys

from . import heceler, ipa_vurgu_hecesi, kucuk, normalizasyon_sinavi, okunus_sinavi, vurgu_sinavi


def turkce_vurgu():
    from turkce_vurgu.g2p import sozcuk_okunusu
    from turkce_vurgu.vurgu import vurgulu_hece
    vurgu_sinavi(lambda w, ozel: vurgulu_hece(kucuk(w), ozel))
    okunus_sinavi(lambda w: sozcuk_okunusu(w))


def turkce_normalize():
    from turkce_normalize import normalize
    normalizasyon_sinavi(normalize)


def son_hece():
    vurgu_sinavi(lambda w, ozel: len(heceler(kucuk(w))) - 1)


def espeak():
    from phonemizer.backend import EspeakBackend          # pip install phonemizer + espeak-ng kurulu olmalı
    e = EspeakBackend("tr", with_stress=True)
    ipa = lambda w: e.phonemize([w], strip=True)[0]
    vurgu_sinavi(lambda w, ozel: ipa_vurgu_hecesi(ipa(w)))
    okunus_sinavi(ipa)


SISTEMLER = {"turkce-vurgu": turkce_vurgu, "turkce-normalize": turkce_normalize, "son-hece": son_hece,
             "espeak": espeak}

if __name__ == "__main__":
    for ad in sys.argv[1:] or ["turkce-vurgu", "son-hece"]:
        print(f"== {ad}")
        SISTEMLER[ad]()
