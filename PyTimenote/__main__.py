from rich.console import Console

from PyTimenote.timenote.category import CategoryList
from PyTimenote.timenote.note import NotesList
from PyTimenote.utils.data import load_data
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
    if_config = config_init(console)  # 初始化配置文件目录
    if not if_config:
        console.print("再见!")
        return
    else:
        (if_ok, config) = init_config(console)  # 加载配置文件
        datas = load_data(console, config)  # 加载数据
        notes = CategoryList(datas, console)  # 初始化笔记列表
        ls = notes.build_tree()  # 构建笔记列表
        console.print(ls)
        if not if_ok:
            console.print("再见!")
            return


if __name__ == '__main__':
    main()
