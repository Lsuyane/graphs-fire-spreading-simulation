# Projeto de Grafos

## Como usar

Com o python instalado basta abrir a pasta na sua IDE de preferencia como o vscode e executar ou o arquivo src/__main__.py ou ainda usar o terminal na pasta do projeto para copiar colar o seguinte comando:

```
python src
```

## Projeto

O aplicativo é dividido em módulos, cada um com responsabilidades bem definidas para facilitar a manutenção e a escalabilidade do projeto. A seguir, detalhamos cada módulo e suas funcionalidades:

### Módulo `graph`

Este módulo implementa a estrutura de grafos utilizando listas de adjacência, com suporte a pesos nas arestas. Ele inclui os algoritmos de Dijkstra e BFS, ambos adaptados para retornar, além dos custos, os caminhos mínimos.

Os grafos implementados são simples e direcionados, mas podem ser utilizados como não direcionados ao adicionar arestas que invertem os pares ordenados. Este módulo é a base para a representação e manipulação da estrutura de dados do grafo.

O grafo e implementado a partir de uma interface `SimpleGraph` que está lá so para podermos definir e encapsular funções

Enquanto que a classe Graph implementa os grafos utilizando como base a estrutura Dict do python que armezena dados a partir de chaves e valores como em um hash table assim podemos criar as listas de adjacencia da seguinte forma as chaves são o vertice v é o valor do vertice v e a lista de adjacencias de v com os pesos das arestas por exemplo

Se temos o grafo G tal que V = [a, b, c] e E = [(a b), (a c), (b ,c)] com pesos respectivamente 1, 2, 3 temos que ao utilizar dicts teremos

```python
adjacency_list = {
    "a": [("b", 1), ("c", 2)]
    "b": [("a", 1), ("c", 3)]
    "c": [("a", 2), ("b", 3)]
}
```

Além disso a classe Graph que representa um digrafo também apresnta alguns metodos uteis como Neighborhood
que retorna N(G)

```python
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
```

### Módulo `event`

O módulo `event` implementa o padrão de projeto Observer. Ele contém uma classe que notifica mudanças para outras partes do sistema. Por exemplo, sempre que ocorre uma alteração na simulação, a classe `Firefighter` notifica todas as outras entidades. Cada entidade reage de acordo com sua função: os caminhões de bombeiros são informados sobre um incêndio em um local específico e se dirigem até lá, enquanto o logger registra o evento e exibe no console.

```python
class EventListener(ABC):
    """Abstract base class for any object that listens to events."""

    @abstractmethod
    def handle(self, event: Event):
        """Handles an incoming event.

        Args:
            event (Event): The event to handle.
        """
        pass


class EventPool(ABC):
    """Manages event state and notifies listeners of changes."""

    def __init__(self):
        """Initializes the EventPool with an initial start event."""
        self._listeners: List[EventListener] = []
        self._state = Event.on_start()

    @property
    def event(self) -> Event:
        """Returns the current event state.

        Returns:
            Event: The current event.
        """
        return self._state

    @property
    def listeners(self) -> List[EventListener]:
        """Returns all registered event listeners.

        Returns:
            List[EventListener]: A list of event listeners.
        """
        return self._listeners

    def listen(self, event_listener: EventListener):
        """Registers a new event listener.

        Args:
            event_listener (EventListener): The listener to register.
        """
        self._listeners.append(event_listener)

    def unlisten(self, event_listener: EventListener):
        """Unregisters an existing event listener.

        Args:
            event_listener (EventListener): The listener to remove.
        """
        self._listeners.remove(event_listener)

    def notify(self, event: Event):
        """Notifies all listeners about a new event and updates state.

        Args:
            event (Event): The event to dispatch.
        """
        self._state = event

        for i in self.listeners:
            i.handle(event)

```

## Módulo `fire`

