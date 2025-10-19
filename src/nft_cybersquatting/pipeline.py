"""
检测管线封装，串联四个阶段。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from .data_models import KeywordVariant, MatchResult, TopCollection
from .filters import (
    CommonWordFilter,
    CompositeFilter,
    DistinctNameFilter,
    MinimumLengthFilter,
    OfficialAddressFilter,
)
from .io import load_collections, load_top_collections, load_word_list, write_matches
from .keyword_generator import GeneratorConfig, KeywordGenerator
from .matcher import Matcher


@dataclass
class PipelineConfig:
    generator: GeneratorConfig = field(default_factory=GeneratorConfig)


@dataclass
class PipelineResult:
    top_collections: list[TopCollection]
    keyword_variants: list[KeywordVariant]
    matches: list[MatchResult]

    def summary(self) -> dict[str, int]:
        return {
            "top_collections": len(self.top_collections),
            "keyword_variants": len(self.keyword_variants),
            "matches": len(self.matches),
        }


class DetectionPipeline:
    def __init__(self, config: PipelineConfig | None = None) -> None:
        self.config = config or PipelineConfig()

    def run(
        self,
        top_path: Path,
        candidate_path: Path,
        *,
        common_words_path: Optional[Path] = None,
        output_path: Optional[Path] = None,
    ) -> PipelineResult:
        top_path = Path(top_path)
        candidate_path = Path(candidate_path)
        if common_words_path is not None:
            common_words_path = Path(common_words_path)
        if output_path is not None:
            output_path = Path(output_path)

        top_collections = load_top_collections(top_path)
        generator = KeywordGenerator(self.config.generator)
        variants: list[KeywordVariant] = []
        for collection in top_collections:
            variants.extend(generator.generate(collection))

        candidates = load_collections(candidate_path)
        official_addresses = {
            collection.address.lower()
            for collection in top_collections
            if collection.address
        }
        official_names = {collection.normalized_name for collection in top_collections}

        filters = [
            MinimumLengthFilter(self.config.generator.min_token_length),
            DistinctNameFilter(official_names),
            OfficialAddressFilter(official_addresses),
        ]

        if common_words_path and common_words_path.exists():
            common_words = load_word_list(common_words_path)
            filters.append(CommonWordFilter(common_words))

        composite = CompositeFilter(filters)
        matcher = Matcher(top_collections, variants, composite)
        matches = matcher.match(candidates)

        if output_path:
            write_matches(output_path, matches)

        return PipelineResult(
            top_collections=top_collections,
            keyword_variants=variants,
            matches=matches,
        )
