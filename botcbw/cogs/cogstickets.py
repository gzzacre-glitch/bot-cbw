import discord
from discord.ext import commands
from discord.ui import Button, View

class TicketView(View):
    def __init__(self):
        super().__init__(timeout=None)

    async def criar_canal_ticket(self, interaction: discord.Interaction, tipo_ticket: str, categoria_nome: str):
        guild = interaction.guild
        
        # Procura ou cria a categoria específica para o tipo de ticket
        category = discord.utils.get(guild.categories, name=categoria_nome)
        if not category:
            category = await guild.create_category(categoria_nome)

        # Evita que o usuário crie múltiplos tickets do mesmo tipo ao mesmo tempo
        nome_canal = f"ticket-{tipo_ticket}-{interaction.user.name.lower()}"
        existing_channel = discord.utils.get(guild.text_channels, name=nome_canal)
        if existing_channel:
            await interaction.response.send_message(f"⚠️ Você já possui um ticket aberto nesta categoria: {existing_channel.mention}", ephemeral=True)
            return

        # Configura as permissões (privado para o usuário e staff)
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            interaction.user: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True),
            guild.me: discord.PermissionOverwrite(view_channel=True, send_messages=True)
        }

        # Cria o canal de texto
        channel = await guild.create_text_channel(
            name=nome_canal,
            category=category,
            overwrites=overwrites
        )

        # Mensagem interna do ticket com botão de fechar
        close_view = CloseTicketView()
        
        embed_ticket = discord.Embed(
            title=f"🎫 Ticket de {tipo_ticket.capitalize()} - CB WPS",
            description=f"Olá {interaction.user.mention}!\n\nSeu ticket de **{tipo_ticket}** foi aberto com sucesso. Nossa equipe responsável irá te atender em breve.\n\n*Por favor, envie todas as provas, prints ou detalhes necessários enquanto aguarda.*",
            color=discord.Color.from_rgb(0, 156, 59) # Verde bandeira
        )
        embed_ticket.set_footer(text="Confederação Brasileira de WPS • Sistema de Atendimento")

        await channel.send(embed=embed_ticket, view=close_view)
        await interaction.response.send_message(f"✅ Seu ticket de **{tipo_ticket}** foi criado com sucesso: {channel.mention}", ephemeral=True)

    @discord.ui.button(label="Atendimento", style=discord.ButtonStyle.success, emoji="🎧", custom_id="ticket_atendimento")
    async def btn_atendimento(self, interaction: discord.Interaction, button: Button):
        await self.criar_canal_ticket(interaction, "atendimento", "🎧 ┃ SUPORTE E ATENDIMENTO")

    @discord.ui.button(label="Denúncias", style=discord.ButtonStyle.danger, emoji="🚨", custom_id="ticket_denuncias")
    async def btn_denuncias(self, interaction: discord.Interaction, button: Button):
        await self.criar_canal_ticket(interaction, "denuncia", "🚨 ┃ CANAL DE DENÚNCIAS")

    @discord.ui.button(label="Torneios", style=discord.ButtonStyle.primary, emoji="🏆", custom_id="ticket_torneios")
    async def btn_torneios(self, interaction: discord.Interaction, button: Button):
        await self.criar_canal_ticket(interaction, "torneio", "🏆 ┃ SETOR DE TORNEIOS")

class CloseTicketView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="🔒 Fechar Ticket", style=discord.ButtonStyle.secondary, custom_id="close_ticket")
    async def close_ticket(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_message("🔒 Fechando este canal de atendimento em 5 segundos...")
        await interaction.channel.delete()

class Tickets(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="painelticket", help="Envia o painel oficial de tickets da CB WPS (Apenas Admins)")
    @commands.has_permissions(administrator=True)
    async def painelticket(self, ctx):
        embed = discord.Embed(
            title="🇧🇷 CONFEDERAÇÃO BRASILEIRA DE WPS",
            description=(
                "Precisa de atendimento? Abra um ticket através dos botões abaixo e nossa equipe "
                "irá analisar sua solicitação.\n\n"
                "⚠️ **Antes de abrir um ticket:**\n"
                "Selecione a categoria correta e descreva sua solicitação com o máximo de informações possível."
            ),
            color=discord.Color.from_rgb(255, 223, 0) # Amarelo ouro da bandeira
        )
        
        embed.add_field(
            name="🎧 Atendimento",
            value="Para dúvidas, suporte e assuntos gerais relacionados à Confederação.",
            inline=False
        )
        embed.add_field(
            name="🚨 Denúncias",
            value="Para realizar denúncias ou comunicar situações que precisam ser analisadas pela equipe responsável.",
            inline=False
        )
        embed.add_field(
            name="🏆 Torneios",
            value="Para assuntos relacionados aos torneios, inscrições, organização, partidas e demais questões competitivas.",
            inline=False
        )
        
        embed.set_footer(text="Confederação Brasileira de WPS • Todos os direitos reservados")
        
        await ctx.send(embed=embed, view=TicketView())

async def setup(bot):
    await bot.add_cog(Tickets(bot))