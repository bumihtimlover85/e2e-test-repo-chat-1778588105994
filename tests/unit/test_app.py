"""针对 src/app.py 的单元测试"""
import json
import pytest

from src.app import add, subtract, load_config, save_config, get_env


class TestAdd:
    """add 函数单元测试"""

    def test_add_positive(self):
        assert add(1, 2) == 3

    def test_add_negative(self):
        assert add(-1, -2) == -3

    def test_add_zero(self):
        assert add(0, 0) == 0

    def test_add_mixed(self):
        assert add(-1, 5) == 4


class TestSubtract:
    """subtract 函数单元测试"""

    def test_subtract_positive(self):
        assert subtract(5, 3) == 2

    def test_subtract_negative(self):
        assert subtract(-1, -2) == 1

    def test_subtract_zero(self):
        assert subtract(0, 0) == 0

    def test_subtract_result_negative(self):
        assert subtract(3, 5) == -2


class TestLoadConfig:
    """load_config 函数单元测试"""

    def test_load_valid_config(self, tmp_path):
        config_file = tmp_path / "config.json"
        config_file.write_text(json.dumps({"key": "value", "debug": True}))
        result = load_config(str(config_file))
        assert result == {"key": "value", "debug": True}

    def test_load_empty_config(self, tmp_path):
        config_file = tmp_path / "empty.json"
        config_file.write_text("{}")
        result = load_config(str(config_file))
        assert result == {}

    def test_load_missing_file(self):
        with pytest.raises(FileNotFoundError):
            load_config("/nonexistent/path/config.json")


class TestSaveConfig:
    """save_config 函数单元测试"""

    def test_save_and_reload(self, tmp_path):
        config_file = tmp_path / "output.json"
        config = {"host": "localhost", "port": 8080}
        save_config(str(config_file), config)
        result = load_config(str(config_file))
        assert result == config

    def test_save_overwrite(self, tmp_path):
        config_file = tmp_path / "overwrite.json"
        save_config(str(config_file), {"v": 1})
        save_config(str(config_file), {"v": 2})
        result = load_config(str(config_file))
        assert result == {"v": 2}


class TestGetEnv:
    """get_env 函数单元测试"""

    def test_get_existing_env(self, monkeypatch):
        monkeypatch.setenv("TEST_KEY", "test_value")
        assert get_env("TEST_KEY") == "test_value"

    def test_get_missing_env_default(self):
        assert get_env("NONEXISTENT_KEY_XYZ") == ""

    def test_get_missing_env_custom_default(self):
        assert get_env("NONEXISTENT_KEY_XYZ", "fallback") == "fallback"
