from datetime import datetime
from typing import List, Optional

from fastapi_filter.contrib.sqlalchemy import Filter

from .models import Announcement


class AnnouncementFilter(Filter):
    author_id: Optional[int] = None
    category_id: Optional[int] = None
    created_at__gte: Optional[datetime] = None
    created_at__lt: Optional[datetime] = None

    order_by: List[str] = ['-created_at']

    class Constants(Filter.Constants):
        model = Announcement
