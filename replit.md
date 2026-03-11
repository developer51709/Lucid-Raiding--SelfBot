# Lucid Raiding™ SelfBot v1.0

A Discord selfbot developed by Nyxen and Cursefile.

## Stack
- **Language:** Python 3.11
- **Library:** `discord.py-self` — a fork of discord.py for selfbots
- **UI:** Custom ANSI gradient/color terminal logging via `utils/color.py`

## Project Structure
```
main.py          # Entry point: disclaimer, banner, bot setup
utils/
  color.py       # Terminal color/gradient utilities (Color class, gradient_text, gradient_log)
requirements.txt # discord.py-self
pyproject.toml   # Project metadata
```

## Workflow
- **Start application** — `python main.py` (console output)

## Configuration
- `PREFIX` environment variable sets the bot command prefix (defaults to `!`)
- Discord user token is required to run the bot (not yet implemented in main.py)

## Notes
- Selfbots are against Discord ToS — disclaimer is shown on startup
- App is interactive (console TUI), not a web app
