#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from hypothesis import given
from hypothesis.strategies import text

from word_boundary import word_boundaries


def test_empty():
    """
    The empty string does not contain word boundaries.
    """
    assert len(list(word_boundaries(""))) == 0


@given(text(min_size=1))
def test_sot_eot(example: str) -> None:
    boundaries = list(word_boundaries(example))
    assert len(boundaries) >= 2
    assert boundaries[0] == 0
    assert boundaries[-1] == len(example)
