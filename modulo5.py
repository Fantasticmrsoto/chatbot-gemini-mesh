from datetime import datetime

# ==========================================
# Módulo 5: Registro de Errores [cite: 26]
# ==========================================
class NodoError:
    def __init__(self, codigo, descripcion):
        self.fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S") # [cite: 28]
        self.codigo = codigo
        self.descripcion = descripcion
        self.siguiente = None

class LogErrores:
    def __init__(self):
        self.inicio = None
        self.fin = None

    def registrar_error(self, codigo, descripcion):
        nuevo_error = NodoError(codigo, descripcion)
        if self.inicio is None:
            self.inicio = self.fin = nuevo_error
        else:
            self.fin.siguiente = nuevo_error
            self.fin = nuevo_error
            self.fin = nuevo_error

    def listar_errores(self):
        if self.inicio is None:
            print("No hay errores registrados.")
            return
        actual = self.inicio
        print("\nRegistro de errores:")
        print("-" * 40)
        while actual:
            print(f"[{actual.fecha_hora}] {actual.codigo} - {actual.descripcion}")
            actual = actual.siguiente
        print("-" * 40)