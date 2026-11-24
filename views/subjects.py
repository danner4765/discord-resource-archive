import discord

from views.categories import CategoryView


class SubjectView(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=180)

    @discord.ui.button(
        label="Further Mathematics",
        style=discord.ButtonStyle.primary
    )
    async def further_maths(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):
        embed = discord.Embed(
            title="Further Mathematics Resources",
            description="Select a resource category.",
            color=discord.Color.blurple()
        )

        await interaction.response.edit_message(
            embed=embed,
            view=CategoryView(
                "a_level",
                "further_maths",
                "Further Mathematics"
            )
        )

    @discord.ui.button(
        label="Physics",
        style=discord.ButtonStyle.primary
    )
    async def physics(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):
        embed = discord.Embed(
            title="Physics Resources",
            description="Select a resource category.",
            color=discord.Color.blurple()
        )

        await interaction.response.edit_message(
            embed=embed,
            view=CategoryView(
                "a_level",
                "physics",
                "Physics"
            )
        )

    @discord.ui.button(
        label="Back",
        style=discord.ButtonStyle.secondary,
        row=1
    )
    async def back(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):
        from views.qualification import QualificationView

        embed = discord.Embed(
            title="Resource Archive",
            description="Select your qualification.",
            color=discord.Color.blurple()
        )

        await interaction.response.edit_message(
            embed=embed,
            view=QualificationView()
        )
