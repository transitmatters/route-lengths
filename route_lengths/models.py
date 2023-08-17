from dataclasses import dataclass
from typing import List, Dict
from mbta_gtfs_sqlite.models import RoutePattern, ShapePoint, Trip, StopTime, Stop

from .geo import get_shape_point_geotuple, GeoTuple
from .util import index_by, bucket_by

Shape = List[GeoTuple]


@dataclass
class Models:
    route_patterns_by_route_id: Dict[str, List[RoutePattern]]
    trips_by_route_pattern_id: Dict[str, Trip]
    stops_by_trip_id: Dict[str, List[Stop]]
    shapes_by_trip_id: Dict[str, Shape]
    stops_by_id: Dict[str, Stop]


def load_shape_for_trip(session, trip: Trip) -> Shape:
    shape_points = session.query(ShapePoint).filter_by(shape_id=trip.shape_id).all()
    sorted_shape_points = sorted(shape_points, key=lambda sp: sp.shape_pt_sequence)
    return [get_shape_point_geotuple(sp) for sp in sorted_shape_points]


def load_stops_for_trip(session, trip: Trip) -> List[Stop]:
    stop_times = session.query(StopTime).filter_by(trip_id=trip.trip_id).all()
    stop_times_by_stop_id = index_by(stop_times, lambda st: st.stop_id)
    stop_ids = [st.stop_id for st in stop_times]
    stops = session.query(Stop).filter(Stop.stop_id.in_(stop_ids)).all()
    return list(
        sorted(stops, key=lambda s: stop_times_by_stop_id[s.stop_id].stop_sequence)
    )


def load_stops(session, stop_ids: List[str]):
    stops = session.query(Stop).filter(Stop.stop_id.in_(stop_ids)).all()
    return index_by(stops, lambda s: s.stop_id)


def load_models(session, target_route_ids: List[str]):
    if "*" in target_route_ids:
        route_patterns = session.query(RoutePattern).all()
    else:
        route_patterns = (
            session.query(RoutePattern)
            .filter(RoutePattern.route_id.in_(target_route_ids))
            .all()
        )
    representative_trip_ids = set((rp.representative_trip_id for rp in route_patterns))
    route_patterns_by_route_id = bucket_by(route_patterns, lambda rp: rp.route_id)
    trips = session.query(Trip).filter(Trip.trip_id.in_(representative_trip_ids)).all()
    trips_by_route_pattern_id = index_by(trips, lambda t: t.route_pattern_id)
    stops_by_trip_id = {}
    shapes_by_trip_id = {}
    stops_by_id = {}
    parent_station_ids = []
    for trip in trips:
        stops_for_trip = load_stops_for_trip(session, trip)
        stops_by_trip_id[trip.trip_id] = stops_for_trip
        shapes_by_trip_id[trip.trip_id] = load_shape_for_trip(session, trip)
        parent_station_ids.extend(s.parent_station for s in stops_for_trip)
        stops_by_id.update(index_by(stops_for_trip, lambda s: s.stop_id))
    parent_stations = load_stops(session, parent_station_ids)
    stops_by_id.update(parent_stations)
    return Models(
        route_patterns_by_route_id=route_patterns_by_route_id,
        trips_by_route_pattern_id=trips_by_route_pattern_id,
        stops_by_trip_id=stops_by_trip_id,
        shapes_by_trip_id=shapes_by_trip_id,
        stops_by_id=stops_by_id,
    )
