"""
核心数据模型定义。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Iterable, Optional

from .normalization import normalize_token, normalize_whitespace


@dataclass(frozen=True)
class TopCollection:
    rank: int
    address: str
    name: str
    slug: str
    schema_name: Optional[str] = None
    extra: Dict[str, str] = field(default_factory=dict)

    @property
    def normalized_name(self) -> str:
        return normalize_token(self.name)


@dataclass(frozen=True)
class Collection:
    address: str
    name: str
    slug: str = ""
    extra: Dict[str, str] = field(default_factory=dict)

    @property
    def normalized_name(self) -> str:
        return normalize_token(self.name)


@dataclass(frozen=True)
class KeywordVariant:
    source_rank: int
    source_name: str
    transformation: str
    raw: str

    @property
    def normalized(self) -> str:
        return normalize_token(self.raw)


@dataclass(frozen=True)
class MatchResult:
    source: TopCollection
    candidate: Collection
    variant: KeywordVariant
    match_type: str  # exact / partial
    score: float = 1.0

    def to_dict(self) -> Dict[str, str]:
        return {
            "source_rank": str(self.source.rank),
            "source_name": self.source.name,
            "source_address": self.source.address,
            "candidate_address": self.candidate.address,
            "candidate_name": self.candidate.name,
            "candidate_slug": self.candidate.slug,
            "variant_transformation": self.variant.transformation,
            "variant_raw": normalize_whitespace(self.variant.raw),
            "match_type": self.match_type,
            "score": f"{self.score:.4f}",
        }


def deduplicate_matches(matches: Iterable[MatchResult]) -> list[MatchResult]:
    seen = set()
    result: list[MatchResult] = []
    for item in matches:
        key = (
            item.variant.normalized,
            item.candidate.address.lower(),
            item.match_type,
        )
        if key in seen:
            continue
        seen.add(key)
        result.append(item)
    return result
