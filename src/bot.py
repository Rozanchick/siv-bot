import discord
import src.utils as utils

class SivBot(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        await utils.edit_role_on_reaction(self, payload, 'add')

    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
        await utils.edit_role_on_reaction(self, payload, 'remove')

    async def on_member_join(self, member: discord.Member):
        await utils.add_guest_role(member)
