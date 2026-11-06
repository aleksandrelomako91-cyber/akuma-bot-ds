import discord
from discord.ext import commands
from discord.ui import Button, View

# 1. НАСТРОЙКА БОТА И ПРАВ (ИНТЕНТОВ)
intents = discord.Intents.default()
intents.message_content = True  # Чтобы бот читал команду !тикетменю
intents.guilds = True           # Чтобы бот мог создавать каналы тикетов

bot = commands.Bot(command_prefix="!", intents=intents)

# Счётчик тикетов (начнётся с 001)
ticket_counter = 1

# 2. КНОПКА ЗАКРЫТИЯ ТИКЕТА (внутри созданного канала)
class CloseTicketView(View):
    def __init__(self):
        super().__init__(timeout=None)  # Кнопка работает вечно

    @discord.ui.button(label="Закрыть тикет 🔒", style=discord.ButtonStyle.danger, custom_id="close_ticket")
    async def close_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Этот тикет закроется через 5 секунд...", ephemeral=True)
        # Удаляем текстовый канал тикета
        await interaction.channel.delete()

# 3. ОКНО ДОБРО ПОЖАЛОВАТЬ И КНОПКА СОЗДАНИЯ ТИКЕТА
class TicketMenuView(View):
    def __init__(self):
        super().__init__(timeout=None)  # Кнопка работает вечно

    @discord.ui.button(label="Создать тикет 📩", style=discord.ButtonStyle.success, custom_id="create_ticket")
    async def create_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        global ticket_counter
        guild = interaction.guild
        
        # Делаем красивый номер: 001, 002 и т.д.
        ticket_number = str(ticket_counter).zfill(3)
        channel_name = f"тикет-{ticket_number}"
        
        # Настройка прав: обычные юзеры канал не видят, создатель и бот — видят
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            interaction.user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }
        
        # Создаем канал тикета
        ticket_channel = await guild.create_text_channel(name=channel_name, overwrites=overwrites)
        ticket_counter += 1
        
        # Сообщение внутри созданного тикета
        embed = discord.Embed(
            title=f"Тикет №{ticket_number}",
            description=f"Привет, {interaction.user.mention}! Опиши свою проблему здесь. Администрация скоро ответит тебе.\n\nЧтобы закрыть обращение, нажмите кнопку ниже.",
            color=discord.Color.blue()
        )
        await ticket_channel.send(embed=embed, view=CloseTicketView())
        
        # Невидимый ответ пользователю, нажавшему кнопку
        await interaction.response.send_message(f"Тикет успешно создан! Перейдите в канал: {ticket_channel.mention}", ephemeral=True)

# 4. ЗАПУСК БОТА
@bot.event
async def on_ready():
    print(f"Бот {bot.user.name} успешно запущен!")
    # Регистрируем кнопки в памяти бота, чтобы они работали после перезапусков
    bot.add_view(TicketMenuView())
    bot.add_view(CloseTicketView())

# 5. КОМАНДА ДЛЯ СОЗДАНИЯ ОКНА ПРИВЕТСТВИЯ
@bot.command()
@commands.has_permissions(administrator=True)
async def тикетменю(ctx):
    embed = discord.Embed(
        title="🎫 Поддержка / Обращения",
        description="Добро пожаловать! Если вам нужно связаться с администрацией или у вас возникли вопросы, нажмите на кнопку ниже, чтобы создать приватный тикет.",
        color=discord.Color.green()
    )
    # Отправляем меню СТРОГО в тот канал, где написали команду
    await ctx.send(embed=embed, view=TicketMenuView())
    # Удаляем сообщение "!тикетменю" от админа для красоты
    await ctx.message.delete()

# =======================================================
# ВСТАВЬ СВОЙ СЕКРЕТНЫЙ ТОКЕН ВМЕСТО ТОЧЕК НИЖЕ
# =======================================================
import os
from keep_alive import keep_alive

# ... весь остальной ваш код бота выше ...

keep_alive()
bot.run(os.environ.get('TOKEN'))
  # 2. Затем запускаем бота, беря токен из настроек сервера

