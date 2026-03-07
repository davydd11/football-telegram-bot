import logging 

logger = logging.getLogger(__name__)


from aiogram.fsm.state import State, StatesGroup


class AddPlayer(StatesGroup):

    """
    States used when a user is adding a new player.
    """

    select_name = State()
    select_age = State()
    select_nationality = State()
    select_club = State()
    select_matches = State()
    select_goals = State()
    select_trophys = State()


class FindPlayer(StatesGroup):

    """
    States used when a user is searching for a player.
    """

    select_name = State()
    select_age = State() 
    select_nationality = State()      
    select_club = State()
    select_matches = State()
    select_goals = State()
    select_trophys = State()
