"""Tests for Egyptian phone number recognizer."""

import pytest
from presidio_analyzer.predefined_recognizers import PhoneRecognizer

from tests import assert_result_within_score_range


@pytest.fixture(scope="module")
def recognizer():
    return PhoneRecognizer(
        supported_regions=["EG"],
        supported_entity="EG_PHONE_NUMBER",
        supported_language="en",
        context=[
            "mobile",
            "phone",
            "telephone",
            "number",
            "contact",
            "موبايل",
            "رقم الموبايل",
            "تليفون",
            "هاتف",
        ],
    )


@pytest.fixture(scope="module")
def entities():
    return ["EG_PHONE_NUMBER"]


@pytest.mark.parametrize(
    "text, expected_len, expected_positions",
    [
        ("+201001234567", 1, ((0, 13),)),
        ("01001234567", 1, ((0, 11),)),
        ("My phone number is +201001234567", 1, ((19, 32),)),
        ("Call me at 01001234567", 1, ((11, 22),)),
        ("Hello world", 0, ()),
    ],
)
def test_egyptian_phone_numbers(
    text, expected_len, expected_positions, recognizer, entities
):
    results = recognizer.analyze(text, entities)

    assert len(results) == expected_len

    for result, (start, end) in zip(results, expected_positions):
        assert_result_within_score_range(
            result, entities[0], start, end, 0.4, 1.0
        )


def test_supported_entity(recognizer):
    assert recognizer.supported_entities == ["EG_PHONE_NUMBER"]


def test_supported_regions(recognizer):
    assert recognizer.supported_regions == ["EG"]
