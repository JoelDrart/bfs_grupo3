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
    G.add_edges_from([(1, 2), (2, 3), (3, 4), (4, 1)])
    graph_data = nx.node_link_data(G)
    return jsonify(graph_data)


@app.route('/process_graph', methods=['POST'])
def process_graph():
    data = request.json
    G = nx.Graph()
    print('Grafo recibido:')
    # Convertir los datos del grafo en un objeto NetworkX
    for element in data:
        if element['group'] == 'nodes':
            G.add_node(element['data']['id'])
        elif element['group'] == 'edges':
            G.add_edge(element['data']['source'], element['data']['target'])

    print(G)
    # Ejecutar BFS desde un nodo (puedes cambiar el nodo inicial)
    start_node = list(G.nodes)[0]  # Tomar el primer nodo como inicio
    visited_nodes, parents = bfs_tree(G, start_node)

    # Construir el árbol de búsqueda a partir de los padres
    tree_edges = [(parent, child) for child, parent in parents.items() if parent is not None]

    return jsonify({
        'visited_nodes': visited_nodes,
        'bfs_tree': tree_edges
    })

def bfs_tree(graph, start):
    visited = []  # Lista para nodos visitados
    queue = [start]  # Cola para manejar nodos a explorar
    parent = {start: None}  # Diccionario para registrar padres

    while queue:
        node = queue.pop(0)  # Extraer el primer nodo de la cola
        if node not in visited:
            visited.append(node)  # Marcar el nodo como visitado
            for neighbor in graph[node]:
                if neighbor not in visited and neighbor not in queue:
                    queue.append(neighbor)  # Agregar vecinos no visitados a la cola
                    parent[neighbor] = node  # Registrar el nodo padre

    return visited, parent

# Punto de entrada de la aplicación
if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
