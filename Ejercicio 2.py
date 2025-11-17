

from dataclasses import dataclass
from typing import Dict, Set, List, Tuple
from collections import deque
import heapq

# ---- Vértice ----
@dataclass
class Vertice:
    nombre: str
    episodios: Set[int]

# ---- Grafo ----
class Grafo:
    def __init__(self):
        self.vertices: Dict[str, Vertice] = {}
        self.ady: Dict[str, Dict[str, int]] = {}

    def agregar_vertice(self, nombre: str, episodios: Set[int]):
        if nombre not in self.vertices:
            self.vertices[nombre] = Vertice(nombre, set(episodios))
            self.ady[nombre] = {}
        else:
            self.vertices[nombre].episodios |= episodios

    def agregar_arista_auto(self, a: str, b: str):
        # peso = episodios compartidos
        ea = self.vertices[a].episodios
        eb = self.vertices[b].episodios
        w = len(ea & eb)
        self.ady[a][b] = w
        self.ady[b][a] = w

    # ---- MST (Prim) ----
    def mst(self, inicio: str) -> List[Tuple[str, str, int]]:
        visitados = set([inicio])
        res = []
        heap = []
        for v, w in self.ady[inicio].items():
            heapq.heappush(heap, (w, inicio, v))
        while heap:
            w, u, v = heapq.heappop(heap)
            if v in visitados:
                continue
            visitados.add(v)
            res.append((u, v, w))
            for x, wx in self.ady[v].items():
                if x not in visitados:
                    heapq.heappush(heap, (wx, v, x))
        return res

    # ---- Mayor episodios compartidos ----
    def max_compartidos(self):
        mayor = -1
        pares = []
        vistos = set()
        for u in self.ady:
            for v, w in self.ady[u].items():
                if (v, u) in vistos:
                    continue
                vistos.add((u, v))
                if w > mayor:
                    mayor = w
                    pares = [(u, v)]
                elif w == mayor:
                    pares.append((u, v))
        return mayor, pares

    # ---- Camino por BFS (menos aristas) ----
    def camino_hops(self, a: str, b: str) -> List[str]:
        cola = deque([a])
        padre = {a: None}
        while cola:
            u = cola.popleft()
            if u == b:
                break
            for v in self.ady[u]:
                if v not in padre:
                    padre[v] = u
                    cola.append(v)
        if b not in padre:
            return []
        camino = []
        x = b
        while x is not None:
            camino.append(x)
            x = padre[x]
        return list(reversed(camino))

    # ---- Camino por "fuerza" (Dijkstra) ----
    def camino_fuerte(self, a: str, b: str) -> List[str]:
        INF = float("inf")
        dist = {v: INF for v in self.vertices}
        dist[a] = 0
        padre = {v: None for v in self.vertices}
        heap = [(0, a)]
        while heap:
            d, u = heapq.heappop(heap)
            if d > dist[u]:
                continue
            if u == b:
                break
            for v, w in self.ady[u].items():
                costo = INF if w == 0 else (1 / w)
                nd = d + costo
                if nd < dist[v]:
                    dist[v] = nd
                    padre[v] = u
                    heapq.heappush(heap, (nd, v))
        if dist[b] == INF:
            return []
        cam = []
        x = b
        while x is not None:
            cam.append(x)
            x = padre[x]
        return list(reversed(cam))

    # ---- Personajes que aparecen en N episodios ----
    def aparecen_en(self, n: int) -> List[str]:
        return [v for v, obj in self.vertices.items() if len(obj.episodios) == n]

# ---- Construcción ejemplo ----
def armar_ejemplo() -> Grafo:
    g = Grafo()
    E = set(range(1, 10))

    g.agregar_vertice("C-3PO", E)
    g.agregar_vertice("R2-D2", E)

    g.agregar_vertice("Luke Skywalker", {4,5,6,7,8,9})
    g.agregar_vertice("Darth Vader", {4,5,6})
    g.agregar_vertice("Yoda", {2,3,5,8,9})
    g.agregar_vertice("Boba Fett", {4,5,6})
    g.agregar_vertice("Leia", {4,5,6,7,8,9})
    g.agregar_vertice("Rey", {7,8,9})
    g.agregar_vertice("Kylo Ren", {7,8,9})
    g.agregar_vertice("Chewbacca", {4,5,6,7,8,9})
    g.agregar_vertice("Han Solo", {4,5,6,7})
    g.agregar_vertice("BB-8", {7,8,9})

    lista = list(g.vertices.keys())
    for i in range(len(lista)):
        for j in range(i+1, len(lista)):
            g.agregar_arista_auto(lista[i], lista[j])

    return g
