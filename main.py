"""
𝙻𝚞𝚌𝚒𝚍 𝚁𝚊𝚒𝚍𝚒𝚗𝚐™ 𝚂𝚎𝚕𝚏𝙱𝚘𝚝 𝚟𝟷.𝟶
───────────────────────────
𝙳𝚎𝚟𝚎𝚕𝚘𝚙𝚎𝚛𝚜:
- 𝙽𝚢𝚡𝚎𝚗
- 𝙲𝚞𝚛𝚜𝚎𝚏𝚒𝚕𝚎
───────────────────────────
𝙻𝚒𝚗𝚔𝚜:
- 𝙶𝚒𝚝𝙷𝚞𝚋:
https://github.com/developer51709/Lucid-Raiding--SelfBot
- 𝙳𝚒𝚜𝚌𝚘𝚛𝚍:
https://discord.gg/k7DWBCsRHC
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
import importlib
from pathlib import Path
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

def print_banner():
    gradient_log(
        (255, 0, 0),
        (0, 0, 255),
        """
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
░▓▓░░░░░▓▓░░░▓▓░░▓▓▓▓▓░░▓▓▓▓▓▓░▓▓▓▓▓▓░░
░▓▓░░░░░▓▓░░░▓▓░▓▓░░░▓▓░░░▓▓░░░▓▓░░░▓▓░
░▓▓░░░░░▓▓░░░▓▓░▓▓░░░░░░░░▓▓░░░▓▓░░░▓▓░
░▓▓░░░░░▓▓░░░▓▓░▓▓░░░▓▓░░░▓▓░░░▓▓░░░▓▓░
░▓▓▓▓▓▓░░▓▓▓▓▓░░░▓▓▓▓▓░░▓▓▓▓▓▓░▓▓▓▓▓▓░░
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
Lucid Raiding™ SelfBot v1.0
───────────────────────────
Developers:
- Nyxen
- Cursefile
        """
    )

# ============================
#  Cog Loader
# ============================

async def load_cogs(bot):
    """Load all cogs from the cogs directory."""
    cogs_dir = Path(__file__).parent / "cogs"
    
    if not cogs_dir.exists():
        gradient_log((255, 255, 0), (255, 0, 0), "[WARNING] Cogs directory not found")
        return
    
    cog_count = 0
    error_count = 0
    
    for cog_file in cogs_dir.glob("*.py"):
        if cog_file.name.startswith("_"):
            continue
        
        cog_name = cog_file.stem
        try:
            await bot.load_extension(f"cogs.{cog_name}")
            gradient_log((0, 255, 0), (0, 255, 0), f"[LOADED] {cog_name}")
            cog_count += 1
        except Exception as e:
            gradient_log((255, 0, 0), (255, 0, 0), f"[ERROR] Failed to load {cog_name}: {e}")
            error_count += 1
    
    gradient_log((0, 255, 255), (0, 255, 255), f"[INFO] Loaded {cog_count} cog(s), {error_count} error(s)")

# ============================
#  Bot Setup
# ============================

def create_bot():
    """Create and configure the bot instance."""
    intents = discord.Intents.default()
    intents.message_content = True
    
    bot = commands.Bot(
        command_prefix=get_prefix,
        intents=intents,
        self_bot=True
    )
    
    @bot.event
    async def on_ready():
        gradient_log(
            (0, 255, 0),
            (0, 255, 255),
            f"[CONNECTED] Logged in as {bot.user}"
        )
        gradient_log(
            (100, 200, 255),
            (100, 200, 255),
            f"[STATUS] Prefix: {get_prefix(bot, None)}"
        )
    
    @bot.event
    async def on_command_error(ctx, error):
        gradient_log(
            (255, 0, 0),
            (255, 0, 0),
            f"[ERROR] Command error in {ctx.command}: {error}"
        )
    
    return bot

async def main():
    """Main entry point for the bot."""
    print_disclaimer()
    print_banner()
    
    token = os.environ.get("DISCORD_TOKEN")
    if not token:
        gradient_log(
            (255, 0, 0),
            (255, 0, 0),
            "[ERROR] DISCORD_TOKEN environment variable not set. Please add your Discord token."
        )
        sys.exit(1)
    
    bot = create_bot()
    
    async with bot:
        await load_cogs(bot)
        try:
            await bot.start(token)
        except KeyboardInterrupt:
            gradient_log((255, 255, 0), (255, 0, 0), "[SHUTDOWN] Bot interrupted")
            await bot.close()
        except Exception as e:
            gradient_log((255, 0, 0), (255, 0, 0), f"[FATAL] {e}")
            sys.exit(1)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        gradient_log((255, 255, 0), (255, 0, 0), "[SHUTDOWN] Bot interrupted")
        sys.exit(0)
