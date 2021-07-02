from datetime import datetime
from typing import Optional, Set

from prettytable import PrettyTable
from pydantic import BaseModel

DATE_FORMAT = "%d/%m/%Y"


class HashableModel(BaseModel):
    def __hash__(self):
        return hash(
            (type(self),)
            + tuple(self.dict(exclude={"started_after", "was_happening", "ended_before"}))
        )


class Item(HashableModel):
    name: str
    start: datetime
    end: Optional[datetime]
    started_after = {
        "en": "{name} was {time} year(s) short to happen",
        "pt": "Faltava(m) {time} ano(s) para {name} acontecer",
    }
    was_happening = {
        "en": "{name} had happened {time} year(s) prior",
        "pt": "{name} havia acontecido há {time} ano(s)",
    }
    ended_before = {
        "en": "{name} had ended {time} year(s) prior",
        "pt": "{name} havia acabado há {time} ano(s)",
    }


class Person(Item):
    started_after = {
        "en": "{name} was {time} year(s) short to be born",
        "pt": "Faltava(m) {time} ano(s) para {name} nascer",
    }
    was_happening = {"en": "{name} had {time} year(s) old", "pt": "{name} tinha {time} ano(s)"}
    ended_before = {
        "en": "{name} had passed away {time} year(s) prior",
        "pt": "{name} havia falecido há {time} ano(s)",
    }


class Scenario(BaseModel):
    name: str
    items: Set[Item]
    milestones: Set[Item]
    start: datetime
    end: datetime

    def generate(self, language="en"):
        s_items = sorted(list(self.items), key=lambda i: i.start)
        s_milestones = sorted(list(self.milestones), key=lambda i: i.start)
        table = [[""] + [f"{m.name} ({m.start.strftime(DATE_FORMAT)})" for m in s_milestones]] + [
            [i.name] + [self.get_timeline_situation(language, i, m) for m in s_milestones]
            for i in s_items
        ]
        return table

    def pretty(self, format_method=PrettyTable.get_string, language="en"):
        ptable = PrettyTable()
        table = self.generate(language)
        ptable.field_names = table[0]
        ptable.add_rows(table[1:])
        return format_method(ptable)

    def get_timeline_situation(self, language, item, milestone):
        if item.end and item.end < milestone.start:
            return item.ended_before[language].format(
                name=item.name, time=int((milestone.start - item.end).days / 365)
            )
        elif (not item.end and item.start < milestone.start) or (
            item.start < milestone.start < item.end
        ):
            return item.was_happening[language].format(
                name=item.name, time=int((milestone.start - item.start).days / 365)
            )
        else:
            return item.started_after[language].format(
                name=item.name, time=int((item.start - milestone.start).days / 365)
            )
