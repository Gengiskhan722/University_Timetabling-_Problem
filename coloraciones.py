import itertools
import networkx as nx
import matplotlib.pyplot as plt

# Grafo
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

nodes = list(adj_list.keys())

# Validación
def es_valido(asignacion):
    for u in adj_list:
        for v in adj_list[u]:
            if asignacion[u] == asignacion[v]:
                return False
    return True

# Normalización
def normalizar(asignacion):
    mapa = {}
    nuevo_color = 1
    resultado = {}

    for nodo in nodes:
        color = asignacion[nodo]
        if color not in mapa:
            mapa[color] = nuevo_color
            nuevo_color += 1
        resultado[nodo] = mapa[color]

    return tuple(resultado[n] for n in nodes)

# Obtener soluciones únicas
def obtener_unicas(t):
    colores = list(range(1, t+1))
    soluciones = {}
    
    for asign in itertools.product(colores, repeat=len(nodes)):
        asignacion = dict(zip(nodes, asign))
        if es_valido(asignacion):
            canonica = normalizar(asignacion)
            if canonica not in soluciones:
                soluciones[canonica] = asignacion  

    return list(soluciones.values())

# Construir grafo con networkx
G = nx.Graph()
for u in adj_list:
    for v in adj_list[u]:
        G.add_edge(u, v)

pos = nx.spring_layout(G, seed=42)

def graficar_coloraciones(coloraciones):
    for i, asignacion in enumerate(coloraciones):
        plt.figure()
        unique_colors = sorted(set(asignacion.values()))
        color_index = {c: idx for idx, c in enumerate(unique_colors)}

        node_colors = [color_index[asignacion[n]] for n in G.nodes()]

        nx.draw(
            G,
            pos,
            with_labels=True,
            node_color=node_colors,
            cmap=plt.cm.Set3, 
            edge_color='black',
            node_size=800,
            font_color='black',
            linewidths=1.5,
            edgecolors='black'
        )

        plt.title(f"Coloración única {i+1}")
        plt.show()


# Ejecutar
coloraciones_unicas = obtener_unicas(3)

print(f"Coloraciones únicas encontradas: {len(coloraciones_unicas)}")

graficar_coloraciones(coloraciones_unicas)