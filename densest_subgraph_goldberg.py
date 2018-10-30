from graph_tool.all import *
import itertools


def undirected_to_flow_network(graph):
    graph_reversed = [(y, x) for (x, y) in graph]
    directed_edges = graph + graph_reversed
    network = Graph()
    vertex_labels = network.add_edge_list(directed_edges, hashed=True)
    network.vertex_properties['labels'] = vertex_labels

    deg = network.degree_property_map('out')
    network.vertex_properties['degrees'] = deg # original graph vertex degrees

    # set all internal edge capacity to 1
    cap = network.new_edge_property("int")
    for e in network.edges():
        cap[e] = 1
    network.edge_properties["cap"] = cap

    # add source & sink vertices
    s = network.add_vertex()
    vertex_labels[s] = 's'
    t = network.add_vertex()
    vertex_labels[t] = 't'

    m = len(graph) # original edges
    for v in network.vertices():
        if v == s or v == t:
            continue

        # add source -> vertex edges, set all edge capacity to m
        sv = network.add_edge(s, v, add_missing=False)
        cap[sv] = m

        # add vertex -> sink edges, set edge capacity later
        vt = network.add_edge(v, t, add_missing=False)

    # sanity check
    v = set(list(itertools.chain(*graph)))
    assert(network.num_vertices() == len(v) + 2)
    assert(network.num_edges() == 2*m + 2*len(v))

    return network, s, t


def update_sink_edge_weights(network, s, t, m, g):
    deg = network.vertex_properties['degrees']
    cap = network.edge_properties["cap"]
    for e in t.in_edges():
        # set all sink edge capacity to m + 2g - deg(v)
        cap[e] = m + 2 * g - deg[e.source()]
    return network, s, t


def densest_subgraph(network, s, t):
    n = network.num_vertices() - 2
    m = (network.num_edges() - 2*n) / 2
    l = 0
    u = m
    V = None
    while u - l >= 1/(n * (n-1)):
        g = (u + l) / 2
        update_sink_edge_weights(network, s, t, m, g)
        cap = network.edge_properties["cap"]
        residual = push_relabel_max_flow(network, s, t, cap) # O(V^3) = O(n^3)
        partition = min_st_cut(network, s, cap, residual) # O(V+E) = O(n+m)
        # Vertices with value True belong to the source side of the cut
        partition[s] = False # remove source node from source partition for convenient view return
        view = GraphView(network, vfilt=partition)
        if view.num_vertices() == 0:
            u = g
        else:
            l = g
            V = view
    return V


if __name__ == '__main__':
    # 1, 2, 3, 4 fully connected, 5 only connected to 1
    graph = [
            ('5', '1'),
            ('1', '2'), ('1', '3'), ('1', '4'),
            ('2', '3'), ('2', '4'),
            ('3', '4')]
    network, s, t = undirected_to_flow_network(graph)
    subgraph_view = densest_subgraph(network, s, t)
    lab = subgraph_view.vertex_properties['labels']
    sub_vertices = set([lab[v] for v in lab])
    subgraph_edges = []
    for e in graph:
        if e[0] in sub_vertices and e[1] in sub_vertices:
            subgraph_edges.append(e)
    subgraph = Graph(directed=False)
    vertex_labels = subgraph.add_edge_list(subgraph_edges, hashed=True)
    graph_draw(subgraph, vertex_text=vertex_labels,
               output="densest_subgraph.png")
