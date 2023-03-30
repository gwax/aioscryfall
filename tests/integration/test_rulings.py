from typing import TYPE_CHECKING
from uuid import UUID

from aioscryfall import rulings

if TYPE_CHECKING:
    from aiohttp import ClientSession


async def test_card(client_session: "ClientSession") -> None:
    result = await rulings.card(client_session, UUID("70496f16-c4c0-4c03-beef-454eb4824cd1"))
    assert [ruling.comment for ruling in result.data] == [
        "Because the first ability requires a target, it "
        + "is not a mana ability. It uses the stack and can "
        + "be responded to.",
        "If the target of any of Deathrite Shaman’s three "
        + "abilities is an illegal target when that ability "
        + "tries to resolve, it won’t resolve and none of its "
        + "effects will happen. You won’t add mana to your mana "
        + "pool, no opponent will lose life, or you won’t gain "
        + "life, as appropriate.",
    ]


async def test_multiverse_id(client_session: "ClientSession") -> None:
    result = await rulings.multiverse_id(client_session, 290529)
    assert [ruling.comment for ruling in result.data] == [
        "Because the first ability requires a target, it "
        + "is not a mana ability. It uses the stack and can "
        + "be responded to.",
        "If the target of any of Deathrite Shaman’s three "
        + "abilities is an illegal target when that ability "
        + "tries to resolve, it won’t resolve and none of its "
        + "effects will happen. You won’t add mana to your mana "
        + "pool, no opponent will lose life, or you won’t gain "
        + "life, as appropriate.",
    ]


async def test_mtgo_id(client_session: "ClientSession") -> None:
    result = await rulings.mtgo_id(client_session, 46777)
    assert [ruling.comment for ruling in result.data] == [
        "Because the first ability requires a target, it "
        + "is not a mana ability. It uses the stack and can "
        + "be responded to.",
        "If the target of any of Deathrite Shaman’s three "
        + "abilities is an illegal target when that ability "
        + "tries to resolve, it won’t resolve and none of its "
        + "effects will happen. You won’t add mana to your mana "
        + "pool, no opponent will lose life, or you won’t gain "
        + "life, as appropriate.",
    ]


async def test_arena_id(client_session: "ClientSession") -> None:
    result = await rulings.arena_id(client_session, 82504)
    assert [ruling.comment for ruling in result.data] == [
        "Powerstone tokens are a kind of predefined token. "
        + "Each one has the artifact subtype “Powerstone” and "
        + "the ability “{T}: Add {C}. This mana can’t be spent "
        + "to cast a nonartifact spell.”",
        "You can use the {C} added by a Powerstone token on "
        + "anything that isn’t a nonartifact spell. This includes "
        + "paying costs to activate abilities of both artifact and "
        + "nonartifact permanents, paying ward costs, and so on.",
        "Although all the cards in The Brothers’ War that create "
        + "Powerstone tokens create a tapped Powerstone token, "
        + "entering the battlefield tapped isn’t part of the token’s "
        + "definition. Notably, if you create a token that is a copy "
        + "of a Powerstone token, the token copy won’t enter the "
        + "battlefield tapped.",
    ]


async def test_set_code_and_number(client_session: "ClientSession") -> None:
    result = await rulings.set_code_and_number(client_session, "rtr", "213")
    assert [ruling.comment for ruling in result.data] == [
        "Because the first ability requires a target, it "
        + "is not a mana ability. It uses the stack and can "
        + "be responded to.",
        "If the target of any of Deathrite Shaman’s three "
        + "abilities is an illegal target when that ability "
        + "tries to resolve, it won’t resolve and none of its "
        + "effects will happen. You won’t add mana to your mana "
        + "pool, no opponent will lose life, or you won’t gain "
        + "life, as appropriate.",
    ]
