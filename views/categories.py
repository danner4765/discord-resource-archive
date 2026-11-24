import discord

from services.resource_loader import get_category
from services.resource_embed import build_resource_embed


class CategoryView(discord.ui.View):

    def __init__(self, qualification, subject, subject_name):
        super().__init__(timeout=180)

        self.qualification = qualification
        self.subject = subject
        self.subject_name = subject_name

    async def show_resources(self, interaction, category):

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

    @discord.ui.button(
        label="Topicals",
        style=discord.ButtonStyle.primary
    )
    async def topicals(self, interaction, button):
        await self.show_resources(interaction, "topicals")

    @discord.ui.button(
        label="Notes",
        style=discord.ButtonStyle.primary
    )
    async def notes(self, interaction, button):
        await self.show_resources(interaction, "notes")

    @discord.ui.button(
        label="YouTubers",
        style=discord.ButtonStyle.primary
    )
    async def youtubers(self, interaction, button):
        await self.show_resources(interaction, "youtubers")

    @discord.ui.button(
        label="Textbooks",
        style=discord.ButtonStyle.primary
    )
    async def textbooks(self, interaction, button):
        await self.show_resources(interaction, "textbooks")

    @discord.ui.button(
        label="Back",
        style=discord.ButtonStyle.secondary,
        row=1
    )
    async def back(self, interaction, button):

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
