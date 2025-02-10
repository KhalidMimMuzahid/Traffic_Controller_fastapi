
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from modules.cameras.models import Camera
from modules.cameras.schemas import DirectionTypeEnum


async def create_camera(db: AsyncSession, name: str, road_no = int,road_name = str, direction_type= DirectionTypeEnum, intersection_id = int,zone_id = int):
    new_camera = Camera(name=name, road_no=road_no, road_name=road_name, direction_type=direction_type, intersection_id=intersection_id, zone_id=zone_id)
    print("------------------------------------------------------------------------------------------------")
    print({'camera': new_camera})
    db.add(new_camera)
    await db.commit()
    await db.refresh(new_camera)
    return new_camera
# async def get_zones(db: AsyncSession):
#     result = await db.execute(select(Zone))
#     return result.scalars().all()