from datetime import datetime
from enum import Enum

from pydantic import BaseModel

from typing import Optional, Set


class HashableModel(BaseModel):
    def __hash__(self):
        return hash((type(self),) + tuple(self.__dict__.values()))


class Item(HashableModel):
    name: str
    start: datetime
    end: Optional[datetime]


class Person(Item):
    pass


class Milestone(HashableModel):
    name: str
    start: datetime
    end: Optional[datetime]


class Scenario(BaseModel):
    name: str
    items: Set[Item]
    milestones: Set[Milestone]
    start: datetime
    end: datetime

    def generate(self):
        s_items = sorted(list(self.items), key=lambda i: i.start)
        s_milestones = sorted(list(self.milestones), key=lambda i: i.start)
        table = [[""]+[f"{m.name} ({m.start})" for m in s_milestones]]
        for i in s_items:
            row = [i.name]
            for m in s_milestones:
                row.append((m.start - i.start).days / 365)
            table.append(row)
        return table
