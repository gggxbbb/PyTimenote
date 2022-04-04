from rich.console import Console

from PyTimenote.timenote.category import CategoryList
from PyTimenote.utils.data import load_data
from rich.prompt import Prompt
from rich.markdown import Markdown
from rich.panel import Panel
from .utils.config import init_config
from .utils.init import config_init


# noinspection PyBroadException
def main():
    """
    程序主入口
    """
    console = Console(markup=True, color_system='truecolor')
    console.print("[bold]时光记[/] - [green]JSON 备份文件查看器[/]")
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
        if not if_ok:
            console.print("再见!")
            return
        while True:
            console.print(ls)
            n_target = Prompt.ask("看哪个呢(输入 q 退出)")
            if n_target == 'q':
                break
            try:
                path_to_target = n_target.split('.')
                root_category = list(notes.categories.values())[int(path_to_target[0])]
                if len(path_to_target) == 2:
                    if root_category.children_category:
                        target_index = int(path_to_target[1]) - len(root_category.children_category)
                    else:
                        target_index = int(path_to_target[1])
                    target = root_category.children_note.notes[target_index]
                elif len(path_to_target) == 3:
                    sub_category = list(root_category.children_category.categories.values())[int(path_to_target[1])]
                    target = sub_category.children_note.notes[int(path_to_target[2])]
                else:
                    raise ValueError
                md = Markdown(target.content)
                panel = Panel(md, title=target.get_info())
                console.print(panel)
            except Exception as e:
                console.print('[red]异常的路径![/red]')


if __name__ == '__main__':
    main()
