from modules.zones.schemas import ZoneReferenceResponseForCreateRoad
from modules.intersections.schemas import IntersectionReferenceResponseForCreateRoad

def transform_road_data(road):
    """Transforms a Road ORM object into a dictionary format with nested schema."""
    return {
        "id": road.id,
        "name": road.name,
        "road_no": road.road_no,
        "zone": ZoneReferenceResponseForCreateRoad(**road.intersection.zone.__dict__) if road.intersection and road.intersection.zone else None,
        "intersection": IntersectionReferenceResponseForCreateRoad(**road.intersection.__dict__) if road.intersection else None
    }