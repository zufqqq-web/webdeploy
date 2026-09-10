from aiogram.fsm.state import StatesGroup, State

class OrderStates(StatesGroup):
    name = State()
    phone = State()
    address = State()
    comment = State()
