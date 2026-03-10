# color util for colored logging
# this file works like colorama but with more colors and gradient support

# Usage Examples:

# log(Color.RED, "Error:", "Something went wrong")

# gradient_log((255, 0, 0), (0, 0, 255), "Horizontal gradient")

# gradient_log(
#     (0, 255, 0),
#     (0, 0, 255),
#     "Line 1\nLine 2\nLine 3",
#     vert=True
# )

import sys
import os
import math
import random
import time
import re

# ============================
# ANSI COLOR HELPERS
# ============================

RESET = "\033[0m"

def rgb_to_ansi(r: int, g: int, b: int) -> str:
    """Convert RGB values to ANSI 24-bit foreground color."""
    return f"\033[38;2;{r};{g};{b}m"

def rgb_bg_to_ansi(r: int, g: int, b: int) -> str:
    """Convert RGB values to ANSI 24-bit background color."""
    return f"\033[48;2;{r};{g};{b}m"


# ============================
# COLOR CLASS
# ============================

class Color:
    BLACK   = rgb_to_ansi(0, 0, 0)
    RED     = rgb_to_ansi(255, 0, 0)
    GREEN   = rgb_to_ansi(0, 255, 0)
    BLUE    = rgb_to_ansi(0, 0, 255)
    CYAN    = rgb_to_ansi(0, 255, 255)
    MAGENTA = rgb_to_ansi(255, 0, 255)
    YELLOW  = rgb_to_ansi(255, 255, 0)
    WHITE   = rgb_to_ansi(255, 255, 255)

    @staticmethod
    def rgb(r, g, b):
        return rgb_to_ansi(r, g, b)

    @staticmethod
    def random():
        return rgb_to_ansi(
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255)
        )


# ============================
# GRADIENT MATH
# ============================

def lerp(a: float, b: float, t: float) -> float:
    """Linear interpolation."""
    return a + (b - a) * t

def lerp_color(c1, c2, t):
    """Interpolate between two RGB tuples."""
    return (
        int(lerp(c1[0], c2[0], t)),
        int(lerp(c1[1], c2[1], t)),
        int(lerp(c1[2], c2[2], t)),
    )


# ============================
# GRADIENT TEXT (HORIZONTAL + VERTICAL)
# ============================

def gradient_text(
    text: str,
    start_color: tuple,
    end_color: tuple,
    hor: bool = True,
    vert: bool = False
) -> str:
    """
    Apply a gradient to text.

    hor=True  → horizontal gradient (left→right)
    vert=True → vertical gradient (top→bottom)

    If both are True, vertical takes priority.
    """

    # Split into lines for vertical gradients
    lines = text.split("\n")

    # Vertical gradient mode
    if vert:
        total = max(len(lines) - 1, 1)
        out_lines = []

        for i, line in enumerate(lines):
            t = i / total
            r, g, b = lerp_color(start_color, end_color, t)
            color = rgb_to_ansi(r, g, b)
            out_lines.append(color + line + RESET)

        return "\n".join(out_lines)

    # Horizontal gradient mode (default)
    if hor:
        out = []
        length = max(len(text) - 1, 1)

        for i, ch in enumerate(text):
            t = i / length
            r, g, b = lerp_color(start_color, end_color, t)
            out.append(f"{rgb_to_ansi(r, g, b)}{ch}")

        return "".join(out) + RESET

    # If neither hor nor vert, return plain text
    return text


# ============================
# LOGGING HELPERS
# ============================

def log(color, *msg):
    """Print a colored log message."""
    print(color + " ".join(str(m) for m in msg) + RESET)

def gradient_log(start, end, *msg, hor=True, vert=False):
    """Print a gradient-colored log message with horizontal or vertical mode."""
    text = " ".join(str(m) for m in msg)
    print(gradient_text(text, start, end, hor=hor, vert=vert))