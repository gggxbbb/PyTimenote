import json
from pathlib import Path
from typing import Any, List

from rich.console import Console

from PyTimenote.timenote.category import TimenoteCategory
from PyTimenote.timenote.note import TimenotePost
from PyTimenote.utils.config import Config


def load_json(file_path: Path) -> List[TimenotePost | Any]:
    with open(file_path, "r", encoding="utf-8") as f:
        opt = []
        tables = json.loads(f.read())["tables"]
        for v in tables:
            match v["name"]:
                case "note":
                    for i in v["data"]:
                        opt.append(TimenotePost.from_dict(i))
                case "category":
                    for i in v["data"]:
                        opt.append(TimenoteCategory.from_dict(i))
    return opt


def load_data(console: Console, config: Config) -> List[TimenotePost | Any]:
    path = Path(config.data_dir)
    # Get the last modified json file
    file_path = max(path.glob("*.json"), key=lambda p: p.stat().st_mtime)
    console.print(f"加载数据：{file_path}")
    return load_json(file_path)
