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

# Colores 
colores_hex = {
    1: '#e41a1c',  
    2: '#377eb8',  
    3: '#4daf4a',  
    4: '#984ea3'   
}


# Inicialización

vertices = list(adj_list.keys())
coloreado = {v: None for v in vertices}

# Grado de saturación
def saturacion(v):
    colores_vecinos = set()
    for vecino in adj_list[v]:
        if coloreado[vecino] is not None:
            colores_vecinos.add(coloreado[vecino])
    return len(colores_vecinos)

# Grado normal
def grado(v):
    return len(adj_list[v])

# DSATUR
repeticiones = 100
tiempos = []

for _ in range(repeticiones):

    coloreado = {v: None for v in vertices}

    inicio = time.perf_counter()

    # DSATUR
    while None in coloreado.values():

        no_coloreados = [v for v in vertices if coloreado[v] is None]

        v = max(
            no_coloreados,
            key=lambda x: (saturacion(x), grado(x))
        )

        colores_vecinos = {
            coloreado[u] for u in adj_list[v] if coloreado[u] is not None
        }

        color = 1
        while color in colores_vecinos:
            color += 1

        coloreado[v] = color

    fin = time.perf_counter()

    tiempos.append((fin - inicio) * 1000)  

# Calcular estadísticas
promedio = sum(tiempos) / len(tiempos)

print("\nTiempo de ejecución DSATUR:")
print(f"Promedio ({repeticiones} ejecuciones): {promedio:.6f} ms")
print(f"Mínimo: {min(tiempos):.6f} ms")
print(f"Máximo: {max(tiempos):.6f} ms")


# Resultado
print("Coloración DSATUR:")
for v in coloreado:
    print(f"{v}: Color {coloreado[v]}")

print(f"\nNúmero de colores usados: {len(set(coloreado.values()))}")

# Graficar 
G = nx.Graph()
for u in adj_list:
    for v in adj_list[u]:
        G.add_edge(u, v)

pos = nx.spring_layout(G, k=1.5, iterations=100, seed=42)

# convertir colores a lista
node_colors = [coloreado[n] for n in G.nodes()]

plt.figure(figsize=(8, 6))

nx.draw(
    G,
    pos,
    with_labels=True,
    node_color=node_colors,
    cmap=plt.cm.Set3,  
    edgecolors="black",
    node_size=900,
    font_color="black",
    linewidths=1.5,
    edge_color="black"
)

plt.title("Coloración con DSATUR (misma paleta que Greedy)")
plt.show()