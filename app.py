from flask import Flask
from mate import cebar_mate # Importamos tu lógica original

app = Flask(__name__)

@app.route('/')
def inicio():
    # 1. Ejecutamos nuestra lógica real con el agua a 80 grados
    estado_del_mate = cebar_mate(80)
    
    # 2. Devolvemos un HTML súper básico ("Hola Mundo" style)
    return f"""
    <html>
        <body style="text-align: center; margin-top: 50px; font-family: Arial;">
            <h1>🧉 Sistema de Cebado de Mate</h1>
            <h2>Estado en vivo: {estado_del_mate}</h2>
            <p>Este texto se generó ejecutando el código real de Python.</p>
        </body>
    </html>
    """

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)