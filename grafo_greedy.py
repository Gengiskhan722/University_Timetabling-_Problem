import networkx as nx
import matplotlib.pyplot as plt
import time
#Lista de adyacencia
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
#Orden de coloreo del grafo
orden = ['B', 'A', 'H', 'F', 'I', 'E', 'D', 'C', 'G']

#Construcción del grafo
G = nx.Graph()

for nodo, vecinos in adj_list.items():
    for vecino in vecinos:
        G.add_edge(nodo, vecino)

#Algoritmo de coloreo secuencial
repeticiones = 100
tiempos = []

for _ in range(repeticiones):

    colores = {}

    inicio = time.perf_counter()

    # Algoritmo greedy
    for nodo in orden:
        colores_vecinos = set(
            colores.get(vecino)
            for vecino in adj_list[nodo]
            if vecino in colores
        )

        color = 1
        while color in colores_vecinos:
            color += 1

        colores[nodo] = color

    fin = time.perf_counter()

    tiempos.append((fin - inicio) * 1000)  

# Calcular promedio
promedio = sum(tiempos) / len(tiempos)

print("\nTiempo de ejecución Greedy:")
print(f"Promedio ({repeticiones} ejecuciones): {promedio:.6f} ms")
print(f"Mínimo: {min(tiempos):.6f} ms")
print(f"Máximo: {max(tiempos):.6f} ms")

#Imprimir resultado
print("Coloreo resultante (Greedy con orden dado):")
for nodo in orden:
    print(f"{nodo} -> Color {colores[nodo]}")

#Dibujar grafo
pos = nx.spring_layout(G, k=1.5, iterations=100, seed=42)

#Convertir colores a lista para dibujar
color_map = [colores[nodo] for nodo in G.nodes()]

plt.figure(figsize=(8, 6))

nx.draw(
    G, pos,
    with_labels=True,
    node_color=color_map,
    cmap=plt.cm.Set3,
    edgecolors="black",
    node_size=1200,
    font_size=12,
    font_weight="bold",
    edge_color="black",
    width=1.5
)

plt.title("Coloreo secuencial con orden especifico.")

plt.savefig("grafo_greedy.png", dpi=300, bbox_inches='tight')
plt.show()