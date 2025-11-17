
from dataclasses import dataclass
from typing import List, Optional
from collections import deque

# ---- Registro Pokemon ----
@dataclass
class Pokemon:
    nombre: str
    numero: int
    tipos: List[str]
    debilidades: List[str]
    mega: bool
    gigamax: bool

# ---- Nodo ABB ----
class NodoABB:
    def __init__(self, clave, pokemon):
        self.clave = clave
        self.pokemon = pokemon
        self.izq = None
        self.der = None

# ---- ABB general ----
class ABB:
    def __init__(self, clave_func):
        self.raiz = None
        self.clave_func = clave_func

    def insertar(self, p: Pokemon):
        clave = self.clave_func(p)
        self.raiz = self._insertar(self.raiz, clave, p)

    def _insertar(self, nodo, clave, p):
        if nodo is None:
            return NodoABB(clave, p)
        if clave < nodo.clave:
            nodo.izq = self._insertar(nodo.izq, clave, p)
        elif clave > nodo.clave:
            nodo.der = self._insertar(nodo.der, clave, p)
        else:
            nodo.pokemon = p
        return nodo

    def buscar(self, clave):
        aux = self.raiz
        while aux is not None:
            if clave == aux.clave:
                return aux.pokemon
            elif clave < aux.clave:
                aux = aux.izq
            else:
                aux = aux.der
        return None

    def inorder(self) -> List[Pokemon]:
        resultado = []
        def _in(nodo):
            if nodo is None:
                return
            _in(nodo.izq)
            resultado.append(nodo.pokemon)
            _in(nodo.der)
        _in(self.raiz)
        return resultado

    def por_niveles(self) -> List[Pokemon]:
        res = []
        if self.raiz is None:
            return res
        cola = deque([self.raiz])
        while cola:
            nodo = cola.popleft()
            res.append(nodo.pokemon)
            if nodo.izq:
                cola.append(nodo.izq)
            if nodo.der:
                cola.append(nodo.der)
        return res

    def buscar_parcial(self, texto: str) -> List[Pokemon]:
        texto = texto.lower()
        lista = []
        for p in self.inorder():
            if texto in p.nombre.lower():
                lista.append(p)
        return lista

# ---- Índice por tipo ----
class NodoTipo:
    def __init__(self, tipo):
        self.tipo = tipo
        self.lista = []
        self.izq = None
        self.der = None

class IndiceTipos:
    def __init__(self):
        self.raiz = None

    def insertar(self, tipo: str, p: Pokemon):
        tipo = tipo.lower()
        self.raiz = self._insertar(self.raiz, tipo, p)

    def _insertar(self, nodo, tipo, p):
        if nodo is None:
            nodo = NodoTipo(tipo)
            nodo.lista.append(p)
            return nodo
        if tipo < nodo.tipo:
            nodo.izq = self._insertar(nodo.izq, tipo, p)
        elif tipo > nodo.tipo:
            nodo.der = self._insertar(nodo.der, tipo, p)
        else:
            nodo.lista.append(p)
        return nodo

    def buscar(self, tipo: str):
        tipo = tipo.lower()
        aux = self.raiz
        while aux is not None:
            if tipo == aux.tipo:
                return aux.lista
            elif tipo < aux.tipo:
                aux = aux.izq
            else:
                aux = aux.der
        return []

    def listado_conteo(self):
        salida = []
        def _in(n):
            if n is None:
                return
            _in(n.izq)
            salida.append((n.tipo, len(n.lista)))
            _in(n.der)
        _in(self.raiz)
        return salida

# ---- Pokedex ----
class Pokedex:
    def __init__(self):
        self.indice_num = ABB(lambda p: p.numero)
        self.indice_nom = ABB(lambda p: p.nombre.lower())
        self.indice_tipo = IndiceTipos()
        self.todos = []

    def agregar(self, p: Pokemon):
        self.todos.append(p)
        self.indice_num.insertar(p)
        self.indice_nom.insertar(p)
        for t in p.tipos:
            self.indice_tipo.insertar(t, p)

    # Funciones pedidas
    def buscar_numero(self, n):
        return self.indice_num.buscar(n)

    def buscar_nombre_parcial(self, txt):
        return self.indice_nom.buscar_parcial(txt)

    def listar_por_numero(self):
        return self.indice_num.inorder()

    def listar_por_nombre(self):
        return self.indice_nom.inorder()

    def listar_por_niveles_nombre(self):
        return self.indice_nom.por_niveles()

    def pokemons_de_tipo(self, tipo):
        return [p.nombre for p in self.indice_tipo.buscar(tipo)]

    def debiles_a(self, tipo):
        tipo = tipo.lower()
        res = []
        for p in self.todos:
            for d in p.debilidades:
                if d.lower() == tipo:
                    res.append(p)
                    break
        return res

    def conteo_tipos(self):
        return self.indice_tipo.listado_conteo()

    def contar_megas(self):
        return sum(1 for p in self.todos if p.mega)

    def contar_gigamax(self):
        return sum(1 for p in self.todos if p.gigamax)
