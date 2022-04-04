from dataclasses import dataclass
from datetime import datetime
from typing import Any, Callable

from dataclasses_json import dataclass_json

from rich.console import Console
from rich.tree import Tree
from typing import Dict, List


class TimenoteWeather:
    weathers = {
        104: "阴",
        150: "晴",
        250: "大风",
        350: "下雪",
        450: "下雨"
    }


class TimenoteMood:
    moods = {
        "MOOD_UNKNOWN": "未知",  # 未知
        "MOOD_HAPPY": "开心",  # 开心
        "MOOD_SAD": "难过",  # 难过
        "MOOD_ANGRY": "生气",  # 生气
        "MOOD_GLOOMY": "阴沉",  # 阴沉
        "MOOD_NORMAL": "一般"  # 一般
    }


@dataclass_json
@dataclass
class TimenotePost:
    categoryId: int
    categoryName: str
    content: str
    contentType: int
    id: int
    isRemove: int
    location: str
    mood: str
    music: str
    time: int
    title: str
    weather: int

    def get_info(self) -> str:
        return f'[white i]{self.get_create_time()}[/] {self.title} [white i]--{TimenoteMood.moods[self.mood]}的{TimenoteWeather.weathers[self.weather]}天'

    def get_create_time(self) -> str:
        # 将 self.id 作为时间戳转换为时间
        created_time = datetime.fromtimestamp(self.id / 1000)
        return created_time.strftime('%Y-%m-%d')


class NotesList:
    notes: [TimenotePost]
    console: Console

    def __init__(self, data: List[TimenotePost | Any], console: Console):
        self.console = console
        self.notes = []
        for note in data:
            if isinstance(note, TimenotePost):
                note: TimenotePost
                self.notes.append(note)
                if note.categoryId == -1:
                    note.categoryName = "未分类"

    def build_tree(self, parent_tree: Tree, index: int = 0) -> Tree:
        for note in self.notes:
            parent_tree.add(f'[green]{index}[/] {note.get_info()}')
            index += 1
        return parent_tree
