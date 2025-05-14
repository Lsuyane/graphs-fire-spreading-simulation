import math
from graphs.graph import SimpleGraph
from typing import Dict, List, Set, Tuple, Union
from graphs.functions import predecessors_to_list

def dijkstra(graph: SimpleGraph, origin: str) -> Dict[str, Dict[str, Union[float, List[str]]]]:
    """Computes the shortest paths from a given origin vertex using Dijkstra's algorithm.

    This function calculates the shortest distances from the origin vertex to 
    all other reachable vertices in the graph and returns a dictionary containing 
    the distances and the shortest paths.

    Args:
        graph (SimpleGraph): The graph on which the algorithm is applied.
        origin (str): The starting vertex for path calculations.

    Returns:
        Dict[str, Dict[str, Union[float, List[str]]]]: A dictionary containing:
            - "distances": A dictionary where keys are vertices and values are shortest distances.
            - "paths": A dictionary mapping each vertex to the shortest path from the origin.
    """
    distances: Dict[str, float] = dict()
    predecessors: Dict[str, str] = dict()
    visited_vertices: Set[str] = set()
    frontier_queue: List[Tuple[float, str]] = []

    for vertex in graph.vertices:
        distances[vertex] = math.inf
        predecessors[vertex] = None

    distances[origin] = 0
    frontier_queue.append((0, origin))

    while frontier_queue:
        frontier_queue.sort(key=lambda x: x[0])
        current_distance, predecessor = frontier_queue.pop(0)
        visited_vertices.add(predecessor)

        for neighbor in graph.neighborhood(predecessor):
            if neighbor not in visited_vertices:
                neighbor_distance = distances[neighbor]
                new_neighbor_distance = current_distance + graph.weight(predecessor, neighbor)

                if new_neighbor_distance < neighbor_distance:
                    distances[neighbor] = new_neighbor_distance
                    predecessors[neighbor] = predecessor
                    frontier_queue.append((new_neighbor_distance, neighbor))

    return predecessors_to_list(predecessors, distances)


def breadth_first_search(graph: SimpleGraph, origin: str) -> Dict[str, Dict[str, Union[float, List[str]]]]:
    """Performs a breadth-first search (BFS) starting from the given origin vertex.

    BFS finds the shortest path in an unweighted graph by exploring neighbors layer by layer.

    Args:
        graph (SimpleGraph): The graph on which the algorithm is applied.
        origin (str): The starting vertex for path calculations.

    Returns:
        Dict[str, Dict[str, Union[float, List[str]]]]: A dictionary containing:
            - "distances": A dictionary where keys are vertices and values are shortest distances in terms of hops.
            - "paths": A dictionary mapping each vertex to the shortest path from the origin.
    """
    distances: Dict[str, float] = dict()
    predecessors: Dict[str, str] = dict()
    frontier_queue: List[Tuple[float, str]] = []

    for vertex in graph.vertices:
        distances[vertex] = math.inf
        predecessors[vertex] = None

    distances[origin] = 0
    frontier_queue.append((0, origin))

    while frontier_queue:
        current_distance, predecessor = frontier_queue.pop(0)

        for neighbor in graph.neighborhood(predecessor):
            if math.isinf(distances[neighbor]):
                neighbor_distance = current_distance + 1
                distances[neighbor] = neighbor_distance
                predecessors[neighbor] = predecessor
                frontier_queue.append((neighbor_distance, neighbor))

    return predecessors_to_list(predecessors, distances)
