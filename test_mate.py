import unittest
from mate import cebar_mate

class TestMate(unittest.TestCase):
    
    def test_temperatura_ideal(self):
        resultado = cebar_mate(85)
        self.assertEqual(resultado, "Temperatura ideal, mate listo.")

    def test_agua_hervida(self):
        resultado = cebar_mate(90)
        self.assertEqual(resultado, "Agua muy caliente, se quemó la yerba.")

    def test_agua_fria(self):
        resultado = cebar_mate(75)
        self.assertEqual(resultado, "Está helado el mate, falta temperatura, te va a doler la panza.")

if __name__ == '__main__':
    unittest.main()