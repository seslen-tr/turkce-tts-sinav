# -*- coding: utf-8 -*-
"""Metin hazırlama sınavı: kaynak sütunu, birden çok doğru okunuş, gevşek karşılaştırma."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from turkce_tts_sinav import (OKUNUS_AYIRICI, VARSAYILAN_KAYNAK, _normalizasyon_olc,  # noqa: E402
                              _satirlar, normalizasyon_sinavi)

SATIRLAR = [
    ["3-5 kişi", "üç ila beş kişi | üç beş kişi", "aralik", "deneme"],
    ["Saat 14:30'da", "Saat on dört otuzda", "saat"],  # üç sütun: varsayılan kaynak
    ["-12,5", "eksi on iki buçuk | eksi on iki virgül beş", "ondalik", ""],  # boş sütun: varsayılan kaynak
]


class Normalizasyon(unittest.TestCase):
    def test_kaynak_sutunu(self):
        s = _normalizasyon_olc(SATIRLAR, lambda m: "", gevsek=False)
        self.assertEqual(s["kaynaklar"], {"deneme": {"tam": 0, "ornek": 1},
                                          VARSAYILAN_KAYNAK: {"tam": 0, "ornek": 2}})

    def test_her_okunus_dogru(self):
        for i in (0, -1):
            s = _normalizasyon_olc(SATIRLAR, lambda m: next(p[1].split(OKUNUS_AYIRICI)[i]
                                                            for p in SATIRLAR if p[0] == m), gevsek=False)
            self.assertEqual((s["tam"], s["wer"]), (1.0, 0.0))

    def test_en_yakin_okunus(self):
        # "üç beş kişiler": ikinci okunuşa 1 sözcük uzak; WER paydası da o okunuşun uzunluğu
        s = _normalizasyon_olc(SATIRLAR[:1], lambda m: "üç beş kişiler", gevsek=False)
        self.assertEqual(s["wer"], 1 / 3)

    def test_gevsek(self):
        satir = [["Saat 14:30'da.", "Saat on dört otuz'da.", "saat"]]
        cikti = lambda m: "saat ON DÖRT otuzda"  # noqa: E731
        self.assertEqual(_normalizasyon_olc(satir, cikti, gevsek=False)["tam"], 0.0)
        self.assertEqual(_normalizasyon_olc(satir, cikti, gevsek=True)["tam"], 1.0)

    def test_gercek_veri(self):
        beklenen = {p[0]: p[1].split(OKUNUS_AYIRICI)[0] for p in _satirlar("normalizasyon.tsv")}
        s = normalizasyon_sinavi(beklenen.__getitem__, yaz=False)
        self.assertEqual(s["tam"], 1.0)
        self.assertEqual(s["ornek"], sum(k["ornek"] for k in s["kaynaklar"].values()))
        self.assertIn(VARSAYILAN_KAYNAK, s["kaynaklar"])
        self.assertIn("bagimsiz-dorukdumlu", s["kaynaklar"])
        self.assertTrue(any(OKUNUS_AYIRICI in p[1] for p in _satirlar("normalizasyon.tsv")))


if __name__ == "__main__":
    unittest.main()
