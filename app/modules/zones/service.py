
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from modules.zones.models import Zone



async def create_zone(db: AsyncSession, name: str):
    zone = Zone(name=name)
    db.add(zone)
    await db.commit()
    await db.refresh(zone)
    return zone
# async def get_zones(db: AsyncSession):
#     result = await db.execute(select(Zone))
#     return result.scalars().all()