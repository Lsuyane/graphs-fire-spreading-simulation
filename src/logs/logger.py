import os
from events import Event, EventListener


class Logger(EventListener):
    counter: int = 0

    def __init__(self, output_file: str = "simulation.txt", verbose: bool = True):
        self._output_file = output_file
        self.verbose = verbose

    def handle(self, event: Event):
        self.add_iteration_mark()

        if event.type == Event.ON_START:
            self.log("The simulation was started")

        elif event.type == Event.ON_GET_FIRE:
            self.log(f"The vertex '{event.target}' is on fire")

        elif event.type == Event.ON_SET:
            self.log(
                f"The fire truck '{event.receiver_id:02}' was designed for the vertex '{event.target}'"
            )

        elif event.type == Event.ON_ALREADY:
            self.log(
                f"The fire truck '{event.sender_id:02}' was already to fight the fire"
            )

        elif event.type == Event.ON_PUT_OUT:
            self.log(
                f"The the fire truck '{event.sender_id:02}' managed to put out the fire at '{event.target}'"
            )

        elif event.type == Event.ON_REFUEL:
            self.log(
                f"The the fire truck '{event.sender_id:02}' need to refuel the water tank'"
            )

    def add_iteration_mark(self):
        Logger.counter += 1
        self.log(f"{Logger.counter:03}", end=": ")

    def log(self, text: str, end: str = "\n"):
        path = os.path.join(os.getcwd(), "output", self._output_file)

        with open(path, "a+", encoding="utf-8") as file:
            file.write(text)
            file.write(end)
            file.close()

        if self.verbose:
            print(text.replace('\t', '  '), end=end)
