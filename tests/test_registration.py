import pytest
import sqlite3
import os
import io
import sys
from registration.registration import create_db, add_user, authenticate_user, display_users

@pytest.fixture(scope="module")
def setup_database():
    """Фикстура для настройки базы данных перед тестами и её очистки после."""
    create_db()
    yield
    try:
        os.remove('users.db')
    except PermissionError:
        pass

@pytest.fixture
def connection():
    """Фикстура для получения соединения с базой данных и его закрытия после теста."""
    conn = sqlite3.connect('users.db')
    yield conn
    conn.close()


def test_create_db(setup_database, connection):
    """Тест создания базы данных и таблицы пользователей."""
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users';")
    table_exists = cursor.fetchone()
    assert table_exists, "Таблица 'users' должна существовать в базе данных."

def test_add_new_user(setup_database, connection):
    """Тест добавления нового пользователя."""
    add_user('testuser', 'testuser@example.com', 'password123')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE username='testuser';")
    user = cursor.fetchone()
    assert user, "Пользователь должен быть добавлен в базу данных."

# Возможные варианты тестов:
"""
Тест добавления пользователя с существующим логином.
Тест успешной аутентификации пользователя.
Тест аутентификации несуществующего пользователя.
Тест аутентификации пользователя с неправильным паролем.
Тест отображения списка пользователей.
"""

def test_inv_password(setup_database, connection):
    '''Тест аутентификации пользователя с неправильным паролем.'''
    username = 'testuser'
    password = 'password12'
    assert False == authenticate_user(username, password)

def test_inv_login(setup_database, connection):
    '''Тест аутентификации несуществующего пользователя.'''
    username = 'testuser22'
    password = 'password123'
    assert False == authenticate_user(username, password)

def test_correct_aut(setup_database, connection):
    '''Тест успешной аутентификации пользователя.'''
    username = 'testuser'
    password = 'password123'
    assert True == authenticate_user(username, password)

def test_exist_login(setup_database, connection):
    '''Тест добавления пользователя с существующим логином.'''
    username = 'testuser'
    email = 'testuser@example.com'
    password = 'password123'
    assert False == add_user(username, email, password)

def test_display_users(setup_database, connection):
    '''Тест отображения списка пользователей.'''
    captured_output = io.StringIO()          
    sys.stdout = captured_output           
    display_users()                        
    sys.stdout = sys.__stdout__           
    a = 'Логин: testuser, Электронная почта: testuser@example.com'
    output_string = captured_output.getvalue().strip()
    assert output_string == a


    