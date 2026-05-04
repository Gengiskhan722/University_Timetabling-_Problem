import networkx as nx
import matplotlib.pyplot as plt
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
# Construcción del grafo
G = nx.Graph()

for nodo, vecinos in adj_list.items():
    for vecino in vecinos:
        G.add_edge(nodo, vecino)

# Layout 
pos = nx.spring_layout(G, k=1.5, iterations=100, seed=42)
# Dibujo
plt.figure(figsize=(8, 6))

nx.draw(
    G, pos,
    with_labels=True,
    node_color="white",      
    edgecolors="black",      
    node_size=1200,
    font_size=12,
    font_weight="bold",
    edge_color="black",      
    width=1.5
)

plt.title("Grafo de Conflicto (sin coloreo)")
# Guardar imagen
plt.savefig("grafo_conflicto.png", dpi=300, bbox_inches='tight')
plt.show()