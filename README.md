# NFT 仿冒集合检测工具

该仓库提供一个整合化的 NFT 仿冒检测工具，涵盖候选筛选、关键词生成、匹配与误报过滤四个阶段，可直接在命令行运行。

## 目录结构

- `data/`：示例数据集，包含 top 集合、全量集合及常见词列表。
- `src/nft_cybersquatting/`：工具实现代码，可作为 Python 包引入。

## 快速开始

```bash
cd Name
PYTHONPATH=src python3 -m nft_cybersquatting.cli \
  --output results.csv
```

运行结束后将输出匹配统计信息，并把检测结果写入到 `results.csv`。

## 常用参数

- `--top`：Top 集合 CSV 路径，默认使用 `data/top_collections.csv`。
- `--all`：全量集合 CSV 路径，默认 `data/all_collections.csv`。
- `--common-words`：常见词过滤列表，可替换为自定义文件。
- `--min-token-length`：生成关键词的最小长度，默认 3。
- `--extra-prefix / --extra-suffix`：追加自定义前缀或后缀策略。
- `--disable-acronym`：禁用首字母缩写策略。

## 单个名称关键词生成

若只想为某个官方集合名称生成仿冒关键词，可指定 `--single-name`，同时可选填 `--single-address`、`--single-rank` 等辅助信息：

```bash
cd Name
PYTHONPATH=src python3 -m nft_cybersquatting.cli \
  --single-name "Bored Ape Yacht Club" \
  --single-output bayc_keywords.csv
```

默认会使用 `data/common_words.txt` 过滤常见词，结果保存至 `keywords.csv`（或通过 `--single-output` 自定义）。

## 自定义流程

`nft_cybersquatting.pipeline.DetectionPipeline` 提供了 Python API，可在 Notebook 或其他项目中按需组合阶段：

```python
from pathlib import Path
from nft_cybersquatting import DetectionPipeline

pipeline = DetectionPipeline()
result = pipeline.run(
    top_path=Path("data/top_collections.csv"),
    candidate_path=Path("data/all_collections.csv"),
    common_words_path=Path("data/common_words.txt"),
)

print(result.summary())
```

`result.matches` 为 `MatchResult` 列表，可进一步做评分、验证或接入下游分析。
