"""
简化版 Aho-Corasick 自动机，实现高效子串匹配。
"""

from __future__ import annotations

from collections import deque
from typing import Dict, List, Optional, Set


class AhoCorasickAutomaton:
    def __init__(self) -> None:
        self._next: List[Dict[str, int]] = [{}]
        self._fail: List[int] = [0]
        self._output: List[Set[str]] = [set()]
        self._built = False

    def add(self, word: str) -> None:
        if not word:
            return
        node = 0
        for ch in word:
            node = self._next[node].setdefault(ch, len(self._next))
            if node == len(self._fail):
                self._next.append({})
                self._fail.append(0)
                self._output.append(set())
        self._output[node].add(word)
        self._built = False

    def build(self) -> None:
        queue: deque[int] = deque()
        for ch, nxt in self._next[0].items():
            self._fail[nxt] = 0
            queue.append(nxt)
        while queue:
            node = queue.popleft()
            for ch, nxt in self._next[node].items():
                queue.append(nxt)
                fail_state = self._fail[node]
                while ch not in self._next[fail_state] and fail_state != 0:
                    fail_state = self._fail[fail_state]
                self._fail[nxt] = self._next[fail_state].get(ch, 0)
                self._output[nxt].update(self._output[self._fail[nxt]])
        self._built = True

    def find(self, text: str) -> Set[str]:
        if not self._built:
            self.build()
        matches: Set[str] = set()
        state = 0
        for ch in text:
            while ch not in self._next[state] and state != 0:
                state = self._fail[state]
            state = self._next[state].get(ch, 0)
            if self._output[state]:
                matches.update(self._output[state])
        return matches
