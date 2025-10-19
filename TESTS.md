# 测试说明

本工具提供 pytest 测试用例，覆盖核心关键词生成与检测流程，免去手动运行 CLI 的需求。

## 环境准备

推荐使用 Python 3.9+，并在项目根目录执行以下命令安装依赖：

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip pytest
```

## 运行测试

在 `Name/` 目录下执行：

```bash
env PYTHONPATH=src pytest
```

或使用已激活的虚拟环境：

```bash
PYTHONPATH=src pytest
```

## 测试内容

- **关键词生成**：验证 `KeywordGenerator` 对单个集合名称的默认策略（前后缀、首字母缩写等）。
- **检测管线**：使用临时数据集构建完整流程，校验过滤逻辑与匹配结果。

如需扩展测试，可在 `tests/` 目录新增模块，复用现有夹具和临时文件策略。
