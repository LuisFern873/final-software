from flask import Flask, jsonify, abort
from models import *

app = Flask(__name__)

@app.route('/billetera/contactos/<minumero>')
def obtenerContactos(minumero):
    cuenta = search(minumero)
    if not cuenta:
        return jsonify(message='Cuenta inexistente') # Se podria incluir un abort()
    else:
        contacts = cuenta.contactos()
        return jsonify(contacts)

# http://127.0.0.1:5000/billetera/pagar/21345/123/100
# http://127.0.0.1:5000/billetera/pagar/123/456/50
# http://127.0.0.1:5000/billetera/historial/123

@app.route('/billetera/pagar/<minumero>/<numerodestino>/<int:valor>')
def realizarPago(minumero, numerodestino, valor):
    cuentaInicio = search(minumero)
    cuentaDestino = search(numerodestino)
    if not cuentaInicio or not cuentaDestino:
        return jsonify(message='Cuenta inexistente')
    # Realizar pago
    fecha = cuentaInicio.pagar(numerodestino, valor)
    return jsonify(f'Realizado en {fecha}.')


@app.route('/billetera/historial/<minumero>')
def obtenerHistorial(minumero):
    cuenta = search(minumero)
    if not cuenta:
        return jsonify(message='Cuenta inexistente')
    else:
        history = cuenta.historial()
        return jsonify(history)
    
# @app.errorhandler(400)
# def not_found(error):
#     return jsonify({
#         'message': 'Cuenta inexistente'
#     }), 400
    
@app.route('/')
def hello():
   return jsonify(message=';)')


if __name__ == '__main__':
    app.run()



