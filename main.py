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

# ============================
#  Bot Setup Functions
# ============================
def get_prefix(bot, message):
    prefix = os.environ.get("PREFIX")
    if prefix is None:
        prefix = "!"
    return prefix