import discord
from discord.ext import commands

DONO_VENDAS_ID = 848956596092796968

# Links das imagens dos produtos (Substitua pelos seus links do Imgur/Imgbb)
URL_IMAGEM_ESMERALDA = "https://i.imgur.com/iJUOnFG.png"
URL_IMAGEM_CARD = "https://i.imgur.com/Rhna2qs.png"
URL_IMAGEM_IMPULSO = "https://i.imgur.com/08CmKaU.png"
URL_IMAGEM_DIAMANTE = "https://i.imgur.com/TB54QtJ.png"

# Controle de Estoque (30 de cada)
ESTOQUE = {
    "Sócio Esmeralda (60 Dias)": {"preco": "R$ 14,50", "qtd": 30},
    "Sócio Esmeralda (90 Dias)": {"preco": "R$ 19,50", "qtd": 30},
    "Sócio Esmeralda (120 Dias)": {"preco": "R$ 27,00", "qtd": 30},
    "Card WPS": {"preco": "R$ 3,50", "qtd": 30},
    "Sócio Diamante (60 Dias)": {"preco": "R$ 22,80", "qtd": 30},
    "Sócio Diamante (90 Dias)": {"preco": "R$ 29,50", "qtd": 30},
    "Sócio Diamante (120 Dias)": {"preco": "R$ 44,50", "qtd": 30},
}

class SelectProdutos(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Sócio Esmeralda - 60 Dias", value="Sócio Esmeralda (60 Dias)", description="R$ 14,50 | Benefícios Esmeralda"),
            discord.SelectOption(label="Sócio Esmeralda - 90 Dias", value="Sócio Esmeralda (90 Dias)", description="R$ 19,50 | Benefícios Esmeralda"),
            discord.SelectOption(label="Sócio Esmeralda - 120 Dias", value="Sócio Esmeralda (120 Dias)", description="R$ 27,00 | Benefícios Esmeralda"),
            discord.SelectOption(label="Card WPS", value="Card WPS", description="R$ 3,50 | Card na comunidade"),
            discord.SelectOption(label="Sócio Diamante - 60 Dias", value="Sócio Diamante (60 Dias)", description="R$ 22,80 | Benefícios Máximos"),
            discord.SelectOption(label="Sócio Diamante - 90 Dias", value="Sócio Diamante (90 Dias)", description="R$ 29,50 | Benefícios Máximos"),
            discord.SelectOption(label="Sócio Diamante - 120 Dias", value="Sócio Diamante (120 Dias)", description="R$ 44,50 | Benefícios Máximos"),
        ]
        super().__init__(placeholder="🛒 Selecione o produto que deseja comprar...", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        produto_nome = self.values[0]
        produto_info = ESTOQUE.get(produto_nome)

        if produto_info["qtd"] <= 0:
            return await interaction.response.send_message("❌ Desculpe, este produto está esgotado!", ephemeral=True)

        ESTOQUE[produto_nome]["qtd"] -= 1

        guild = interaction.guild
        categoria = discord.utils.get(guild.categories, name="Tickets Compra")
        
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            interaction.user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
        }

        canal_ticket = await guild.create_text_channel(
            name=f"compra-{interaction.user.name}",
            category=categoria,
            overwrites=overwrites
        )

        embed_ticket = discord.Embed(
            title="🛍️ Pedido de Compra Solicitado",
            description=f"Olá {interaction.user.mention}!\n\n"
                        f"**Produto Escolhido:** {produto_nome}\n"
                        f"**Valor:** `{produto_info['preco']}`\n\n"
                        f"Aguarde o responsável <@{DONO_VENDAS_ID}> responder para finalizar o pagamento e aprovar seu produto.",
            color=discord.Color.green()
        )
        embed_ticket.set_footer(text="Comunidade Brasileira de WPS - Sistema de Vendas")

        await canal_ticket.send(content=f"{interaction.user.mention} | <@{DONO_VENDAS_ID}>", embed=embed_ticket)
        await interaction.response.send_message(f"✅ Seu ticket de compra foi gerado em {canal_ticket.mention}!", ephemeral=True)

