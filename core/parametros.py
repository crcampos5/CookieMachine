
import json

FILE_NAME = 'parameters/parameters.json'

#Esta es una clase tipo singleton para que todos los objectos tengan disponible los parametros
class Parametros:
    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
            cls._instancia._cargar_parametros(FILE_NAME)
        return cls._instancia

    def _cargar_parametros(self, archivo):
        with open(archivo, 'r') as f:
            self.parametros = json.load(f)
            f.close()

    def get_parametro(self, nombre):
        return self.parametros.get(nombre)