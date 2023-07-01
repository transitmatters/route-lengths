from geopy.distance import geodesic
from mbta_gtfs_sqlite.models import ShapePoint, Stop
from typing import Tuple, Any, Callable

GeoTuple = Tuple[float, float]


CENTER_OF_BOSTON = (42.358056, -71.063611)


def get_geotuple(
    model: Any,
    get_lat_lon: Callable[[Any], Tuple[float, float]],
    source: GeoTuple = CENTER_OF_BOSTON,
):
    (y1, x1) = get_lat_lon(model)
    (y2, x2) = source
    x_distance = geodesic((x1, y1), (x2, y1)).km
    y_distance = geodesic((x1, y1), (x1, y2)).km
    x_distance_signed = (1 if x1 > x2 else -1) * x_distance
    y_distance_signed = (1 if y1 > y2 else -1) * y_distance
    return (x_distance_signed, y_distance_signed)


def get_shape_point_geotuple(shape_point: ShapePoint):
    return get_geotuple(shape_point, lambda sp: (sp.shape_pt_lat, sp.shape_pt_lon))


def get_stop_geotuple(stop: Stop):
    return get_geotuple(stop, lambda s: (s.stop_lat, s.stop_lon))


def geotuple_distance(p1: GeoTuple, p2: GeoTuple):
    (x1, y1) = p1
    (x2, y2) = p2
    return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