class ViewLoja(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(SelectProdutos())

class LojaCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="enviarloja")
    @commands.has_permissions(administrator=True)
    async def enviar_loja(self, ctx):
        await ctx.message.delete()

        # Embed 1: Sócio Esmeralda
        embed_esmeralda = discord.Embed(
            title="💚 VIP ESMERALDA",
            description="🚨 **Atenção:** todos valores são usados na melhoria do servidor para realização dos campeonatos.\n\n"
                        "Compras somente com: <@848956596092796968>\n\n"
                        "**Benefícios**\n"
                        "• 🏆 Acesso antecipado em pré-campeonatos\n"
                        "• 🔄 Inscrever 2 jogadores 50%off fora da janela de transferência por campeonato\n"
                        "• ⭐️ Cargo exclusivo personalizado\n"
                        "• 🏷️ Troca de apelido\n"
                        "• 📹 Enviar foto/vídeo no chat\n\n"
                        "**Validade e Valores**\n"
                        f"• 60 dias por: R$ 14,50 `(Estoque: {ESTOQUE['Sócio Esmeralda (60 Dias)']['qtd']}/30)`\n"
                        f"• 90 dias por: R$ 19,50 `(Estoque: {ESTOQUE['Sócio Esmeralda (90 Dias)']['qtd']}/30)`\n"
                        f"• 120 dias por: R$ 27,00 `(Estoque: {ESTOQUE['Sócio Esmeralda (120 Dias)']['qtd']}/30)`\n\n"
                        "Compras somente com: <@848956596092796968>",
            color=discord.Color.green()
        )
        embed_esmeralda.set_thumbnail(url=URL_IMAGEM_ESMERALDA)

        # Embed 2: Card WPS
        embed_card = discord.Embed(
            title="🃏 CARD WPS",
            description="🚨 **Atenção:** todos valores são usados na melhoria do servidor para realização dos campeonatos.\n\n"
                        "Compras somente com: <@848956596092796968>\n\n"
                        "> **Adicione sua Card do WPS na Comunidade Brasileira de WPS**\n"
                        "Sempre que digitar `+seunickname` sua card será exibida para a comunidade inteira.\n\n"
                        f"**Valor Único:** R$ 3,50 `(Estoque: {ESTOQUE['Card WPS']['qtd']}/30)`\n\n"
                        "Compras somente com: <@848956596092796968>",
            color=discord.Color.blue()
        )
        embed_card.set_thumbnail(url=URL_IMAGEM_CARD)

        # Embed 3: Impulso
        embed_impulso = discord.Embed(
            title="🚀 IMPULSO DO SERVIDOR",
            description="🚀 Impulsione o servidor da Comunidade Brasileira de WPS\n\n"
                        "**Benefícios**\n"
                        "• 🃏 Card WPS no servidor com comando 50%off\n"
                        "• 🔄 Inscrever jogadores 20%off fora da janela de transferência\n"
                        "• 📹 Enviar foto/vídeo no chat\n"
                        "• 🎟️ Participar de sorteios exclusivos\n\n"
                        "**Validade:** Duração do impulso\n\n"
                        "🚀 Impulsione o servidor",
            color=discord.Color.purple()
        )
        embed_impulso.set_thumbnail(url=URL_IMAGEM_IMPULSO)

        # Embed 4: Sócio Diamante
        embed_diamante = discord.Embed(
            title="💎 VIP DIAMANTE",
            description="🚨 **Atenção:** todos valores são usados na melhoria do servidor para realização dos campeonatos.\n\n"
                        "Compras somente com: <@848956596092796968>\n\n"
                        "**Benefícios**\n"
                        "• 💚 Todos benefícios do VIP Esmeralda\n"
                        "• 🏆 Acesso antecipado em todos campeonatos\n"
                        "• 🔄 Inscrever jogadores 100%off fora da janela de transferência\n"
                        "• 📢 Divulgar link com Everyone\n"
                        "• 🎧 Call personalizada para seu clube\n"
                        "• 🎟️ Participar de sorteios exclusivos\n"
                        "• 💬 Grupo com os Donos e Moderadores\n"
                        "• 👾 Figurinha jogador com uniforme personalizado do seu clube\n\n"
                        "**Validade e Valores**\n"
                        f"• 60 dias por: R$ 22,80 `(Estoque: {ESTOQUE['Sócio Diamante (60 Dias)']['qtd']}/30)`\n"
                        f"• 90 dias por: R$ 29,50 `(Estoque: {ESTOQUE['Sócio Diamante (90 Dias)']['qtd']}/30)`\n"
                        f"• 120 dias por: R$ 44,50 `(Estoque: {ESTOQUE['Sócio Diamante (120 Dias)']['qtd']}/30)`\n\n"
                        "Compras somente com: <@848956596092796968>",
            color=discord.Color.dark_purple()
        )
        embed_diamante.set_thumbnail(url=URL_IMAGEM_DIAMANTE)

        await ctx.send(embed=embed_esmeralda)
        await ctx.send(embed=embed_card)
        await ctx.send(embed=embed_impulso)
        await ctx.send(embed=embed_diamante, view=ViewLoja())

async def setup(bot):
    await bot.add_cog(LojaCog(bot))
