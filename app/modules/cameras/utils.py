
from modules.roads.schemas import RoadReferenceResponseForCreateCamera
from modules.zones.schemas import ZoneReferenceResponseForCreateCamera
from modules.intersections.schemas import IntersectionReferenceResponseForCreateCamera

def transform_camera_data(camera):
    """Transforms a Road ORM object into a dictionary format with nested schema."""
    return {
        "id": camera.id,
        "name": camera.name,
        "direction_type": camera.direction_type,
        "road": RoadReferenceResponseForCreateCamera(**camera.road.__dict__)if camera.road else None,
        "zone": ZoneReferenceResponseForCreateCamera(**camera.zone.__dict__) if camera.zone else None,
        "intersection": IntersectionReferenceResponseForCreateCamera(**camera.intersection.__dict__) if camera.intersection else None
    }