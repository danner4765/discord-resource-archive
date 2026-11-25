
import discord

from services.resource_loader import get_category
from services.resource_embed import build_resource_embed


CATEGORIES = {
    "Topicals": "topicals",
    "Notes": "notes",
    "YouTubers": "youtubers",
    "Textbooks": "textbooks"
}


class CategoryView(discord.ui.View):

    def __init__(self, qualification, subject, subject_name):
        super().__init__(timeout=180)

        self.qualification = qualification
        self.subject = subject
        self.subject_name = subject_name

        options = [
            discord.SelectOption(
                label=category_name,
                value=category_key
            )
            for category_name, category_key in CATEGORIES.items()
        ]

        select = discord.ui.Select(
            placeholder="Choose a resource category...",
            options=options,
            min_values=1,
            max_values=1
        )

        async def select_callback(interaction):

            category = select.values[0]

            resources = get_category(
                self.qualification,
                self.subject,
                category
            )

            embed = build_resource_embed(
                self.subject_name,
                category,
                resources
            )

            await interaction.response.edit_message(
                embed=embed,
                view=self
            )

        select.callback = select_callback
        self.add_item(select)

        back_button = discord.ui.Button(
            label="Back",
            style=discord.ButtonStyle.secondary
        )

        async def back_callback(interaction):

            from views.subjects import SubjectView

            names = {
                "a_level": "A Level",
                "igcse": "IGCSE",
                "o_level": "O Level"
            }

            qualification_name = names[self.qualification]

            embed = discord.Embed(
                title=f"{qualification_name} Resources",
                description="Select a subject to continue.",
                color=discord.Color.blurple()
            )

            await interaction.response.edit_message(
                embed=embed,
                view=SubjectView(self.qualification)
            )

        back_button.callback = back_callback
        self.add_item(back_button)
