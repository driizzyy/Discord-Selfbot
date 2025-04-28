from discord.ext import commands

def setup(bot):
    @bot.command()
    async def hello(ctx):
        """Say hello to the world."""
        await ctx.send("👋 Hello from Fun Commands!")

    @bot.command()
    async def joke(ctx):
        """Send a random joke."""
        jokes = [
            "Why did the Python programmer go hungry? Because his food was all 'null'!",
            "Debugging: Removing the needles from the haystack.",
            "I would tell you a UDP joke, but you might not get it."
        ]
        await ctx.send(random.choice(jokes))