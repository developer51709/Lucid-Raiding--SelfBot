"""
Raiding cog: Commands for server raiding operations.
"""

import discord
from discord.ext import commands
import asyncio
import random
import string
from utils.color import log
from utils.messages import default_raid
from config import config
from datetime import datetime
import aiohttp
import json
import os

class Raiding(commands.Cog):
    """Raiding commands for the bot."""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ghostping", help="Ghost ping a user (delete immediately)")
    async def ghostping(self, ctx, user: discord.User):
        """Send a ghost ping to a user (message deletes after mention)."""
        try:
            await ctx.message.delete()
        except discord.Forbidden:
            pass
        
        try:
            msg = await ctx.send(f"{user.mention}")
            await msg.delete()
        except discord.HTTPException as e:
            await ctx.send(f"Failed to send ghost ping: {e}")

    
    @commands.command(name="spam", help="Spam a message multiple times")
    async def spam(self, ctx, count: int, *, message: str):
        """Spam a message multiple times (be careful!)."""
        try:
            await ctx.message.delete()
        except discord.Forbidden:
            pass
        
        if count < 1 or count > 100:
            await ctx.send("Count must be between 1 and 100.")
            return
        
        if len(message) > 2000:
            await ctx.send("Message is too long (max 2000 characters).")
            return
        
        try:
            for _ in range(count):
                await ctx.send(message)
        except discord.HTTPException as e:
            await ctx.send(f"Failed to spam: {e}")


    @commands.command(name="raid", help="Spam the raid message in the current channel")
    async def raid(self, ctx, count: int = 10):
        """Spam the raid message in the current channel."""
        try:
            await ctx.message.delete()
        except discord.Forbidden:
            pass

        if count < 1 or count > 100:
            await ctx.send("Count must be between 1 and 100.")
            return

        try:
            for _ in range(count):
                await ctx.send(default_raid)
        except discord.HTTPException as e:
            await ctx.send(f"Failed to spam: {e}")



async def setup(bot):
    await bot.add_cog(Raiding(bot))