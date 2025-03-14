
from modules.cameras.schemas import CameraReferenceResponseForCreateVehicle
from modules.roads.schemas import RoadReferenceResponseForCreateVehicle
from modules.zones.schemas import ZoneReferenceResponseForCreateVehicle
from modules.intersections.schemas import IntersectionReferenceResponseForCreateVehicle
import base64

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
        "photo":vehicle.photo,
        "license_photo": vehicle.license_photo,




        "camera": CameraReferenceResponseForCreateVehicle(**vehicle.camera.__dict__)if vehicle.camera else None,
        "road": RoadReferenceResponseForCreateVehicle(**vehicle.road.__dict__)if vehicle.road else None,
        "zone": ZoneReferenceResponseForCreateVehicle(**vehicle.zone.__dict__) if vehicle.zone else None,
        "intersection": IntersectionReferenceResponseForCreateVehicle(**vehicle.intersection.__dict__) if vehicle.intersection else None,
        "created_at":   vehicle.created_at
         }

# def transform_vehicle_data(vehicle):
#     """
#     Convert binary photo to a base64 encoded string if the photo exists.
#     """
#     if vehicle.photo:
#         vehicle.photo = base64.b64encode(vehicle.photo).decode('utf-8')
#     return vehicle
