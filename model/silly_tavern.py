from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class SillyEntry:
    uid: int  # ex. 5, the name in the entries dict is a string of this, i.e. "5".
    key: [str]  # ex. 'turtles', 'animals', 'like'
    keysecondary: [str]
    comment: str  # like a description I guess.
    content: str  # ex. "{{user}} likes turtles."
    constant: bool  # always false for our purposes
    selective: bool  # always false for our purposes
    order: int  # akin to priority
    position: int  # akin to weight


@dataclass
class SillyBook:
    name: str  # ex. 'Genesis'
    description: str  # ex. "A description for the book"
    entries: Dict[str, SillyEntry]

    # Not part of their formatting, just for my usage.
    is_creation: Optional[bool]

    def __init__(self, name: str = 'Exported', description: str = '', entries: Dict[str, SillyEntry] = None,
                 is_creation: Optional[bool] = None, **kwargs):
        self.name = name
        self.description = description
        self.is_creation = is_creation
        self.entries = {}
        if entries is not None and len(entries) > 0:
            for key, value in entries.items():
                if isinstance(value, dict):
                    self.entries[key] = SillyEntry(**value)
                else:
                    self.entries[key] = value
