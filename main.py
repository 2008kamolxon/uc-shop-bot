import asyncio
import sqlite3
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession

BOT_TOKEN = "8587124620:AAEHFuLfW9ShQyiixnhNBPhdqXBhchO_fDs"

# ТАЛАБ БЎЙИЧА АДМИНЛАР БОШҚАРУВИ:
SUPER_ADMIN_ID = 855685628  # Муҳаммадкамол (Барча ҳуқуқлар: /stats, /send, тасдиқлаш)
SECOND_ADMIN_ID = 8712932427  # Иккинчи админнинг ID'си (Фақат чекларни тасдиқлаш/бекор қилиш)

# Чек юбориладиган барча админлар
ALL_ADMIN_IDS = [SUPER_ADMIN_ID, SECOND_ADMIN_ID]

CARD_NUMBER = "5614 6835 1555 4699"
CARD_HOLDER = "Ilyos Kabulov"
    default=DefaultBotProperties(parse_mode="HTML")
)
dp = Dispatcher(storage=MemoryStorage())

# --- БАЗА БИЛАН ИШЛАШ ---
conn = sqlite3.connect("shop_database.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    username TEXT,
    full_name TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS orders (
    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    uc_amount TEXT,
    price TEXT,
    player_id TEXT,
    status TEXT
)
''')
conn.commit()

# --- FSM ҲОЛАТЛАРИ ---
class OrderState(StatesGroup):
    waiting_for_id = State()
    waiting_for_receipt = State()

class BroadcastState(StatesGroup):
    waiting_for_message = State()

# --- ТУГМАЛАР ---
main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="💎 UC Харид қилиш")],
        [KeyboardButton(text="📦 Менинг буюртмаларим"), KeyboardButton(text="📞 Қўллаб-қувватлаш")]
    ],
    resize_keyboard=True
)

uc_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="💎 60 UC — 13,000 сўм", callback_data="buy_60_13000")],
        [InlineKeyboardButton(text="💎 120 UC — 26,000 сўм", callback_data="buy_120_26000")],
        [InlineKeyboardButton(text="💎 180 UC — 39,000 сўм", callback_data="buy_180_39000")],
        [InlineKeyboardButton(text="💎 325 UC — 58,000 сўм", callback_data="buy_325_58000")],
        [InlineKeyboardButton(text="💎 385 UC — 71,000 сўм", callback_data="buy_385_71000")],
        [InlineKeyboardButton(text="💎 445 UC — 85,000 сўм", callback_data="buy_445_85000")],
        [InlineKeyboardButton(text="💎 660 UC — 117,000 сўм", callback_data="buy_660_117000")],
        [InlineKeyboardButton(text="💎 720 UC — 127,000 сўм", callback_data="buy_720_127000")],
        [InlineKeyboardButton(text="💎 985 UC — 177,000 сўм", callback_data="buy_985_177000")],
        [InlineKeyboardButton(text="💎 1320 UC — 245,000 сўм", callback_data="buy_1320_245000")],
        [InlineKeyboardButton(text="💎 1800 UC — 295,000 сўм", callback_data="buy_1800_295000")],
        [InlineKeyboardButton(text="💎 1920 UC — 325,000 сўм", callback_data="buy_1920_325000")],
        [InlineKeyboardButton(text="💎 2125 UC — 365,000 сўм", callback_data="buy_2125_365000")],
        [InlineKeyboardButton(text="💎 2460 UC — 405,000 сўм", callback_data="buy_2460_405000")],
        [InlineKeyboardButton(text="💎 2785 UC — 475,000 сўм", callback_data="buy_2785_475000")],  
        [InlineKeyboardButton(text="💎 3850 UC — 575,000 сўм", callback_data="buy_3850_575000")],
        [InlineKeyboardButton(text="💎 4175 UC — 655,000 сўм", callback_data="buy_4175_655000")],
        [InlineKeyboardButton(text="💎 4510 UC — 685,000 сўм", callback_data="buy_4510_685000")],   
        [InlineKeyboardButton(text="💎 5650 UC — 905,000 сўм", callback_data="buy_5650_905000")],
        [InlineKeyboardButton(text="💎 8100 UC — 1,200,000 сўм", callback_data="buy_8100_1200000")],
        [InlineKeyboardButton(text="💎 9900 UC — 1,450,000 сўм", callback_data="buy_9900_1450000")],
        [InlineKeyboardButton(text="💎 11950 UC — 1,740,000 сўм", callback_data="buy_11950_1740000")],
        [InlineKeyboardButton(text="💎 16200 UC — 2,350,000 сўм", callback_data="buy_16200_2350000")]
    ]
)

# --- ҚЎЛЛАБ-ҚУВВАТЛАШ ---
@dp.message(F.text == "📞 Қўллаб-қувватлаш")
async def support(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "💬 <b>Саволлар ва муаммолар бўйича админга мурожаат қилинг:</b>\n\n"
        "👨‍💻 Админ: @ashur0vmk",
        reply_markup=main_keyboard
    )

# --- БОТ БУЙРУҚЛАРИ ---
@dp.message(Command("start"))
async def start_cmd(message: types.Message, state: FSMContext):
    await state.clear()
    cursor.execute("INSERT OR IGNORE INTO users VALUES (?, ?, ?)", 
                   (message.from_user.id, message.from_user.username, message.from_user.full_name))
    conn.commit()
    
    await message.answer(
        f"Ассалому алайкум, {message.from_user.first_name}!\n\n"
        f"🔥 MADIYIM PUBG UC SHOP ботига хуш келибсиз!\n"
        f"Биз оркали PUBG UC'ларни хамёнбоп нархларда харид килишингиз мумкин.\n\n"
        f"Керакли бўлимни танланг:",
        reply_markup=main_keyboard,
        parse_mode="Markdown"
    )

@dp.message(F.text == "💎 UC Харид қилиш")
async def buy_uc(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("🛒 <b>Керакли UC пакетини танланг:</b>", reply_markup=uc_keyboard)

# --- МЕНИНГ БУЮРТМАЛАРИМ ---
@dp.message(F.text == "📦 Менинг буюртмаларим")
async def my_orders(message: types.Message, state: FSMContext):
    await state.clear()
    cursor.execute("SELECT uc_amount, price, player_id, status FROM orders WHERE user_id = ? ORDER BY order_id DESC LIMIT 5", (message.from_user.id,))
    orders = cursor.fetchall()
    
    if not orders:
        await message.answer("📭 Сизда ҳали ҳеч қандай буюртмалар йўқ.", reply_markup=main_keyboard)
        return
        
    text = "📦 <b>Охирги буюртмаларингиз:</b>\n\n"
    for order in orders:
        text += f"💎 <b>{order[0]} UC</b> | 💰 {order[1]} сўм\n🎮 ID: <code>{order[2]}</code>\nҲолат: <b>{order[3]}</b>\n-------------------\n"
    
    await message.answer(text, reply_markup=main_keyboard)

# --- ХАРИД ЖАРАЁНИ ---
@dp.callback_query(F.data.startswith("buy_"))
async def process_uc_choice(callback: types.CallbackQuery, state: FSMContext):
    _, uc, price = callback.data.split("_")
    await state.update_data(chosen_uc=uc, chosen_price=price)
    await callback.message.answer(f"✅ Танланди: <b>{uc} UC</b> ({price} сўм)\n\n🎮 Илтимос, <b>PUBG Player ID</b> рақамингизни киритинг:")
    await state.set_state(OrderState.waiting_for_id)
    await callback.answer()

@dp.message(OrderState.waiting_for_id)
async def process_player_id(message: types.Message, state: FSMContext):
    player_id = message.text
    await state.update_data(player_id=player_id)
    data = await state.get_data()
    
    await message.answer(
        f"💳 <b>Тўлов босқичи</b>\n\n"
        f"💎 Товар: <b>{data['chosen_uc']} UC</b>\n"
        f"💰 Сумма: <b>{data['chosen_price']} сўм</b>\n"
        f"🎮 PUBG ID: <code>{player_id}</code>\n\n"
        f"Қуйидаги картага тўловни амалга оширинг:\n"
        f"💳 Карта: <code>{CARD_NUMBER}</code>\n"
        f"👤 Эгаси: <b>{CARD_HOLDER}</b>\n\n"
        f"📸 Тўлов қилгач, <b>чек суратини (скриншот)</b> шу ерга юборинг!",
        reply_markup=main_keyboard
    )
    await state.set_state(OrderState.waiting_for_receipt)

@dp.message(OrderState.waiting_for_receipt, F.photo)
async def process_receipt(message: types.Message, state: FSMContext):
    photo_id = message.photo[-1].file_id
    data = await state.get_data()
    
    cursor.execute("INSERT INTO orders (user_id, uc_amount, price, player_id, status) VALUES (?, ?, ?, ?, ?)",
                   (message.from_user.id, data.get('chosen_uc'), data.get('chosen_price'), data.get('player_id'), "⏳ Кутилмоқда"))
    conn.commit()
    order_id = cursor.lastrowid
    
    await message.answer("⏳ <b>Чек қабул қилинди!</b>\nАдмин тўловни текшириб, UC юборгач сизга хабар беради.", reply_markup=main_keyboard)
    
    username = f"@{message.from_user.username}" if message.from_user.username else "Йўқ"
    caption_text = (
        f"🔔 <b>ЯНГИ ТЎЛОВ ЧЕКИ! (#Order{order_id})</b>\n\n"
        f"👤 Харидор: {username} ({message.from_user.first_name})\n"
        f"💎 Товар: <b>{data.get('chosen_uc')} UC</b>\n"
        f"💰 Сумма: <b>{data.get('chosen_price')} сўм</b>\n"
        f"🎮 PUBG ID: <code>{data.get('player_id')}</code>"
    )

    for admin_id in ALL_ADMIN_IDS:
        admin_keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="✅ Тасдиқлаш", callback_data=f"confirm_{order_id}_{message.from_user.id}_{data.get('chosen_uc')}"),
                    InlineKeyboardButton(text="❌ Бекор қилиш", callback_data=f"cancel_{order_id}_{message.from_user.id}")
                ]
            ]
        )
        try:
            await bot.send_photo(
                chat_id=int(admin_id),
                photo=photo_id,
                caption=caption_text,
                reply_markup=admin_keyboard
            )
            print(f"✅ Админга муваффақиятли юборилди: {admin_id}")
        except Exception as e:
            print(f"❌ Админга ({admin_id}) юборишда ХАТОЛИК: {e}")

    await state.clear()

# --- АДМИН ТАСДИҚЛАШ/БЕКОР ҚИЛИШ (Иккала админ учун ҳам очиқ) ---
@dp.callback_query(F.data.startswith("confirm_"))
async def confirm_order(callback: types.CallbackQuery):
    _, order_id, user_id, uc = callback.data.split("_")
    cursor.execute("UPDATE orders SET status = '✅ Бажарилди' WHERE order_id = ?", (order_id,))
    conn.commit()
    
    await bot.send_message(
        chat_id=int(user_id),
        text=f"🎉 <b>Хушхабар!</b> Тўловингиз тасдиқланди ва <b>{uc} UC</b> ҳисобингизга туширилди! Танловингиз учун раҳмат!"
    )
    admin_name = f"@{callback.from_user.username}" if callback.from_user.username else callback.from_user.first_name
    await callback.message.edit_caption(caption=callback.message.caption + f"\n\n✅ <b>ТАСДИҚЛАНДИ</b> ({admin_name})")
    await callback.answer("Буюртма тасдиқланди!")

@dp.callback_query(F.data.startswith("cancel_"))
async def cancel_order(callback: types.CallbackQuery):
    _, order_id, user_id = callback.data.split("_")
    cursor.execute("UPDATE orders SET status = '❌ Бекор қилинди' WHERE order_id = ?", (order_id,))
    conn.commit()
    
    await bot.send_message(
        chat_id=int(user_id),
        text="❌ <b>Тўловингиз тасдиқланмади.</b> Чекда хатолик бўлиши мумкин. Ёрдам учун админга мурожаат қилинг."
    )
    admin_name = f"@{callback.from_user.username}" if callback.from_user.username else callback.from_user.first_name
    await callback.message.edit_caption(caption=callback.message.caption + f"\n\n❌ <b>БЕКОР ҚИЛИНДИ</b> ({admin_name})")
    await callback.answer("Буюртма бекор қилинди!")

# --- ФАҚАТ МУҲАММАДКАМОЛ УЧУН БУЙРУҚЛАР (SUPER_ADMIN_ID) ---
@dp.message(Command("stats"), F.from_user.id == SUPER_ADMIN_ID)
async def admin_stats(message: types.Message):
    cursor.execute("SELECT COUNT(*) FROM users")
    users_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM orders WHERE status = '✅ Бажарилди'")
    successful_orders = cursor.fetchone()[0]
    
    await message.answer(
        f"📊 <b>MADIYIM UC SHOP Статистикаси:</b>\n\n"
        f"👥 Жами фойдаланувчилар: <b>{users_count} та</b>\n"
        f"✅ Муваффақиятли буюртмалар: <b>{successful_orders} та</b>"
    )

@dp.message(Command("send"), F.from_user.id == SUPER_ADMIN_ID)
async def start_broadcast(message: types.Message, state: FSMContext):
    await message.answer("📢 Барча фойдаланувчиларга юбориладиган <b>хабар матнини ёзинг</b>:")
    await state.set_state(BroadcastState.waiting_for_message)

@dp.message(BroadcastState.waiting_for_message, F.from_user.id == SUPER_ADMIN_ID)
async def process_broadcast(message: types.Message, state: FSMContext):
    cursor.execute("SELECT user_id FROM users")
    users = cursor.fetchall()
    count = 0
    
    for user in users:
        try:
            await bot.send_message(user[0], message.text)
            count += 1
            await asyncio.sleep(0.05)
        except Exception:
            pass
            
    await message.answer(f"✅ Хабар <b>{count} та</b> фойдаланувчига муваффақиятли етказилди!")
    await state.clear()

async def main():
    print("🚀 MADIYIM UC SHOP боти ишга тушди!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
