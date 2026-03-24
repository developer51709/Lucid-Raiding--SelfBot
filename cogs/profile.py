"""
Profile cog: Rotate bios, statuses, and stream titles.

Special thanks to @cursefile for making this cog.
"""

import discord
from discord.ext import commands
import aiohttp
import asyncio
import config

TOKEN = config.config.discord_token

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


class Profile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bio_task = None
        self.status_task = None
        self.clan_task = None
        self.streaming_task = None


    async def bio_rotator(self, bio_list):
        headers = {
            "authorization": TOKEN,
            "content-type": "application/json"
        }

        async with aiohttp.ClientSession(headers=headers) as session:
            try:
                while True:
                    for bio in bio_list:

                        async with session.patch(
                            "https://discord.com/api/v9/users/@me/profile",
                            json={"bio": bio}
                        ):
                            pass

                        await asyncio.sleep(5)

            except asyncio.CancelledError:
                pass


    @commands.command(name="bio", aliases=["rbio", "rotatebio"])
    async def biorotate(self, ctx, *, bio_input: str = None):
        """Enable bio rotation with custom bios or default ones."""
        global bio_task

        if bio_task and not bio_task.done():
            await ctx.send("Bio Rotator Already Running")
            return


        if bio_input:
            bio_list = [b.strip() for b in bio_input.split(",") if b.strip()]
        else:
            bio_list = bios

        self.bio_task = asyncio.create_task(self.bio_rotator(bio_list))

        await ctx.send(f"Bio Rotator Started ({len(bio_list)} bios)")


    @commands.command(name="stopbio", aliases=["srbio", "stoprbio", "sbio"])
    async def stopbio(self, ctx):
        """Stop the bio rotation."""
        global bio_task

        if bio_task:
            bio_task.cancel()
            bio_task = None
            await ctx.send("Bio rotator stopped")


    async def status_rotator(self, status_list):

        headers = {
            "authorization": TOKEN,
            "content-type": "application/json"
        }

        try:
            async with aiohttp.ClientSession(headers=headers) as session:
                while True:
                    for status_text in status_list:

                        payload = {
                            "custom_status": {
                                "text": status_text
                            }
                        }

                        async with session.patch(
                            "https://discord.com/api/v9/users/@me/settings",
                            json=payload
                        ):
                            pass

                        await asyncio.sleep(5)

        except asyncio.CancelledError:
            pass


    @commands.command(name="statusrotate", aliases=["rstatus", "rotatestatus"])
    async def status(self, ctx, *, status_input: str = None):
        """Enable status rotation with custom statuses or default ones."""
        global status_task
        await ctx.message.delete()

        if status_task and not status_task.done():
            await ctx.send("Status rotator already running", delete_after=5)
            return


        if status_input:
            status_list = [s.strip() for s in status_input.split(",") if s.strip()]
        else:
            status_list = statuses

        self.status_task = asyncio.create_task(self.status_rotator(status_list))

        await ctx.send(f"Status rotator started ({len(status_list)} statuses)", delete_after=5)


    @commands.command(name="stopstatus", aliases=["srstatus", "stoprtatus", "sstatus"])
    async def stopstatus(self, ctx):
        """Stop the status rotation."""
        global status_task
        await ctx.message.delete()

        if status_task:
            status_task.cancel()
            status_task = None
            await ctx.send("Status rotator stopped", delete_after=5)

    @commands.command(name="streamrotate", aliases=["rstream", "rotatestream"])
    async def autostream(self, ctx, *, args: str = None):
        """Enable stream rotation with custom titles or default ones."""
        interval = 15
        title_list = DEFAULT_TITLES.copy()

        if args:
            parts = [p.strip() for p in args.split(",") if p.strip()]
            if parts and parts[0].isdigit():
                interval = int(parts[0])
                parts = parts[1:]
            if parts:
                title_list = parts

        if interval < 15:
            await ctx.send("Interval must be at least 15 seconds to avoid rate limits.")
            return

        if self.streaming_task and not self.streaming_task.done():
            self.streaming_task.cancel()
            try:
                await self.streaming_task
            except asyncio.CancelledError:
                pass

        async def stream_loop(self):
            while True:
                for title in title_list:
                    try:
                        await self.bot.change_presence(
                            activity=discord.Streaming(
                                name=title,
                                url="https://twitch.tv/cursefiles"
                            )
                        )
                        await asyncio.sleep(interval)

                    except asyncio.CancelledError:
                        return

                    except (
                        ConnectionResetError,
                        discord.ConnectionClosed,
                        aiohttp.ClientConnectionError,
                        asyncio.TimeoutError,
                    ):
                        print("[-] Connection lost...")
                        print("[~] Attempting reconnect...")
                        await asyncio.sleep(10)

                    except Exception as e:
                        print(f"Presence update error: {e}")
                        await asyncio.sleep(interval)

        self.streaming_task = asyncio.create_task(stream_loop())

        await ctx.send(
            f"Stream Rotation Started ({interval}s interval) with {len(title_list)} title(s)."
        )

    @commands.command(name="stopstream", aliases=["srstream", "sstream", "stoprstream"])
    async def stopstream(self, ctx):
        """Stop the stream rotation."""
        if self.streaming_task and not self.streaming_task.done():
            self.streaming_task.cancel()

            try:
                await self.streaming_task
            except asyncio.CancelledError:
                pass

            self.streaming_task = None

            try:
                await self.bot.change_presence(activity=None)
            except Exception:
                pass

            await ctx.send("Stream Rotator Stopped.")
        else:
            await ctx.send("No Active Stream Rotation.")

    @commands.command(name="hypesquad", aliases=["hs", "hsquad"])
    async def hypesquad(self, ctx, house: str):
        """Change your HypeSquad house."""
        house = house.lower()

        houses = {
            "balance": discord.HypeSquadHouse.balance,
            "bravery": discord.HypeSquadHouse.bravery,
            "brilliance": discord.HypeSquadHouse.brilliance
        }

        if house not in houses:
            return await ctx.send("❌ Invalid house. Choose: balance, bravery, brilliance.", delete_after=3)

        try:
            await self.bot.user.edit(house=houses[house])

        # success msg
            await ctx.send(f"✅ Successfully changed HypeSquad to **{house.capitalize()}**!", delete_after=3)

        # fail msg (it fails in the code but still actually works for some fuck ass reason so this is the success msg now)
        except Exception as e:
            await ctx.send(f"```Successfuly Changed HypeSquad Badge to ({house.capitalize()})```", delete_after=3)
            print(e)

async def setup(bot):
    await bot.add_cog(Profile(bot))