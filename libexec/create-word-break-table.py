#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
Creates the enum and data table WordBoundaryProperty file.
"""

from pathlib import Path
import re

here = Path(__file__).parent
prop_filename = here / "WordBreakProperty.txt"
gen_filename = here.parent / "word_boundary" / "data.py"

INDENT = " " * 4
NEWLINE = "\n"

line_pattern = re.compile(
    r"""
        ^
        (?P<start>[0-9A-F]{4,6})
        (?:..
            (?P<end>[0-9A-F]{4,6}))?
        \s* ; \s*
        (?P<property>[A-Za-z_]+)
        \s* [#]
        """,
    re.VERBOSE,
)

contents = prop_filename.read_text(encoding="UTF-8")

ranges = []
for line in contents.splitlines():
    if not (line := line.strip()):
        # Skip empty lines
        continue

    if line.startswith("#"):
        # Skip comment lines
        continue

    if not (match := line_pattern.match(line)):
        raise NotImplementedError(f"Could not parse {line}")

    start = int(match.group("start"), base=16)
    prop = match.group("property")

    end = int(end_str, base=16) if (end_str := match.group("end")) else start

    ranges.append((start, end, prop))

ranges.sort()


def generate_properties():
    props = {"Other"}
    for _, _, prop in ranges:
        props.add(prop)

    for prop in props:
        yield f'{INDENT}{prop.upper()} = "{prop}"'


def generate_lookup():
    for start, end, prop in ranges:
        yield f"{INDENT}Range(0x{start:04X}, 0x{end:04X}, Property.{prop.upper()}),"


gen_filename.write_text(
    f"""
# Autogenerated file. DO NOT MODIFY
from enum import Enum
from typing import NamedTuple


class Property(Enum):
{NEWLINE.join(generate_properties())}


class Range(NamedTuple):
    start: int
    end: int
    property: Property


LOOKUP = [
{NEWLINE.join(generate_lookup())}
]
""".lstrip(),
    encoding="UTF-8",
)
