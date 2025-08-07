import asyncio
import logging
import re
import os
from discord.ext import commands
import subprocess
logger = logging.getLogger(__name__)
from pathlib import Path
from GreyBot.utils.interactions import _embeds
Base = Path(__file__).parent.parent.parent
greyCode = Base / "assets" / "GreybelDiscordCode.gs"
greybel = r"C:\Users\jorda\AppData\Roaming\npm\greybel.cmd" # Hard Coded. Get over it.




class FunRunMiniScript(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.author = None

    def parse_error(self,output: str):
        # if you're reading this. ChatGTP made this reg ex thing.
        ansi_clean = re.sub(r'\x1B\[[0-?]*[ -/]*[@-~]', '', output)
        match = re.search(r' error:\s*(.+?)\s+at\s', ansi_clean)
        if match:
            return match.group(1).strip()
        return ansi_clean.strip()

    def clean_code(self,code):
        logger.info(f"Loading {greyCode}")
        code = code.strip()
        if code.startswith("```") or code.endswith("```"):
            code = code.replace("```","")
        with open(greyCode,"w") as f:
            f.write(code)
        return code

    async def run_greybel(self,code):
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
                logger.info(f"Subproccess pid: {proc.pid}")
                try:
                    out, err = proc.communicate(timeout=5)
                    result = err, out
                    logger.info(f"Done running with: STDOUT: {out} ERR: {err}")
                    self.OUT = result

                except subprocess.TimeoutExpired as e:
                    logger.error(f"Script timed out: {e}")
                    proc.kill()
                    logger.error(f"Killed {proc.pid}")
                    self.OUT = "timeout"
                finally:
                    try:
                        subprocess.run(["taskkill", "/F", "/IM", "node.exe"], shell=True)
                    except Exception as f:
                        logger.error(f"Couldnt kill node procs... {f}")
                    return self.OUT
            except:
                return "intresting error. "

        result = await asyncio.to_thread(_run)
        logger.info(f"Result Obtained from Thread. {result}")
        if result == "timeout":
            return _embeds.embed_code_execution(False, self.author, f"Error: Script timed out after 3 sec.")
        elif not result:
            return _embeds.embed_code_execution(False, self.author, f"Error: Something bad has happened.")
        stderr, stdout = result
        if stderr:
            return _embeds.embed_code_execution(False,self.author,f"Error: {self.parse_error(stderr)}")
        elif stdout:
            return _embeds.embed_code_execution(True,self.author,stdout)
        return _embeds.embed_code_execution(True,self.author,"Code ran but there appears to be no output...")

    @commands.command(name="greybel",description="Run Miniscript code")
    async def FunRunGS(self,ctx,*,code:str or None):
        print(f"ctx:{ctx}, code: {code}")
        self.author = ctx.author
        if ctx.message.reference and not code:
            try:
                replied_message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
                code = replied_message.content
            except:
                await ctx.send("Couldn't fetch the replied message.")
                return

        if not code:
            await ctx.send("No code provided.")
            return
        output = await self.run_greybel(code)
        await ctx.send(embed=output)

    @FunRunGS.error
    async def RunError(self,ctx,error):
        logger.warning(f"Code Run Failed. {error}")
        if isinstance(error,commands.MissingRequiredArgument):
            try:
                await ctx.send("That command would probly work if you gave it something to run...")
            except:
                logger.error("Some Dumbass did a thing and it broke")
async def setup(bot):
    """Required."""
    await bot.add_cog(FunRunMiniScript(bot))
