import discord
from discord.ext import commands
import wikipediaapi

# Set up intents.
intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.message_content = True

# Set up the bot with intents. Change '!' if you like any other symbol.
bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online)
    print(f'Logged in as {bot.user.name}')


@bot.command()
async def wiki(ctx, language, *, query):
    try:
        supported_languages = ['en', 'tr']  # Add more languages if needed
        
        if language.lower() not in supported_languages:
            await ctx.send("Unsupported language. Please use 'en' for English or 'tr' for Turkish.")
            return
        
        wiki_wiki = wikipediaapi.Wikipedia(
            language=language.lower(),
            extract_format=wikipediaapi.ExtractFormat.WIKI,
            user_agent='MyDiscordBot/1.0'
        )
        page = wiki_wiki.page(query)
        
        response = f"**{page.title}**\n{page.fullurl}"
        await ctx.send(response)
    except wikipediaapi.exceptions.DisambiguationError as e:
        await ctx.send("Ambiguous query. Please provide more specific search terms.")
    except wikipediaapi.exceptions.PageError as e:
        await ctx.send("No results found for the given query.")

# Run the bot
bot.run('MTE0MDc1NTUwMjMyMjcwMDMwMA.GcLHCz.cfehHln7Z1dbt-jviGsZxqcqfkIinJge1Oi0fg')
