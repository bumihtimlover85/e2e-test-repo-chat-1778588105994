"""集成测试 - 验证模块间协作"""
from src.app import add, subtract, load_config, save_config, get_env


class TestConfigWorkflow:
    """配置读写完整流程集成测试"""

    def test_save_load_roundtrip(self, tmp_path):
        """验证配置保存后能正确加载"""
        config_path = str(tmp_path / "app_config.json")
        original = {"app_name": "myapp", "version": "1.0", "debug": True}
        save_config(config_path, original)
        loaded = load_config(config_path)
        assert loaded == original

    def test_config_with_nested_data(self, tmp_path):
        """验证嵌套配置的保存和加载"""
        config_path = str(tmp_path / "nested_config.json")
        config = {
            "database": {"host": "localhost", "port": 5432},
            "features": ["auth", "logging"],
            "enabled": True,
        }
        save_config(config_path, config)
        loaded = load_config(config_path)
        assert loaded == config


class TestEnvAndConfigIntegration:
    """环境变量与配置协作集成测试"""

    def test_env_overrides_config(self, tmp_path, monkeypatch):
        """环境变量可覆盖配置值"""
        config_path = str(tmp_path / "env_config.json")
        config = {"db_host": "localhost", "db_port": "5432"}
        save_config(config_path, config)

        loaded = load_config(config_path)
        monkeypatch.setenv("DB_HOST", "production.db.example.com")

        db_host = get_env("DB_HOST", loaded["db_host"])
        assert db_host == "production.db.example.com"

        db_port = get_env("DB_PORT", loaded["db_port"])
        assert db_port == "5432"


class TestArithmeticWithConfig:
    """算术运算与配置协作集成测试"""

    def test_computation_with_config_params(self, tmp_path):
        """从配置文件读取参数并进行计算"""
        config_path = str(tmp_path / "calc_config.json")
        config = {"a": 10, "b": 3}
        save_config(config_path, config)

        params = load_config(config_path)
        result_add = add(params["a"], params["b"])
        result_sub = subtract(params["a"], params["b"])

        assert result_add == 13
        assert result_sub == 7

    def test_multi_step_computation(self):
        """多步计算流程"""
        step1 = add(5, 3)       # 8
        step2 = subtract(step1, 2)  # 6
        step3 = add(step2, 10)  # 16
        assert step3 == 16


class TestFileIOIntegration:
    """文件 I/O 集成测试"""

    def test_multiple_configs_same_dir(self, tmp_path):
        """同一目录下多个配置文件的管理"""
        configs = {
            "dev.json": {"env": "development", "debug": True},
            "prod.json": {"env": "production", "debug": False},
        }
        for name, cfg in configs.items():
            save_config(str(tmp_path / name), cfg)

        dev = load_config(str(tmp_path / "dev.json"))
        prod = load_config(str(tmp_path / "prod.json"))

        assert dev["env"] == "development"
        assert dev["debug"] is True
        assert prod["env"] == "production"
        assert prod["debug"] is False

    def test_config_update_workflow(self, tmp_path):
        """配置更新工作流"""
        config_path = str(tmp_path / "update_config.json")
        save_config(config_path, {"counter": 0})
        for i in range(1, 4):
            cfg = load_config(config_path)
            cfg["counter"] = i
            save_config(config_path, cfg)
        final = load_config(config_path)
        assert final["counter"] == 3
