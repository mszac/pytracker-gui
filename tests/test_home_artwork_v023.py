"""v0.2.23: only the four approved fixed PNG surfaces change; routes stay identical."""
import struct
import unittest
from pathlib import Path
from pytracker_gui.screens import DashboardScreen

ASSETS=Path(__file__).resolve().parents[1]/'pytracker_gui'/'assets'

class HomeArtworkV023Tests(unittest.TestCase):
    def test_four_asset_names_dimensions_and_small_size(self):
        expected=('experiment','logs','statistics','manual')
        self.assertEqual(tuple(item[0] for item in DashboardScreen.TILES),expected)
        self.assertEqual(DashboardScreen.TILE_SIZE,(546,365))
        for key in expected:
            with self.subTest(key=key):
                path=ASSETS/f'dashboard-{key}.png'
                raw=path.read_bytes()
                self.assertEqual(raw[:8],b'\x89PNG\r\n\x1a\n')
                self.assertEqual(struct.unpack('>II',raw[16:24]),(546,365))
                self.assertLess(len(raw),350_000)
                self.assertEqual(raw[25],2, 'PNG color type must be RGB for small runtime assets')

if __name__=='__main__':unittest.main()
