def cebar_mate(temperatura_agua):
    if temperatura_agua > 85:
        return "Agua muy caliente, se lavó el mate."
    elif temperatura_agua < 75:
        return "Agua muy fría, falta temperatura."
    else:
        return "Temperatura ideal, mate listo."