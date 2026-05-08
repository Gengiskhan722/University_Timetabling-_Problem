#Benemerita Universidad Autonoma de Puebla
#Desarrollado por: Jose Ernesto Munoz Cabanas 
#Facultad de Ciencias de la Computacion
#Proyecto para proceso de admision a la Maestria en sistemas distribuidos
#Implementacion de representacion grafica de un grafo de conflictos y aplicacion de algoritmos de coloreo para
#la optimizacion de University Timetabling Problem.
#Librerias
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import networkx as nx
from tkinter import messagebox

#Construccion del grafo de conflictos en base a lista de adyacencia
def construir_grafo(adj):
    G = nx.Graph()
    for u in adj:
        for v in adj[u]:
            G.add_edge(u, v)
    return G

# ALGORITMOS

#Algoritmo de coloreo secuencial vorazon Greedy
def greedy(adj):
    colores = {}
    for nodo in adj:
        usados = {colores.get(v) for v in adj[nodo] if v in colores}
        c = 1
        while c in usados:
            c += 1
        colores[nodo] = c
    return colores

#Algoritmo de coloreo de Daniel Brelaz DSATUR 
def dsatur(adj):
    vertices = list(adj.keys())
    col = {v: None for v in vertices}

    def sat(v):
        return len({col[u] for u in adj[v] if col[u]})
    #mMientras haya vértices sin colorear sigue el proceso
    while None in col.values():
        v = max([x for x in vertices if col[x] is None],
                key=lambda x: (sat(x), len(adj[x]))) # Compara tuplas de grado de saturacion y grado general para todos los elementos dentro de x

        usados = {col[u] for u in adj[v] if col[u]}
        c = 1
        while c in usados:
            c += 1
        col[v] = c

    return col

#Algorito de coloreo exacto de BROWN
def brown(adj):
    #Grafica y obtiene el límite superior en el peor caso que equivale al número n de vértices.
    G = construir_grafo(adj)
    best = None
    ub = len(G.nodes())

    def backtrack(coloring):
        nonlocal best, ub

        if len(coloring) == len(G.nodes()):
            used = len(set(coloring.values()))
            if best is None or used < ub:
                ub = used
                best = coloring.copy()
            return

        if len(set(coloring.values())) >= ub:
            return

        uncolored = [v for v in G.nodes() if v not in coloring]
        v = max(uncolored, key=lambda x: G.degree[x])

        usados = {coloring[n] for n in G.neighbors(v) if n in coloring}

        for c in range(1, ub+1):
            if c not in usados:
                coloring[v] = c
                backtrack(coloring) 
                del coloring[v]

    backtrack({})
    return best

