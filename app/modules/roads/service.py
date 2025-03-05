
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from modules.zones.models import Zone
from modules.intersections.models import Intersection

from fastapi import HTTPException
from modules.roads.models import Road
from modules.zones.schemas import ZoneReferenceResponseForCreateRoad
from modules.intersections.schemas import IntersectionReferenceResponseForCreateRoad
from utils.query_builder import query_builder
from modules.roads.utils import transform_road_data


async def create_road(db: AsyncSession, name: str, road_no = int, intersection_id = int):
    intersection_result = await db.execute(select(Intersection).where(Intersection.id == intersection_id).options(joinedload(Intersection.zone)))
    intersection = intersection_result.scalar_one_or_none()
    if not intersection:
         raise HTTPException(status_code=404, detail=f"There have no Intersection with ID {intersection_id}")
    zone_id = intersection.zone.id
    #  making an instance of the zone object that inherits from zone Class (Models class)
    new_road = Road(name=name,  road_no=road_no, intersection_id=intersection_id, zone_id=zone_id)
    db.add(new_road)
    await db.commit()
    await db.refresh(new_road)
    return {
          "id" : new_road.id,
          "name" : new_road.name,
          "road_no" : new_road.road_no,
          "zone": ZoneReferenceResponseForCreateRoad(**intersection.zone.__dict__),
          "intersection" : IntersectionReferenceResponseForCreateRoad(**intersection.__dict__),
    }


async def get_roads(db: AsyncSession, page:int, limit:int, id:int):
    filters= {"id": id} # Dynamic filters
    return await query_builder(
        db=db,
        model=Road,
        filters=filters,
        page=page,
        limit=limit,
        relationships=[Road.intersection, Road.zone],  # ✅ Joined load applied
        transform_fn=transform_road_data  # ✅ Transform function applied
    )


    # result = await db.execute(select(Road))
    # cameras=  result.scalars().all() 
    # return cameras
    # # result = await db.execute(select(Camera).options(joinedload(Camera.intersection), joinedload(Camera.zone)))
    # # cameras= result.scalars().all() 
    # # return cameras

