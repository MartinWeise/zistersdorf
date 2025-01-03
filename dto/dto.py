from typing import List

from ics import Event


class ParseResponse:
    events: List[Event]
    pages: int
