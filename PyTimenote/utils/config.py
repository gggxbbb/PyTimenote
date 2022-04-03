from dataclasses import dataclass
from pathlib import Path

from dataclasses_json import dataclass_json
from rich.console import Console
from rich.prompt import Prompt, IntPrompt

from PyTimenote.utils.init import config_init


@dataclass_json
@dataclass
class Config:
    """
    配置文件根类
    """
    # 数据文件目录
    data_dir: str = ''


def init_config(console: Console) -> (bool, Config):
    """
    初始化配置文件, 交互式配置
    :param console: 全局 Console 对象
    :return: 成功与否与加载的配置文件
    """
    config_file = Path.home() / ".PyTimenote" / "config.json"
    if not config_file.exists():
        if_ok = config_init(console, force=True)
        if not if_ok:
            return False, None
    with open(config_file, "r", encoding="utf8") as f:
        config: Config = Config.from_json(f.read())

    if (not config.data_dir) or (not Path(config.data_dir).exists()):
        console.print('[red]未配置 [bold]记时光[/] 数据目录[/].')
        while True:
            data_path = choose_data_path(console) / '应用' / '记时光'
            if data_path.exists():
                break
            else:
                console.print('[red]未找到 [bold]记时光[/] 数据目录[/], 请重新选择.')
        config.data_dir = str(data_path.absolute())
        console.print(f'[green]已选择数据目录[/]: {config.data_dir}')

    with open(config_file, "w", encoding="utf8") as f:
        f.write(config.to_json(ensure_ascii=False))

    return True, config


def choose_data_path(console: Console) -> Path:
    maybe_path = []
    for path in Path.home().iterdir():
        if path.is_dir():
            if 'OneDrive' in path.name:
                maybe_path.append(path)
    if len(maybe_path) == 0:
        return Path(Prompt.ask('[red]未找到 OneDrive 目录[/], 请手动指定数据目录', console=console))
    elif len(maybe_path) == 1:
        return maybe_path[0]
    else:
        console.print(f'找到多个 OneDrive 目录, 请选择:')
        for i, path in enumerate(maybe_path):
            console.print(f'[green]{i}[/] - {path}')
        index = IntPrompt.ask('请输入序号', console=console)
        return maybe_path[index]
