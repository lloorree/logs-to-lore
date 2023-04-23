from dataclasses import dataclass
from typing import Optional, List


@dataclass
class SillyExtra:
    type: Optional[str]  # ex. 'bookmark_created' or 'generic'


@dataclass
class TavernEntry:
    name: str  # ex. "Detailed Example Character",
    is_user: bool  # false, only true for user messages
    is_name: bool
    send_date: any  # 1680582371135 or "2023-4-8 @00h 12m 00s 59ms"
    mes: str  # "A greeting for CAI for Detailed Example Character."
    chid: Optional[str]  # "9"  seems to be character id, but is it used? no value if it is the user.
    extras: Optional[SillyExtra]
    swipe_id: Optional[int]
    swipes: Optional[List[str]]
    extra: any
    is_system: Optional[bool]  # In sillytavern, is yes for user 'TavernAI'.

    def __init__(self, name: str = 'You', is_user: bool = True, is_name: bool = True, send_date: any = '',
                 mes: str = '', chid: Optional[str] = None, extras: Optional[SillyExtra] = None, swipe_id: int = 0,
                 swipes: Optional[List[str]] = None, extra: any = None, is_system: Optional[bool] = None,
                 user_override=None, **kwargs):
        self.name = name
        if name == 'You' and user_override is not None:
            self.name = user_override
        self.is_user = is_user
        self.is_name = is_name
        self.send_date = send_date
        self.mes = mes
        self.chid = chid
        self.extras = extras
        self.swipe_id = swipe_id
        self.extra = extra
        self.swipes = swipes
        if self.swipes is None or len(self.swipes) == 0:
            self.swipes = [self.mes]
        self.is_system = is_system

    def fulltext_raw(self) -> str:
        return ' ' + self.mes + ' '
