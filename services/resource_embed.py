import discord


def build_resource_embed(subject, category, resources):

    embed = discord.Embed(
        title=f"{subject} — {category.title()}",
        color=discord.Color.blurple()
    )

    if not resources:
        embed.description = "No resources have been added yet."

    else:
        resource_list = []

        for resource in resources:
            name = resource["name"]
            url = resource["url"]

            resource_list.append(f"• [{name}]({url})")

        embed.description = "\n\n".join(resource_list)

    return embed
