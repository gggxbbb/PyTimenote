from dataclasses import dataclass
from typing import List, Any, Dict

from dataclasses_json import dataclass_json

from PyTimenote.timenote.note import TimenotePost, NotesList

from rich.console import Console
from rich.tree import Tree


@dataclass_json
@dataclass
class TimenoteCategory:
    bgColor: int
    categoryName: str
    categoryDesc: str
    id: int
    isDefault: int
    isLock: int
    noteCount: int
    parentCategoryId: int
    time: int


@dataclass
class CategoryNode:
    category: TimenoteCategory
    children_note: NotesList | None
    children_category: "CategoryList|None"

    def build_tree(self, parent_tree: Tree, index: int = 0) -> Tree:
        this_tree = parent_tree.add(f'[green]{index}[/] {self.category.categoryName}')
        this_index = 0
        if self.children_category is not None:
            for children_category in self.children_category.categories.values():
                children_category.build_tree(this_tree, this_index)
                this_index += 1
        if self.children_note is not None:
            self.children_note.build_tree(this_tree, this_index)
            this_index += 1
        return parent_tree


class CategoryList:
    categories: Dict[int, CategoryNode]
    console: Console

    def __init__(self, data: List[TimenoteCategory | TimenotePost | Any], console: Console, no_unknown: bool = False):
        self.console = console
        self.categories = {}
        if not no_unknown:
            root_categories: Dict[int, TimenoteCategory] = {
                -1: TimenoteCategory(
                    id=-1,
                    categoryName="未分类",
                    categoryDesc="未分类",
                    bgColor=0,
                    isDefault=0,
                    isLock=0,
                    noteCount=0,
                    parentCategoryId=0,
                    time=0,
                )
            }
        else:
            root_categories: Dict[int, TimenoteCategory] = {}
        children_category: Dict[int, List[TimenoteCategory]] = {}
        notes: Dict[int, List[TimenotePost]] = {}

        # 数据分类，区分 根分类, 子分类, 日记
        for item in data:
            if isinstance(item, TimenotePost):  # 如果为日记
                item: TimenotePost
                if item.categoryId not in notes.keys():
                    notes[item.categoryId] = []
                notes[item.categoryId].append(item)
            elif isinstance(item, TimenoteCategory):  # 如果为分类
                item: TimenoteCategory
                if item.parentCategoryId == 0:  # 为根分类
                    root_categories[item.id] = item
                else:  # 为子分类
                    if item.parentCategoryId not in children_category.keys():
                        children_category[item.parentCategoryId] = []
                    children_category[item.parentCategoryId].append(item)

        # 合并子分类自身数据和子分类文章
        children_data: Dict[int, List[TimenoteCategory | TimenotePost]] = {}
        for (k, v) in children_category.items():
            v: List[TimenoteCategory]
            children_data[k] = v
            for item in children_data[k]:
                item.parentCategoryId = 0
                if item.id in notes.keys():
                    children_data[k] += notes[item.id]

        # 创建 CategoryNode
        for (k, v) in root_categories.items():
            if k in children_data.keys():
                sub_data = CategoryList(children_data[k], self.console, no_unknown=True)
            else:
                sub_data = None
            if k in notes.keys():
                note = NotesList(notes[k], self.console)
            else:
                note = None
            self.categories[k] = CategoryNode(v, note, sub_data)

    def build_tree(self, parent_tree: Tree | None = None) -> Tree:
        this_tree: Tree = parent_tree or Tree("时光记")
        index = 0
        for category in self.categories.values():
            category.build_tree(this_tree, index)
            index += 1
        return this_tree
