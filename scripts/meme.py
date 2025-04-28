import requests
from discord.ext import commands

def setup(bot):
    @bot.command()
    async def meme(ctx):
        """Send a random meme from r/memes."""
        url = "https://meme-api.com/gimme/memes"
        response = requests.get(url).json()
        
        await ctx.send(response["url"])