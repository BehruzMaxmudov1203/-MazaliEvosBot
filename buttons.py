from aiogram import types

foods = {
    "lavash": 30000,
    "chips": 10000,
    "kola": 8000,
    "tooster": 29000,
    "xotdog": 25000
}



def create_phone_send_button():
    kbs = [
        [types.KeyboardButton(
            text="Telefon raqamni yuborish", request_contact=True)
        ]
    ]
    return types.ReplyKeyboardMarkup(keyboard=kbs, resize_keyboard=True)


def create_location_send_button():
    kbs = [
        [types.KeyboardButton(
            text="Jo'ylashuvingizni yuboring", request_location=True)
        ]
    ]
    return types.ReplyKeyboardMarkup(keyboard=kbs, resize_keyboard=True)


def create_food_menyu():
    kbs_copy = []
    row = []
    count_elements = len(foods.keys())
    i = 0
    for food, price in foods.items():
        row.append(types.InlineKeyboardButton(text=f"{food} {price} UZS", callback_data=food))
        if len(row) == 2 or i == count_elements - 1:
            kbs_copy.append(row)
            row = []
        i += 1
    kbs_copy.append([types.InlineKeyboardButton(text="Davom ettirish", callback_data="stop_purchase")])
    return types.InlineKeyboardMarkup(inline_keyboard=kbs_copy)



def create_order_button(total_amount):
    kbs = [
        [types.InlineKeyboardButton(text=f"To'lash ({total_amount})", url="https://my.click.uz/services/pay/96E4C0E8F56A4CFD905F014916E5115D")],
    ]
    return types.InlineKeyboardMarkup(inline_keyboard=kbs)
