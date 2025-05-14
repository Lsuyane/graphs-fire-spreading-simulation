from typing import Dict, Tuple

from graphs import Graph


def input_edge() -> Tuple[str, str, float] | None:
    entry = input(
        "Insira os pares de vertices com peso separados por espaço ou enter para finalizar\nEx: v1 v2 3\n> "
    ).split()

    if len(entry) == 0 | len(entry) == 1 | len(entry) == 2:
        return None

    return (entry[0], entry[1], float(entry[2]))


def input_map() -> Graph:
    entry = input_edge()
    edges = []

    while entry is not None:
        edges.append(entry)
        entry = input_edge()

    return Graph(edges)


def input_vertex_float():
    entry = input(
        "Insira os pares de vertice e quantidades de água separados por espaço ou enter para finalizar\nEx: v1 3.5\n> "
    ).split()

    if len(entry) == 0:
        return None

    return (entry[0], float(entry[1]))


def input_water_per_vertex(graph: Graph) -> Dict[str, float]:
    edges = []

    for _ in graph.vertices:
        entry = input_vertex_float()
        edges.append(entry)

    return Graph(edges)
