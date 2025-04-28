from discord.ext import commands

def setup(bot):
    @bot.command()
    async def changestatus(ctx, *, status: str = "online"):
        """Change bot's status."""
        await bot.change_presence(activity=discord.Game(name=status))
        await ctx.send(f"> ✅ Status changed to `{status}`")