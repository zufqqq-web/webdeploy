from aiogram.fsm.state import StatesGroup, State

class AdminAddProduct(StatesGroup):
    name = State()
    description = State()
    ingredients = State()
    category = State()
    image = State()
    price_25 = State()
    price_30 = State()
    price_35 = State()

class AdminBroadcast(StatesGroup):
    text = State()
    confirm = State()
