import discord
from discord import app_commands, Interaction
from discord._types import ClientT
from discord.ext import commands
from discord import ui


class CodeModal(discord.ui.Modal,title="Run MiniScript"):
    title = ui.TextInput(label="code",placeholder='print "hello world!"',required=True)
