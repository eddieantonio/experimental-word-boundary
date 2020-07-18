from enum import Enum


class Op(Enum):
    UNASSIGNED = "?"
    BOUNDARY = "÷"
    NO_BOUNDARY = "×"


def word_boundaries(text: str):
    if not text:
        return

    fenceposts = [Op.UNASSIGNED] * (len(text) + 1)
    assert len(fenceposts) >= 2

    # WB1
    fenceposts[0] = Op.BOUNDARY

    # WB2
    fenceposts[-1] = Op.BOUNDARY

    for index, op in enumerate(fenceposts):
        if op == Op.BOUNDARY:
            yield index
