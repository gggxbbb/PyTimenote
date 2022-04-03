from rich.console import Console

from .utils.init import config_init
from .utils.config import Config, init_config


def main():
    """
    程序主入口
    """
    console = Console(markup=True)
    console.print("[bold]时光记[/] - [green]CLI[/]")
    if not console.color_system == 'truecolor':
        console.print(f'该终端不支持 24 位颜色，程序将运行在 {console.color_system} 模式下，部分体验可能不佳。')
    if_config = config_init(console)
    if not if_config:
        console.print("再见!")
        return
    else:
        if_ok: bool
        config: Config
        (if_ok, config) = init_config(console)
        if not if_ok:
            console.print("再见!")
            return


if __name__ == '__main__':
    main()
