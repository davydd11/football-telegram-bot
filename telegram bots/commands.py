import logging 

logger = logging.getLogger(__name__)


from aiogram.filters import Command
from aiogram.types.bot_command import BotCommand

# /start
START_COMMAND = Command('start')
HELP_COMMAND = Command('help') 
TOP_COMMAND = Command('top')
ADDPLAYER_COMMAND = Command('add_player')
FINDPLAYER_COMMAND = Command('find_player')
    

START_BOT_COMMAND = BotCommand(command='start', description="Start the bot: ")
HELP_BOT_COMMAND = BotCommand(command='help', description="Instructions of the bot: ")
TOP_BOT_COMMAND = BotCommand(command='top', description="Show top 5 players:")
ADDPLAYER_BOT_COMMAND = BotCommand(command='add_player', description="add a player to your list: ")
FINDPLAYER_BOT_COMMAND = BotCommand(command='find_player', description="find the info about the player: ")