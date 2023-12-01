import unittest
from datetime import datetime
from app import app

class FlaskTest(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    # (1)
    # Obtener los contactos de una numero existente (Exito)
    def test_cuenta_contactos(self):
        minumero = 21345
        response = self.app.get(f'/billetera/contactos/{minumero}')

        self.assertEqual(response.status_code, 200)
        data = response.get_json()

        self.assertEqual(data['123'], 'Luisa')
        self.assertEqual(data['456'], 'Andrea')

    # (2)
    # Obtener los contactos de una numero inexistente (Failure)
    def test_cuenta_inexistente_contactos(self):
        minumero = 999
        response = self.app.get(f'/billetera/contactos/{minumero}')

        # self.assertEqual(response.status_code, 200)

        data = response.get_json()
        self.assertEqual(data['message'], 'Cuenta inexistente')

    # (3)
    # Realizar pago entre numeros existentes (Exito)
    def test_cuenta_pago(self):
        minumero = 21345
        numerodestino = 123
        valor = 100
        response = self.app.get(f'/billetera/pagar/{minumero}/{numerodestino}/{valor}')

        self.assertEqual(response.status_code, 200)

        data = response.get_json()
        self.assertEqual(data, f'Realizado en {datetime.now().date()}.')

    # (4)
    # Realizar pago entre numeros inexistentes (Failure)
    def test_cuenta_inxistente_pago(self):
        minumero = 999
        numerodestino = 123
        valor = 1000
        response = self.app.get(f'/billetera/pagar/{minumero}/{numerodestino}/{valor}')

        data = response.get_json()
        self.assertEqual(data['message'], f'Cuenta inexistente')

    # (5)
    # Ver historial de cuenta (Exito)
    def test_cuenta_historial(self):
        minumero = 21345
        numerodestino = 123
        valor = 100
        # Se realiza un pago para verificar si este se guarda en el historial 
        pago = self.app.get(f'/billetera/pagar/{minumero}/{numerodestino}/{valor}')

        response = self.app.get(f'/billetera/historial/{minumero}')

        # {"envios":["Numero destino: 123 | Fecha: 2023-11-30 | Valor: 100"],"recepciones":[],"saldo":100}

        data = response.get_json()
        self.assertEqual(data['envios'][0], "Numero destino: 123 | Fecha: 2023-11-30 | Valor: 100")

    # (6)
    # Ver historial de cuenta (Failure)
    def test_cuenta_inexistente_historial(self):
        minumero = 999
        response = self.app.get(f'/billetera/historial/{minumero}')

        data = response.get_json()
        self.assertEqual(data['message'], 'Cuenta inexistente')


if __name__ == '__main__':
    unittest.main()
