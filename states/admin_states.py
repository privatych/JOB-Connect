from aiogram.fsm.state import StatesGroup, State


class BroadcastState(StatesGroup):
    broadcast_message = State()
    confirm_message = State()