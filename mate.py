import os # Prueba de funcionamiento de Ruff

def cebar_mate(temperatura_agua):
    if temperatura_agua >= 90:
        return "Caliente"
    elif temperatura_agua < 80:
        return "Frio"
    else:
        return "Perfecto"
