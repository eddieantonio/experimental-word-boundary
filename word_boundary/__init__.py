import inspect
from enum import Enum
from typing import List, Optional, Callable

from .data import Property, LOOKUP


class Op(Enum):
    UNASSIGNED = "?"
    BOUNDARY = "÷"
    NO_BOUNDARY = "×"
    IGNORE = "→"


def wb1(left: Property, right: Property) -> Op:
    "Break at the start of text"
    if left == Property.SOT:
        return Op.BOUNDARY
    return Op.UNASSIGNED


def wb2(left: Property, right: Property) -> Op:
    "Break at the end of text"
    if right == Property.SOT:
        return Op.BOUNDARY
    return Op.UNASSIGNED


def wb3(left: Property, right: Property) -> Op:
    if left == Property.CR and right == Property.LF:
        return Op.NO_BOUNDARY
    return Op.UNASSIGNED


def wb3a(left: Property, right: Property) -> Op:
    "break after newlines"
    if left in (Property.NEWLINE, Property.CR, Property.LF):
        return Op.BOUNDARY
    return Op.UNASSIGNED


def wb3b(left: Property, right: Property) -> Op:
    "break before newlines"
    if right in (Property.NEWLINE, Property.CR, Property.LF):
        return Op.BOUNDARY
    return Op.UNASSIGNED


def wb3d(left: Property, right: Property) -> Op:
    "Keep horizontal whitespace together"
    if left == Property.WSEGSPACE and right == Property.WSEGSPACE:
        return Op.NO_BOUNDARY
    return Op.UNASSIGNED


def wb999(left: Property, right: Property) -> Optional[Op]:
    "Otherwise, break at every character (include ideographs)"
    return Op.BOUNDARY


def word_boundaries(text: str):
    if not text:
        return

    fenceposts = [Op.UNASSIGNED] * (len(text) + 1)
    properties = (
        [Property.SOT] + [word_break_property(c) for c in text] + [Property.EOT]
    )

    assert len(text) + 1 == len(fenceposts)
    assert len(fenceposts) + 1 == len(properties)

    def apply_rule(rule: Callable) -> Op:
        sig = inspect.signature(rule)
        params = sig.parameters
        if not len(params) == 2:
            raise NotImplementedError
        if params["left"].annotation != Property:
            raise NotImplementedError
        if params["right"].annotation != Property:
            raise NotImplementedError
        left = properties[i]
        right = properties[i + 1]
        return rule(left, right)

    rules = [
        wb1,
        wb2,
        wb3,
        wb3a,
        wb3b,
        # TODO: wb3c
        wb3d,
        # TODO: other rules
        wb999,
    ]

    # Apply rules in order:
    for i in range(len(fenceposts)):
        rule = iter(rules)
        while fenceposts[i] == Op.UNASSIGNED:
            fenceposts[i] = apply_rule(next(rule))

    # Output boundaries
    for index, op in enumerate(fenceposts):
        if op == Op.BOUNDARY:
            yield index


def word_break_property(ch: str, table=LOOKUP) -> Property:
    assert len(ch) == 1

    codepoint = ord(ch)

    def bisect(start: int, end: int) -> Property:
        if start > end:
            return Property.OTHER

        midpoint = start + (end - start) // 2
        r = table[midpoint]

        if codepoint < r.start:
            return bisect(start, midpoint - 1)
        elif codepoint > r.end:
            return bisect(midpoint + 1, end)
        else:
            assert r.start <= codepoint <= r.end
            return r.property

    return bisect(0, len(table) - 1)
