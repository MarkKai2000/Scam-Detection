from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from nft_cybersquatting import DetectionPipeline, PipelineConfig  # noqa: E402
from nft_cybersquatting.keyword_generator import KeywordGenerator  # noqa: E402
from nft_cybersquatting.keyword_generator import GeneratorConfig  # noqa: E402
from nft_cybersquatting.data_models import TopCollection  # noqa: E402


@pytest.fixture
def sample_collection() -> TopCollection:
    return TopCollection(
        rank=1,
        address="0xabc",
        name="Test Collection",
        slug="test-collection",
    )


def test_keyword_generator_variants(sample_collection: TopCollection) -> None:
    generator = KeywordGenerator(
        GeneratorConfig(
            prefixes=("verify",),
            suffixes=("nft",),
            min_token_length=3,
            include_acronym=True,
        )
    )
    variants = generator.generate(sample_collection)
    texts = {variant.raw for variant in variants}
    assert "Test Collection" in texts
    assert "verify Test Collection" in texts
    assert "Test Collection nft" in texts
    assert any(variant.transformation == "acronym" for variant in variants)


def test_pipeline_matches(tmp_path: Path) -> None:
    top_path = tmp_path / "top.csv"
    all_path = tmp_path / "all.csv"
    common_path = tmp_path / "common.txt"

    top_path.write_text(
        "rank,address,name,slug,schema_name\n"
        "1,0xabc,Test Collection,test-collection,ERC721\n",
        encoding="utf-8",
    )
    all_path.write_text(
        "address,name,slug\n"
        "0xabc,Test Collection,test-collection\n"
        "0x111,Official Test Collection,official-test-collection\n"
        "0x222,Test Collection Drop,test-collection-drop\n",
        encoding="utf-8",
    )
    common_path.write_text("official\n", encoding="utf-8")

    pipeline = DetectionPipeline(PipelineConfig())
    result = pipeline.run(
        top_path=top_path,
        candidate_path=all_path,
        common_words_path=common_path,
    )

    summary = result.summary()
    assert summary["top_collections"] == 1
    assert summary["matches"] >= 1

    candidate_addresses = {match.candidate.address for match in result.matches}
    assert "0xabc" not in candidate_addresses
    assert "0x111" in candidate_addresses or "0x222" in candidate_addresses
