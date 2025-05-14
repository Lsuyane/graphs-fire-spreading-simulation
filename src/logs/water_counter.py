from typing import Dict
from events import Event, EventListener


class WaterCount(EventListener):
    def __init__(self, water_per_vertex: Dict[str, float]):
        self._countage = 0
        self._water_per_vertex = water_per_vertex

    @property
    def count(self) -> float:
        return self._countage

    def handle(self, event):
        if event.type == Event.ON_PUT_OUT:
            self._countage += self._water_per_vertex[event.target]
