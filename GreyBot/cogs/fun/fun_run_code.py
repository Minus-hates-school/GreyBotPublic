import asyncio
import logging
import re
import os
from discord.ext import commands
import discord
from discord import app_commands
import subprocess
from pathlib import Path
from GreyBot.utils.interactions import _embeds

logger = logging.getLogger(__name__)
Base = Path(__file__).parent.parent.parent
greyCode = Base / "assets" / "GreybelDiscordCode.gs"
greybel = r"C:\Users\jorda\AppData\Roaming\npm\greybel.cmd"  # Hardcoded

class CodeInputModal(discord.ui.Modal, title="Run Greybel Code"):
    code = discord.ui.TextInput(label="Miniscript Code", style=discord.TextStyle.paragraph, required=True,max_length=999,min_length=1)

    def __init__(self, cog, interaction_user):
        super().__init__()
        self.cog = cog
        self.user = interaction_user

    async def on_submit(self, interaction: discord.Interaction):
        self.cog.author = self.user
        await interaction.response.defer(thinking=True)
        result = await self.cog.run_greybel(self.code.value)
        await interaction.followup.send(embed=result, ephemeral=True)


class FunRunModalScript(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.author = None

    def parse_error(self, output: str):
        ansi_clean = re.sub(r'\x1B\[[0-?]*[ -/]*[@-~]', '', output)
        match = re.search(r'Prepare error:\s*(.+?)\s+at\s', ansi_clean)
        if match:
            return match.group(1).strip()
        return ansi_clean.strip()

    def clean_code(self, code):
        logger.info(f"Loading {greyCode}")
        code = code.strip().replace("```", "")
        with open(greyCode, "w") as f:
            f.write(code)
        return code

    async def run_greybel(self, code):
        logger.warning(f"Running code: {self.clean_code(code)}")

        def _run():
            try:
                logger.debug(f"Running {greyCode}")
                proc = subprocess.Popen(
                    [greybel, "execute", "-si", "-et", "Mock", greyCode],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    start_new_session=True
                )
                logger.info(f"Subprocess PID: {proc.pid}")
                try:
                    out, err = proc.communicate(timeout=3)
                    result = err, out
                    logger.info(f"Finished with STDOUT: {out} | STDERR: {err}")
                    return result
                except subprocess.TimeoutExpired:
                    logger.error("Script timed out")
                    proc.kill()
                    logger.warning(f"Killed process {proc.pid}")
                    return "timeout"
                finally:
                    try:
                        subprocess.run(["taskkill", "/F", "/IM", "node.exe"], shell=True)
                    except Exception as e:
                        logger.error(f"Failed to kill Node.js processes: {e}")
            except Exception as e:
                logger.error(f"Unhandled exception: {e}")
                return None

        result = await asyncio.to_thread(_run)
        logger.info(f"Thread finished. Result: {result}")

        if result == "timeout":
            return _embeds.embed_code_execution(False, self.author, "Error: Script timed out after 3 seconds.")
        elif not result:
            return _embeds.embed_code_execution(False, self.author, "Error: Something went wrong.")

        stderr, stdout = result
        if stderr:
            return _embeds.embed_code_execution(False, self.author, f"Error: {self.parse_error(stderr)}")
        elif stdout:
            return _embeds.embed_code_execution(True, self.author, stdout)
        return _embeds.embed_code_execution(False, self.author, "Unknown error occurred.")

    @app_commands.command(name="grey", description="Run Greybel Localy")
    async def greybel_slash(self, interaction: discord.Interaction):
        await interaction.response.send_modal(CodeInputModal(self, interaction.user))

async def setup(bot):
    await bot.add_cog(FunRunModalScript(bot))
