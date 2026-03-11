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
from datetime import datetime
from utils.color import Color, gradient_text, gradient_log
from config import config

# ============================
#  Bot Setup Functions
# ============================
def get_prefix(bot, message):
    """Get command prefix from config."""
    return config.prefix

def clear_console():
    """Clear the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_disclaimer():
    """Display startup disclaimer."""
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
    input("Press Enter to continue...")
    clear_console()

def print_banner():
    """Display bot banner."""
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
        return 0, 0
    
    cog_count = 0
    error_count = 0
    
    gradient_log((100, 200, 255), (100, 200, 255), "[STARTUP] Loading cogs...")
    
    for cog_file in cogs_dir.glob("*.py"):
        if cog_file.name.startswith("_"):
            continue
        
        cog_name = cog_file.stem
        try:
            await bot.load_extension(f"cogs.{cog_name}")
            gradient_log((0, 255, 100), (0, 255, 100), f"  ✓ {cog_name}")
            cog_count += 1
        except Exception as e:
            gradient_log((255, 100, 0), (255, 100, 0), f"  ✗ {cog_name}: {e}")
            error_count += 1
    
    if cog_count > 0 or error_count > 0:
        gradient_log(
            (0, 255, 200),
            (0, 255, 200),
            f"[STARTUP] Loaded {cog_count} cog(s), {error_count} error(s)"
        )
    
    return cog_count, error_count

# ============================
#  Bot Initialization
# ============================

def create_bot():
    """Create and configure the bot instance."""
    # intents = discord.Intents.default()
    # intents.message_content = True
    
    bot = commands.Bot(
        command_prefix=get_prefix,
        # intents=intents,
        self_bot=True,
        help_command=None  # Disable default help
    )
    
    # Track startup state
    bot.startup_time = None
    bot.ready = False
    
    @bot.event
    async def on_ready():
        """Handle bot ready event - only runs once."""
        if bot.ready:
            return
        
        bot.ready = True
        bot.startup_time = datetime.now()
        
        gradient_log(
            (0, 255, 0),
            (0, 255, 255),
            f"[READY] Logged in as {bot.user} ({bot.user.id})"
        )
        
        # Set bot status/activity
        await set_bot_status(bot)
        
        # Print startup info
        await print_startup_info(bot)
    
    @bot.event
    async def on_command(ctx):
        """Log command execution."""
        gradient_log(
            (100, 200, 255),
            (100, 200, 255),
            f"[COMMAND] {ctx.author} → {ctx.command.name}"
        )
    
    @bot.event
    async def on_command_error(ctx, error):
        """Handle command errors."""
        error_msg = str(error)
        gradient_log(
            (255, 100, 0),
            (255, 0, 0),
            f"[ERROR] Command '{ctx.command}' failed: {error_msg}"
        )
        
        try:
            await ctx.send(f"Error: {error_msg}")
        except:
            pass
    
    return bot

async def set_bot_status(bot):
    """Set bot status and activity."""
    activity_type = config.activity_type.lower()
    
    activity_map = {
        "playing": discord.ActivityType.playing,
        "listening": discord.ActivityType.listening,
        "watching": discord.ActivityType.watching,
        "competing": discord.ActivityType.competing,
    }
    
    activity_enum = activity_map.get(activity_type, discord.ActivityType.playing)
    activity = discord.Activity(type=activity_enum, name=config.status)
    
    await bot.change_presence(activity=activity)
    gradient_log(
        (100, 255, 100),
        (100, 255, 100),
        f"[STATUS] Set status to '{activity_type}: {config.status}'"
    )

async def print_startup_info(bot):
    """Print detailed startup information."""
    uptime = datetime.now() - bot.startup_time
    
    gradient_log(
        (0, 200, 255),
        (100, 200, 255),
        """
╭──────────────────────────────╮
│  Bot Startup Complete        │
╰──────────────────────────────╯
        """
    )
    
    info_lines = [
        f"User: {bot.user} ({bot.user.id})",
        f"Prefix: {config.prefix}",
        f"Status: {config.status}",
        f"Guilds: {len(bot.guilds)}",
        f"Startup Time: {uptime.total_seconds():.2f}s",
    ]
    
    for line in info_lines:
        print(f"  {line}")
    
    print()

# ============================
#  Cog Loader
# ============================

async def load_cogs_verbose(bot):
    """Load all cogs from the cogs directory with detailed logging."""
    return await load_cogs(bot)

# ============================
#  Main Entry Point
# ============================

async def main():
    """Main entry point for the bot."""
    print_disclaimer()
    print_banner()
    
    # Validate configuration
    gradient_log(
        (100, 200, 255),
        (100, 200, 255),
        "[STARTUP] Validating configuration..."
    )
    
    if not config.validate():
        sys.exit(1)
    
    gradient_log(
        (0, 255, 100),
        (0, 255, 100),
        f"[CONFIG] {config}"
    )
    
    # Create bot instance
    gradient_log(
        (100, 200, 255),
        (100, 200, 255),
        "[STARTUP] Initializing bot..."
    )
    
    bot = create_bot()
    
    async with bot:
        # Load cogs before connecting
        await load_cogs_verbose(bot)
        
        # Connect to Discord
        gradient_log(
            (100, 200, 255),
            (100, 200, 255),
            "[STARTUP] Connecting to Discord..."
        )
        
        try:
            await bot.start(config.discord_token)
        except KeyboardInterrupt:
            gradient_log((255, 255, 0), (255, 0, 0), "[SHUTDOWN] Bot interrupted by user")
            await bot.close()
        except discord.errors.LoginFailure:
            gradient_log((255, 0, 0), (255, 0, 0), "[ERROR] Invalid Discord token")
            sys.exit(1)
        except Exception as e:
            gradient_log((255, 0, 0), (255, 0, 0), f"[FATAL] {e}")
            traceback.print_exc()
            sys.exit(1)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        gradient_log((255, 255, 0), (255, 0, 0), "[SHUTDOWN] Bot interrupted")
        sys.exit(0)
    except Exception as e:
        gradient_log((255, 0, 0), (255, 0, 0), f"[FATAL] Unhandled exception: {e}")
        traceback.print_exc()
        sys.exit(1)
