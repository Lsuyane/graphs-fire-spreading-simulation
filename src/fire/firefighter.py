from typing import Dict, List, Set

from fire import FireTruck, Allocator
from graphs import Graph, breadth_first_search
from events import Event, EventPool


class FireFighter(Allocator):
    def __init__(
        self,
        map: Graph,
        start_fire_vertex: str,
        positions: List[str],
        tank_water_capacity: float,
        water_per_vertex: Dict[str, float],
        water_sources: List[str],
        event_pool: EventPool,
    ):
        self._map = map
        self._water_per_vertex = water_per_vertex
        self._on_fire_vertices = [start_fire_vertex]
        self._burned_vertices = set()
        self._event_pool = event_pool
        self._allocataded: List[str] = []
        self._fire_path = breadth_first_search(self._map, start_fire_vertex)
        self._fire_distance = 0
        self._positions = positions
        self._start_fire_vertex = start_fire_vertex
        self._tank_water_capacity = tank_water_capacity
        self._water_sources = water_sources

    @property
    def burned_vertices(self) -> List[str]:
        return list(self._burned_vertices)

    @property
    def on_fire_vertices(self) -> List[str]:
        return self._on_fire_vertices

    @property
    def not_burned_vertices(self) -> List[str]:
        return [
            vertex
            for vertex in self._map.vertices
            if vertex not in self._on_fire_vertices
            or vertex not in self._burned_vertices
        ]

    @property
    def fire_trucks(self) -> List[FireTruck]:
        return [
            listener
            for listener in self._event_pool.listeners
            if isinstance(listener, FireTruck)
        ]

    @property
    def event(self):
        return self._event_pool.event

    def fire_distances(self):
        dist = []
        
        for _, path in self._fire_path.items():
            if path["distance"] not in dist:
                dist.append(path["distance"]) 

        return dist

    def notify(self, event: Event):
        self._event_pool.notify(event)

    def notify_and_update(self, event: Event):
        self._event_pool.notify(event)
        self.update()

    def spread_fire(self) -> Set[str]:
        self._fire_distance += 1
        new_fire = []

        if self._fire_distance in self.fire_distances():
            for vertex, path in self._fire_path.items():
                if (
                    path["distance"] == self._fire_distance
                    and vertex in self.not_burned_vertices
                ):
                    self._on_fire_vertices.insert(-1, vertex)
                    new_fire.insert(-1, vertex)

        return new_fire

    def put_out_fire(self, vertex: str):
        try:
            self._on_fire_vertices.remove(vertex)
            self._allocataded.remove(vertex)
            self._burned_vertices.add(vertex)
        except ValueError:
            return

    def move_truck(self, index_truck: int, vertex: str):
        truck = self.fire_trucks[index_truck]
        truck.schedule_move_to(vertex)

    def refuel_truck(self, index_truck: int):
        truck = self.fire_trucks[index_truck]
        truck.schedule_refuel()

    def next(self):
        for i in self.on_fire_vertices:
            if i not in self._allocataded:
                self._allocataded.append(i)
                return i
            else:
                self._allocataded = []

        return None

    def start(self):
        for index, position in enumerate(self._positions):
            truck = FireTruck(
                self._map,
                index,
                position,
                self._tank_water_capacity,
                self._water_per_vertex,
                self._water_sources,
                self._positions,
                self,
            )

            self._event_pool.listen(truck)

        next = self.next()

        self.notify(Event.on_get_fire(self._start_fire_vertex))

        for truck in self.fire_trucks:
            self.move_truck(truck.id, next)
            self.notify(Event.on_set(next, None, truck.id))

    def update(self):
        # checking changes

        self.handle_events()

        # notify changes to trucks
        for i in self.spread_fire():
            event = Event.on_get_fire(i)
            self.notify(event)

        # updates truck states to apply the new changes
        for truck in self.fire_trucks:
            truck.update()

            if self.event.type != Event.ON_GET_FIRE:
                self.handle_events()

    def handle_events(self):
        event = self.event

        if event:
            # truck need refuel water
            if event.type == Event.ON_REFUEL:
                self.refuel_truck(event.sender_id)

            # truck is already to put out fire
            if event.type == Event.ON_ALREADY:
                next_vertex = self.next()

                if next_vertex:
                    self.move_truck(event.sender_id, next_vertex)
                    self.notify(
                        Event(Event.ON_SET, next_vertex, None, event.sender_id)
                    )

            # truck put out fire
            if event.type == Event.ON_PUT_OUT:
                self.put_out_fire(event.target)

                next = self.next()

                if next:
                    self.move_truck(event.sender_id, next)
                    self.notify(
                        Event(Event.ON_SET, next, None, event.sender_id)
                    )

    def end(self) -> bool:
        all_vertices_was_burned = len(self.not_burned_vertices) == 0
        no_vertices_on_fire = len(self._on_fire_vertices) == 0
        return all_vertices_was_burned or no_vertices_on_fire

    def __repr__(self):
        return "FireFighter()"
