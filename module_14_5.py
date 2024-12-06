# Цель: написать простейшие CRUD функции для взаимодействия с базой данных.

# Задача "Регистрация покупателей":


from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor
from crud_functions import initiate_db, add_user, is_included

API_TOKEN = ''

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
initiate_db()

# Класс состояний для процесса регистрации
class RegistrationState(StatesGroup):
    username = State()  # Состояние для имени пользователя
    email = State()     # Состояние для электронной почты
    age = State()       # Состояние для возраста


# Создаём клавиатуру с кнопкой "Регистрация"
main_menu = ReplyKeyboardMarkup(resize_keyboard=True) # Клавиатура будет адаптироваться под размер экрана
main_menu.add(KeyboardButton("Регистрация"))  # Добавляем кнопку "Регистрация"

# Обработчик команды /start
@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    """
    Отправляет сообщение с главным меню при старте бота.

    """
    await message.answer("Привет! Я бот, помогающий твоему здоровью.", reply_markup=main_menu)

# Начало регистрации
@dp.message_handler(lambda message: message.text == "Регистрация")
async def sign_up(message: types.Message):
    """
    Начало процесса регистрации. Запрашивает имя пользователя.

    """
    await message.answer("Введите имя пользователя (только латинский алфавит):")
    await RegistrationState.username.set()

# Установка имени пользователя
@dp.message_handler(state=RegistrationState.username)
async def set_username(message: types.Message, state: FSMContext):
    """
    Проверяет, существует ли имя пользователя, и запрашивает email, если имя уникально.

    """
    username = message.text.strip()  # Удаляем лишние пробелы
    if is_included(username):   # Проверяем, существует ли пользователь
        await message.answer("Пользователь существует, введите другое имя.")
    else:
        await state.update_data(username=username)  # Сохраняем имя пользователя в состоянии
        await message.answer("Введите свой email:")
        await RegistrationState.email.set()  # Переходим к следующему состоянию


# Установка email
@dp.message_handler(state=RegistrationState.email)
async def set_email(message: types.Message, state: FSMContext):
    """
    Сохраняет email и запрашивает возраст.

    """
    email = message.text.strip() # Удаляем лишние пробелы
    await state.update_data(email=email)  # Сохраняем email в состоянии
    await message.answer("Введите свой возраст:")
    await RegistrationState.age.set()  # Переходим к следующему состоянию

# Установка возраста и завершение регистрации
@dp.message_handler(state=RegistrationState.age)
async def set_age(message: types.Message, state: FSMContext):
    """
    Cохраняет возраст, добавляет пользователя в базу и завершает регистрацию.

    """
    age = message.text.strip()  # Удаляем лишние пробелы
    if not age.isdigit(): # Проверяем, является ли возраст числом
        await message.answer("Возраст должен быть числом. Попробуйте ещё раз:")
        return

    age = int(age)  # Преобразуем возраст в число
    data = await state.get_data()  # Получаем данные из состояния (username, email)
    add_user(data['username'], data['email'], age)  # Добавляем пользователя в базу
    await message.answer("Регистрация прошла успешно.")
    await state.finish()  # Завершаем процесс регистрации


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
