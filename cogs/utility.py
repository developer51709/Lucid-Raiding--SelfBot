"""
Utility cog: User management and utility commands.
"""

import discord
from discord.ext import commands
from utils.color import gradient_log

class Utility(commands.Cog):
    """Utility commands for the bot."""
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="status", help="Change bot status and activity")
    async def status(self, ctx, activity_type: str, *, message: str):
        """Change bot status and activity type."""
        gradient_log((0, 255, 0), (0, 255, 0), f"[COMMAND] {ctx.author} used status")
        
        try:
            await ctx.message.delete()
        except discord.Forbidden:
            pass
        
        activity_type = activity_type.lower()
        activity_map = {
            "playing": discord.ActivityType.playing,
            "listening": discord.ActivityType.listening,
            "watching": discord.ActivityType.watching,
            "competing": discord.ActivityType.competing,
        }
        
        if activity_type not in activity_map:
            await ctx.send(f"Invalid activity type. Use: {', '.join(activity_map.keys())}")
            return
        
        activity = discord.Activity(type=activity_map[activity_type], name=message)
        await self.bot.change_presence(activity=activity)
        
        await ctx.send(f"Status changed to: {activity_type} {message}")
    
    @commands.command(name="username", help="Change bot username")
    async def username(self, ctx, *, new_name: str):
        """Change the bot's username."""
        gradient_log((0, 255, 0), (0, 255, 0), f"[COMMAND] {ctx.author} used username")
        
        try:
            await ctx.message.delete()
        except discord.Forbidden:
            pass
        
        if len(new_name) < 2 or len(new_name) > 32:
            await ctx.send("Username must be between 2 and 32 characters.")
            return
        
        try:
            await self.bot.user.edit(username=new_name)
            await ctx.send(f"Username changed to: {new_name}")
        except discord.HTTPException as e:
            await ctx.send(f"Failed to change username: {e}")
    
    @commands.command(name="nick", help="Change nickname in guild")
    async def nick(self, ctx, *, new_nick: str):
        """Change the bot's nickname in the current guild."""
        gradient_log((0, 255, 0), (0, 255, 0), f"[COMMAND] {ctx.author} used nick")
        
        try:
            await ctx.message.delete()
        except discord.Forbidden:
            pass
        
        if not ctx.guild:
            await ctx.send("This command can only be used in a guild.")
            return
        
        try:
            await ctx.guild.me.edit(nick=new_nick)
            await ctx.send(f"Nickname changed to: {new_nick}")
        except discord.HTTPException as e:
            await ctx.send(f"Failed to change nickname: {e}")
    
    @commands.command(name="ghostping", help="Ghost ping a user (delete immediately)")
    async def ghostping(self, ctx, user: discord.User):
        """Send a ghost ping to a user (message deletes after mention)."""
        gradient_log((0, 255, 0), (0, 255, 0), f"[COMMAND] {ctx.author} used ghostping on {user}")
        
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
        gradient_log((0, 255, 0), (0, 255, 0), f"[COMMAND] {ctx.author} used spam ({count}x)")
        
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
    
    @commands.command(name="clear", help="Clear messages from channel")
    async def clear(self, ctx, count: int):
        """Delete messages from the channel."""
        gradient_log((0, 255, 0), (0, 255, 0), f"[COMMAND] {ctx.author} used clear ({count} messages)")
        
        try:
            await ctx.message.delete()
        except discord.Forbidden:
            pass
        
        if count < 1 or count > 100:
            await ctx.send("Count must be between 1 and 100.")
            return
        
        try:
            deleted = await ctx.channel.purge(limit=count)
            await ctx.send(f"Deleted {len(deleted)} message(s).")
        except discord.HTTPException as e:
            await ctx.send(f"Failed to clear messages: {e}")
    
    @commands.command(name="avatar", help="Change bot avatar")
    async def avatar(self, ctx, *, image_url: str = None):
        """Change the bot's avatar from URL or attachment."""
        gradient_log((0, 255, 0), (0, 255, 0), f"[COMMAND] {ctx.author} used avatar")
        
        try:
            await ctx.message.delete()
        except discord.Forbidden:
            pass
        
        try:
            # Check for attachment
            if ctx.message.attachments:
                image_data = await ctx.message.attachments[0].read()
            elif image_url:
                import aiohttp
                async with aiohttp.ClientSession() as session:
                    async with session.get(image_url) as resp:
                        if resp.status != 200:
                            await ctx.send("Failed to fetch image URL.")
                            return
                        image_data = await resp.read()
            else:
                await ctx.send("Provide an image URL or attach an image.")
                return
            
            await self.bot.user.edit(avatar=image_data)
            await ctx.send("Avatar changed successfully.")
        except Exception as e:
            await ctx.send(f"Failed to change avatar: {e}")
    
    @commands.command(name="about", help="Show bot info")
    async def about(self, ctx):
        """Display bot information."""
        gradient_log((0, 255, 0), (0, 255, 0), f"[COMMAND] {ctx.author} used about")
        
        try:
            await ctx.message.delete()
        except discord.Forbidden:
            pass
        
        embed = discord.Embed(
            title="Lucid Raiding™ SelfBot v1.0",
            color=discord.Color.blue()
        )
        embed.add_field(name="User", value=self.bot.user, inline=False)
        embed.add_field(name="ID", value=self.bot.user.id, inline=False)
        embed.add_field(name="Guilds", value=len(self.bot.guilds), inline=False)
        embed.add_field(name="Latency", value=f"{round(self.bot.latency * 1000)}ms", inline=False)
        
        await ctx.send(embed=embed)

async def setup(bot):
    """Setup function to load this cog."""
    await bot.add_cog(Utility(bot))
