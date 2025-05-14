import math
from fire import Allocator
from graphs import Graph, dijkstra
from typing import Dict, List
from events import EventListener, Event


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

    @property
    def location(self) -> str:
        return self._position

    @location.setter
    def location(self, location: str):
        if location not in self._map.vertices:
            raise ValueError(f"'{location}' is not a vertex in the graph")

        self._position = location

    @property
    def next_steps(self) -> str:
        return self._steps_queue

    @property
    def target(self) -> str | None:
        if len(self._targets_stack) > 0:
            return self._targets_stack[0]

        return None

    @property
    def id(self) -> int:
        return self._id

    @property
    def water_sources(self) -> List[str]:
        self.update_paths()
        return [
            i for i in list(self._water_positions + self._firefighter_posts)
        ]

    def add_target(self, target: str):
        if target not in self._map.vertices:
            raise ValueError(
                f"{target} is unreachable from {self.location} in {self._map}"
            )

        self._targets_stack.insert(0, target)

    def remove_target(self):
        self._targets_stack.pop(0)
        self.update_step_queue()

    def update_step_queue(self):
        target = self.target
        self.update_paths()

        if target:
            path = self._paths[target]["path"]
            self._steps_queue = path

    def nearest(self, vertices: List[str]) -> str | None:
        less_distance: float = math.inf
        nearest_vertex = None

        self.update_paths()

        for vertex, path in self._paths.items():
            if vertex in vertices:
                if less_distance > path["distance"]:
                    less_distance = path["distance"]
                    nearest_vertex = vertex

        return nearest_vertex

    def notify(self, event_type: str):
        e = Event(event_type, self.location, self._id)
        self._event_manager.notify_and_update(e)

    def schedule_move_to(self, destination: str):
        self.add_target(destination)
        self.update_step_queue()

    def schedule_refuel(self):
        vertex = self.nearest(self.water_sources)
        
        if self.location == vertex:
            self.refuel()

        else:
            self.schedule_move_to(vertex)

    def refuel(self):
        if (
            self.location in self.water_sources
            and self._tank_level < self._water_capacity
        ):
            self._tank_level = self._water_capacity
            self.notify(Event.ON_ALREADY)

    def put_out_fire(self):
        vertex = self.location
        water_needed = self._water_per_vertex.get(vertex)

        if water_needed is None:
            raise ValueError(
                "Not found water needed to put out fire in water_per_vertex dict"
            )

        if (
            vertex in self._on_fire_vertices
            and self._tank_level > water_needed
        ):
            self._tank_level -= water_needed
            self.notify(Event.ON_PUT_OUT)

            if self._tank_level < water_needed:
                self.notify(Event.ON_REFUEL)

        else:
            self.notify(Event.ON_REFUEL)

    def update_paths(self):
        self._paths = dijkstra(self._map, self._position)

    def already(self):
        e = Event(Event.ON_ALREADY, self.location, self._id)
        self._event_manager.notify(e)

    def handle(self, event: Event):
        if event.type == Event.ON_GET_FIRE:
            self._on_fire_vertices.append(event.target)

        if event.type == Event.ON_PUT_OUT:
            try:
                self._on_fire_vertices.remove(event.target)
            except ValueError:
                pass

        if event.type == Event.ON_WAIT:
            self._waiting = True

        if event.type == Event.ON_CONTINUE:
            self._waiting = False

    def update(self):
        if not self._waiting:
            if len(self._steps_queue) > 0:
                self.location = self._steps_queue.pop(0)
                self._event_manager.notify(Event(Event.ON_MOVE, self.location, self._id))

                if self.location == self.target:
                    if self.target in self._on_fire_vertices:
                        self.put_out_fire()

                    if self.target in self.water_sources:
                        self.refuel()

                    self.remove_target()

                else:
                    if self.location in self._on_fire_vertices:
                        self.put_out_fire()

                    if self.location in self.water_sources:
                        self.refuel()

            if len(self._targets_stack) == 0:
                self.already()

    def __repr__(self):
        return f"FireTruck({self.id}, {self._tank_level}, {self.target})"
