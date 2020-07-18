from enum import Enum
from typing import List


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
    # TODO: other rules
    wb999(fenceposts)

    # Output boundaries
    for index, op in enumerate(fenceposts):
        if op == Op.BOUNDARY:
            yield index
