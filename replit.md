# Lucid Raiding™ SelfBot v1.0

A Discord selfbot developed by Nyxen and Cursefile.

## Stack
- **Language:** Python 3.11
- **Library:** `discord.py-self` — a fork of discord.py for selfbots
- **UI:** Custom ANSI gradient/color terminal logging via `utils/color.py`

## Project Structure
```
main.py              # Entry point: disclaimer, banner, bot setup, cog loader
utils/
  color.py           # Terminal color/gradient utilities (Color class, gradient_text, gradient_log)
cogs/                # Modular command cogs
  __init__.py        # Package init
  core.py            # Core commands (ping, help_custom)
requirements.txt     # discord.py-self
pyproject.toml       # Project metadata
```

## Workflow
- **Start application** — `python main.py` (console output)

## Configuration
- `PREFIX` environment variable sets the bot command prefix (defaults to `!`)
- Discord user token is required to run the bot (not yet implemented in main.py)

## Core Features
- **Modular cog loader:** Automatically loads all cogs from `cogs/` directory
- **Async event handlers:** Ready event, command error handling
- **Colored logging:** All bot events logged with gradients via `utils.color`
- **Example commands:** `!ping`, `!help_custom` in core.py

## Adding New Cogs
1. Create a new file in `cogs/` (e.g., `cogs/raid.py`)
2. Define a class extending `commands.Cog` with command methods decorated with `@commands.command()`
3. Add an async `setup(bot)` function at the end
4. The cog will auto-load on bot startup

Example:
```python
from discord.ext import commands

class MyCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="mycommand")
    async def my_command(self, ctx):
        await ctx.send("Response")

async def setup(bot):
    await bot.add_cog(MyCommands(bot))
```

## Running the Bot
Requires `DISCORD_TOKEN` environment variable with your Discord user token.
```bash
export DISCORD_TOKEN="your_token_here"
python main.py
```

## Notes
- Selfbots are against Discord ToS — disclaimer is shown on startup
- App is interactive console bot, not a web app
