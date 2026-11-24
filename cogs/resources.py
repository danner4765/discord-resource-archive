import discord
from discord.ext import commands

from views.qualification import QualificationView


class Resources(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def resources(self, ctx):

        embed = discord.Embed(
            title="Resource Archive",
            description=(
                "Welcome! Select your qualification "
                "to browse available resources.\n\n"
                " "
            ),
            color=discord.Color.blurple()
        )

        view = QualificationView()

        await ctx.send(
            embed=embed,
            view=view
        )


async def setup(bot):
    await bot.add_cog(Resources(bot))
