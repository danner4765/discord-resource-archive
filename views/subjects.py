
import discord

from views.categories import CategoryView


SUBJECTS = {
    "a_level": {
        "Mathematics": "mathematics",
        "Further Mathematics": "further_maths",
        "Physics": "physics",
        "Chemistry": "chemistry",
        "Biology": "biology",
        "Computer Science": "computer_science"
    },

    "igcse": {
        "Mathematics": "mathematics",
        "Additional Mathematics": "additional_maths",
        "Physics": "physics",
        "Chemistry": "chemistry",
        "Biology": "biology",
        "Computer Science": "computer_science",
        "English": "english",
        "Urdu": "urdu",
        "Pak Studies": "pak_studies",
        "Islamiat": "islamiat"
    },

    "o_level": {
        "Mathematics": "mathematics",
        "Additional Mathematics": "additional_maths",
        "Physics": "physics",
        "Chemistry": "chemistry",
        "Biology": "biology",
        "Computer Science": "computer_science",
        "English": "english",
        "Urdu": "urdu",
        "Pak Studies": "pak_studies",
        "Islamiat": "islamiat"
    }
}


class SubjectView(discord.ui.View):

    def __init__(self, qualification):
        super().__init__(timeout=180)

        self.qualification = qualification

        options = [
            discord.SelectOption(
                label=subject_name,
                value=subject_key
            )
            for subject_name, subject_key
            in SUBJECTS[qualification].items()
        ]

        select = discord.ui.Select(
            placeholder="Choose a subject...",
            options=options,
            min_values=1,
            max_values=1
        )

        async def select_callback(interaction):

            subject_key = select.values[0]

            subject_name = next(
                name
                for name, key in SUBJECTS[qualification].items()
                if key == subject_key
            )

            embed = discord.Embed(
                title=f"{subject_name} Resources",
                description="Select a resource category.",
                color=discord.Color.blurple()
            )

            await interaction.response.edit_message(
                embed=embed,
                view=CategoryView(
                    qualification,
                    subject_key,
                    subject_name
                )
            )

        select.callback = select_callback
        self.add_item(select)

        back_button = discord.ui.Button(
            label="Back",
            style=discord.ButtonStyle.secondary
        )

        async def back_callback(interaction):

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

        back_button.callback = back_callback
        self.add_item(back_button)

