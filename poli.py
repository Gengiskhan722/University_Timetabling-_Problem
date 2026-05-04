from collections import defaultdict
from functools import lru_cache
import copy
# Utilidades
def canonical_form(adj):
    return tuple(sorted((k, tuple(sorted(v))) for k, v in adj.items()))

def print_graph(adj, indent):
    for k in adj:
        print(" " * indent + f"{k}: {adj[k]}")

# Operaciones sobre grafos
def delete_edge(adj, u, v):
    new_adj = copy.deepcopy(adj)
    new_adj[u].remove(v)
    new_adj[v].remove(u)
    return new_adj

def contract_edge(adj, u, v):
    new_adj = copy.deepcopy(adj)

    for neighbor in new_adj[v]:
        if neighbor != u:
            new_adj[u].append(neighbor)
            new_adj[neighbor].append(u)

    del new_adj[v]

    for node in new_adj:
        new_adj[node] = [u if x == v else x for x in new_adj[node]]

    # eliminar loops y duplicados
    new_adj[u] = list(set([x for x in new_adj[u] if x != u]))
    for node in new_adj:
        new_adj[node] = list(set(new_adj[node]))

    return new_adj

def is_edgeless(adj):
    return all(len(v) == 0 for v in adj.values())

# Operaciones con polinomios
def add_poly(p1, p2, sign=1):
    result = defaultdict(int, p1)
    for k, v in p2.items():
        result[k] += sign * v
    return dict(result)

# Algoritmo con trazas
def chromatic_polynomial_debug(adj, depth=0):
    indent = depth * 4
    print(" " * indent + "Grafo actual:")
    print_graph(adj, indent)

    # Caso base
    if is_edgeless(adj):
        n = len(adj)
        print(" " * indent + f"--> Grafo sin aristas: devuelve t^{n}")
        return {n: 1}

    # Elegir una arista
    for u in adj:
        if adj[u]:
            v = adj[u][0]
            break

    print(" " * indent + f"Arista elegida: ({u}, {v})")

    # Construir subgrafos
    G_minus = delete_edge(adj, u, v)
    G_contract = contract_edge(adj, u, v)

    print(" " * indent + "G - e:")
    print_graph(G_minus, indent + 2)

    print(" " * indent + "G / e:")
    print_graph(G_contract, indent + 2)

    # Recursión
    p1 = chromatic_polynomial_debug(G_minus, depth + 1)
    p2 = chromatic_polynomial_debug(G_contract, depth + 1)

    # Combinar
    result = add_poly(p1, p2, sign=-1)

    print(" " * indent + f"Combinando: P(G) = P(G-e) - P(G/e)")
    print(" " * indent + f"P(G-e): {p1}")
    print(" " * indent + f"P(G/e): {p2}")
    print(" " * indent + f"Resultado: {result}")
    print(" " * indent + "-"*40)

    return result
adj_list = {
    'A': ['B', 'C', 'D', 'G'],
    'B': ['A', 'C', 'E', 'H'],
    'C': ['A', 'B', 'F', 'I'],
    'D': ['A', 'E', 'F', 'G'],
    'E': ['B', 'D', 'F', 'H'],
    'F': ['C', 'D', 'E', 'I'],
    'G': ['A', 'D', 'H', 'I'],
    'H': ['B', 'E', 'G', 'I'],
    'I': ['C', 'F', 'G', 'H']
}

# Ejecutar
poly = chromatic_polynomial_debug(adj_list)

print("\nPolinomio final:")
for exp in sorted(poly.keys(), reverse=True):
    print(f"{poly[exp]} * t^{exp}")