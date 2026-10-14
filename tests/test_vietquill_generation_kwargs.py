"""Model-free tests for decoding kwargs, style presets and candidate filtering."""

import pytest

from vietquill import ParaphraseStyle
from vietquill.generation.controllable_paraphraser.base import BaseParaphraseGenerator

SRC = "Hôm nay trời đẹp quá."


class DummyGenerator(BaseParaphraseGenerator):
    def paraphrase(self, text, **kwargs):
        return []

    def paraphrases(self, texts, **kwargs):
        return []


class FakeEstimator:
    def __init__(self, scores):
        self.scores = scores
        self.calls = 0

    def estimate(self, sentence1, sentence2):
        self.calls += 1
        return {"semantic_score": self.scores[sentence2]}


def resolve(**kwargs):
    """Runs the same kwargs pipeline as paraphrase() and returns (controls, filter, gen_kwargs, n)."""
    gen = DummyGenerator()
    controls = gen._resolve_controls(kwargs)
    quality_filter = gen._pop_quality_filter(kwargs)
    gen_kwargs, _, n = gen._prepare_gen_kwargs(kwargs)
    return controls, quality_filter, gen_kwargs, n


def test_default_decoding_is_beam_search():
    controls, (estimator, min_semantic), gk, n = resolve()
    assert controls == (90, 85, 80)
    assert estimator is None and min_semantic is None
    assert gk["do_sample"] is False
    assert gk["num_beams"] == 5
    assert gk["num_return_sequences"] == n + 2
    assert gk["early_stopping"] is True
    assert "top_p" not in gk


def test_beam_search_widens_beams_to_cover_returns():
    _, _, gk, _ = resolve(num_candidates=6, num_beams=2)
    assert gk["num_return_sequences"] == 8
    assert gk["num_beams"] == 8


def test_sampling_with_one_beam_is_plain_sampling():
    _, _, gk, _ = resolve(do_sample=True, num_beams=1, num_candidates=3)
    assert gk["num_beams"] == 1
    assert gk["num_return_sequences"] == 5
    assert gk["do_sample"] is True
    assert "early_stopping" not in gk
    assert {"top_k", "top_p", "temperature"} <= gk.keys()


def test_sampling_with_beams_is_beam_sampling():
    _, _, gk, _ = resolve(do_sample=True, num_beams=2, num_candidates=3)
    assert gk["num_beams"] == 5


@pytest.mark.parametrize(
    "style, expected",
    [
        (ParaphraseStyle.CONSERVATIVE, dict(do_sample=False, num_beams=5)),
        ("balanced", dict(do_sample=True, num_beams=1, top_p=0.9, temperature=0.7, top_k=0)),
        (ParaphraseStyle.DIVERSE, dict(do_sample=True, num_beams=1, top_p=0.95, temperature=1.0, top_k=0)),
    ],
)
def test_style_sets_decoding(style, expected):
    _, _, gk, _ = resolve(style=style)
    for key, value in expected.items():
        assert gk[key] == value


def test_diverse_oversamples_and_sets_min_semantic():
    controls, (_, min_semantic), gk, n = resolve(style=ParaphraseStyle.DIVERSE, num_candidates=2)
    assert controls == (85, 60, 40)
    assert min_semantic == 80
    assert gk["num_return_sequences"] == n + 6
    assert "oversample" not in gk and "min_semantic" not in gk


def test_explicit_kwargs_override_style():
    _, (_, min_semantic), gk, _ = resolve(
        style="diverse", top_p=0.8, num_beams=4, min_semantic=90, oversample=1
    )
    assert gk["top_p"] == 0.8
    assert gk["num_beams"] == 4  # beam-sampling, already >= 1 + 1 returns
    assert gk["num_return_sequences"] == 2
    assert min_semantic == 90

    _, _, gk, _ = resolve(style="balanced", do_sample=False)
    assert gk["do_sample"] is False
    assert gk["num_beams"] == 5  # widened to num_candidates + BALANCED oversample (4)


def test_style_does_not_leak_into_generate_kwargs():
    _, _, gk, _ = resolve(style="diverse", lexical=30)
    for key in ("style", "lexical", "semantic", "syntactic", "estimator", "min_semantic", "oversample"):
        assert key not in gk


def test_estimator_from_attribute_or_kwarg():
    gen = DummyGenerator()
    est = FakeEstimator({})
    assert gen._pop_quality_filter({"estimator": est})[0] is est
    gen.estimator = est
    assert gen._pop_quality_filter({})[0] is est


def test_postprocess_dedupes_and_drops_source():
    out = BaseParaphraseGenerator._postprocess(SRC, [SRC, " A ", "A", "B", ""], 3)
    assert out == ["A", "B"]
    assert BaseParaphraseGenerator._postprocess(SRC, [SRC, SRC], 2) == [SRC]


def test_postprocess_filters_by_semantic_score():
    est = FakeEstimator({"A": 60, "B": 85, "C": 92})
    out = BaseParaphraseGenerator._postprocess(SRC, ["A", "B", "C"], 2, est, 80)
    assert out == ["B", "C"]


def test_postprocess_falls_back_to_best_when_none_pass():
    est = FakeEstimator({"A": 60, "B": 75})
    out = BaseParaphraseGenerator._postprocess(SRC, ["A", "B"], 2, est, 80)
    assert out == ["B"]


def test_postprocess_skips_filter_without_threshold_or_estimator():
    est = FakeEstimator({"A": 10, "B": 10})
    assert BaseParaphraseGenerator._postprocess(SRC, ["A", "B"], 2, est, None) == ["A", "B"]
    assert est.calls == 0
    assert BaseParaphraseGenerator._postprocess(SRC, ["A", "B"], 2, None, 80) == ["A", "B"]
