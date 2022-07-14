import discord, os, asyncio
from discord.ext import commands, tasks
from discord import app_commands
import services.gcal as gcal
import services.weather as weather


class Utils(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.daily.start()

    @app_commands.command(name="info", description="information on the bot instance")
    async def info(self, interaction: discord.Interaction) -> None:
        commit = os.popen('git rev-parse --short HEAD').read().strip()
        embed = discord.Embed(
            title="Daily Discord Bot",
            url="https://github.com/marvelman3284/daily-discord")
        embed.add_field(name="Running Commit", value=commit,
                        inline=False)  # What commit is running?
        embed.add_field(name="Server count",
                        value=(len(self.bot.guilds)),
                        inline=False)
        embed.add_field(name="Owner", value=self.bot.owner_id, inline=False)
        await interaction.response.send_message(embed=embed)


    @app_commands.command(name="ping", description="Displays latency between client and bot")
    async def ping(self, ctx: discord.Interaction):
        """Displays latency between client and bot"""
        latency = round(self.bot.latency * 1000, 2)
        return await ctx.response.send_message('Pong! ' + str(latency) + 'ms')


    @app_commands.command(name="next", description="Get the next few upcoming events")
    async def next(self, ctx: discord.Interaction):
        events = gcal.filter(gcal.get_events()['normal'])

        embed = discord.Embed(
            title="Upcoming events"
        )

        for event in events:
            embed.add_field(name=event[11:], value=event[:10], inline=True)

        await ctx.response.send_message(embed=embed)

    @app_commands.command(name="weather", description="Get todays weather")
    async def weather(self, ctx: discord.Interaction):
        # Get todays weather
        key = self.bot.getConfig('API', 'key')
        lat = self.bot.getConfig('API', 'lat')
        lon = self.bot.getConfig('API', 'lon')

        week_weather = weather.get_weather(key, lat, lon)
        week_weather = week_weather[0]

        await ctx.response.send_message(week_weather)


    @app_commands.command(name="week", description="Get this weeks weather")
    async def week(self, ctx: discord.Interaction):
        # Get todays weather
        key = self.bot.getConfig('API', 'key')
        lat = self.bot.getConfig('API', 'lat')
        lon = self.bot.getConfig('API', 'lon')

        week_weather = weather.get_weather(key, lat, lon)

        embed = discord.Embed(
            title="Weeks Weather"
        )

        for weathers in week_weather:
            # HACK
            weathers = weathers.replace(":", ";", 1)
            weathers = weathers.partition(";")
            embed.add_field(name=weathers[0], value=weathers[-1], inline=True)

        await ctx.response.send_message(embed=embed)


    @tasks.loop(seconds=60)
    async def daily(self):

        def get_events(category: str) -> discord.Embed:
            events = gcal.filter(gcal.get_events()[category])

            if category == 'normal':
                cal_embed = discord.Embed(
                    title="Upcoming events"
                )
            else:
                cal_embed = discord.Embed(
                    title="Upcoming workouts"
                )

            for event in events:
                cal_embed.add_field(name=event[11:], value=event[:10], inline=True)

            return cal_embed

        # Get todays weather
        key = self.bot.getConfig('API', 'key')
        lat = self.bot.getConfig('API', 'lat')
        lon = self.bot.getConfig('API', 'lon')

        week_weather = weather.get_weather(key, lat, lon)

        weather_embed = discord.Embed(
            title="Weeks Weather"
        )

        for weathers in week_weather:
            # HACK:
            weathers = weathers.replace(":", ";", 1)
            weathers = weathers.partition(";")
            weather_embed.add_field(name=weathers[0], value=weathers[-1], inline=True)

        await self.bot.get_user(529118747521318913).send(embed=weather_embed)
        await self.bot.get_user(529118747521318913).send(embed=get_events('normal'))
        await self.bot.get_user(529118747521318913).send(embed=get_events('workout'))


    @daily.before_loop
    async def before_task(self):
        print('waiting...')
        await self.bot.wait_until_ready()

    
    # == START OWNER COMMANDS == #
    @app_commands.command(name="quit", description="take the bot down")
    @commands.is_owner()
    async def quit(self, ctx: discord.Interaction):
        await ctx.response.send_message('bot is going down NOW!')
        raise SystemExit


async def setup(bot: commands.Bot):
    await bot.add_cog(Utils(bot), guilds=[discord.Object(id=664600025573359626), discord.Object(id=529118747521318913)])
