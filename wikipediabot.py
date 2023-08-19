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
async def wiki(ctx, *, query):
    try:
        if query.startswith("tr "):  # Check if the query starts with 'tr '
            response = "Özür dilerim. Hiçbir sonuç bulunamadı."
            await ctx.send(response)
        else:
            language = 'en'  # Default language is English
            supported_languages = ['en', 'tr']  # Add more languages if needed.

            if query.startswith("en:") or query.startswith("tr:"):
                lang_code, query = query.split(":", 1)
                if lang_code.lower() in supported_languages:
                    language = lang_code.lower()
                else:
                    await ctx.send("Unsupported language. Please use 'en' for English or 'tr' for Turkish.")
                    return

            wiki_wiki = wikipediaapi.Wikipedia(
                language=language,
                extract_format=wikipediaapi.ExtractFormat.WIKI,
                user_agent='MyDiscordBot/1.0'
            )
            page = wiki_wiki.page(query)

            if not page.exists():
                await ctx.send("No results found for the given query.")
                return

            response = f"**{page.title}**\n{page.fullurl}"
            await ctx.send(response)
    except wikipediaapi.DisambiguationError as e:
        await ctx.send("Ambiguous query. Please provide more specific search terms.")
    except Exception as e:
        await ctx.send("An error occurred while processing your request.")

# Run the bot
bot.run('token')
