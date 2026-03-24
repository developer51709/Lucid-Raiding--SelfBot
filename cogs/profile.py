import discord
from discord.ext import commands
import aiohttp
import asyncio
from config import TOKEN



DEFAULT_TITLES = [
    "The Curse Of War",
    "The Curse Of Greed",
    "The Curse Of Lust",
    "The Curse Of Wrath",
    "The Curse Of Pride",
    "The Curse Of Envy",
    "The Curse Of Death",
    "The Curse Of Life",
    "The Curse Of Love",
    "The Curse Of Hate"
]

bios = [
    "**#cursed**",
    "Probably Rate Limited",
    "alt account: @hgrm",
    "Coding The Worlds Best Selfbot As We Speak.                                                                    https://discord.gg/znZRS5DkGM"
]

statuses = [
    "#cursed",
    "#vile",
    "#purge",
    "#slice",
    "#burn",
    "#vault",
    "#rebirthed",
    "Coding The Worlds Best Selfbot As We Speak."
]

headers = {
    "authorization": TOKEN,
    "content-type": "application/json",
    "user-agent": "Mozilla/5.0"
}

