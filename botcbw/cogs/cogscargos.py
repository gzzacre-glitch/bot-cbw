import discord
from discord.ext import commands

class Cargos(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="setar", help="Atribui um cargo a um membro. Ex: !setar @usuario @cargo")
    @commands.has_permissions(manage_roles=True)
    async def setar(self, ctx, membro: discord.Member, cargo: discord.Role):
        # Verifica se o bot tem hierarquia superior ao cargo que quer dar
        if ctx.guild.me.top_role <= cargo:
            await ctx.send("❌ Eu não posso atribuir este cargo, pois ele está acima ou no mesmo nível do meu cargo mais alto.")
            return

        try:
            await membro.add_roles(cargo)
            embed = discord.Embed(
                title="✅ Cargo Atribuído com Sucesso!",
                description=f"O membro {membro.mention} recebeu o cargo {cargo.mention}.",
                color=discord.Color.green()
            )
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(f"❌ Ocorreu um erro ao tentar setar o cargo: {e}")

    @setar.error
    async def setar_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("❌ Você não tem permissão para usar este comando (requer 'Gerenciar Cargos').")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("❌ Uso incorreto! Forma correta: `!setar @Membro @Cargo`")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("❌ Não consegui encontrar o membro ou o cargo especificado. Certifique-se de marcá-los corretamente.")

async def setup(bot):
    await bot.add_cog(Cargos(bot))