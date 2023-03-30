"""Models for common Scryfall datatypes and enums."""

from enum import Enum


class ScryColor(str, Enum):
    """Enum for https://scryfall.com/docs/api/colors#color-arrays ."""

    WHITE = "W"
    BLUE = "U"
    BLACK = "B"
    RED = "R"
    GREEN = "G"
    COLORLESS = "C"
    TAP = "T"


class ScryGame(str, Enum):
    """ScryGame represents a mode for playing Magic: The Gathering."""

    PAPER = "paper"
    ARENA = "arena"
    MTGO = "mtgo"
    SEGA = "sega"
    ASTRAL = "astral"
