import unittest
from mate import cebar_mate

class TestMate(unittest.TestCase):
    
    def test_temperatura_ideal(self):
        resultado = cebar_mate(85)
        self.assertEqual(resultado, "Perfecto")

    def test_agua_hervida(self):
        resultado = cebar_mate(90)
        self.assertEqual(resultado, "Caliente")

    def test_agua_fria(self):
        resultado = cebar_mate(75)
        self.assertEqual(resultado, "Frio")

if __name__ == '__main__':
    unittest.main()
