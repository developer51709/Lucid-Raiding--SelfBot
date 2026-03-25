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
        self.help_banner = "**「ʟᴜᴄɪᴅ ʀᴀɪᴅɪɴɢ™ sᴇʟғʙᴏᴛ ᴠ1.0」**\n\n"
    
    @commands.command(name="ping", help="Show the SelfBot's ping")
    async def ping(self, ctx):
        """Respond with pong and latency."""
        latency = round(self.bot.latency * 1000)
        await ctx.send(f"Pong! {latency}ms")
        try:
            await ctx.message.delete()
        except discord.Forbidden:
            pass
    
    @commands.command(name="help", help="Show command help")
    async def help_command(self, ctx, command_name: str = None):
        """Display help for commands in custom format."""
        try:
            await ctx.message.delete()
        except discord.Forbidden:
            pass
        
        # If a specific command is requested
        if command_name:
            cmd = self.bot.get_command(command_name)
            if not cmd:
                await ctx.send(f"Command '{command_name}' not found.")
                return
            
            # Build help for specific command
            help_text = self.help_banner
            prefix = ctx.clean_prefix
            help_text += f"**⪼** `{prefix}{cmd.name}`"
            
            if cmd.help:
                help_text += f" — {cmd.help}"
            
            if cmd.params:
                params = [p for p in cmd.params.keys() if p != "self"]
                if params:
                    help_text += f"\n\nUsage: {prefix}{cmd.name} {' '.join(f'<{p}>' for p in params)}"
            
            await ctx.send(f"{help_text}")
            return
        
        # Build help for all commands
        help_text = self.help_banner
        
        # Collect all commands from all cogs
        commands_list = []
        for cog in self.bot.cogs.values():
            for cmd in cog.get_commands():
                if cmd.hidden:
                    continue
                commands_list.append((cmd.name, cmd.help or "No description"))
        
        # Also add commands not in a cog
        for cmd in self.bot.walk_commands():
            if cmd.cog is None and not cmd.hidden:
                if (cmd.name, cmd.help or "No description") not in commands_list:
                    commands_list.append((cmd.name, cmd.help or "No description"))
        
        # Sort alphabetically
        commands_list.sort(key=lambda x: x[0])
        
        # Format commands
        prefix = ctx.clean_prefix
        for cmd_name, cmd_help in commands_list:
            help_text += f"**⪼** `{prefix}{cmd_name}`\n-# {cmd_help}\n\n"
        
        # Split into chunks if message is too long
        if len(help_text) > 2000:
            chunks = []
            current_chunk = self.help_banner
            
            for cmd_name, cmd_help in commands_list:
                line = f"**⪼** `{prefix}{cmd_name}`\n-# {cmd_help}\n\n"
                if len(current_chunk) + len(line) > 1900:
                    chunks.append(current_chunk)
                    current_chunk = self.help_banner + line
                else:
                    current_chunk += line
            
            if current_chunk:
                chunks.append(current_chunk)
            
            for chunk in chunks:
                await ctx.send(f"{chunk}")
        else:
            await ctx.send(f"{help_text}")
    
    @commands.Cog.listener()
    async def on_message(self, message):
        """Listen to messages (for logging purposes)."""
        if message.author == self.bot.user:
            return

async def setup(bot):
    """Setup function to load this cog."""
    await bot.add_cog(Core(bot))
