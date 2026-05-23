import unittest
from mate import cebar_mate

class TestMate(unittest.TestCase):
    
    def test_temperatura_ideal(self):
        resultado = cebar_mate(80)
        self.assertEqual(resultado, "Temperatura ideal, mate listo.")

    def test_agua_hervida(self):
        resultado = cebar_mate(90)
        self.assertEqual(resultado, "Agua muy caliente, se lavó el mate.")

if __name__ == '__main__':
    unittest.main()