As classes `Firefighter` e `Firetruck` implementam o padrão de projeto Worker. Nesse padrão, a classe `Firefighter` atua como comandante, enquanto a classe `Firetruck` executa as ordens. Isso garante que dois caminhões de bombeiros não sejam enviados ao mesmo vértice desnecessariamente, otimizando os recursos.

O módulo `fire` também controla como o incêndio se propaga e como as entidades interagem com ele. Ele gerencia as ações dos bombeiros, garantindo que o comportamento do sistema seja consistente e realista.

```python
class FireTruck(EventListener):
    def __init__(
        self,
        map: Graph,
        truck_index: int,
        start_position: str,
        tank_water_capacity: float,
        water_per_vertex: Dict[str, float],
        water_positions: List[str],
        firefighter_posts: List[str],
        event_manager: Allocator,
    ):
        self._id = truck_index
        self._map = map
        self._position = start_position
        self._tank_level = tank_water_capacity
        self._water_capacity = tank_water_capacity
        self._water_per_vertex = water_per_vertex
        self._water_positions = water_positions
        self._firefighter_posts = firefighter_posts
        self._event_manager = event_manager
        self._targets_stack = []
        self._steps_queue = []
        self._on_fire_vertices = []
        self._waiting = False

        if tank_water_capacity <= 0:
            raise ValueError(
                f"water_capacity needs be greather than zero but is '{tank_water_capacity}'."
            )

        for _, water in water_per_vertex.items():
            if water <= 0:
                raise ValueError(
                    f"water_capacity needs be greather than zero but is '{tank_water_capacity}'."
                )

```

### Módulo `map`

Este módulo é responsável por gerar mapas de forma automática, criando uma matriz `n x n`. Também é possível inserir manualmente o mapa, permitindo maior flexibilidade na configuração do ambiente da simulação.

```python

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

```

### Módulo `logs`

O módulo `logs` é responsável por registrar os eventos da simulação em um relatório. Este relatório pode ser exibido no console ou salvo em um arquivo na pasta `output`, permitindo uma análise posterior dos dados.

Incluem uma classe para calculo de consumo de agua, vertices queimados e tempo de simulação

```python
from typing import Dict
from events import Event, EventListener


class WaterCount(EventListener):,
    def __init__(self, water_per_vertex: Dict[str, float]):
        self._countage = 0
        self._water_per_vertex = water_per_vertex

    @property
    def count(self) -> float:
        return self._countage

    def handle(self, event):
        if event.type == Event.ON_PUT_OUT:
            self._countage += self._water_per_vertex[event.target]
```

### Arquitetura do Projeto\n"

Toda a aplicação foi desenvolvida com base nos princípios de Programação Orientada a Objetos (OOP) e utiliza padrões de projeto para garantir modularidade e reutilização de código. A combinação dos padrões Observer e Worker, juntamente com a estrutura modular, torna o sistema robusto e fácil de entender.
Este projeto foi projetado para ser extensível, permitindo a adição de novos recursos e funcionalidades no futuro.

## Estrategias de performace\n"

A ideia do algoritmo e é a seguinte, assim que se inicia a simulaçao o fogo se expande para a distancia atual + 1, comteplando todos os vizinhos distantes em 1. A classe gerenciadora atribui tarefas para as classes trabalhadoras, assim elas recebem um objetivo, calculam a distancia até ele e o caminho em seguida ao apagar o fogo notificam a classe genrenciadora para que outro caminhão não vá lá, caso não consigua apagar o fogo notifica a classe gerenciadora e pede para encher o tanque, o objetivo atual vai para uma fila de objetivos futuros enquanto a recarga não é feita em seguida ao recarregar a classe gereciadora é notificada. A cada passo do caminhão se houver fogo ou ponto de agua ele apaga e enche o tank assim como o fogo não volta ele economiza tempo, como ele notifica caso um caminha estivesse indo para lá ele e notificado e classe gerenciadora dá outro objetivo a ele.
