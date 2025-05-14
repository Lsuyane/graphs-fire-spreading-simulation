from events import Event, EventListener


class Timer(EventListener):
    def __init__(self):
        self._time_count = 0

    @property
    def time(self) -> int:
        return self._time_count

    def handle(self, event: Event):
        if event.type == Event.ON_PUT_OUT:
            self._time_count += 1
