"""最小化示例应用模块"""
import os
import json


def add(a: int, b: int) -> int:
    """加法运算"""
    return a + b


def subtract(a: int, b: int) -> int:
    """减法运算"""
    return a - b


def load_config(path: str) -> dict:
    """从 JSON 文件加载配置"""
    with open(path, "r") as f:
        return json.load(f)


def save_config(path: str, config: dict) -> None:
    """保存配置到 JSON 文件"""
    with open(path, "w") as f:
        json.dump(config, f, indent=2)


def get_env(key: str, default: str = "") -> str:
    """获取环境变量"""
    return os.environ.get(key, default)
