# e2e-test-repo-chat-1778588105994

Auto created by MultiAgentSystem

## 项目结构

```
├── .github/
│   └── workflows/
│       └── ci.yml            # GitHub Actions CI 配置
├── src/
│   ├── __init__.py
│   └── app.py                # 最小化业务模块
├── tests/
│   ├── __init__.py
│   ├── unit/                 # 单元测试目录
│   │   ├── __init__.py
│   │   └── test_app.py
│   └── integration/          # 集成测试目录
│       ├── __init__.py
│       └── test_integration.py
├── requirements.txt          # 项目依赖
├── requirements-dev.txt      # 开发/测试依赖
└── README.md
```

## 本地运行测试

### 安装依赖

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### 运行单元测试（含覆盖率）

```bash
pytest tests/unit/ --cov=src --cov-report=term-missing --cov-fail-under=80
```

### 运行集成测试

```bash
pytest tests/integration/
```

### 运行所有测试

```bash
pytest --cov=src --cov-report=term-missing
```

### 运行 Lint 检查

```bash
ruff check src/ tests/
```

## CI 流水线

本项目使用 GitHub Actions CI 流水线，在 push 到 `main` 分支或提交 PR 时自动触发，包含三个独立 Job：

| Job | 说明 |
|-----|------|
| **Unit Tests** | 运行单元测试，覆盖率要求 ≥ 80% |
| **Integration Tests** | 运行集成测试 |
| **Lint** | 使用 ruff 进行静态检查 |
