import requests
import re
from discord.ext import commands

token = open("token.txt").read() # w folderze obok kodu jest zapisany w pliku .txt unikalny token bota, który pozwala na jego aktywowanie i przypisanie do odpowiednich serwerów
bot = commands.Bot(command_prefix='$')


@bot.event
async def on_ready():
    print("gotowe")


@bot.command()
async def przelicz(ctx, _s):
    inputs = _s.split(':')

    try:
        main_input = inputs[0]
        target_currency = inputs[1].upper()
    except IndexError:
        await ctx.send("Nie używaj znaku spacji przy wprowadzaniu danych")
        return

    try:
        base_currency = re.findall(r'\D+', main_input)[0].upper()
    except IndexError:
        await ctx.send("Niepoprawne dane wejściowe")
        return

    try:
        amount = float(re.findall(r'\d+', main_input)[0])
    except IndexError:
        amount = 1

    parameters = {
        "base": base_currency
    }

    exchange_rate_p = requests.get("https://api.exchangeratesapi.io/latest", params=parameters)

    try:
        for key, val in exchange_rate_p.json()["rates"].items():
            if key == target_currency:
                await ctx.send("{} {} - {} {}".format(amount, base_currency, round(amount * val, 2), key))
    except KeyError:
        await ctx.send("Niepoprawne dane wejściowe")


bot.run(token)
