from datetime import datetime

class Operacion:
    def __init__(self, numeroDestino, fecha, valor):
        self.numeroDestino = numeroDestino
        self.fecha = fecha
        self.valor = valor
    def __str__(self):
        return f"Numero destino: {self.numeroDestino} | Fecha: {self.fecha} | Valor: {self.valor}"

class Cuenta:
    def __init__(self, numero, nombre, saldo, contacts):
        self.numero = numero
        self.nombre = nombre
        self.saldo = saldo
        self.contacts = contacts
        self.envios = []

    def __str__(self):
        return f"Numero: {self.numero} | Saldo: {self.saldo} | Contactos: {self.contacts}"
    
    def historial(self):
        dict = {}
        dict["saldo"] = self.saldo

        dict["envios"] = []
        dict["recepciones"] = []

        for envio in self.envios:
            dict["envios"].append(str(envio))

        for operacion in DBoperaciones:
            if operacion.numeroDestino == self.numero:
                dict["recepciones"].append(str(operacion))
        return dict

    def pagar(self, destino, valor):
        operacion = Operacion(destino, datetime.now().date(), valor)

        # Encontrar en la base de datos la cuenta destino 
        cuentaDestino = None
        for cuenta in DBcuentas:
            if cuenta.numero == destino:
                cuentaDestino = cuenta
                break
        if not cuentaDestino:
            print("Cuenta destino inexistente.")
            return

        # Verificar si hay suficiente saldo para realizar la transacción
        if valor > cuentaDestino.saldo:
            print("Cuenta sin saldo suficiente.")
            return
        
        # Realizar la transacción
        self.saldo -= valor
        cuentaDestino.saldo += valor

        # Registrar la operación en la base de datos
        self.envios.append(operacion)
        DBoperaciones.append(operacion)

        return str(operacion.fecha)

    def contactos(self):
        # Buscar info de contactos
        dict = {}
        for cuenta in DBcuentas:
            if cuenta.numero in self.contacts:
                dict[cuenta.numero] = cuenta.nombre
        return dict

DBcuentas = [
    Cuenta("21345", "Arnaldo", 200, ["123", "456"]),
    Cuenta("123", "Luisa", 400, ["456"]),
    Cuenta("456", "Andrea", 300, ["21345"])
]

DBoperaciones = [
]

def search(numero):
    for cuenta in DBcuentas:
        if cuenta.numero == numero:
            return cuenta
    return None


