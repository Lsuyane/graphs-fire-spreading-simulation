import math

from typing import List, Tuple

from graphs import Graph


def generate_vertices_names(
    vertices_number: int = 26, vertices_labels: List[str] | None = None
) -> List[str]:
    """Generates a list of vertex names based on the specified number of vertices and optional labels.

    If the number of vertices exceeds the number of provided labels, the labels are repeated with an appended index starting from 1.

    Args:
        vertices_number (int): The total number of vertices to generate. Defaults to 26.
        vertices_labels (List[str] | None): A list of labels to use for the vertices.
            If None, the labels default to the English alphabet (a-z).

    Returns:
        List[str]: A list of generated vertex names, where each name is a combination
        of a label (uppercase) and an optional numeric suffix for repeated labels.
    """
    vertices = []

    labels = (
        vertices_labels
        if vertices_labels is not None
        else list("abcdefghijklmnopqrstuvwxyz")
    )

    # fixes an empty label list
    if len(labels) == 0:
        labels = [""]

    num_labels = len(labels)
    len_vertex_name = math.ceil(vertices_number / num_labels)
    vertex_count = 0
    numeric_suffix = ""

    for index in range(len_vertex_name):
        if len_vertex_name > 1:
            numeric_suffix = index + 1

        for label in labels:
            vertex_name = f"{label.upper()}{numeric_suffix}"
            vertices.append(vertex_name)
            vertex_count += 1

            if vertex_count >= vertices_number:
                break

    return vertices


def create_shape(shape: int | Tuple[int, int]) -> Tuple[int, int]:
    """Retuers a tuple representings rows and cols of a map

    Args:
        shape(int|Tuple[int, int]): A number of rows and cols

    Returns:
        tuple: A tuple with row and cols number

    """
    if isinstance(shape, Tuple):
        row_number, col_number = shape
    else:
        row_number = shape
        col_number = shape

    return (row_number, col_number)


def link_vertices_in_row(vertex_names: List[str]):
    edges = []
    previous_vertex = None

    for counter, current_vertex in enumerate(vertex_names):
        if previous_vertex is not None:
            edges.append((previous_vertex, current_vertex, 1))
        else:
            previous_vertex = current_vertex

    return edges


def link_vertices_in_col(previous_row: List[str], current_row: List[str]):
    edges = []

    if len(previous_row) != len(current_row):
        raise ValueError("The lines must be the same length")

    for i in range(len(current_row)):
        edges.append((previous_row[i], current_row[i], 1))

    return edges


def generate_map(
    map_shape: int | Tuple[int, int] = 26,
    vertices_labels: List[str] | None = None,
) -> Graph:
    iteration = 0
    rows = []
    edges = []
    current_row = []
    row_number, col_number = create_shape(map_shape)

    vertices_number = row_number * col_number
    vertex_names = generate_vertices_names(vertices_number, vertices_labels)

    # splits the vertex in rows
    for vertex in vertex_names:
        current_row.append(vertex)
        iteration += 1

        if iteration == col_number:
            rows.append(current_row)
            current_row = []
            iteration = 0

    # created all edges between vertices
    for i in range(len(rows)):
        j = i + 1

        edges += link_vertices_in_row(rows[i])

        if j < len(rows):
            edges += link_vertices_in_row(rows[j])
            edges += link_vertices_in_col(rows[i], rows[j])

    return Graph(edges)
