from flask import Flask
from mate import cebar_mate # Importamos la lógica original

app = Flask(__name__)

@app.route('/')
def inicio():
    # 1. Ejecuto la lógica real con un valor de temperatura específico
    #No se prueba el parametro de temperatura, sino el resultado que se muestra en la página
    estado_del_mate = cebar_mate(85)
    
    # 2.  HTML básico (parecido a "Hola Mundo")
    return f"""
    <html>
        <body style="text-align: center; margin-top: 50px; font-family: Arial;">
            <h1>🧉 Sistema de Cebado de Mates cambiado</h1>
            <h2>Estado en vivo: {estado_del_mate}</h2>
            <p>Este es el estado actual del mate según la temperatura del agua</p>
        </body>
    </html>
    """

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)