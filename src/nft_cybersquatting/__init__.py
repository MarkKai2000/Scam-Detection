"""
NFT 仿冒集合检测工具包。

该工具整合候选筛选、关键词生成、匹配与过滤四个阶段，
可在命令行中通过 ``python -m nft_cybersquatting.cli`` 调用。
"""

from .pipeline import DetectionPipeline, PipelineConfig, PipelineResult

__all__ = [
    "DetectionPipeline",
    "PipelineConfig",
    "PipelineResult",
]

__version__ = "0.1.0"
