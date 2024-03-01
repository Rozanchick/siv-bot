import discord
import logging

GUEST_ROLE_ID = 1167877977363726378
WELCOME_CHANNEL_ID = 1213155212622303353
RULES_CHANNEL_ID = 1167491641314136154
ROLES_GRANT_CHANNEL_ID = 1189304848366182470
ROLES_GRANT_MESSAGE_ID = 1189307422922256464
EMOJI_TO_ROLE = {
    discord.PartialEmoji(name='👤'): GUEST_ROLE_ID,
    discord.PartialEmoji(name='🤡'): 1189583838737879081,
    discord.PartialEmoji(name='😇'): 1189584104560279634,
    discord.PartialEmoji(name='👼'): 1189584257815941160,
    discord.PartialEmoji(name='💀'): 1212773064639778887,
    discord.PartialEmoji(name='☠️'): 1212772830463139900,
    discord.PartialEmoji(name='⚔️'): 1198331612715299056,
}

async def edit_role_on_reaction(bot_instance, payload, operation = 'add'):
    """Adds or removes a role based on a reaction emoji."""
    # Make sure that the message the user is reacting to is the one we care about.
    if payload.message_id != ROLES_GRANT_MESSAGE_ID:
        return

    guild = bot_instance.get_guild(payload.guild_id)
    if guild is None:
        # Check if we're still in the guild and it's cached.
        return

    try:
        role_id = EMOJI_TO_ROLE[payload.emoji]
    except KeyError:
        # If the emoji isn't the one we care about then exit as well.
        logging.warning(f'Emoji not found. Emoji: {payload.emoji}')
        return

    role = guild.get_role(role_id)
    if role is None:
        # Make sure the role still exists and is valid.
        logging.warning(f'Role not found. Role id: {role_id}')
        return

    if operation == 'remove':
        # The payload for `on_raw_reaction_remove` does not provide `.member`
        # so we must get the member ourselves from the payload's `.user_id`.
        member = guild.get_member(payload.user_id)
        if member is None:
            # Make sure the member still exists and is valid.
            logging.warning(f'Member not found. payload.user_id: {payload.user_id}')
            return
    else:
        member = payload.member

    await edit_role_to_member(member, role, operation)

async def edit_role_to_member(member: discord.Member, roles, operation = 'add'):
    """Wrapper for add or remove roles methods."""
    try:
        if operation == 'add':
            await member.add_roles(roles)
        elif operation == 'remove':
            await member.remove_roles(roles)
        else:
            logging.error('Unavailable operation option. Check argument for toggle_role_on_reaction func')
    except discord.HTTPException:
        # If we want to do something in case of errors we'd do it here.
        logging.error(f'An error occured while editing roles on user with id: {member}')
        pass

async def add_guest_role(member: discord.Member):
    guild = member.guild
    if guild is None:
        # Check if we're still in the guild and it's cached.
        return

    role = guild.get_role(GUEST_ROLE_ID)
    if role is None:
        # Make sure the role still exists and is valid.
        logging.warning(f'Guest role not found. Role id: {GUEST_ROLE_ID}')
        return
    try:
        await edit_role_to_member(member, role, operation = 'add')
    except discord.HTTPException:
        logging.error('Error on member.add_roles')
        pass

async def new_members_greetings(member: discord.Member):
    """Приветствие новых пользователей."""
    channel = member.guild.get_channel(WELCOME_CHANNEL_ID)
    rules_channel = member.guild.get_channel(RULES_CHANNEL_ID)
    roles_grant_channel = member.guild.get_channel(ROLES_GRANT_CHANNEL_ID)
    if channel is None:
        logging.error(f'Welcome channel not found. Id: {WELCOME_CHANNEL_ID}')
        return
    if rules_channel is None:
        logging.error(f'Rules channel not found. Id: {RULES_CHANNEL_ID}')
        return
    if roles_grant_channel is None:
        logging.error(f'Roles grant channel not found. Id: {ROLES_GRANT_CHANNEL_ID}')
        return

    welcome_message = f"Привет, {member.mention}! Добро пожаловать на сервер! 🎉\nДля доп. информации просьба ознакомиться с {rules_channel.mention} и {roles_grant_channel.mention}."
    await channel.send(welcome_message)
