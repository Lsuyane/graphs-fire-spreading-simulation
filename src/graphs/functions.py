import random
from typing import Dict, List
from graphs import Graph


def predecessors_to_list(
    predecessors: Dict[str, str], distances: Dict[str, float]
) -> Dict[str, Dict[str, object]]:
    """Converts predecessors and distances into a structured path dictionary.

    This function constructs the shortest path for each vertex based on
    predecessor relationships and distances.

    Args:
        predecessors (Dict[str, str]): A dictionary mapping each vertex to its predecessor.
        distances (Dict[str, float]): A dictionary mapping each vertex to its shortest distance from the source.

    Returns:
        Dict[str, Dict[str, object]]: A dictionary where:
            - Each key is a vertex.
            - Each value is a dictionary containing:
                - "distance": The shortest distance to the vertex.
                - "path": The sequence of vertices forming the shortest path.
    """
    paths = {}

    for vertex, distance in distances.items():
        path = []
        predecessor = predecessors.get(vertex)

        while predecessor is not None:
            path.insert(0, predecessor)
            predecessor = predecessors.get(predecessor)

        path.append(vertex)
        paths[vertex] = {"distance": distance, "path": path}

    return paths


def random_vertices(graph: Graph, num_vertices: int = 1) -> List[str]:
    """Selects and returns a list of random vertices from the graph.

    This function retrieves a specified number of randomly selected vertices
    from the graph. If the graph is empty, an empty list is returned.

    Args:
        graph (Graph): The graph from which vertices are selected.
        num_vertices (int, optional): The number of vertices to select. Defaults to 1.

    Returns:
        List[str]: A list containing the randomly selected vertices.
    """
    return (
        [random.choice(list(graph.vertices)) for _ in range(num_vertices)]
        if graph.vertices
        else []
    )
