import discord


class QualificationView(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=180)

    async def select_qualification(self, interaction, qualification, name):

        from views.subjects import SubjectView

        embed = discord.Embed(
            title=f"{name} Resources",
            description="Select a subject to continue.",
            color=discord.Color.blurple()
        )

        await interaction.response.edit_message(
            embed=embed,
            view=SubjectView(qualification)
        )

    @discord.ui.button(
        label="A Level",
        style=discord.ButtonStyle.primary
    )
    async def alevel(self, interaction, button):
        await self.select_qualification(
            interaction, "a_level", "A Level"
        )

    @discord.ui.button(
        label="IGCSE",
        style=discord.ButtonStyle.primary
    )
    async def igcse(self, interaction, button):
        await self.select_qualification(
            interaction, "igcse", "IGCSE"
        )

    @discord.ui.button(
        label="O Level",
        style=discord.ButtonStyle.primary
    )
    async def olevel(self, interaction, button):
        await self.select_qualification(
            interaction, "o_level", "O Level"
        )
