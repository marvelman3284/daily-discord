import discord, os, asyncio
from discord.ext import commands
from datetime import datetime 


class Utils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # @commands.command(brief='Information about the bot instance')
    # async def info(self, ctx):
    #     commit = os.popen('git rev-parse --short HEAD').read().strip()
    #     embed = discord.Embed(
    #         title="Daily Discord Bot",
    #         url="https://github.com/marvelman3284/daily-discord")
    #     embed.add_field(name="Running Commit", value=commit,
    #                     inline=False)  # What commit is running?
    #     embed.add_field(name="Server count",
    #                     value=(len(self.bot.guilds)),
    #                     inline=False)
    #     embed.add_field(name="Owner", value=self.bot.owner_id, inline=False)
    #     await ctx.send(embed=embed)
    #

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        # while True:
            # sleep(1)
        await message.author.send("hello world")

    @commands.command()
    async def ping(self, ctx):
        """Displays latency between client and bot"""
        latency = round(self.bot.latency * 1000, 2)
        return await ctx.send('Pong! ' + str(latency) + 'ms')

    #     # == START OWNER COMMANDS == #
    # @commands.command(hidden=True)
    # @commands.is_owner()
    # async def quit(self, ctx):
    #     await ctx.send('bot is going down NOW!')
    #     raise SystemExit
