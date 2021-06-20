# Team : QSTI
import discord
import functions as F
import asyncio

# Notes:
# The translator will not activate when the final language is the same as the source langusge
# must use "." before saying something for it to be activated

# Loading glossary
import json
with open("csTermsGlossary.json", "r") as f:
    Glossary = json.load(f)
    f.close()

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith("!destLang "):
        F.destLang = message.content[10:]

        await message.channel.send(
            f"Final language has been set to \"{F.destLang}\"")

    if message.content.startswith("."):
        content = message.content.replace(".", "")
        srcLang = F.detectLang(content)
        if srcLang != F.destLang:
            await message.delete()
            translatedText = F.translate(content, srcLang, F.destLang)
            stringvar = f" Original: {content} \n translated: {translatedText}"
            answer_embed = discord.Embed(color=discord.Color.red(),
                                         description=stringvar)
            answer_embed.set_author(name=message.author.name,
                                    icon_url=message.author.avatar_url)
            await message.channel.send(embed=answer_embed)

    if message.content.startswith("!s"):
        word = message.content[2:]
        term = F.findWord(word, list(Glossary.keys()))
        link = Glossary[term]
        stringvar = f"Term from Glossary: {term} \n {link}"
        answer_embed = discord.Embed(color=discord.Color.red(),
                                     title=word,
                                     description=stringvar)
        await message.channel.send(embed=answer_embed)

    if message.content.startswith("!trivia"):
        emoji_array = ["1️⃣","2️⃣","3️⃣","4️⃣"]
        players_answered = {}
        question = F.getTriviaQuestion()
        question_embed = discord.Embed(color=discord.Color.red(),title="Trivia",description=question[0])
        for a in range(0,4):
          question_embed.add_field(name=emoji_array[a],value=question[1][a])
        sent_msg = await message.channel.send(embed=question_embed)        
        for emoji_num in emoji_array:
          await sent_msg.add_reaction(emoji_num)        
        await asyncio.sleep(15)
        fetched_msg = await message.channel.fetch_message(sent_msg.id)
        for Reaction in fetched_msg.reactions:
          print(Reaction.emoji == "1️⃣")
          async for user in Reaction.users():
            if str(Reaction.emoji) == "1️⃣":
              print(user.id)
              F.giveMoney(str(user.id),100)
        print("done")

            

    if message.content.startswith("!help"):
        bot_purpose = "This discord bot is a bot who brings people closer efficiently from people with various backgrounds.  Users can  communicate with others since this bot can translate to various languages so the other person can understand.  This bot also has trivia questions for the user to learn more about different cultures, games to participate with others, and can learn various computer science words while also having fun with different people"
        help_embed = discord.Embed(color=discord.Color.red(),title="Help",description=bot_purpose)
        help_embed.add_field(name="!destLang [language code]",value="sets the output language")
        help_embed.add_field(name="!s [term]",value="searches for a computer science term, returns a useful link",inline=False)
        help_embed.add_field(name="!trivia",value="play a trivia, earn coins!",inline=False)
        help_embed.add_field(name="!balance",value="checks how much money you have",inline=False)
        await message.channel.send(embed=help_embed)

    if message.content.startswith("!balance"):
        try:
            await message.channel.send(
                f"You have {F.checkBalance(message.author.id)}")
        except KeyError:
            await message.channel.send("You have no credits")


client.run("TOKEN")
