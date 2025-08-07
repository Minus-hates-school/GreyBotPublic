import asyncio
import os
import discord
import logging
from discord.ext import commands
from discord import app_commands
from GreyBot.utils.logging_utils import setup_logger
from GreyBot.utils.core.args_utils import parse_args
from GreyBot.utils.core.env_util import Enviormental
TOKEN = os.getenv("TOKEN")

logger = logging.getLogger(__name__)
COGS_ROOT_PATH = os.path.join(os.path.dirname(__file__), "cogs")
intents = discord.Intents.all()

async def load_cogs(bot):
    """
    Loads the directories under the /cogs/ Package
    :param bot:
    :return:
    """
    logger.info("Loading Cogs")
    failed_loads = []
    for dir in os.listdir(COGS_ROOT_PATH):
        if dir.startswith("_"):
            logger.debug(f"Skipping {dir} twas hidden")
            continue
        if dir.startswith("debug") and not logger.level == logging.DEBUG:
            logger.debug(f"Skipping {dir} Not in debug cogs")
        cog_subdir_path = os.path.join(COGS_ROOT_PATH, dir)

        for file in os.listdir(cog_subdir_path):
            if file.endswith(".py") and not file.startswith("_"):
                cog_path = os.path.join(cog_subdir_path, file)
                logger.info(f"Loading Cog: {cog_path}")
                try:
                    await bot.load_extension(f"GreyBot.cogs.{dir}.{file[:-3]}")
                    logger.debug(f"Loaded Cog: {cog_path} : GreyBot.cogs.{dir}.{file[:-3]}")
                except Exception as e:
                    logger.warning("Failed to load: {%s}.{%s}, {%s}", dir, file, e)
                    failed_loads.append(f"{file[:-3]}")
    if failed_loads:
        logger.warning(f"Cog loading finished. Failed to load the following cogs: {', '.join(failed_loads)}")
    else:
        logger.info("Loaded all cogs successfully.")


async def init_bot(TOKEN, bot):
    print("INIT BOT. ")
    try:
        logger.debug("Initializing bot")
        await load_cogs(bot)
        logger.info(f"Loaded{"\n".join(list(bot.cogs.keys()))}")
        await bot.start(TOKEN)
    except TypeError as e:
        print(f"Failed init: {e}")


def main():
    args = Enviormental()
    setup_logger(
        level=args.LOGGING_LEVEL if args.LOGGING_LEVEL else int(os.getenv("LOGGING_LEVEL", 20)),
        stream_logs=args.STREAM_LOGS if args.STREAM_LOGS != None else bool(os.getenv("STREAM_LOGS", False)),
    )
    print("Logger setup...")
    bot = commands.Bot(command_prefix="/", intents=intents)
    bot.remove_command("help")
    ## DATABASE

    ## END DATABASE
    try:
        print(f"Loaded Token: {args.TOKEN}")
        if args.TOKEN is None:
            args.add_var("TOKEN",value=input("Bot Token: "))
        asyncio.run(init_bot(TOKEN=args.TOKEN, bot=bot))
    except:
        print(Exception)


if __name__ == "__main__":
    main()

