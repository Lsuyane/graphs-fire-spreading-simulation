from typing import Dict, List
from events import Event, EventListener


class Path(EventListener):
    def __init__(self):
        self._paths: Dict[str, List[str]] = dict()

    @property
    def paths(self) -> Dict[str, List[str]]:
        return self._paths

    def handle(self, event: Event):
        if event.type == Event.ON_MOVE:
            key = str(event.sender_id)

            if key not in self._paths:
                self._paths[key] = []
                
            self._paths[key].append(event.target)
