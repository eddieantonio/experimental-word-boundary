#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from hypothesis import given, assume
from hypothesis.strategies import text, sampled_from, characters

from word_boundary import word_boundaries
from custom_strategies import ideographs, non_empty_text


def test_empty():
    """
    The empty string does not contain word boundaries.
    """
    assert len(list(word_boundaries(""))) == 0


@given(non_empty_text())
def test_sot_eot(example: str) -> None:
    boundaries = list(word_boundaries(example))
    assert len(boundaries) >= 2
    assert boundaries[0] == 0
    assert boundaries[-1] == len(example)


def test_crlf() -> None:
    # TODO: come up with a more robust test case
    boundaries = list(word_boundaries("\r\n"))
    assert boundaries == [0, len("\r\n")]


@given(
    sampled_from(
        "\r"
        "\n"
        "\N{LINE TABULATION}"
        "\N{FORM FEED}"
        "\N{NEXT LINE}"
        "\N{LINE SEPARATOR}"
        "\N{PARAGRAPH SEPARATOR}"
    ),
    non_empty_text(),
    non_empty_text(),
)
def test_newline(newline: str, left: str, right: str) -> None:
    assume("\r\n" != left[-1] + newline)
    assume("\r\n" != newline + right[:1])

    left_boundaries = len(list(word_boundaries(left)))
    right_boundaries = len(list(word_boundaries(right)))
    example = left + newline + right
    assert len(list(word_boundaries(example))) == left_boundaries + right_boundaries


@given(
    text(
        alphabet=characters(
            whitelist_categories=("Zs",),
            blacklist_characters="\u00a0\u2007\u2011\u202f",
        ),
        min_size=1,
    )
)
def test_keep_whitespace_together(example):
    boundaries = list(word_boundaries(example))
    assert boundaries == [0, len(example)]


@given(ideographs())
def test_break_everywhere(ideographs: str) -> None:
    # There should be as many boundaries as possible
    assert len(list(word_boundaries(ideographs))) == len(ideographs) + 1
