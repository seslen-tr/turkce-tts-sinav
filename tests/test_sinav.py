# -*- coding: utf-8 -*-
"""python -m unittest discover -s tests"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from turkce_tts_sinav import heceler, ipa_vurgu_hecesi, literatur, vurgu_sinavi  # noqa: E402


class Sinav(unittest.TestCase):
    def test_hece(self):
        self.assertEqual(heceler("ankara"), [0, 2, 4])

    def test_ipa_vurgu(self):
        self.assertEqual(ipa_vurgu_hecesi("anˈkaɾa"), 1)
        self.assertEqual(ipa_vurgu_hecesi("ˈankaɾa"), 0)
        self.assertIsNone(ipa_vurgu_hecesi("ankaɾa"))

    def test_literatur_okunur(self):
        o = literatur()
        self.assertGreater(len(o), 100)
        self.assertTrue(all("kaynak" in x and x["kaynak"] for x in o))

    def test_son_hece_taban_cizgisi(self):
        s = vurgu_sinavi(lambda w, ozel: len(heceler(w.lower())) - 1, yaz=False)
        self.assertEqual(s["vikisozluk_kesin"][0], 0)


if __name__ == "__main__":
    unittest.main()
