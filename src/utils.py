from graphs import Graph
from maps import input_map, input_water_per_vertex


def truncate(number: float, decimal_places: int = 2) -> float:
    """Returns a trucated number into n decimal plates

    Args:
        number (float): the number to be trucated
        decimal_places (int): the number of places to trucante number

    Returns:
        float: A trucated number into n decimal places
    """
    scale_factor = 10**decimal_places
    return int(number * scale_factor) / float(scale_factor)


def print_map(graph: Graph):
    """
    Prints the adjacency list representation of a graph.
    Args:
        graph (Graph): The graph object containing vertices and their corresponding edges.
    The function iterates through the graph's edges list and prints each vertex
    along with its connected vertices in a formatted string.
    """

    print("{")

    for vertex, edge_list in graph.edges_list.items():
        print(
            f"  '{vertex}': {[destination for destination, _ in edge_list]},"
        )

    print("}")


def input_points(txt: str, min: int = 0):
    buff = input(txt).split()

    if len(buff) < min:
        raise ValueError(f"The vertex list must be has almost {min} vertices")

    return (i for i in buff)


def input_data():
    map = input_map()
    print("Indique a localização do:")

    start = input("- inicio do incendio: ")
    firefighters = input_points(
        "- postos de brigadistas (separados por espaço): ", 3
    )
    water = input_points("- fontes de agua (separados por espaço): ")

    wc = input("\nIndique capacidade de agua do caminhão: ")
    wpv = input_water_per_vertex(map)

    return {
        "map": map,
        "fire_start_position": start,
        "firefighters_positions": firefighters,
        "water_sources": water,
        "water_per_vertex": wpv,
        "firetruck_water_capacity": wc,
    }
