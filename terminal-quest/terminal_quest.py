from __future__ import annotations

import json
import os
import random
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional, Tuple


SAVE_FILE = "savegame.json"


@dataclass
class GameState:
    node: str = "start"
    hp: int = 10
    coins: int = 0
    inventory: List[str] = None
    runs: int = 1  # how many times you've played (fun for flavor)

    def __post_init__(self) -> None:
        if self.inventory is None:
            self.inventory = []


# A small, data-driven story graph
STORY: Dict[str, Dict] = {
    "start": {
        "text": "You wake up in a tiny tavern with a note: 'Don't trust the goose.' Outside, fog hugs the street.",
        "choices": [
            {"label": "Step outside into the fog", "to": "fog_street"},
            {"label": "Ask the bartender about the note", "to": "bartender"},
        ],
    },
    "bartender": {
        "text": "The bartender squints. 'Ah. The goose again. If you see it, offer it a coin. Or run.'",
        "gain": {"coins": 1},
        "choices": [
            {"label": "Pocket the coin and leave", "to": "fog_street"},
            {"label": "Check behind the bar", "to": "behind_bar"},
        ],
    },
    "behind_bar": {
        "text": "You find a rusty key and a suspicious jar labeled 'Confidence'.",
        "gain": {"items": ["rusty_key"]},
        "choices": [
            {"label": "Take the key and go outside", "to": "fog_street"},
            {"label": "Drink 'Confidence' (probably fine)", "to": "confidence_jar"},
        ],
    },
    "confidence_jar": {
        "text": "Your chest fills with courage. Also, regret. You gain 2 HP but lose 1 coin to the universe's tax.",
        "gain": {"hp": 2},
        "lose": {"coins": 1},
        "choices": [{"label": "Stride outside like you own the fog", "to": "fog_street"}],
    },
    "fog_street": {
        "text": "The fog parts to reveal two paths: a lantern-lit alley and a quiet market square.",
        "choices": [
            {"label": "Take the lantern alley", "to": "lantern_alley"},
            {"label": "Go to the market square", "to": "market"},
        ],
    },
    "lantern_alley": {
        "text": "A lockbox sits under a lantern. Something scratches inside. The box has a tiny keyhole.",
        "choices": [
            {
                "label": "Use rusty key on the lockbox",
                "to": "lockbox_open",
                "requires": ["rusty_key"],
            },
            {"label": "Ignore it (nope) and continue", "to": "bridge"},
        ],
    },
    "lockbox_open": {
        "text": "Inside is a small whistle and a very polite spider. The spider offers you 3 coins for letting it out.",
        "choices": [
            {"label": "Accept the coins and take the whistle", "to": "bridge", "gain": {"coins": 3, "items": ["whistle"]}},
            {"label": "Keep the spider (absolutely not)", "to": "bad_end_spider"},
        ],
    },
    "market": {
        "text": "The market is empty… except for a goose wearing a tiny hat. It stares at you like it knows your search history.",
        "choices": [
            {"label": "Offer the goose a coin", "to": "goose_deal", "requires_any": ["coins"]},
            {"label": "Run away immediately", "to": "bridge"},
            {"label": "Honk back (establish dominance)", "to": "goose_honk"},
        ],
    },
    "goose_deal": {
        "text": "The goose accepts the coin with a nod. It drops a shiny compass at your feet and waddles away.",
        "lose": {"coins": 1},
        "gain": {"items": ["compass"]},
        "choices": [{"label": "Follow the compass toward the bridge", "to": "bridge"}],
    },
    "goose_honk": {
        "text": "You honk. The goose honks louder. Reality honks. You lose 2 HP from pure psychic damage.",
        "lose": {"hp": 2},
        "choices": [{"label": "Retreat to the bridge with dignity (none left)", "to": "bridge"}],
    },
    "bridge": {
        "text": "You arrive at an old bridge. A toll sign reads: 'Pay 2 coins OR answer the riddle of vibes.'",
        "choices": [
            {"label": "Pay 2 coins", "to": "forest_gate", "requires": ["coins", "coins"]},
            {"label": "Answer the riddle of vibes", "to": "vibes_riddle"},
        ],
    },
    "vibes_riddle": {
        "text": "A hooded figure asks: 'What gets bigger the more you take away?'",
        "choices": [
            {"label": "A hole", "to": "forest_gate", "gain": {"coins": 1}},
            {"label": "My motivation on Mondays", "to": "bad_end_vibes"},
            {"label": "Time", "to": "bad_end_vibes"},
        ],
    },
    "forest_gate": {
        "text": "Beyond the bridge is a gate into a glowing forest. A plaque says: 'Only the prepared may enter.'",
        "choices": [
            {"label": "Enter the forest", "to": "finale"},
            {"label": "Check your pockets and rethink life", "to": "pockets"},
        ],
    },
    "pockets": {
        "text": "You check what you’ve got and do a quick mental inventory (like a responsible adult).",
        "choices": [{"label": "Back to the gate", "to": "forest_gate"}],
    },
    "finale": {
        "text": "The forest hums. The air tastes like peppermint and plot twists.",
        "choices": [
            {"label": "Use compass to find the heart of the forest", "to": "good_end", "requires": ["compass"]},
            {"label": "Blow the whistle to call for help", "to": "neutral_end", "requires": ["whistle"]},
            {"label": "Walk forward bravely (no tools, just vibes)", "to": "bad_end_fog"},
        ],
    },
    "good_end": {
        "text": "The compass leads you to a warm clearing. The goose is there, no hat now, just wisdom. You win. Probably.",
        "end": True,
    },
    "neutral_end": {
        "text": "The whistle echoes. A rescue cart arrives driven by the polite spider. It’s weird, but you’re safe. Ending: ‘Unexpected Allies’.",
        "end": True,
    },
    "bad_end_fog": {
        "text": "You walk forward and immediately trip into a perfectly placed fog-puddle. The forest politely rejects you. Ending: ‘Try Again, Hero’.",
        "end": True,
    },
    "bad_end_spider": {
        "text": "The spider becomes your manager and schedules daily standups at 6am. You lose forever. Ending: ‘Agile Doom’.",
        "end": True,
    },
    "bad_end_vibes": {
        "text": "The hooded figure sighs. 'Incorrect. Your vibe license is revoked.' You are escorted out by geese. Ending: ‘Vibe Check Failed’.",
        "end": True,
    },
}


