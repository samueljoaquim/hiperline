from datetime import datetime
from enum import StrEnum
from typing import Optional, Set

from prettytable import PrettyTable
from pydantic import BaseModel

DATE_FORMAT = "%d/%m/%Y"


class PointInTime(StrEnum):
    STARTED_AFTER = "started_after"
    WAS_HAPPENING = "was_happening"
    ENDED_BEFORE = "ended_before"


class HashableModel(BaseModel):
    def __hash__(self):
        return hash(
            (type(self),)
            + tuple(self.model_dump(exclude=set([i.__str__() for i in PointInTime])))
        )


class Item(HashableModel):
    name: str
    start: datetime
    end: Optional[datetime] = None
    started_after: dict = {
        "en": "{name} was {time} year(s) short to happen",
        "pt": "Faltava(m) {time} ano(s) para {name} acontecer",
    }
    was_happening: dict = {
        "en": "{name} had happened {time} year(s) prior",
        "pt": "{name} havia acontecido há {time} ano(s)",
    }
    ended_before: dict = {
        "en": "{name} had ended {time} year(s) prior",
        "pt": "{name} havia acabado há {time} ano(s)",
    }


class Person(Item):
    started_after: dict = {
        "en": "{name} was {time} year(s) short to be born",
        "pt": "Faltava(m) {time} ano(s) para {name} nascer",
    }
    was_happening: dict = {"en": "{name} had {time} year(s) old", "pt": "{name} tinha {time} ano(s)"}
    ended_before: dict = {
        "en": "{name} had passed away {time} year(s) prior",
        "pt": "{name} havia falecido há {time} ano(s)",
    }


class Scenario(BaseModel):
    name: str
    items: Set[Item]
    milestones: Set[Item]
    start: datetime
    end: datetime

    def generate_events(self):
        s_items = sorted(list(self.items), key=lambda i: i.start)
        s_milestones = sorted(list(self.milestones), key=lambda i: i.start)
        table = [[""] + [f"{m.name} ({m.start.strftime(DATE_FORMAT)})" for m in s_milestones]] + [
            [self.get_timeline_situation(i, m) for m in s_milestones]
            for i in s_items
        ]
        return table

    def generate(self, language="en"):
        s_items = sorted(list(self.items), key=lambda i: i.start)
        s_milestones = sorted(list(self.milestones), key=lambda i: i.start)
        table = [[""] + [f"{m.name} ({m.start.strftime(DATE_FORMAT)})" for m in s_milestones]] + [
            [i.name] + [self.get_textual_timeline_situation(language, i, m) for m in s_milestones]
            for i in s_items
        ]
        return table

    def pretty(self, format_method=PrettyTable.get_string, language="en"):
        ptable = PrettyTable()
        table = self.generate(language)
        ptable.field_names = table[0]
        ptable.add_rows(table[1:])
        return format_method(ptable)

    def get_timeline_situation(self, item, milestone):
        if item.end and item.end < milestone.start:
            return (item.name, PointInTime.ENDED_BEFORE, int((milestone.start - item.end).days / 365))
        elif (not item.end and item.start < milestone.start) or (
            item.start < milestone.start < item.end
        ):
            return (item.name, PointInTime.WAS_HAPPENING, int((milestone.start - item.start).days / 365))
        else:
            return (item.name, PointInTime.STARTED_AFTER, int((item.start - milestone.start).days / 365))

    def get_textual_timeline_situation(self, language, item, milestone):
        situation = self.get_timeline_situation(item, milestone)
        sentence_dict = getattr(item, situation[1].__str__())
        return sentence_dict[language].format(name=situation[0], time=situation[2])
