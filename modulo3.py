class EstadoBot:
    def __init__(self, system_instruction, temperatura):
        self.system_instruction = system_instruction
        self.temperatura = temperatura

class NodoEstado:
    def __init__(self, estado):
        self.estado = estado
        self.siguiente = None

class PilaRestauracion:
    def __init__(self):
        self.cima = None

    def push(self, estado):
        nuevo_nodo = NodoEstado(estado)
        nuevo_nodo.siguiente = self.cima
        self.cima = nuevo_nodo

    def pop(self):
        if self.cima is None:
            return None
        estado_restaurado = self.cima.estado
        self.cima = self.cima.siguiente
        return estado_restaurado