def apply_delta(state: GameState, delta: Optional[Dict]) -> None:
    if not delta:
        return
    if "hp" in delta:
        state.hp += int(delta["hp"])
    if "coins" in delta:
        state.coins += int(delta["coins"])
        if state.coins < 0:
            state.coins = 0
    if "items" in delta:
        for item in delta["items"]:
            if item not in state.inventory:
                state.inventory.append(item)


def has_requirements(state: GameState, choice: Dict) -> bool:
    # requires: list of item names OR a special "coins" token repeated for how many needed
    req = choice.get("requires", [])
    if req:
        # handle coin requirements like ["coins","coins"] meaning 2 coins
        needed_coins = sum(1 for x in req if x == "coins")
        if needed_coins and state.coins < needed_coins:
            return False
        # handle item requirements
        for r in req:
            if r != "coins" and r not in state.inventory:
                return False

    # requires_any: allow if you have at least one token item/condition
    req_any = choice.get("requires_any", [])
    if req_any:
        for r in req_any:
            if r == "coins" and state.coins > 0:
                return True
            if r in state.inventory:
                return True
        return False

    return True


def spend_for_choice(state: GameState, choice: Dict) -> None:
    req = choice.get("requires", [])
    needed_coins = sum(1 for x in req if x == "coins")
    if needed_coins:
        state.coins = max(0, state.coins - needed_coins)


def random_event(state: GameState) -> Optional[str]:
    """
    Small random events that sometimes trigger after a move.
    Keep it light and silly.
    """
    roll = random.random()
    if roll < 0.18:
        state.coins += 1
        return "Random event: You find a coin on the ground. The universe winks."
    if roll < 0.30:
        state.hp = max(1, state.hp - 1)
        return "Random event: A dramatic gust of wind steals 1 HP. Yes, that’s a thing."
    if roll < 0.36 and "snack" not in state.inventory:
        state.inventory.append("snack")
        return "Random event: You acquire a Snack. It’s legally binding."
    return None


def save_game(state: GameState) -> None:
    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(asdict(state), f, indent=2)


def load_game() -> GameState:
    with open(SAVE_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    return GameState(**data)


def render_hud(state: GameState) -> None:
    inv = ", ".join(state.inventory) if state.inventory else "empty"
    print(f"\nHP: {state.hp} | Coins: {state.coins} | Inventory: {inv}\n")


def get_available_choices(state: GameState, node: Dict) -> List[Dict]:
    return [c for c in node.get("choices", []) if has_requirements(state, c)]


def main() -> None:
    random.seed()  # fresh run
    state = GameState()

    print("=== TERMINAL QUEST ===")
    print("Type a number to choose. Type 'save', 'load', or 'quit'.\n")

    while True:
        if state.hp <= 0:
            print("You have 0 HP. The fog consumes you. Ending: ‘Nap Time Forever’.")
            break

        node = STORY[state.node]
        render_hud(state)

        # apply node effects on entry (once per visit is more complex; keep it simple)
        apply_delta(state, node.get("gain"))
        apply_delta(state, {k: -v for k, v in (node.get("lose") or {}).items()})

        print(node["text"])

        if node.get("end"):
            print("\n=== THE END ===")
            if state.runs == 1:
                print("Tip: Run it again. Random events + different choices change the vibe.")
            break

        choices = get_available_choices(state, node)
        if not choices:
            print("\nNo valid choices left. The story collapses politely.")
            break

        print("\nChoices:")
        for i, c in enumerate(choices, start=1):
            print(f"  {i}. {c['label']}")

        user_in = input("\nYour move: ").strip().lower()

        if user_in == "quit":
            print("You step out of the story and close the book. Fair.")
            break
        if user_in == "save":
            save_game(state)
            print(f"Saved to {SAVE_FILE}.")
            continue
        if user_in == "load":
            if os.path.exists(SAVE_FILE):
                state = load_game()
                print(f"Loaded from {SAVE_FILE}.")
            else:
                print("No save file found yet.")
            continue

        # parse numeric choice
        try:
            idx = int(user_in) - 1
            if idx < 0 or idx >= len(choices):
                raise ValueError
        except ValueError:
            print("Please type a valid choice number (or 'save'/'load'/'quit').")
            continue

        chosen = choices[idx]

        # Spend any coin requirements (like paying toll)
        spend_for_choice(state, chosen)

        # Apply choice gains (optional)
        apply_delta(state, chosen.get("gain"))

        # Move to next node
        state.node = chosen["to"]

        # Random event after moving (sometimes)
        event_text = random_event(state)
        if event_text:
            print(f"\n{event_text}")

    print("\nThanks for playing!")


if __name__ == "__main__":
    main()
