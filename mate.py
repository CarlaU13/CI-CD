def cebar_mate(temperatura_agua):
    if temperatura_agua > 90:
        return "Agua muy caliente, se quemó la yerba."
    elif temperatura_agua < 80:
        return "Está helado el mate, falta temperatura, te va a doler la panza."
    else:
        return "Temperatura ideal, mate listo."