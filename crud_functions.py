import sqlite3  # Импортируем библиотеку SQLite для работы с базой данных


# Функция для инициализации базы данных
def initiate_db():
    """
    Создаёт базу данных и таблицу Users, если она ещё не создана.
    """
    conn = sqlite3.connect('shop.db')  # Устанавливаем соединение с базой данных (файл будет создан, если его нет)
    cursor = conn.cursor()  # Создаём объект-курсор для выполнения SQL-запросов

    # SQL-запрос для создания таблицы Users
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,  -- Уникальный идентификатор пользователя (автоматически увеличивается)
        username TEXT NOT NULL,                -- Имя пользователя (не может быть пустым)
        email TEXT NOT NULL,                   -- Электронная почта (не может быть пустой)
        age INTEGER NOT NULL,                  -- Возраст (не может быть пустым)
        balance INTEGER NOT NULL               -- Баланс (не может быть пустым)
    )
    ''')

    conn.commit()  # Сохраняем изменения
    conn.close()  # Закрываем соединение


# Функция для добавления нового пользователя
def add_user(username, email, age):
    """
    Добавляет нового пользователя в таблицу Users.
    Начальный баланс всегда равен 1000.
    """
    conn = sqlite3.connect('shop.db')  # Подключаемся к базе данных
    cursor = conn.cursor()

    # SQL-запрос для вставки нового пользователя
    cursor.execute('''
    INSERT INTO Users (username, email, age, balance)
    VALUES (?, ?, ?, 1000)
    ''', (username, email, age))  # Передаём данные пользователя

    conn.commit()  # Сохраняем изменения
    conn.close()  # Закрываем соединение


# Функция для проверки, существует ли пользователь
def is_included(username):
    """
    Проверяет, есть ли пользователь с данным именем в таблице Users.
    Возвращает True, если пользователь существует, иначе False.
    """
    conn = sqlite3.connect('shop.db')  # Подключаемся к базе данных
    cursor = conn.cursor()

    # SQL-запрос для поиска пользователя по имени
    cursor.execute('SELECT * FROM Users WHERE username = ?', (username,))
    user = cursor.fetchone()  # Получаем первую найденную запись (или None, если записи нет)

    conn.close()  # Закрываем соединение
    return user is not None  # Возвращаем True, если пользователь найден
