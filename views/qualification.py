import discord


class QualificationView(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=180)

    @discord.ui.button(
        label="A Level",
        style=discord.ButtonStyle.primary
    )
    async def alevel(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):
        from views.subjects import SubjectView

        embed = discord.Embed(
            title="A Level Resources",
            description="Select a subject to continue.",
            color=discord.Color.blurple()
        )

        await interaction.response.edit_message(
            embed=embed,
            view=SubjectView()
        )

    @discord.ui.button(
        label="IGCSE",
        style=discord.ButtonStyle.primary
    )
    async def igcse(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):
        await interaction.response.send_message(
            "IGCSE resources are coming soon!",
            ephemeral=True
        )

    @discord.ui.button(
        label="O Level",
        style=discord.ButtonStyle.primary
    )
    async def olevel(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):
        await interaction.response.send_message(
            "O Level resources are coming soon!",
            ephemeral=True
        )
