import os
import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Carrega variáveis de ambiente se houver arquivo .env
load_dotenv()

# Configuração de Intents do Discord
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"🤖 Bot {bot.user.name} conectado com sucesso ao Discord!")
    print("--------------------------------------------------")

async def load_extensions():
    # Carrega as cogs existentes do seu projeto
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            try:
                await bot.load_extension(f"cogs.{filename[:-3]}")
                print(f"✅ Cog '{filename}' carregada com sucesso.")
            except Exception as e:
                print(f"❌ Erro ao carregar cog '{filename}': {e}")

async def main():
    async with bot:
        await load_extensions()
        # Lê o token da variável de ambiente DISCORD_TOKEN
        token = os.getenv("DISCORD_TOKEN")
        if not token:
            print("❌ ERRO: A variável DISCORD_TOKEN não foi configurada!")
            return
        await bot.start(token)

if __name__ == "__main__":
    asyncio.run(main())