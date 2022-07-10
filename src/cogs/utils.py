import discord, os, asyncio
from discord.ext import commands, tasks
import services.gcal as gcal
import services.weather as weather


class Utils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.daily.start()


    @commands.command(brief='Information about the bot instance')
    async def info(self, ctx):
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
        await ctx.send(embed=embed)


    @commands.command()
    async def ping(self, ctx):
        """Displays latency between client and bot"""
        latency = round(self.bot.latency * 1000, 2)
        return await ctx.send('Pong! ' + str(latency) + 'ms')


    @commands.command(brief="Gets the next 5 calender events")
    async def next(self, ctx):
        events = gcal.filter(gcal.get_events()['normal'])

        embed = discord.Embed(
            title="Upcoming events"
        )

        for event in events:
            embed.add_field(name=event[11:], value=event[:10], inline=True)

        await ctx.send(embed=embed)

    @commands.command(brief="Get the weather")
    async def weather(self, ctx):
        # Get todays weather
        key = self.bot.getConfig('API', 'key')
        lat = self.bot.getConfig('API', 'lat')
        lon = self.bot.getConfig('API', 'lon')

        week_weather = weather.get_weather(key, lat, lon)
        week_weather = week_weather[0]

        await ctx.send(week_weather)


    @commands.command(brief="Get the weather")
    async def week(self, ctx):
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

        await ctx.send(embed=embed)


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
            # HACK
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
    @commands.command(hidden=True)
    @commands.is_owner()
    async def quit(self, ctx):
        await ctx.send('bot is going down NOW!')
        raise SystemExit
