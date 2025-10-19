"""
名称归一化工具函数。
"""

from __future__ import annotations

import re
import unicodedata
from functools import lru_cache

_NON_ALNUM = re.compile(r"[^a-z0-9]")
_COLLAPSE_WS = re.compile(r"\s+")


def normalize_whitespace(value: str) -> str:
    """
    将字符串归一化为单空格分隔。
    """
    if not value:
        return ""
    value = unicodedata.normalize("NFKC", value)
    value = value.replace("_", " ")
    value = _COLLAPSE_WS.sub(" ", value.strip())
    return value


@lru_cache(maxsize=10_000)
def normalize_token(value: str) -> str:
    """
    将字符串转换为仅含小写字母与数字的 token。
    """
    if not value:
        return ""
    value = normalize_whitespace(value)
    value = value.lower()
    value = _NON_ALNUM.sub("", value)
    return value


def tokenize(value: str) -> list[str]:
    """
    按空格切分归一化名称，返回非空 token 列表。
    """
    value = normalize_whitespace(value)
    if not value:
        return []
    return [part for part in value.split(" ") if part]
