import abc
from itertools import groupby
from typing import Dict, List, Set, Tuple


class SimpleGraph(abc.ABC):
    """Abstract base class for a simple graph representation.

    This class defines the interface for a graph, including methods for
    accessing vertices, edges, neighborhoods, and weights, as well as
    methods for adding and removing vertices and edges.

    Attributes:
        vertices (Set[str]): A set of all vertices in the graph.
        edges_list (Dict[str, List[Tuple[str, float]]]):
            A dictionary where keys are vertex identifiers and values are
            lists of tuples representing edges and their weights.
    """

    @property
    @abc.abstractmethod
    def vertices(self) -> Set[str]:
        """Returns the set of graph vertices."""
        pass

    @property
    @abc.abstractmethod
    def edges_list(self) -> Dict[str, List[Tuple[str, float]]]:
        """Returns the adjacency list of the graph."""
        pass

    @abc.abstractmethod
    def neighborhood(self, vertex: str) -> List[str]:
        """Gets the neighboring vertices of a given vertex.

        Args:
            vertex (str): The vertex whose neighbors are to be retrieved.

        Returns:
            List[str]: A list of adjacent vertices.
        """
        pass

    @abc.abstractmethod
    def edges(
        self, origin: str, dest: str | None = None
    ) -> List[Tuple[str, float]]:
        """Retrieves edges from a given origin vertex.

        Args:
            origin (str): The origin vertex.
            dest (str, optional): If specified, returns edges between the
                origin and destination vertex. Otherwise, returns all edges
                originating from the vertex.

        Returns:
            List[Tuple[str, float]]: A list of edges with their weights.
        """
        pass

    @abc.abstractmethod
    def weight(self, origin: str, dest: str) -> float:
        """Gets the weight of an edge between two vertices.

        Args:
            origin (str): The origin vertex.
            dest (str): The destination vertex.

        Returns:
            float: The weight of the edge.
        """
        pass

    @abc.abstractmethod
    def add_vertex(self, vertices: List[str] | str) -> None:
        """Adds one or more vertices to the graph.

        Args:
            vertices (List[str] | str): A single vertex or a list of vertices.
        """
        pass

    @abc.abstractmethod
    def add_edge(self, origin: str, destination: str, distance: float) -> None:
        """Adds an edge between two vertices with the given weight.

        Args:
            origin (str): The origin vertex.
            destination (str): The destination vertex.
            distance (float): The weight of the edge.
        """
        pass

    @abc.abstractmethod
    def remove_vertex(self, vertex: str) -> None:
        """Removes a vertex and all associated edges from the graph.

        Args:
            vertex (str): The vertex to be removed.
        """
        pass


class Graph(SimpleGraph):
    """Represents a graph using an adjacency list.

    Attributes:
        __vertices (Set[str]): Set of graph vertices.
        __edge_list (Dict[str, List[Tuple[str, float]]]):
            Dictionary mapping each vertex to a list of tuples containing
            neighboring vertices and edge weights.
    """

    def __init__(self, edge_list: List[Tuple[str, str, float]] = []):
        """Initializes a graph with a list of edges.

        Args:
            edge_list (List[Tuple[str, str, float]]): A list of edges,
                where each edge is represented by a tuple containing
                the origin vertex, destination vertex, and weight.
        """
        self.__vertices: Set[str] = set()
        self.__edge_list: Dict[str, List[Tuple[str, float]]] = {}

        for edge in edge_list:
            self.add_edge(edge[0], edge[1], edge[2])

            # If it's not a self-loop, add the edge again in the reverse direction
            if edge[0] != edge[1]:
                self.add_edge(edge[1], edge[0], edge[2])

    @property
    def vertices(self) -> Set[str]:
        """Returns the set of graph vertices.

        Returns:
            Set[str]: The set of vertices.
        """
        return self.__vertices

    @property
    def edges_list(self) -> Dict[str, List[Tuple[str, float]]]:
        """Returns the adjacency list of the graph.

        Returns:
            Dict[str, List[Tuple[str, float]]]: The adjacency list dictionary.
        """
        return self.__edge_list

    def neighborhood(self, vertex: str) -> List[str]:
        """Gets the neighboring vertices of a given vertex.

        Args:
            vertex (str): The vertex whose neighbors are to be retrieved.

        Returns:
            List[str]: A list of adjacent vertices.
        """
        return {n[0] for n in self.__edge_list[vertex]}

    def edges(
        self, origin: str, dest: str | None = None
    ) -> List[Tuple[str, float]]:
        """Retrieves edges from a given origin vertex.

        Args:
            origin (str): The origin vertex.
            dest (str, optional): If specified, returns edges between the
                origin and destination vertex. Otherwise, returns all edges.

        Returns:
            List[Tuple[str, float]]: A list of edges with their weights.
        """
        _edges = [edge for edge in self.__edge_list[origin]]
        _edges.sort()

        return [
            item
            for key, group in groupby(_edges, lambda edge: edge[0])
            if key == dest or dest is None
            for item in group
        ]

    def weight(self, origin: str, dest: str) -> float:
        """Gets the weight of an edge between two vertices.

        Args:
            origin (str): The origin vertex.
            dest (str): The destination vertex.

        Returns:
            float: The weight of the edge.
        """
        return self.edges(origin, dest)[0][1]

    def add_vertex(self, vertices: List[str] | str) -> None:
        """Adds one or more vertices to the graph.

        Args:
            vertices (List[str] | str): A single vertex or a list of vertices.
        """
        if isinstance(vertices, str):
            self.__vertices.add(vertices)
        else:
            for vertex in vertices:
                self.__vertices.add(vertex)

    def add_edge(self, origin: str, destination: str, distance: float) -> None:
        """Adds an edge between two vertices with the given weight.

        Args:
            origin (str): The origin vertex.
            destination (str): The destination vertex.
            distance (float): The weight of the edge.
        """
        self.add_vertex([origin, destination])

        neighborhood = self.__edge_list.get(origin, [])
        neighborhood.append((destination, distance))

        self.__edge_list.update({origin: neighborhood})

    def remove_vertex(self, vertex: str) -> None:
        """Removes a vertex and all associated edges from the graph.

        Args:
            vertex (str): The vertex to be removed.
        """
        if vertex in self.__vertices:
            for vi in self.__vertices:
                neighborhood = self.__edge_list.get(vi, [])
                neighborhood = list(
                    filter(lambda t: t[0] != vertex, neighborhood)
                )
                self.__edge_list.update({vi: neighborhood})

            self.__edge_list.pop(vertex)
            self.__vertices.remove(vertex)

    def __repr__(self) -> str:
        """Returns a string representation of the graph's adjacency list."""
        return f"{self.edges_list}"
