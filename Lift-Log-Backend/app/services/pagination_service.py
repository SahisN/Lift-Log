from __future__ import annotations

import math
import typing as t
from dataclasses import dataclass


@dataclass(frozen=True)
class PaginatedData:
    items: list[t.Any]
    page: int
    page_size: int
    total_pages: int


class PaginationService:
    def paginate_list(
        self, model_list: list[t.Any], page: int, page_size: int, total_items: int
    ) -> PaginatedData:
        total_pages = math.ceil(total_items / page_size) if page_size else 0

        return PaginatedData(
            items=model_list,
            page=page,
            page_size=len(model_list),
            total_pages=total_pages,
        )
