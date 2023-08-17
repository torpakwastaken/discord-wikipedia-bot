A simple Discord bot that fetches data from Wikipedia and sends it into the Discord chat channel with a link.
Only two Python libraries are needed for this. (Not counting hosting)

code pip install discord.py

AND

pip install wikipedia-api

Then create your own bot by going here and creating one. URL: (https://discord.com/developers/applications)
Get your bot token and replace it with:

bot.run('YOUR DISCORD BOT TOKEN')

Voila!

#commands
simply type "!wiki" then a keyword. 

example: "!wiki depp"

"!wiki en depp" will link you the english wikipedia page . "!wiki tr depp" will link you the turkish version. you can add more languages which I have commented on the code itself.

