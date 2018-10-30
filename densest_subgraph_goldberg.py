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
    g = m/2
    for v in network.vertices():
        if v == s or v == t:
            continue

        # add source -> vertex edges, set all edge capacity to m
        sv = network.add_edge(s, v, add_missing=False)
        cap[sv] = m

        # add vertex -> sink edges, set all edge capacity to m + 2g - deg(v)
        vt = network.add_edge(v, t, add_missing=False)
        cap[vt] = m + 2 * g - deg[v]

    # sanity check
    v = set(list(itertools.chain(*graph)))
    assert(network.num_vertices() == len(v) + 2)
    assert(network.num_edges() == 2*m + 2*len(v))

    return network


if __name__ == '__main__':
    # 1, 2, 3, 4 fully connected, 5 only connected to 1
    graph = [(5, 1),
            (1, 2), (1, 3), (1, 4),
            (2, 3), (2, 4),
            (3, 4)]
    network = undirected_to_flow_network(graph)
