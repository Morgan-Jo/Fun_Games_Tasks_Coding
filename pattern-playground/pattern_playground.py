from __future__ import annotations

import argparse
import sys
from typing import Callable, Dict

PatternFn = Callable[[int, str, str], str]


def pyramid(size: int, char: str, alt: str = " ") -> str:
    """Centered pyramid. size = height."""
    lines = []
    for row in range(size):
        spaces = " " * (size - row - 1)
        blocks = char * (2 * row + 1)
        lines.append(spaces + blocks)
    return "\n".join(lines)


def diamond(size: int, char: str, alt: str = " ") -> str:
    """Centered diamond. size must be odd."""
    mid = size // 2
    lines = []
    for i in range(size):
        dist = abs(mid - i)
        spaces = " " * dist
        blocks = char * (size - 2 * dist)
        lines.append(spaces + blocks)
    return "\n".join(lines)


def checkerboard(size: int, char: str, alt: str = ".") -> str:
    """Square checkerboard using char + alt."""
    lines = []
    for r in range(size):
        row = []
        for c in range(size):
            row.append(char if (r + c) % 2 == 0 else alt)
        lines.append("".join(row))
    return "\n".join(lines)


def hollow_box(size: int, char: str, alt: str = " ") -> str:
    """Square hollow box. Border uses char, inside uses alt (default space)."""
    if size == 1:
        return char

    top_bottom = char * size
    middle = char + (alt * (size - 2)) + char
    lines = [top_bottom] + [middle] * (size - 2) + [top_bottom]
    return "\n".join(lines)


PATTERNS: Dict[str, PatternFn] = {
    "pyramid": pyramid,
    "diamond": diamond,
    "checkerboard": checkerboard,
    "hollow_box": hollow_box,
}


def validate_args(pattern: str, size: int) -> None:
    if pattern not in PATTERNS:
        raise ValueError(f"Unknown pattern '{pattern}'. Choose from: {', '.join(PATTERNS)}")

    if size < 1 or size > 200:
        raise ValueError("size must be between 1 and 200.")

    if pattern == "diamond":
        if size < 3 or size % 2 == 0:
            raise ValueError("diamond size must be an odd number >= 3.")
    if pattern in {"pyramid"} and size < 2:
        raise ValueError("pyramid size should be >= 2 for a meaningful output.")
    if pattern in {"hollow_box"} and size < 2:
        raise ValueError("hollow_box size must be >= 2.")


def prompt_if_missing(value: str | None, prompt: str, default: str) -> str:
    if value is not None:
        return value
    entered = input(f"{prompt} [{default}]: ").strip()
    return entered if entered else default


def parse_cli() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate fun ASCII patterns (pyramid, diamond, checkerboard, hollow_box)."
    )
    parser.add_argument("--pattern", choices=sorted(PATTERNS.keys()), help="Pattern name")
    parser.add_argument("--size", type=int, help="Size of the pattern (meaning depends on pattern)")
    parser.add_argument("--char", type=str, help="Primary character (default: '*')")
    parser.add_argument("--alt", type=str, help="Secondary character (default: '.') for checkerboard or inner fill")
    return parser.parse_args()


def normalize_char(s: str, fallback: str) -> str:
    s = (s or "").strip()
    if not s:
        return fallback
    # Use the first visible character if a longer string is given
    return s[0]


def main() -> int:
    args = parse_cli()

    # If any key fields are missing, fall back to interactive mode.
    interactive = args.pattern is None or args.size is None

    if interactive:
        print("Pattern Playground (interactive mode)")
        print("Available patterns:", ", ".join(sorted(PATTERNS.keys())))
        pattern = prompt_if_missing(None, "Choose a pattern", "pyramid")
        size_str = prompt_if_missing(None, "Choose a size", "7")
        char = prompt_if_missing(None, "Choose a character", "*")
        alt = prompt_if_missing(None, "Choose an alternate character", ".")
        try:
            size = int(size_str)
        except ValueError:
            print("Size must be an integer.", file=sys.stderr)
            return 2
    else:
        pattern = args.pattern
        size = args.size
        char = args.char if args.char is not None else "*"
        alt = args.alt if args.alt is not None else "."

    pattern = pattern.strip().lower()
    char = normalize_char(char, "*")
    alt = normalize_char(alt, ".")

    try:
        validate_args(pattern, size)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 2

    output = PATTERNS[pattern](size, char, alt)
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())