#Lectura de lista de adyacencia definida por el usuario o para el grafo de clases
class EntradaGrafo:
    def __init__(self, root, callback):
        self.root = root
        self.callback = callback

        self.frame = tk.Frame(root)
        self.frame.pack(fill="both", expand=True)

        tk.Label(self.frame, text="Número de vértices", font=("Arial", 14)).pack(pady=10)

        self.entry_n = tk.Entry(self.frame)
        self.entry_n.pack(pady=5)

        tk.Button(self.frame, text="Generar tabla", command=self.generar_tabla).pack(pady=10)
        tk.Button(self.frame, text="Grafo de clases",command=self.cargar_grafo_clases).pack(pady=5)

        self.tabla_frame = tk.Frame(self.frame)
        self.tabla_frame.pack()

        self.filas = []
    #Se genera un form para que el usuario pueda introducir su lista de adyacencia
    def generar_tabla(self):
        for widget in self.tabla_frame.winfo_children():
            widget.destroy()

        self.filas = []
        
        valor = self.entry_n.get().strip()
        # Validar que no esté vacío
        if not valor:
            messagebox.showerror("Error", "Ingrese un número de vértices")
            return

        # Validar que sea número entero
        if not valor.isdigit():
            messagebox.showerror("Error", "Solo se permiten números enteros positivos")
            return

        n = int(valor)

        # Validar que sea mayor que 0
        if n <= 0:
            messagebox.showerror("Error", "El número debe ser mayor que 0")
            return
        
        if n > 50:
            messagebox.showerror("Error", "Máximo 50 vértices permitido")
            return
        

        tk.Label(self.tabla_frame, text="Vértice", width=10).grid(row=0, column=0)
        tk.Label(self.tabla_frame, text="Adyacencias (coma)", width=30).grid(row=0, column=1)

        for i in range(n):
            v = tk.Entry(self.tabla_frame)
            a = tk.Entry(self.tabla_frame)

            v.grid(row=i+1, column=0, padx=5, pady=2)
            a.grid(row=i+1, column=1, padx=5, pady=2)

            self.filas.append((v, a))

        tk.Button(self.frame, text="Continuar", command=self.procesar).pack(pady=20)

    #Se crea la lista de adyacencia como estructura de datos 
    def procesar(self):
        adj = {}

        for v_entry, a_entry in self.filas:
            v = v_entry.get().strip()
            vecinos = a_entry.get().strip()

            if not v:
                continue

            lista = [x.strip() for x in vecinos.split(",")] if vecinos else []
            adj[v] = lista

        if not adj:
            messagebox.showerror("Error", "Sin datos")
            return

        # Validación básica
        for v in adj:
            for u in adj[v]:
                if u not in adj:
                    messagebox.showerror("Error", f"El nodo {u} no existe")
                    return

        self.frame.destroy()
        self.callback(adj)
    #Se carga la lista de adyacencia predefinida para nuestro problema de grafo de clases
    def cargar_grafo_clases(self):
        adj = {
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

        self.frame.destroy()
        self.callback(adj)

# INTERFAZ
class App:
    def __init__(self, root, adj_list, callback):
        self.root = root
        self.root.title("Coloreo de Grafos")
        self.root.geometry("900x600")
        self.callback = callback
        self.adj = adj_list
        self.G = construir_grafo(self.adj)

        # Layout principal
        self.frame_left = tk.Frame(root, width=200, bg="#2c3e50")
        self.frame_left.pack(side="left", fill="y")

        self.frame_right = tk.Frame(root)
        self.frame_right.pack(side="right", fill="both", expand=True)

        # Botones
        tk.Label(self.frame_left, text="Algoritmos",
                 bg="#2c3e50", fg="white",
                 font=("Arial", 14, "bold")).pack(pady=20)

        tk.Button(self.frame_left, text="Ver Grafo",
                  command=self.ver_grafo, width=20).pack(pady=10)

        tk.Button(self.frame_left, text="Greedy",
                  command=self.ejecutar_greedy, width=20).pack(pady=10)

        tk.Button(self.frame_left, text="DSATUR",
                  command=self.ejecutar_dsatur, width=20).pack(pady=10)

        tk.Button(self.frame_left, text="Brown",
                  command=self.ejecutar_brown, width=20).pack(pady=10)

        tk.Button(self.frame_left, text="Salir",
                  command=root.quit, width=20).pack(pady=30)
        
        tk.Button(self.frame_left, text="Regresar",
          command=self.regresar_menu, width=20).pack(pady=10)

        # Canvas matplotlib
        self.fig, self.ax = plt.subplots(figsize=(5, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame_right)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        self.pos = nx.spring_layout(self.G,k=1.5, iterations=100, seed=42)

        self.dibujar()

    # DIBUJO de los grafos y coloreos resultantes
    def dibujar(self, colores=None, titulo="Grafo"):
        self.ax.clear()
        if colores:
            node_colors = [
            "#ff0000" if colores[n] == 1 else
            "#00cc00" if colores[n] == 2 else
            "#ffd700" if colores[n] == 3 else
            "#87cefa"
            for n in self.G.nodes()
            ]
        else:
            node_colors = "white"
        nx.draw(
            self.G, self.pos,
            ax=self.ax,
            with_labels=True,
            node_color=node_colors,
            edgecolors="black",
            node_size=1000
        )

        self.ax.set_title(titulo)
        self.canvas.draw()

    # ACCIONES
    def ver_grafo(self):
        self.dibujar(titulo="Grafo de Conflictos")

    def ejecutar_greedy(self):
        colores = greedy(self.adj)
        self.dibujar(colores, "Greedy")

    def ejecutar_dsatur(self):
        colores = dsatur(self.adj)
        self.dibujar(colores, "DSATUR")

    def ejecutar_brown(self):
        colores = brown(self.adj)
        self.dibujar(colores, "Brown (Óptimo)")

    def regresar_menu(self):
        self.frame_left.destroy()
        self.frame_right.destroy()
        EntradaGrafo(self.root, self.callback)


# EJECUCIÓN del main para lanzar aplicacion
root = tk.Tk()
root.title("Coloreo de Grafos - Sistema de Horarios")
root.geometry("900x600")

def lanzar_app(adj_list):
    App(root, adj_list,lanzar_app)

EntradaGrafo(root, lanzar_app)

root.mainloop()
