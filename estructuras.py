class Nodo:
    def __init__(self, nombre: str, identificacion: str):
        self.nombre = nombre
        self.identificacion = identificacion
        self.siguiente = None
        self.turnos_atendidos = 0

class ListaCircular:
    def __init__(self):
        self.cabeza = None
        self.actual = None
        self._tamanio = 0

    def esta_vacia(self) -> bool:
        return self.cabeza is None

    def agregar(self, nombre: str, identificacion: str):
        nuevo_nodo = Nodo(nombre, identificacion)
        if self.esta_vacia():
            self.cabeza = nuevo_nodo
            self.cabeza.siguiente = self.cabeza
            self.actual = self.cabeza
        else:
            actual = self.cabeza
            while actual.siguiente != self.cabeza:
                actual = actual.siguiente
            actual.siguiente = nuevo_nodo
            nuevo_nodo.siguiente = self.cabeza
        self._tamanio += 1

    def mostrar(self) -> list:
        if self.esta_vacia():
            return []
        elementos = []
        actual = self.cabeza
        while True:
            elementos.append({
                "nombre": actual.nombre,
                "identificacion": actual.identificacion,
                "turnos_atendidos": actual.turnos_atendidos,
                "es_actual": (actual == self.actual)
            })
            actual = actual.siguiente
            if actual == self.cabeza:
                break
        return elementos

    def buscar(self, identificacion: str):
        if self.esta_vacia():
            return None
        actual = self.cabeza
        while True:
            if actual.identificacion == identificacion:
                return actual
            actual = actual.siguiente
            if actual == self.cabeza:
                break
        return None

    def eliminar(self, identificacion: str) -> bool:
        if self.esta_vacia():
            return False
        
        actual = self.cabeza
        anterior = None
        encontrado = False

        # Buscar el nodo a eliminar
        while True:
            if actual.identificacion == identificacion:
                encontrado = True
                break
            anterior = actual
            actual = actual.siguiente
            if actual == self.cabeza:
                break

        if not encontrado:
            return False

        # Caso 1: Único elemento en la lista
        if self._tamanio == 1:
            self.cabeza = None
            self.actual = None
        else:
            # Encontrar el último nodo para actualizar su enlace si es necesario
            ultimo = self.cabeza
            while ultimo.siguiente != self.cabeza:
                ultimo = ultimo.siguiente

            if actual == self.cabeza:
                self.cabeza = actual.siguiente
                ultimo.siguiente = self.cabeza
            else:
                anterior.siguiente = actual.siguiente

            # Si el nodo eliminado era el actual, movemos el actual al siguiente
            if actual == self.actual:
                self.actual = actual.siguiente

        self._tamanio -= 1
        return True

    def contar(self) -> int:
        return self._tamanio

    def siguiente_turno(self):
        if self.esta_vacia():
            return None
        self.actual.turnos_atendidos += 1
        self.actual = self.actual.siguiente
        return self.actual

    def anterior_turno(self):
        if self.esta_vacia():
            return None
        actual = self.cabeza
        while actual.siguiente != self.actual:
            actual = actual.siguiente
        self.actual = actual
        return self.actual

    def obtener_turno_actual(self):
        if self.esta_vacia():
            return None
        return self.actual

    def avanzar_varios(self, pasos: int):
        if self.esta_vacia():
            return None
        for _ in range(pasos):
            self.siguiente_turno()
        return self.actual