from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class AnnouncementFilter(BaseModel):
    author: Optional[int] = None
    category: Optional[int] = None
    start_data: Optional[datetime] = None
    end_data: Optional[datetime] = None
