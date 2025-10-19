"""
数据读写工具。
"""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Iterable, List, Sequence, Set

from .data_models import Collection, KeywordVariant, MatchResult, TopCollection
from .normalization import normalize_token


def _read_csv(path: Path) -> List[dict]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        return [row for row in reader]


def load_top_collections(path: Path) -> List[TopCollection]:
    rows = _read_csv(path)
    seen_names: Set[str] = set()
    collections: List[TopCollection] = []
    for row in rows:
        name = row.get("name") or row.get("Name") or ""
        normalized = normalize_token(name)
        if not normalized:
            continue
        if normalized in seen_names:
            continue
        seen_names.add(normalized)
        try:
            rank = int(row.get("rank") or row.get("Rank") or 0)
        except ValueError:
            rank = 0
        collections.append(
            TopCollection(
                rank=rank,
                address=(row.get("address") or row.get("Address") or "").strip(),
                name=name.strip(),
                slug=(row.get("slug") or row.get("Slug") or "").strip(),
                schema_name=(row.get("schema_name") or row.get("Schema") or "").strip() or None,
                extra={k: v for k, v in row.items() if k not in {"rank", "address", "name", "slug", "schema_name"}},
            )
        )
    return collections


def load_collections(path: Path) -> List[Collection]:
    rows = _read_csv(path)
    collections: List[Collection] = []
    for row in rows:
        name = row.get("name") or row.get("Name") or ""
        if not name:
            continue
        collections.append(
            Collection(
                address=(row.get("address") or row.get("Address") or "").strip(),
                name=name.strip(),
                slug=(row.get("slug") or row.get("Slug") or "").strip(),
                extra={k: v for k, v in row.items() if k not in {"address", "name", "slug"}},
            )
        )
    return collections


def load_word_list(path: Path) -> Set[str]:
    with path.open("r", encoding="utf-8") as f:
        tokens = {normalize_token(line.strip()) for line in f if line.strip()}
    return {token for token in tokens if token}


def write_matches(path: Path, matches: Iterable[MatchResult]) -> None:
    matches = list(matches)
    if not matches:
        headers: Sequence[str] = [
            "source_rank",
            "source_name",
            "source_address",
            "candidate_address",
            "candidate_name",
            "candidate_slug",
            "variant_transformation",
            "variant_raw",
            "match_type",
            "score",
        ]
    else:
        headers = list(matches[0].to_dict().keys())
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        for item in matches:
            writer.writerow(item.to_dict())


def write_keywords(path: Path, variants: Iterable[KeywordVariant]) -> None:
    variants = list(variants)
    headers: Sequence[str] = [
        "source_rank",
        "source_name",
        "transformation",
        "raw",
        "normalized",
    ]
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        for variant in variants:
            writer.writerow(
                {
                    "source_rank": variant.source_rank,
                    "source_name": variant.source_name,
                    "transformation": variant.transformation,
                    "raw": variant.raw,
                    "normalized": variant.normalized,
                }
            )
