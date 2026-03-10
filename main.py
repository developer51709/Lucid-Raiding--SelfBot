"""
𝙻𝚞𝚌𝚒𝚍 𝚁𝚊𝚒𝚍𝚒𝚗𝚐™ 𝚂𝚎𝚕𝚏𝙱𝚘𝚝 𝚟𝟷.𝟶
───────────────────────────
𝙳𝚎𝚟𝚎𝚕𝚘𝚙𝚎𝚛𝚜:
- 𝙽𝚢𝚡𝚎𝚗
- 𝙲𝚞𝚛𝚜𝚎𝚏𝚒𝚕𝚎
───────────────────────────
𝙻𝚒𝚗𝚔𝚜:
- 𝙶𝚒𝚝𝙷𝚞𝚋:

- 𝙳𝚒𝚜𝚌𝚘𝚛𝚍:

───────────────────────────
"""

import utils.color
import discord
from discord.ext import commands
import os
import asyncio
import time
import random
import json
import sys
import traceback
from utils.color import Color, gradient_text, gradient_log

# ============================
#  Bot Setup Functions
# ============================
def get_prefix(bot, message):
    prefix = os.environ.get("PREFIX")
    if prefix is None:
        prefix = "!"
    return prefix

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_disclaimer():
    gradient_log(
        (255, 0, 0), 
        (0, 0, 255), 
        """
╭──────────────────────────────╮
│ Disclaimer:                  │
│  SelfBots are against the    │
│  Discord ToS and can get     │
│  your account termed and/or  │
│  suspended.                  │
│                              │
│  The developers of this bot  │
│  are not responsible for     │
│  any damage caused by this   │
│  bot.                        │
╰──────────────────────────────╯
        """
    )
    # Wait for user input
    input("Press Enter to continue...")
    clear_console()

# ============================
#  Bot Setup
# ============================







print_disclaimer()