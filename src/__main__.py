from graphs import random_vertices
from maps import generate_map
from app import App
# from utils import input_data


def main():
    """Runs the main app"""

    app_map = generate_map(4)
    fire_start_vertex = random_vertices(app_map)[0]
    firefighters_position = random_vertices(app_map, 3)
    water_sources_position = random_vertices(app_map, 3)
    fire_truck_volume = 150
    water_per_vertex = {vertex: 15 for vertex in app_map.vertices}

    # inp = input_data()

    # app_map = inp["map"]
    # fire_start_vertex = inp["fire_start_position"]
    # firefighters_position = inp["firefighters_positions"]
    # water_sources_position = inp["water_sources"]
    # fire_truck_volume = inp["water_per_vertex"]
    # water_per_vertex = inp["firetruck_water_capacity"]

    app = App(
        app_map,
        fire_start_vertex,
        firefighters_position,
        water_sources_position,
        water_per_vertex,
        fire_truck_volume,
        verbose=2,
    )

    app.run()
    app.results()


if __name__ == "__main__":
    main()
