from graph_tool.all import *
import itertools
import functools
from glob import glob
import os.path
import time

EPSILON = 0.001


def process_graph(edges):
    g = Graph(directed=False)
    vertex_labels = g.add_edge_list(edges, hashed=True)
    g.vertex_properties['labels'] = vertex_labels

    density = g.num_edges() / g.num_vertices()
    max_density = density

    print(f'threshold: undefined, edges: {g.num_edges()}, vertexes: {g.num_vertices()}, max_density: {max_density}')
    while g.num_vertices() != 0:
        threshold = 2 * (1 + EPSILON) * density
        to_remove = set()
        for v in g.vertices():
            if v.is_valid() and v.out_degree() <= threshold:
                to_remove.add(v)
        for v in reversed(sorted(to_remove)):
            g.remove_vertex(v) # also remove edges
        if g.num_vertices() == 0:
            break
        density = g.num_edges() / g.num_vertices()
        if density > max_density:
            max_density = density
        print(f'threshold: {threshold}, edges: {g.num_edges()}, vertexes: {g.num_vertices()}, max_density: {max_density}')


if __name__ == '__main__':
    inputs = glob(os.path.join("data", "ca-GrQc_preprocessed.txt"))
    for filename in inputs:
        with open(filename) as f:
            print(f'Processing {filename}')
            lines = f.readlines()
            edges = list(map(lambda l: tuple(l.split()), lines))
            process_graph(edges)

