from typing import Dict, List

from events import EventPool
from graphs import Graph
from fire import FireFighter
from logs import Logger, Timer, Path, WaterCount


class App:
    def __init__(
        self,
        map: Graph,
        fire_start_vertex: str,
        firefighters_position: List[str],
        water_sources_position: List[str],
        water_needed_extinguish_fire: Dict[str, float],
        fire_truck_water_volume: float = 150,
        verbose: int = 1,
    ):
        self._map = map
        self._fire_start_vertex = fire_start_vertex
        self._firefighters_position = firefighters_position
        self._water_sources_position = water_sources_position
        self._water_per_vertex = water_needed_extinguish_fire
        self._fire_truck_volume = fire_truck_water_volume
        self._event_pool = EventPool()
        self._firefighters = FireFighter(
            self.map,
            self._fire_start_vertex,
            self._firefighters_position,
            self._fire_truck_volume,
            self._water_per_vertex,
            self._water_sources_position,
            self._event_pool,
        )
        self._verbose = verbose
        self._already_runned = False
        # verbose == 1 enables file log
        # verbose == 2 enables file log and prints
        self._logger = Logger("simulation.txt", self._verbose == 2)
        self._timer = Timer()
        self._path = Path()
        self._water_counter = WaterCount(water_needed_extinguish_fire)

    @property
    def map(self) -> Graph:
        """Returns the app map

        Returns:
            Graph: the app map"""
        return self._map

    def start(self):
        self._event_pool.listen(self._logger)
        self._event_pool.listen(self._timer)
        self._event_pool.listen(self._path)
        self._event_pool.listen(self._water_counter)

        self._logger.handle(self._event_pool.event)

        self._firefighters.start()

    def update(self):
        """update state function"""
        self._firefighters.update()

    def run(self, max_iterations=150):
        """main loop"""
        self.start()
        counter = max_iterations

        while not self._firefighters.end() and counter:
            self.update()
            counter -= 1

        self.log_end(counter)

    def log_end(self, counter):
        if counter == 0:
            self._logger.log("many iterations detected stopped.")

        else:
            self._logger.log("simulation finished.")

        self._already_runned = True

    def results(self):
        """Returns the results after execution.

        Raises:
            RuntimeError: If the execution has not been run yet.

        Returns:
            Any: The results of the computation or process.
        """
        if not self._already_runned:
            raise RuntimeError(
                "You must run the process before retrieving results."
            )

        self._logger.log("--------------------------------------------")
        self._logger.log("Simulation Results")
        self._logger.log("--------------------------------------------")
        self._logger.log(f"simulation time: {self._timer.time} units of time,")
        self._logger.log(f"water spend: {self._water_counter.count} L,")
        self._logger.log("truck paths: [")
        self.log_paths()
        self._logger.log("--------------------------------------------")
        self.log_result()

    def log_result(self):
        if len(self._firefighters.not_burned_vertices) == 0:
            self._logger.log("result: The fire was put out")
        else:
            self._logger.log("result: Could not put out the fire")

    def log_paths(self):
        for key, value in self._path.paths.items():
            self._logger.log(
                f"\tfire truck {key}: [",
            )

            for i, char in enumerate(value):
                self._logger.log(f"\t\t'{char}'", end="")
                self._logger.log("," if i < len(value) - 1 else "\n\t],")
        self._logger.log("]")
