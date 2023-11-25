import os
import discord
from discord.ext import commands
import wikipediaapi

COMMAND_PREFIX = '!'
DEFAULT_LANGUAGE = 'en'

# Set up intents
intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.message_content = True

# Set up the bot with intents
bot = commands.Bot(command_prefix=COMMAND_PREFIX, intents=intents)


@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online)
    print(f'Logged in as {bot.user.name}')


@bot.command()
async def wiki(ctx, *, query):
    language_prefixes = {
        'en': 'en ',
        'tr': 'tr ',
        'fr': 'fr ',
        'es': 'es ',
        'de': 'de ',
        'it': 'it ',
        'pt': 'pt ',
        'ja': 'ja ',
        'ko': 'ko ',
        'ru': 'ru ',
        'ar': 'ar ',
    }

    # Checking if the user specified a different language
    language = DEFAULT_LANGUAGE
    for lang, prefix in language_prefixes.items():
        if query.startswith(prefix):
            language = lang
            query = query[len(prefix):]
            break

    try:
        supported_languages = list(language_prefixes.keys())

        if language not in supported_languages:
            await ctx.send(
                f"Unsupported language. Please use one of the following language codes: {', '.join(supported_languages)}."
            )
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

    except wikipediaapi.exceptions.DisambiguationError:
        await ctx.send("Ambiguous query. Please provide more specific search terms.")

    except wikipediaapi.exceptions.HTTPTimeoutError:
        await ctx.send("Wikipedia API request timed out. Please try again later.")

    except wikipediaapi.exceptions.WikipediaException as e:
        await ctx.send(f"An error occurred: {e}")


@bot.command(name='bot_help')
async def help(ctx):
    # Define the help message
    help_message = (
        "-----Welcome to the Wikipedia Bot!\n"
        "-You can use the following commands:\n"
        f"-{COMMAND_PREFIX}wiki [language] [query]: Look up a Wikipedia article. Default language is English ({DEFAULT_LANGUAGE}).\n"
        f"-{COMMAND_PREFIX}bot_help: Show this help message.\n\n"
        "-----Example usages:\n"
        f"-{COMMAND_PREFIX}wiki atatürk: Search for 'atatürk' in English Wikipedia.\n"
        f"-{COMMAND_PREFIX}wiki tr atatürk: Search for 'atatürk' in Turkish Wikipedia.\n"
        "-Created by Torpak.\n"
    )

    await ctx.send(help_message)


@bot.command()
async def report(ctx):
    survey_link = "https://forms.gle/LMQ6oARWknk9DXWj9"
    await ctx.send(f"Please take a moment to fill out our bug - error survey: {survey_link}")


# Run the bot
bot.run(os.environ["DISCORD_TOKEN"])
