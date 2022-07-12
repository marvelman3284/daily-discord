#!/usr/bin/env python3
from discord.ext import commands
import yaml, discord, sys, logging

from cogs.utils import Utils
from help import MorningHelp

class Morning(commands.Bot):
    """An extension of discord.ext.commands.Bot with configuration
    management and database management"""
    def __init__(self,
                 command_prefix,
                 configpath: str,
                 help_command=MorningHelp(),
                 description=None,
                 **options):
        self.configpath = configpath
        conf_file = open(configpath)
        self.config = yaml.safe_load(conf_file)
        super().__init__(command_prefix,
                         help_command=help_command,
                         description=description,
                         **options)

    def getConfig(self, section: str, item: str) -> str:
        """Returns a String value from the bot's config file"""
        if item == 'token':
            raise PermissionError('You can\'t get the token during runtime')
        return self.config[section][item]

    def setConfig(self, section: str, item: str, value: str) -> None:
        """Changes a configuration value, and writes it to the file"""
        if section == "API":
            raise PermissionError(
                "You can't modify API settings while the bot is running!")
        self.config[section][item] = value
        with open(self.configpath, 'w') as configfile:
            yaml.dump(self.config, configfile)

    def run(self):
        """Calls discord.ext.commands.Bot.run() with token info"""
        super().run(self.config['API']['token'])


intents = discord.Intents()
intents.members = True  # Join/Leave messages
intents.guild_messages = True  # Trivia
intents.bans = True  # Ban messages
intents.guilds = True  # Docs says so
intents.guild_reactions = True  # For roles
intents.dm_messages = True # Needed for dms

logging.basicConfig(level=logging.WARN)
bot = Morning(command_prefix='!', intents=intents, configpath=sys.argv[1])


@bot.event
async def on_ready():
    logging.info('Morning bot has started')

bot.add_cog(Utils(bot))

bot.run()
