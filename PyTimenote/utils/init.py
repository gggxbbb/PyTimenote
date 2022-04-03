from rich.console import Console
from rich.prompt import Confirm
from pathlib import Path


def config_init(console: Console, force: bool = False) -> bool:
    """
    初始化配置文件目录和空配置文件
    :param console: 全局 Console 对象
    :param force: 是否强制初始化
    :return: 成功与否
    """
    config_dir = Path.home() / ".PyTimenote"
    if not config_dir.exists() or force:
        if_ok = Confirm.ask(f"看起来这是你第一次运行本程序, 程序将在 {config_dir} 目录下创建配置文件和存放数据, 是否允许并继续?", console=console)
        if if_ok:
            config_dir.mkdir(parents=True, exist_ok=True)
            config_file = config_dir / "config.json"
            config_file.touch()
            if config_file.exists():
                with open(config_file, 'w', encoding='utf-8') as f:
                    f.write('{}')
            return True
        else:
            return False
    else:
        return True
