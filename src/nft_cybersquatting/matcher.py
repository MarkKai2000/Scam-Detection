"""
匹配模块，执行第三阶段关键词匹配。
"""

from __future__ import annotations

from collections import defaultdict
from typing import Dict, Iterable, List, Sequence

from .aho_corasick import AhoCorasickAutomaton
from .data_models import (
    Collection,
    KeywordVariant,
    MatchResult,
    TopCollection,
    deduplicate_matches,
)
from .filters import CompositeFilter
from .normalization import normalize_token


class Matcher:
    def __init__(
        self,
        top_collections: Sequence[TopCollection],
        variants: Sequence[KeywordVariant],
        filters: CompositeFilter | None = None,
    ) -> None:
        self.top_collections = list(top_collections)
        self.variants = list(variants)
        self.filters = filters

        self._variant_map: Dict[int, List[KeywordVariant]] = defaultdict(list)
        for variant in self.variants:
            self._variant_map[variant.source_rank].append(variant)

        self._exact: Dict[str, List[KeywordVariant]] = defaultdict(list)
        self._ac = AhoCorasickAutomaton()
        for variant in self.variants:
            normalized = variant.normalized
            self._exact[normalized].append(variant)
            self._ac.add(normalized)
        self._ac.build()

        self._rank_index: Dict[int, TopCollection] = {
            collection.rank: collection for collection in self.top_collections
        }

    def match(self, candidates: Iterable[Collection]) -> List[MatchResult]:
        matches: List[MatchResult] = []
        for candidate in candidates:
            normalized = candidate.normalized_name

            exact_variants = self._exact.get(normalized, [])
            for variant in exact_variants:
                top = self._rank_index.get(variant.source_rank)
                if not top:
                    continue
                matches.append(
                    MatchResult(
                        source=top,
                        candidate=candidate,
                        variant=variant,
                        match_type="exact",
                    )
                )

            partial_keys = self._ac.find(normalized)
            for key in partial_keys:
                if key == normalized:
                    continue
                for variant in self._exact.get(key, []):
                    top = self._rank_index.get(variant.source_rank)
                    if not top:
                        continue
                    matches.append(
                        MatchResult(
                            source=top,
                            candidate=candidate,
                            variant=variant,
                            match_type="partial",
                        )
                    )

        matches = deduplicate_matches(matches)
        if self.filters:
            matches = self.filters.apply(matches)
        return matches
