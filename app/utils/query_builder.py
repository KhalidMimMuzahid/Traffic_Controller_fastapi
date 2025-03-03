from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import DeclarativeMeta
from sqlalchemy import desc, asc, func
from responses.models import MetaData
from typing import Dict, Optional
import math




async def query_builder(
    db: AsyncSession,
    model: DeclarativeMeta,
    filters: Dict[str, Optional[str]] = None,
    page: int = 1,
    limit: int = 10,
    order_by: str = "id",
    desc_order: bool = True
):
    """
    Build and execute a dynamic query with filtering and pagination.
    
    :param db: Database session
    :param model: SQLAlchemy model class
    :param filters: Dictionary of filter conditions (field_name: value)
    :param page: Current page number (default: 1)
    :param limit: Number of items per page (default: 10)
    :param order_by: Column name to sort by (default: "id")
    :param desc_order: Whether to sort in descending order (default: True)
    :return: Dictionary containing paginated results and metadata
    """
    query = select(model)
    count_query = select(func.count()).select_from(model)  # Base count query

    # Apply dynamic filters
    if filters:
        for field, value in filters.items():
            if value is not None and hasattr(model, field):
                filter_condition = getattr(model, field).ilike(f"%{value}%")
                query = query.filter(filter_condition)
                count_query = count_query.filter(filter_condition)  # Apply filters to count query

    # Execute total count query with applied filters
    total_count_result = await db.execute(count_query)
    total_count = total_count_result.scalar()

    # Compute pagination values
    skip = (page - 1) * limit
    total_page = math.ceil(total_count / limit)
    prev_page = page - 1 if page > 1 else None
    next_page = page + 1 if page < total_page else None

    # Apply ordering
    order_column = getattr(model, order_by, None)
    if order_column:
        query = query.order_by(desc(order_column) if desc_order else order_column)

    # Apply pagination
    query = query.offset(skip).limit(limit)

    # Execute final query
    result = await db.execute(query)

    # Use your MetaData class for structured metadata response
    meta_data = MetaData(prev=prev_page, next=next_page, current=page, total=total_page)

    return {"data": result.scalars().all() if result.scalars().all() else [], "meta_data": meta_data}