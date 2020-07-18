#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
Custom hypothesis strategies.
"""

from hypothesis.strategies import text, characters


def ideographs():
    START_OF_CJK_BLOCK = 0x4E00
    END_OF_CJK_BLOCK = 0x9FFF
    return text(
        min_size=1,
        alphabet=characters(
            whitelist_categories=("Lo",),
            min_codepoint=START_OF_CJK_BLOCK,
            max_codepoint=END_OF_CJK_BLOCK,
        ),
    )


def non_empty_text():
    return text(min_size=1)
