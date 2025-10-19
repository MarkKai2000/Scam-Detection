"""
关键词生成模块，对热门 NFT 集合名称应用多种仿冒策略。
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Sequence, Set

from .data_models import KeywordVariant, TopCollection
from .normalization import normalize_token, normalize_whitespace, tokenize


DEFAULT_PREFIXES: Sequence[str] = (
    "official",
    "real",
    "meta",
    "my",
    "the",
    "crypto",
    "try",
    "mint",
    "get",
)

DEFAULT_SUFFIXES: Sequence[str] = (
    "nft",
    "official",
    "club",
    "dao",
    "mint",
    "drop",
    "labs",
    "verse",
    "token",
    "app",
    "collection",
)

DEFAULT_SUBSTITUTIONS: Dict[str, Sequence[str]] = {
    "a": ("4", "@"),
    "b": ("8",),
    "e": ("3",),
    "g": ("9",),
    "i": ("1",),
    "l": ("1",),
    "o": ("0",),
    "s": ("5", "$"),
    "t": ("7",),
    "z": ("2",),
}


@dataclass
class GeneratorConfig:
    prefixes: Sequence[str] = DEFAULT_PREFIXES
    suffixes: Sequence[str] = DEFAULT_SUFFIXES
    substitutions: Dict[str, Sequence[str]] | None = None
    min_token_length: int = 3
    include_acronym: bool = True


class KeywordGenerator:
    def __init__(self, config: GeneratorConfig | None = None) -> None:
        if config is None:
            config = GeneratorConfig()
        substitutions = config.substitutions or DEFAULT_SUBSTITUTIONS
        self.config = GeneratorConfig(
            prefixes=tuple(config.prefixes),
            suffixes=tuple(config.suffixes),
            substitutions={k: tuple(v) for k, v in substitutions.items()},
            min_token_length=config.min_token_length,
            include_acronym=config.include_acronym,
        )

    def generate(self, collection: TopCollection) -> List[KeywordVariant]:
        seen: Set[str] = set()
        variants: List[KeywordVariant] = []

        def add(raw: str, transformation: str) -> None:
            normalized = normalize_token(raw)
            if len(normalized) < self.config.min_token_length:
                return
            if normalized in seen:
                return
            seen.add(normalized)
            variants.append(
                KeywordVariant(
                    source_rank=collection.rank,
                    source_name=collection.name,
                    transformation=transformation,
                    raw=normalize_whitespace(raw),
                )
            )

        base_name = normalize_whitespace(collection.name)
        sanitized = normalize_token(collection.name)

        add(collection.name, "canonical")
        add(base_name.lower(), "lower")
        add(sanitized, "compact")

        if " " in base_name:
            add(base_name.replace(" ", ""), "remove_space")
            add(base_name.replace(" ", "-"), "dash")
            add(base_name.replace(" ", "."), "dot")

        words = tokenize(collection.name)
        if words and self.config.include_acronym:
            acronym = "".join(word[0] for word in words if word)
            if len(acronym) >= self.config.min_token_length:
                add(acronym, "acronym")

        for prefix in self.config.prefixes:
            add(f"{prefix} {base_name}", f"prefix_{prefix}")

        for suffix in self.config.suffixes:
            add(f"{base_name} {suffix}", f"suffix_{suffix}")

        # 字符省略
        if len(sanitized) > self.config.min_token_length:
            for idx in range(len(sanitized)):
                add(sanitized[:idx] + sanitized[idx + 1 :], "typo_omit")

        # 邻位交换
        if len(sanitized) > self.config.min_token_length:
            for idx in range(len(sanitized) - 1):
                swapped = (
                    sanitized[:idx]
                    + sanitized[idx + 1]
                    + sanitized[idx]
                    + sanitized[idx + 2 :]
                )
                add(swapped, "typo_swap")

        # Leet 替换
        for idx, ch in enumerate(sanitized):
            substitutes = self.config.substitutions.get(ch, ())
            for sub in substitutes:
                add(sanitized[:idx] + sub + sanitized[idx + 1 :], f"leet_{ch}_to_{sub}")

        # 重复字符
        for idx, ch in enumerate(sanitized):
            add(sanitized[:idx] + ch * 2 + sanitized[idx + 1 :], "typo_double")

        # 插入分隔符
        for separator in (".", "-", "_"):
            if len(words) > 1:
                add(separator.join(words), f"join_{separator}")

        return variants


if __name__ == "__main__":
    # 简单测试
    generator = KeywordGenerator()
    collection = TopCollection(
        rank=1,
        address="0x0000000000000000000000000000000000000000",
        name="CryptoPunks",
        slug="cryptopunks",
    )
    keywords = generator.generate(collection)
    for kw in keywords:
        print(kw)