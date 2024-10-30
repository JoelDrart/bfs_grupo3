from flask import Flask, render_template, jsonify, request
import networkx as nx

# Inicializar la aplicación Flask
app = Flask(__name__)

# Definir la ruta principal
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/graph')
def get_graph():
    G = nx.Graph()
    
    #G.add_edges_from([(1, 2), (2, 3), (3, 4), (4, 1), (1,5), (5,6), (6,7), (7,1), (2,5), (3,6), (4,7)])
    #G.add_edges_from([(1,5), (1,2), (5,4), (5,2), (2,3), (4,6), (3,4)])
    
    # Lista de capitalesx de provincia de Ecuador
    capitales = [
        "Quito", "Guayaquil", "Cuenca", "Loja", "Ambato", "Riobamba", 
        "Machala", "Portoviejo", "Manta", "Esmeraldas", "Ibarra", 
        "Tulcán", "Latacunga", "Tena", "Macas", "Nueva Loja", 
        "Santo Domingo", "Zamora", "Babahoyo", "Puyo", "Guaranda", "Coca", "Santa Elena",
        "Azogues"
    ]

    # Añadir nodos (ciudades)
    G.add_nodes_from(capitales)

    # Añadir bordes (conexiones entre ciudades capitales cercanas)
    edges = [
        ("Quito", "Ibarra"), ("Quito", "Latacunga"), ("Quito", "Santo Domingo"),
        ("Guayaquil", "Portoviejo"), ("Guayaquil", "Babahoyo"), 
        ("Cuenca", "Loja"), ("Cuenca", "Machala"), ("Cuenca", "Azogues"),
        ("Ambato", "Latacunga"), ("Ambato", "Riobamba"), ("Ambato", "Tena"),
        ("Riobamba", "Macas"), ("Coca", "Tena"),
        ("Loja", "Zamora"), ("Macas", "Puyo"), ("Ambato", "Puyo"),
        ("Tulcán", "Ibarra"), ("Manta", "Portoviejo"), ("Nueva Loja", "Tena"),
        ("Esmeraldas", "Santo Domingo"), ("Guaranda", "Ambato"), ("Guaranda", "Riobamba"), 
        ("Guaranda", "Babahoyo"), ("Tulcán", "Esmeraldas"),
        ("Nueva Loja", "Coca"), ("Ibarra", "Esmeraldas"), ("Santo Domingo", "Portoviejo"),
        ("Esmeraldas", "Manta"), ("Manta", "Portoviejo"),
        ("Santa Elena", "Portoviejo"), ("Santa Elena", "Guayaquil"), ("Santa Elena", "Manta"),
        ("Azogues", "Macas"), ("Azogues", "Riobamba"),
        ("Machala","Loja"), ("Macas", "Zamora"), ("Riobamba", "Puyo"), ("Nueva Loja","Tulcán")
        
    ]
    
    G.add_edges_from(edges)
    
    graph_data = nx.node_link_data(G)
    return jsonify(graph_data)


@app.route('/process_graph', methods=['POST'])
def process_graph():
    data = request.json
    elements = data['elements']
    start_node = data['startNode']
    
    print('>Datos recibidos:')
    #print(data)
    
    print('>Elementos recibidos:')
    # print(elements)
    print('>Nodo inicial recibido:', start_node)
    
    G = nx.Graph()
    print('>Grafo recibido:')
    # Convertir los datos del grafo en un objeto NetworkX
    for element in elements:
        if element['group'] == 'nodes':
            G.add_node(element['data']['id'])
        elif element['group'] == 'edges':
            G.add_edge(element['data']['source'], element['data']['target'])

    print(G)
    # Ejecutar BFS desde un nodo (puedes cambiar el nodo inicial)
    print('Nodo inicial:', start_node)
    visited_nodes, parents, levels = bfs_tree(G, start_node)

    # Construir el árbol de búsqueda a partir de los padres y añadir los niveles a los nombres de los nodos
    tree_edges = [(parents[child], child) for child in parents if parents[child] is not None]
    labeled_nodes = [f"{node}-{levels[node]}" for node in visited_nodes]


    return jsonify({
        'visited_nodes': labeled_nodes,
        'bfs_tree': tree_edges
    })


def bfs_tree(graph, start):
    visited = []  # Lista para nodos visitados
    queue = [(start, 0)]  # Cola para manejar nodos y sus niveles
    parent = {start: None}  # Diccionario para registrar padres
    levels = {start: 0}  # Diccionario para registrar niveles de cada nodo

    while queue:
        node, level = queue.pop(0)  # Extraer el primer nodo y su nivel de la cola
        if node not in visited:
            visited.append(node)  # Marcar el nodo como visitado
            for neighbor in graph[node]:
                if neighbor not in visited and neighbor not in [n[0] for n in queue]:
                    queue.append((neighbor, level + 1))  # Agregar vecino con su nivel
                    parent[neighbor] = node  # Registrar el nodo padre
                    levels[neighbor] = level + 1  # Registrar el nivel del vecino

    return visited, parent, levels

# Punto de entrada de la aplicación
if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
