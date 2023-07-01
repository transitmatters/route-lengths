from geopy.distance import geodesic
from mbta_gtfs_sqlite.models import ShapePoint, Stop
from typing import Tuple

GeoTuple = Tuple[float, float]


def get_shape_point_geotuple(shape_point: ShapePoint) -> GeoTuple:
    return (shape_point.shape_pt_lat, shape_point.shape_pt_lon)


def get_stop_geotuple(stop: Stop) -> GeoTuple:
    return (stop.stop_lat, stop.stop_lon)


def geotuple_distance(p1: GeoTuple, p2: GeoTuple):
    return geodesic(p1, p2).km
