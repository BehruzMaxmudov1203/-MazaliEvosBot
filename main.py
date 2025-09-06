from aiogram import Dispatcher, types, Bot, F
from aiogram.filters.command import Command
import asyncio
from dotenv import load_dotenv
import os
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from buttons import create_phone_send_button, create_location_send_button, create_food_menyu, foods

DELIVERY_AMOUNT = 5000
DISCOUNT = 0
ADMIN_ID = 385419373
load_dotenv()
TOKEN = os.getenv('TOKEN')
bot = Bot(token=TOKEN)
dp = Dispatcher()


class EvosBotState(StatesGroup):
    full_name = State()
    phone_number = State()
    location = State()
    food_counts = State()  # ['lavash', 'Chips', 'tooster']
    approval = State()


@dp.message(Command("start"))
async def message_handler(message: types.Message):
    kbs = [
        [types.KeyboardButton(text='/delivery')]
    ]
    reply_markub = types.ReplyKeyboardMarkup(keyboard=kbs, resize_keyboard=True)

    await message.answer(
        text="Assalomu aleykum, Evos botiga xush kelibsiz Buyurtma berish uchun /delivery  tugmasini bosing!",
        reply_markup=reply_markub

    )


@dp.message(F.text == '/delivery')
async def start_register(message: types.Message, state: FSMContext):
    await message.answer(text="Buyurtma berish boshlandi ismingizni kiriting:")
    await state.set_state(EvosBotState.full_name)


@dp.message(EvosBotState.full_name)
async def save_full_nme(message: types.Message, state: FSMContext):
    full_name = message.text
    await state.update_data(full_name=full_name)
    await message.answer('Telefon raqamingizni yuboring (yuborish tugmani bosing)',
                         reply_markup=create_phone_send_button())
    await state.set_state(EvosBotState.phone_number)


@dp.message(EvosBotState.phone_number)
async def save_phone_number(message: types.Message, state: FSMContext):
    phone_number = message.contact.phone_number
    await state.update_data(phone_number=phone_number)
    await message.answer("Jo'ylashuv ma'lumotlaringizni yuboring (yuborish tugmani bosing)",
                         reply_markup=create_location_send_button())
    await state.set_state(EvosBotState.location)


@dp.message(EvosBotState.location)
async def save_location(message: types.Message, state: FSMContext):
    location = (message.location.latitude, message.location.longitude)
    await state.update_data(location=location)
    await message.answer("Ma'lumotlar saqlandi menyudan taom tanlang: ",
                         reply_markup=create_food_menyu())
    await state.set_state(EvosBotState.food_counts)


@dp.callback_query(EvosBotState.food_counts)
async def callback_button_food(callback: types.CallbackQuery, state: FSMContext):
    food = callback.data
    state_data = await state.get_data()
    if food == 'stop_purchase':
        await state.set_state(EvosBotState.approval)
        return await callback.message.answer(text=create_check(state_data))

    foods_count = state_data.get('food_counts')
    if not foods_count:
        foods_count = [food]
    else:
        foods_count.append(food)
    await state.update_data(food_counts=foods_count)
    text = "Tanlangan ovqatlar: \n"


    for food_count in set(foods_count):
       text += f"\n{food_count} * {foods_count.count(food_count)}"

    await callback.message.edit_text(text=text, reply_markup=create_food_menyu())


def create_check(data):
    full_name = data.get('full_name')
    food_counts = data.get('food_counts')

    amount = 0
    food_calcullate_text = ""

    # Taomlarni tartib bilan chiqarish
    for idx, food in enumerate(set(food_counts), start=1):
        count = food_counts.count(food)
        total = foods[food] * count
        amount += total
        food_calcullate_text += f"{idx}. {food.capitalize()} × {count}  ➝  {total:,} UZS\n"

    calculated_amount = amount + DELIVERY_AMOUNT - DISCOUNT

    order_info = f"""
━━━━━━━━━━━━━━━━━━
        🧾 <b>EVOS CHECK</b>  
━━━━━━━━━━━━━━━━━━
📌 Buyurtma ID: <code>#{1234}</code>
👤 Mijoz: <b>{full_name}</b>
📍 Manzil: <i>123 Main Street, Tashkent</i>

🍽️ <b>Buyurtma qilgan taomlaringiz:</b>
{food_calcullate_text}
━━━━━━━━━━━━━━━━━━
🛒 Umumiy summa:   {amount:,} UZS
🚚 Yetkazish:      {DELIVERY_AMOUNT:,} UZS
💸 Chegirma:       {DISCOUNT:,} UZS
━━━━━━━━━━━━━━━━━━
💰 <b>YAKUNIY TO‘LOV:</b> {calculated_amount:,} UZS
━━━━━━━━━━━━━━━━━━
✅ Buyurtmangiz qabul qilindi!
Tez orada yetkazib beramiz 🚀
"""
    return order_info



async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
