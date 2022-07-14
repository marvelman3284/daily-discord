#!/usr/bin/env python3
from discord.ext import commands
import yaml, discord, sys, logging, asyncio 

# from cogs.utils import Utils
from help import MorningHelp

class Morning(commands.AutoShardedBot):
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


    async def setup_hook(self):
        await self.load_extension(f"cogs.utils")
        await self.tree.sync(guild=discord.Object(id=self.config['API']['guildid']))

    
intents = discord.Intents.all()
logging.basicConfig(level=logging.INFO)
bot = Morning(command_prefix='!', configpath=sys.argv[1], intents=intents)

bot.run(bot.config['API']['token'])
