import asyncio
import logging
import logging.handlers
import yaml

from typing import List, Optional

import discord
from discord.ext import commands
from aiohttp import ClientSession


class Morning(commands.Bot):
    def __init__(
        self,
        *args,
        initial_extensions: List[str],
        web_client: ClientSession,
        config_path,
        testing_guild_id: Optional[int] = None,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.web_client = web_client
        self.testing_guild_id = testing_guild_id
        self.initial_extensions = initial_extensions
        self.configpath = config_path
        conf_file = open(config_path)
        self.config = yaml.safe_load(conf_file)

    async def setup_hook(self) -> None:
        for extension in self.initial_extensions:
            await self.load_extension(f"cogs.{extension}")

        if self.testing_guild_id:
            guild = discord.Object(self.testing_guild_id)
            self.tree.copy_global_to(guild=guild)
            await self.tree.sync(guild=guild)


async def main():
    logger = logging.getLogger("discord")
    logger.setLevel(logging.INFO)

    handler = logging.handlers.RotatingFileHandler(
        filename="discord.log",
        encoding="utf-8",
        maxBytes=32 * 1024 * 1024,  # 32 MiB
        backupCount=5,  # Rotate through 5 files
    )
    dt_fmt = "%Y-%m-%d %H:%M:%S"
    formatter = logging.Formatter(
        "[{asctime}] [{levelname:<8}] {name}: {message}", dt_fmt, style="{"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    async with ClientSession() as our_client:
        exts = ["utils"]
        async with Morning(
            commands.when_mentioned,
            config_path="config.yml",
            web_client=our_client,
            testing_guild_id=664600025573359626,
            initial_extensions=exts,
            intents=discord.Intents.all(),
        ) as bot:

            await bot.start(bot.config["API"]["token"])


asyncio.run(main())
