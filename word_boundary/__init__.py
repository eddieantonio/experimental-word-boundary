from enum import Enum
from typing import List, Optional

from .data import Property, LOOKUP


class Op(Enum):
    UNASSIGNED = "?"
    BOUNDARY = "÷"
    NO_BOUNDARY = "×"


def wb1(fenceposts: List[Op]) -> None:
    "Break at the start of text"
    fenceposts[0] = Op.BOUNDARY


def wb2(fenceposts: List[Op]) -> None:
    "Break at the end of text"
    fenceposts[-1] = Op.BOUNDARY


def wb3(left: Property, right: Property) -> Optional[Op]:
    if left == Property.CR and right == Property.LF:
        return Op.NO_BOUNDARY
    return None


def wb3a(left: Property, right: Property) -> Optional[Op]:
    "break after newlines"
    if left in (Property.NEWLINE, Property.CR, Property.LF):
        return Op.BOUNDARY
    return None


def wb3b(left: Property, right: Property) -> Optional[Op]:
    "break before newlines"
    if right in (Property.NEWLINE, Property.CR, Property.LF):
        return Op.BOUNDARY
    return None


def wb3d(left: Property, right: Property) -> Optional[Op]:
    "Keep horizontal whitespace together"
    if left == Property.WSEGSPACE and right == Property.WSEGSPACE:
        return Op.NO_BOUNDARY
    return None


def wb999(fenceposts: List[Op]) -> None:
    "Otherwise, break everywhere"
    for i, op in enumerate(fenceposts):
        if op == Op.UNASSIGNED:
            fenceposts[i] = Op.BOUNDARY


def word_boundaries(text: str):
    if not text:
        return

    fenceposts = [Op.UNASSIGNED] * (len(text) + 1)
    assert len(fenceposts) >= 2

    wb1(fenceposts)
    wb2(fenceposts)

    def apply_two_prop_rules():
        for rule in [wb3, wb3a, wb3b, wb3d]:
            # TODO: wb3c
            if decision := rule(a, b):
                fenceposts[i] = decision
                return

    # The following rules require a left and a right
    properties = [word_break_property(c) for c in text]
    for i, (a, b) in enumerate(zip(properties, properties[1:]), start=1):
        apply_two_prop_rules()

    wb999(fenceposts)

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
