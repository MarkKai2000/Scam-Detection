"""
命令行入口。
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .data_models import TopCollection
from .io import load_word_list, write_keywords
from .keyword_generator import (
    DEFAULT_PREFIXES,
    DEFAULT_SUFFIXES,
    GeneratorConfig,
    KeywordGenerator,
)
from .pipeline import DetectionPipeline, PipelineConfig


def _default_data_dir() -> Path:
    return Path(__file__).resolve().parents[2] / "data"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="NFT 仿冒集合检测工具")
    parser.add_argument(
        "--top",
        type=Path,
        default=_default_data_dir() / "top_collections.csv",
        help="Top 集合列表 CSV 路径（默认使用仓库自带数据）",
    )
    parser.add_argument(
        "--all",
        dest="all_collections",
        type=Path,
        default=_default_data_dir() / "all_collections.csv",
        help="全量 NFT 集合 CSV 路径（默认使用仓库自带数据）",
    )
    parser.add_argument(
        "--common-words",
        type=Path,
        default=_default_data_dir() / "common_words.txt",
        help="常见词过滤列表（可选）",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("matches.csv"),
        help="匹配结果输出路径（默认：./matches.csv）",
    )
    parser.add_argument(
        "--min-token-length",
        type=int,
        default=3,
        help="生成关键词的最小 token 长度（默认：3）",
    )
    parser.add_argument(
        "--disable-acronym",
        action="store_true",
        help="禁用首字母缩写生成策略",
    )
    parser.add_argument(
        "--extra-prefix",
        action="append",
        default=[],
        help="额外添加的前缀（可多次指定）",
    )
    parser.add_argument(
        "--extra-suffix",
        action="append",
        default=[],
        help="额外添加的后缀（可多次指定）",
    )
    parser.add_argument(
        "--single-name",
        type=str,
        help="仅针对该名称生成仿冒关键词（启用后不执行全量检测）",
    )
    parser.add_argument(
        "--single-rank",
        type=int,
        default=0,
        help="单个名称对应的 rank（可选，用于输出标识）",
    )
    parser.add_argument(
        "--single-address",
        type=str,
        default="",
        help="单个名称的官方合约地址（可选，用于输出标识）",
    )
    parser.add_argument(
        "--single-slug",
        type=str,
        default="",
        help="单个名称的 slug（可选，用于输出标识）",
    )
    parser.add_argument(
        "--single-output",
        type=Path,
        default=Path("keywords.csv"),
        help="单个名称关键词输出路径（默认：./keywords.csv）",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    prefixes = list(DEFAULT_PREFIXES)
    prefixes.extend(args.extra_prefix)
    suffixes = list(DEFAULT_SUFFIXES)
    suffixes.extend(args.extra_suffix)

    generator_config = GeneratorConfig(
        prefixes=tuple(prefixes),
        suffixes=tuple(suffixes),
        min_token_length=args.min_token_length,
        include_acronym=not args.disable_acronym,
    )

    if args.single_name:
        generator = KeywordGenerator(generator_config)
        collection = TopCollection(
            rank=args.single_rank,
            address=args.single_address,
            name=args.single_name,
            slug=args.single_slug,
        )
        variants = generator.generate(collection)
        if args.common_words and args.common_words.exists():
            common_words = load_word_list(args.common_words)
            variants = [v for v in variants if v.normalized not in common_words]
        write_keywords(args.single_output, variants)
        print(f"已为「{args.single_name}」生成 {len(variants)} 条仿冒关键词。")
        print(f"结果已写入：{args.single_output.resolve()}")
        return 0

    pipeline = DetectionPipeline(PipelineConfig(generator=generator_config))
    result = pipeline.run(
        args.top,
        args.all_collections,
        common_words_path=args.common_words if args.common_words.exists() else None,
        output_path=args.output,
    )

    summary = result.summary()
    print(
        f"完成检测：候选 {summary['top_collections']} 个，"
        f"关键词 {summary['keyword_variants']} 个，"
        f"命中 {summary['matches']} 条。"
    )
    print(f"结果已写入：{args.output.resolve()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
