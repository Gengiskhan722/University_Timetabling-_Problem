import networkx as nx
import matplotlib.pyplot as plt
import time

# Lista de adyacencia
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
# Construir grafo
G = nx.Graph(adj_list)

# DSATUR (heurística de Brelaz) para cota inicial
def dsatur_coloring(graph):
    colors = {}
    saturation = {v: 0 for v in graph.nodes()}
    degree = dict(graph.degree())

    while len(colors) < len(graph):
        # seleccionar nodo no coloreado con mayor saturación (y grado en empate)
        uncolored = [v for v in graph.nodes() if v not in colors]

        v = max(
            uncolored,
            key=lambda x: (saturation[x], degree[x])
        )

        used_colors = {colors[n] for n in graph.neighbors(v) if n in colors}

        c = 0
        while c in used_colors:
            c += 1

        colors[v] = c

        # actualizar saturación
        for n in graph.neighbors(v):
            if n not in colors:
                neighbor_colors = {colors[n2] for n2 in graph.neighbors(n) if n in colors}
                saturation[n] = len(neighbor_colors)

    return colors, max(colors.values()) + 1

# Ordenación DSATUR para backtracking
def saturation_degree(node, coloring, graph):
    neighbor_colors = {coloring[n] for n in graph.neighbors(node) if n in coloring}
    return (len(neighbor_colors), graph.degree[node])

# Algoritmo exacto de Brown 
def brown_coloring(graph):
    _, ub = dsatur_coloring(graph) 
    best_coloring = None

    nodes = list(graph.nodes())

    def backtrack(coloring):
        nonlocal best_coloring, ub

        if len(coloring) == len(nodes):
            used = len(set(coloring.values()))
            if used < ub:
                ub = used
                best_coloring = coloring.copy()
            return

        # poda
        if len(set(coloring.values())) >= ub:
            return

        # seleccionar siguiente nodo 
        uncolored = [v for v in nodes if v not in coloring]
        v = max(uncolored, key=lambda x: saturation_degree(x, coloring, graph))

        used_colors = {coloring[n] for n in graph.neighbors(v) if n in coloring}

        for c in range(ub):  
            if c not in used_colors:
                coloring[v] = c
                backtrack(coloring)
                del coloring[v]

    backtrack({})
    return best_coloring, ub

# Ejecutar algoritmo
repeticiones = 100
tiempos = []

for _ in range(repeticiones):

    inicio = time.perf_counter()

    coloring, num_colors = brown_coloring(G)

    fin = time.perf_counter()

    tiempos.append((fin - inicio) * 1000) 

# Estadísticas
promedio = sum(tiempos) / len(tiempos)

print("\nTiempo de ejecución Brown:")
print(f"Promedio ({repeticiones} ejecuciones): {promedio:.6f} ms")
print(f"Mínimo: {min(tiempos):.6f} ms")
print(f"Máximo: {max(tiempos):.6f} ms")

# Mostrar resultado final
print("\nNúmero mínimo de colores:", num_colors)
print("Coloreo óptimo:", coloring)

# Visualización 
pos = nx.spring_layout(G, k=1.5, iterations=100, seed=42)

# usar directamente los colores del resultado
node_colors = [coloring[n] for n in G.nodes()]

plt.figure(figsize=(8, 6))

nx.draw(
    G,
    pos,
    with_labels=True,
    node_color=node_colors,
    cmap=plt.cm.Set3, 
    node_size=900,
    font_weight='bold',
    edge_color='black',
    linewidths=1.5,
    edgecolors='black'
)

plt.title("Coloreo exacto de Brown (misma paleta que Greedy y DSATUR)")
plt.show()