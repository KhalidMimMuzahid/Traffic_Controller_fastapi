
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import desc, asc, func
import math
from modules.zones.models import Zone
from responses.models import MetaData
from utils.query_builder import query_builder



async def create_zone(db: AsyncSession, name: str):
    zone = Zone(name=name)
    db.add(zone)
    await db.commit()
    await db.refresh(zone)
    return zone

async def get_zones(db: AsyncSession,page, limit, name):
    filters = {"name": name}  # Dynamic filters
    return await query_builder(db, Zone, filters, page, limit)




