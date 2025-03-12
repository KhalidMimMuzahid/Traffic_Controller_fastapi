
from modules.cameras.schemas import CameraReferenceResponseForCreateVehicle
from modules.roads.schemas import RoadReferenceResponseForCreateVehicle
from modules.zones.schemas import ZoneReferenceResponseForCreateVehicle
from modules.intersections.schemas import IntersectionReferenceResponseForCreateVehicle


def transform_vehicle_data(vehicle):
    """Transforms a Road ORM object into a dictionary format with nested schema."""
    return {
        "id": vehicle.id,
        "category": vehicle.category,
        "direction_type": vehicle.direction_type,
        "len_violation": vehicle.len_violation,
        "speed_violation":vehicle.speed_violation,
        "speed":vehicle.speed,
        "tracker_id":vehicle.tracker_id,
        "license_number":vehicle.license_number,

        "camera": CameraReferenceResponseForCreateVehicle(**vehicle.camera.__dict__)if vehicle.camera else None,
        "road": RoadReferenceResponseForCreateVehicle(**vehicle.road.__dict__)if vehicle.road else None,
        "zone": ZoneReferenceResponseForCreateVehicle(**vehicle.zone.__dict__) if vehicle.zone else None,
        "intersection": IntersectionReferenceResponseForCreateVehicle(**vehicle.intersection.__dict__) if vehicle.intersection else None,
        "created_at":   vehicle.created_at
         }