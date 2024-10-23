from flask import Flask, render_template, jsonify
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

# Punto de entrada de la aplicación
if __name__ == '__main__':
    app.run(debug=True)
