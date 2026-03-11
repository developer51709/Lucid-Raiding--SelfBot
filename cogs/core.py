"""
Core cog: Basic bot commands and utilities.
"""

import discord
from discord.ext import commands
from utils.color import gradient_log

class Core(commands.Cog):
    """Core commands for the bot."""
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="ping", help="Ping the bot")
    async def ping(self, ctx):
        """Respond with pong and latency."""
        latency = round(self.bot.latency * 1000)
        gradient_log((0, 255, 0), (0, 255, 0), f"[COMMAND] {ctx.author} used ping")
        await ctx.send(f"Pong! {latency}ms")
    
    @commands.command(name="help_custom", help="Show custom help")
    async def help_custom(self, ctx):
        """Display custom help information."""
        gradient_log((0, 255, 0), (0, 255, 0), f"[COMMAND] {ctx.author} used help_custom")
        
        embed = discord.Embed(
            title="Lucid Raiding™ SelfBot",
            description="Core Commands",
            color=discord.Color.blue()
        )
        embed.add_field(
            name="!ping",
            value="Check bot latency",
            inline=False
        )
        embed.add_field(
            name="!help_custom",
            value="Show this help message",
            inline=False
        )
        embed.set_footer(text="Use !help for all commands")
        
        await ctx.send(embed=embed)
    
    @commands.Cog.listener()
    async def on_message(self, message):
        """Listen to messages (for logging purposes)."""
        if message.author == self.bot.user:
            return
        # You can add custom message handling here

async def setup(bot):
    """Setup function to load this cog."""
    await bot.add_cog(Core(bot))
