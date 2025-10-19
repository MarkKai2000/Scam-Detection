"""
匹配结果过滤器，负责第四阶段的误报清洗。
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Protocol, Sequence, Set

from .data_models import MatchResult
from .normalization import normalize_token


class Filter(Protocol):
    def keep(self, result: MatchResult) -> bool:
        ...


@dataclass
class CommonWordFilter:
    words: Set[str]

    def keep(self, result: MatchResult) -> bool:
        variant = result.variant.normalized
        return variant not in self.words


@dataclass
class OfficialAddressFilter:
    addresses: Set[str]

    def keep(self, result: MatchResult) -> bool:
        return result.candidate.address.lower() not in self.addresses


@dataclass
class MinimumLengthFilter:
    length: int = 3

    def keep(self, result: MatchResult) -> bool:
        return len(result.variant.normalized) >= self.length


@dataclass
class DistinctNameFilter:
    """
    移除与官方名称仅大小写差异的集合。
    """

    official_names: Set[str]

    def keep(self, result: MatchResult) -> bool:
        return result.candidate.normalized_name not in self.official_names


class CompositeFilter:
    def __init__(self, filters: Sequence[Filter]) -> None:
        self._filters = list(filters)

    def keep(self, result: MatchResult) -> bool:
        return all(f.keep(result) for f in self._filters)

    def apply(self, matches: Iterable[MatchResult]) -> list[MatchResult]:
        return [match for match in matches if self.keep(match)]
