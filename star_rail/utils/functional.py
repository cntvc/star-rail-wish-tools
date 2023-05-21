import json
import os
import time
from pathlib import Path

__all__ = [
    "save_json",
    "load_json",
    "clear_screen",
    "pause",
    "color_str",
    "input_int",
    "dedupe",
    "get_format_time",
]


def touch(full_path: str):
    path = Path(full_path)
    os.makedirs(path.parent, exist_ok=True)
    if not path.exists():
        path.touch()


def save_json(full_path: str, data):
    touch(full_path)
    with open(full_path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, sort_keys=False, indent=4)


def load_json(full_path: str) -> dict:
    with open(full_path, "r", encoding="UTF-8") as file:
        data = json.load(file)
    return data


def clear_screen():
    os.system("cls")


def pause():
    os.system("pause")


def color_str(string: str, color: str = "none"):
    """generate color str

    Args:
        string (str): string
        color (str, optional): converted target color. Defaults to "none".
            support color:[red, green, yellow, blue]

    Returns:
        str: colored characters in the command line
    """
    color_list = {
        "red": "\033[1;31;40m",
        "green": "\033[1;32;40m",
        "yellow": "\033[1;33;40m",
        "blue": "\033[1;34;40m",
        "none": "\033[0m",
    }
    color_code = color_list.get(color, None)
    if color_code:
        return "{}{}\033[0m".format(color_code, string)
    else:
        return string


def input_int(left: int, right: int):
    """
    input a integer, and the range of integers is in the interval [left, right]
    """
    while True:
        index = input()
        if not index.isdigit():
            print(color_str("{} 为非法输入，请重试".format(index), "yellow"))
            continue

        index = int(index)
        if index > right or index < left:
            print(color_str("{} 为非法输入，请重试".format(index), "yellow"))
            continue

        return index


def dedupe(items, key=None):
    """Eliminate duplicate elements and keep order

    Args:
        items (iterable)
        key (function, optional): Convert sequence elements to hashable type. Defaults to None.

    Yields:
        _type_: sequence item
    """
    seen = set()
    for item in items:
        val = item if key is None else key(item)
        if val not in seen:
            yield item
            seen.add(val)


def get_format_time(std_time: float = None, time_format: str = "%Y-%m-%d %H:%M:%S"):
    if std_time is None:
        return time.strftime(time_format, time.localtime(time.time()))
    else:
        return time.strftime(time_format, time.localtime(std_time))
