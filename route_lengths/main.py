import json
from mbta_gtfs_sqlite import MbtaGtfsArchive
from mbta_gtfs_sqlite.models import RoutePattern, Trip, ShapePoint, Stop
from geopy.distance import geodesic
from typing import List, Any, Tuple
from dataclasses import dataclass

from .geo import CENTER_OF_BOSTON, geotuple_distance, get_stop_geotuple
from .util import index_by, pairwise
from .config import load_config, Config
from .models import load_models, Models, Shape


@dataclass
class PairwiseDistance:
    from_station_id: str
    to_station_id: str
    distance: float


def get_stop_index_in_shape(stop: Stop, shape: Shape) -> int:
    return min(
        range(len(shape)),
        key=lambda i: geotuple_distance(get_stop_geotuple(stop), shape[i]),
    )


def get_shape_length(shape: Shape) -> float:
    return sum(geotuple_distance(a, b) for a, b in pairwise(shape))


def get_pairwise_distances(stops: List[Stop], shape: Shape) -> List[PairwiseDistance]:
    distances = []
    stop_indices = {
        stop.stop_id: get_stop_index_in_shape(stop, shape) for stop in stops
    }
    for from_stop, to_stop in pairwise(stops):
        from_index = stop_indices[from_stop.stop_id]
        to_index = stop_indices[to_stop.stop_id]
        subshape = shape[from_index:to_index]
        distance = get_shape_length(subshape)
        distances.append(
            PairwiseDistance(
                from_station_id=from_stop.parent_station,
                to_station_id=to_stop.parent_station,
                distance=distance,
            )
        )
    return distances


def get_distances_for_trip_id(trip_id: str, models: Models) -> List[PairwiseDistance]:
    stops = models.stops_by_trip_id[trip_id]
    shape = models.shapes_by_trip_id[trip_id]
    return get_pairwise_distances(stops, shape)


def get_distances_for_longest_route_pattern(
    models: Models,
    route_id: str,
) -> List[PairwiseDistance]:
    results_by_route_pattern_id = {}
    for route_pattern in models.route_patterns_by_route_id[route_id]:
        trip = models.trips_by_route_pattern_id[route_pattern.route_pattern_id]
        distances = get_distances_for_trip_id(trip.trip_id, models)
        results_by_route_pattern_id[route_pattern.route_pattern_id] = distances
    return max(
        results_by_route_pattern_id.values(),
        key=lambda distances: sum(distance.distance for distance in distances),
    )


def get_route_lengths(config: Config):
    output = {}
    archive = MbtaGtfsArchive(local_archive_path=config.feeds_path)
    feed = archive.get_latest_feed()
    feed.download_or_build()
    session = feed.create_sqlite_session()
    models = load_models(session, config.target_route_ids)
    for route_id in config.target_route_ids:
        pairwise_distances = get_distances_for_longest_route_pattern(models, route_id)
        print(f"Route {route_id} has {len(pairwise_distances)} stops")
        output[route_id] = []
        for pd in pairwise_distances:
            print(
                f"{pd.from_station_id} -> {pd.to_station_id}: {round(pd.distance, 2)}"
            )
            output[route_id].append(
                {
                    "from_station_id": pd.from_station_id,
                    "to_station_id": pd.to_station_id,
                    "distance": round(pd.distance, 2),
                }
            )
    with open("./output.json", "w") as output_file:
        output_file.write(json.dumps(output, indent=2))


if __name__ == "__main__":
    config = load_config()
    get_route_lengths(config)