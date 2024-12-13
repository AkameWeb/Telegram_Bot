import telebot 
import pyautogui 
import pygetwindow as gw 
import os 
import subprocess
import sys


# Ваш токен от Telegram 
bot_token = '7435745463:AAGdcvHPMFBPePos387QJO7fSMFfZvVXI7M' # Замените на токен нужного бота 
bot = telebot.TeleBot(bot_token) 
 
# Укажите ID пользователя, который может управлять ботом 
allowed_user_id = 6433489833 # Замените на ваш реальный Telegram ID 
 
# Функция проверки прав доступа 
def check_access(message): 
    if message.from_user.id != allowed_user_id: 
         bot.send_message(message.chat.id, "У вас нет прав для управления этим ботом.")
         print(f"Пользователь {message.from_user.id} пытался выполнить команду, но не имеет прав.") 
         return False 
    return True 
 
@bot.message_handler(commands=['stop']) 
def send_stop(message):
    if not check_access(message): 
        return 
    try:
        bot.delete_message(message.chat.id, message.message_id)
        bot.polling()
        
        subprocess.Popen(['start','C:\\Users\\AkiWeb\\Desktop\\Telegram\\Telegram\\bin\\Debug\\Telegram.exe'], shell = True )
        exit(0)
    except Exception as e: 
         bot.send_message(message.chat.id, f"Произошла ошибка: {e}") 
         print(f"Ошибка при выполнении команды /stop: {e}") 

# Команда для отправки скриншота 
@bot.message_handler(commands=['screenshot']) 
def send_screenshot(message): 
     if not check_access(message): 
        return 
 
     try: 
         # Делаем скриншот 
        screenshot = pyautogui.screenshot() 
 
        # Сохраняем временно скриншот 
        screenshot_path = 'screenshot.png' 
        screenshot.save(screenshot_path) 
 
        # Проверяем, существует ли файл перед отправкой 
        if os.path.exists(screenshot_path): 
             with open(screenshot_path, 'rb') as photo: 
                 bot.send_photo(message.chat.id, photo) 
             os.remove(screenshot_path) # Удаляем файл после отправки 
             print("Команда /screenshot выполнена: скриншот отправлен") 
        else: 
            bot.send_message(message.chat.id, "Не удалось создать скриншот.") 
            print("Команда /screenshot не удалась: файл скриншота не найден") 
     except Exception as e: 
         bot.send_message(message.chat.id, f"Произошла ошибка: {e}") 
         print(f"Ошибка при выполнении команды /screenshot: {e}") 
        
# Команда для отображения всех открытых окон 
@bot.message_handler(commands=['list_windows']) 
def list_windows(message): 
    if not check_access(message): 
        return 
 
    windows = gw.getAllTitles() # Получаем заголовки всех окон 
    windows = [w for w in windows if w] # Убираем пустые строки (иногда бывают скрытые окна) 
 
    if windows: 
         response = "Открытые окна:\n" 
         for i, window in enumerate(windows): 
             response += f"{i+1}. {window}\n" 
         print(f"Команда /list_windows выполнена: найдено {len(windows)} окон")
    else:
        response = "Окна не найдены."
        print("Команда /list_windows выполнена: окна не найдены")
 
    bot.send_message(message.chat.id, response)
 
# Команда для закрытия окна по его индексу
@bot.message_handler(commands=['close_window'])
def close_window(message):
    if not check_access(message):
        return
 
    try:
        # Парсим команду, ожидаем индекс окна
        index = int(message.text.split()[1]) - 1
 
        # Получаем список окон
        windows = gw.getAllTitles()
        windows = [w for w in windows if w]
 
        # Закрываем выбранное окно
        if 0 <= index < len(windows):
            window = gw.getWindowsWithTitle(windows[index])[0]
            window.close()
            bot.send_message(message.chat.id, f"Окно '{windows[index]}' закрыто.")
            print(f"Команда /close_window выполнена: окно '{windows[index]}' закрыто")
        else:
            bot.send_message(message.chat.id, "Неверный индекс окна.")
            print("Команда /close_window: неверный индекс окна")
    except (IndexError, ValueError):
        bot.send_message(message.chat.id, "Пожалуйста, укажите корректный индекс окна. Пример: /close_window 1")
        print("Ошибка: некорректный индекс для команды /close_window")
    except Exception as e:
        bot.send_message(message.chat.id, f"Произошла ошибка: {e}")
        print(f"Ошибка при выполнении команды /close_window: {e}")
 
# Запускаем бота
bot.polling(none_stop=True)