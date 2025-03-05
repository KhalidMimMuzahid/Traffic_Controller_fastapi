from modules.zones.schemas import ZoneReferenceResponseForCreateIntersection

def transform_intersection_data(intersection):
    """Transforms a Road ORM object into a dictionary format with nested schema."""
    return {
        "id": intersection.id,
        "name": intersection.name,
        "zone": ZoneReferenceResponseForCreateIntersection(**intersection.zone.__dict__) if intersection.zone else None,
    }