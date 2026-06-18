def cebar_mate(temperatura_agua):
    #x=3 # Prueba de funcionamiento de Ruff
    if temperatura_agua >= 90:
        return "Caliente"
    elif temperatura_agua < 80:
        return "Frio"
    else:
        return "Perfecto"
