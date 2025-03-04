
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import DeclarativeMeta, joinedload
from sqlalchemy import desc, asc, func
from responses.models import MetaData
from typing import Dict, Optional, Any, List
import math

async def query_builder(
    db: AsyncSession,
    model: DeclarativeMeta,
    filters: Dict[str, Optional[Any]] = None,
    page: int = 1,
    limit: int = 10,
    order_by: str = "id",
    desc_order: bool = True,
    relationships: List = None,  # ✅ Relationships to joinedload
    transform_fn=None  # ✅ Function to transform data (NEW)
):
    """
    Build and execute a dynamic query with filtering, pagination, and relationship loading.

    :param db: Database session
    :param model: SQLAlchemy model class
    :param filters: Dictionary of filter conditions (field_name: value)
    :param page: Current page number (default: 1)
    :param limit: Number of items per page (default: 10)
    :param order_by: Column name to sort by (default: "id")
    :param desc_order: Whether to sort in descending order (default: True)
    :param relationships: List of relationships to joinedload (default: None)
    :param transform_fn: Function to transform ORM objects into dictionaries (default: None)
    :return: Dictionary containing paginated results and metadata
    """

    query = select(model)  # Base query
    count_query = select(func.count()).select_from(model)  # Query to count total rows

    # ✅ Apply dynamic filters
    if filters:
        filters = {k: v for k, v in filters.items() if v is not None}
        for field, value in filters.items():
            if hasattr(model, field):
                column_attr = getattr(model, field)
                filter_condition = column_attr.ilike(f"%{value}%") if isinstance(value, str) else column_attr == value
                query = query.filter(filter_condition)
                count_query = count_query.filter(filter_condition)

    # ✅ Apply relationship loading
    if relationships:
        for relation in relationships:
            query = query.options(joinedload(relation))

    # ✅ Execute total count query
    total_count_result = await db.execute(count_query)
    total_count = total_count_result.scalar() or 0

    # ✅ Compute pagination values
    total_pages = max(math.ceil(total_count / limit), 1)
    prev_page = page - 1 if page > 1 else None
    next_page = page + 1 if page < total_pages else None

    # ✅ Apply ordering
    order_column = getattr(model, order_by, None)
    if order_column:
        query = query.order_by(desc(order_column) if desc_order else asc(order_column))

    # ✅ Apply pagination
    skip = (page - 1) * limit
    query = query.offset(skip).limit(limit)

    # ✅ Execute final query
    result = await db.execute(query)
    data = result.scalars().all()

    # ✅ Transform ORM objects into the desired format if a transform function is provided
    if transform_fn:
        data = [transform_fn(item) for item in data]

    # ✅ Construct metadata response
    meta_data = MetaData(prev=prev_page, next=next_page, current=page, total=total_pages)

    return {"data": data, "meta_data": meta_data}

