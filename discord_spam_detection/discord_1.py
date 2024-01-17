import discord
from discord.ext import commands
from gpt import GptService

intents = discord.Intents.default()
intents.all()

class AntiSpamBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)

        self.message_counts = {}
        self.gpt_service = GptService()

    async def on_ready(self):
        await self.handle_ready()

    async def handle_ready(self):
        print(f'{self.user.name} Discorda bağlandı!')

    async def on_message(self, message):
        await self.handle_message(message)

    async def handle_message(self, message):
        if message.author == self.user:
            return
        gpt_response = self.gpt_service.ask_gpt(message.content)
        
        

        if self.check_spam(message):
            await message.delete()
            await message.author.kick()
            await message.channel.send(f"{message.author.name} adlı kullanıcı spam içeren mesajlar gönderdiği için şutlandı ;) Şu an güvendesiniz!")


        elif gpt_response.lower() == "olumsuz":
            await message.delete()
            await message.author.kick()
            await message.channel.send(f"{message.author.name} adlı kullanıcı küfür ve hakaret içeren mesajlar gönderdiği için şutlandı ;) Şu an güvendesiniz!")
        else:
            pass
        
    def check_spam(self, message):
        content = message.content.lower()

        if content in self.message_counts:
            self.message_counts[content] += 1
        else:
            self.message_counts[content] = 1

        if self.message_counts[content] == 3:
            return True

        return False
bot = AntiSpamBot()
bot.run("discord_token")
