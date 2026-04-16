import functools
import time
from pathlib import Path
from typing import List, Callable

from faststream.rabbit.publisher import RabbitPublisher
from loguru import logger
from pydantic import BaseModel, Field
from sqlalchemy import cast, func, Integer, literal, column


class PaginatedListOutputModel(BaseModel):
    page_size: int | None = None
    current_page: int | None = None
    total_pages: int | None = None
    total_items: int = 0
    items: List[BaseModel] = Field(default_factory=list)


class PaginatedListInputModel(BaseModel):
    page_num: int | None = Field(None, ge=1)
    page_size: int | None = Field(None, ge=1)


class Paginator:
    def __init__(self, page_num: int | None, page_size: int | None):
        self.page_num = page_num
        self.page_size = page_size

    def _check(self):
        return False if not self.page_size or not self.page_num else True

    def skip(self):
        return ((self.page_num - 1) * self.page_size) if self._check() else None

    def limit(self):
        return self.page_size if self._check() else None

    def pagination_fields_for_grouping(self):
        return (
            column("page_size"),
            column("current_page"),
        )


    def total_pages(self, total_items: int):
        return 1 if self.page_size is None else ((total_items + self.page_size - 1) // self.page_size)

    @property
    def total_pages_field(self):
        return cast((func.count().over() + self.page_size - 1) / self.page_size, Integer).label("total_pages")

    @property
    def total_items_field(self):
        return func.count().over().label("total_items")

    @property
    def page_size_field(self):
        return literal(self.page_size).label("page_size")

    @property
    def current_page_field(self):
        return literal(self.page_num).label("current_page")

    @property
    def pagination_fields(self):
        return (
            self.total_pages_field,
            self.total_items_field,
            self.page_size_field,
            self.current_page_field,
        )


def execution_time(f: Callable):
    @functools.wraps(f)
    async def wrapper(*args, **kwargs):
        module_name = f.__module__
        func_name = f.__qualname__
        full_path = f"{module_name}.{func_name}"

        start = time.perf_counter_ns()
        output = await f(*args, **kwargs)
        end = time.perf_counter_ns()

        _execution_time = end - start
        logger.debug(
            f"\n"
            f"{full_path} execution time: \n"
            f"{_execution_time} nanoseconds, \n"
            f"{round(_execution_time / 1000, 3)} microseconds, \n"
            f"{round(_execution_time / 1_000_000, 3)} milliseconds, \n"
            f"{round(_execution_time / 1_000_000_000, 3)} seconds"
        )
        return output
    return wrapper

def producer(publisher: RabbitPublisher):
    def decorator(f: Callable):
        @functools.wraps(f)
        async def wrapper(*args, **kwargs):
            result = await f(*args, **kwargs)
            ack = await publisher.publish(result)
            print(ack)
            return result
        return wrapper
    return decorator

def read_doc(path: Path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()
