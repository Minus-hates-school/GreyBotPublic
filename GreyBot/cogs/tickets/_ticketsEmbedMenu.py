from discord import embeds,interactions,ui
"""
This file holds all the discord embeds for the tickets cogs.
"""
from datetime import datetime
import discord
import time
def unix() -> str: return f"<t:{int(time.time())}>"

def embed_verified_success(name, amount):
    """
    Embedding for user verification success, and therefore a join
    """
    embed = discord.Embed(
        title=''
        , description=f'{name}, human number {amount} has joined.'
        , color=discord.Color.dark_green()
    )
    embed.set_footer(text=unix())
    return embed


def embed_submit_tip(user, ticket_name):
    """
    Embed for creation of a new ticket.
    """
    embed = discord.Embed(
        title=f'{str(user)} opened a ticket.',
        description=f"Tip Submission: {ticket_name}",
        color=discord.Color.green(),
        timestamp=datetime.now(),
    )
    return embed


def embed_ticket_update(user, ticket_name):
    """
    Embed for update of a new ticket.
    """
    embed = discord.Embed(
        title=f'{str(user)} updated a ticket.',
        description=f'Ticket: <#{ticket_name}>',
        color=discord.Color.green(),
        timestamp=datetime.utcnow(),
    )
    return embed


def embed_ticket_delete(user, ticket_name):
    """
    Embed for deletion of a new ticket.
    """
    embed = discord.Embed(
        title=f'{str(user)} deleted a ticket.',
        description=f'Ticket: <#{ticket_name}>',
        color=discord.Color.red(),
        timestamp=datetime.utcnow(),
    )
    return embed


def embed_ticket_remove(user, ticket_name):
    """
    Embed for removal of a new ticket.
    """
    embed = discord.Embed(
        title=f'{str(user)} removed a ticket.',
        description=f'Ticket: <#{ticket_name}>',
        color=discord.Color.red(),
        timestamp=datetime.utcnow(),
    )
    return embed


def embed_cant_do_that(message):
    """
    Embedding for things you cant do.
    """
    embed = discord.Embed(
        title=''
        , description=message
        , color=discord.Color.red()
        , timestamp=datetime.utcnow()
    )
    return embed


def embed_spammer(spammer, message_to_report=None, file_url=None):
    """
    Embedding for detected spam messages.
    """
    embed = discord.Embed(
        title='Firewall has been triggered'
        , description=f'When you send the same message three times, {spammer.mention}, you get the quarantine.'
                      f' Wait for the staff to come let you out.'
        , color=discord.Color.red()
        , timestamp=datetime.utcnow()
    )
    if message_to_report:
        embed.add_field(name='Message:', value=message_to_report, inline=True)
    if file_url:
        embed.add_field(name="Image:", value=file_url, inline=True)
    return embed


def embed_spammer_warn(channel1, channel2):
    """
    Embedding warn for detected spam messages.
    """
    embed = discord.Embed(
        title='Warning'
        , description='When you send the same message **three times**, you get the quarantine.\n'
        , color=discord.Color.red()
        , timestamp=datetime.utcnow()
    )
    report = f"Detected the same message in {channel1.mention} and {channel2.mention}"
    embed.add_field(name="What happened?", value=report, inline=True)
    embed.add_field(
        name="What should you do?"
        , value="Don't panic, and be patent."
                " Someone will answer you as soon as they can."
        , inline=True)
    embed.set_footer(text="In the meantime... Maybe make sure your question contains your code, as well as the output.")
    return embed


def embed_suggestions(author, question):
    embed = discord.Embed(
        title=f'Suggestion by {author.name}'
        , description=f'Please vote using reactions.'
        , color=discord.Color.yellow()
        , timestamp=datetime.utcnow()
    )

    embed.add_field(
        name='Suggestion:'
        , value=f'{question}'
        , inline=True
    )

    return embed


def embed_suggestion_error(channel):
    embed = discord.Embed(
        title='Oops!'
        , description=f'Please only use the /suggest command in {channel.mention}'
        , color=discord.Color.red()
        , timestamp=datetime.utcnow()
    )
    return embed

def embed_default_response(title,content):
    embed = discord.Embed(
        title=title
        , description=content
        , color=discord.Color.dark_green()
        , timestamp=datetime.now()
    )
    return embed

def embed_leaderboard(people_list, server_name, server_logo):
    """
        Embedding for the leaderboard command.
        """
    embed = discord.Embed(
        title=f"{server_name}'s Top Point earners"
        , color=discord.Color.gold()
        , timestamp=datetime.utcnow()
    )

    embed.set_thumbnail(
        url=server_logo
    )
    for place, person in enumerate(people_list):
        embed.add_field(
            name=f"#{place + 1}  -  {person[0].display_name}"
            , value=f"Points: {person[1]}"
            , inline=False
        )
    return embed
