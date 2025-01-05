import requests
import geocoder
import sqlite3
from datetime import datetime, timezone, timedelta

api_key = "3ffabfc1766dc1d96eeb5dfb5c7bca55"

def convert_datetime(timestamp):
    return datetime.fromtimestamp(timestamp)

def adapt_datetime(dt):
    return dt.timestamp()

sqlite3.register_adapter(datetime, adapt_datetime)
sqlite3.register_converter("datetime", convert_datetime)

def print_weather_info(location: str, data_from_file: dict):
    utc_timestamp = data_from_file["dt"]
    offset = data_from_file["timezone"]

    tz = timezone(timedelta(seconds=offset))
    result_time = datetime.fromtimestamp(utc_timestamp, tz)
    formatted_time = result_time.strftime("%Y-%m-%d %H:%M:%S")
    timezone_offset = result_time.strftime("%z")
    formatted_timezone = f"{timezone_offset[:3]}:{timezone_offset[3:]}"

    temperature = round(data_from_file["main"]["temp"])
    feels_like = round(data_from_file["main"]["feels_like"])
    wind_speed = round(data_from_file["wind"]["speed"])

    print("Текущее время:", formatted_time + formatted_timezone)
    print("Название города:", location)
    print("Погодные условия:", data_from_file["weather"][0]["description"])
    print("Текущая температура:", temperature, "градусов по Цельсию")
    print("Ощущается как:", feels_like, "градусов по Цельсию")
    print("Скорость ветра:", wind_speed, "м/с")

def save_to_database(data: tuple):
    try:
        connection = sqlite3.connect("weather.db", detect_types=sqlite3.PARSE_DECLTYPES)
        cursor = connection.cursor()

        cursor.execute('''CREATE TABLE IF NOT EXISTS weather_requests
                          (id INTEGER PRIMARY KEY AUTOINCREMENT,
                          timestamp TIMESTAMP,
                          city TEXT,
                          weather_condition TEXT,
                          temperature FLOAT,
                          feeling FLOAT,
                          speed FLOAT)''')

        cursor.execute(
            "INSERT INTO weather_requests (timestamp, city, weather_condition, temperature, feeling, speed) VALUES (?, ?, ?, ?, ?, ?)",
            data)
        connection.commit()
        connection.close()

    except sqlite3.Error:
        print("ошибка при работе с базой данных, попробуйте снова!")

def get_weather_by_city(city: str):
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=ru"
        response = requests.get(url)
        response.raise_for_status()
        data_from_file = response.json()

        print_weather_info(city, data_from_file)
        save_to_database((datetime.now(timezone.utc), city, data_from_file["weather"][0]["description"],
                          data_from_file["main"]["temp"], data_from_file["main"]["feels_like"],
                          data_from_file["wind"]["speed"]))
    except requests.exceptions.HTTPError:
        print("город не найден, попробуйте снова!")
    except requests.exceptions.RequestException as err:
        print(f"request exception occurred: {err}, попробуйте снова!")

def get_weather_by_location():
    try:
        location = geocoder.ip("me")

        if location:
            latitude, longitude = location.latlng
            url = f"https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={api_key}&units=metric&lang=ru"
            response = requests.get(url)
            response.raise_for_status()
            data_from_file = response.json()
            print_weather_info(location.address, data_from_file)
            save_to_database((datetime.now(timezone.utc), location.address, data_from_file["weather"][0]["description"],
                              data_from_file["main"]["temp"], data_from_file["main"]["feels_like"],
                              data_from_file["wind"]["speed"]))
        else:
            print("не удалось определить текущее местоположение")
    except requests.exceptions.HTTPError as err:
        print(f"http error occurred: {err}, попробуйте снова!")
    except requests.exceptions.RequestException as err:
        print(f"request exception occurred: {err}, попробуйте снова!")

def print_history(n: str):
    try:
        n = int(n)
        if n < 0:
            print("введите значение n > 0")
        else:
            connection = sqlite3.connect("weather.db")
            cursor = connection.cursor()
            cursor.execute(f"SELECT * FROM weather_requests ORDER BY timestamp DESC LIMIT {n}")
            results = cursor.fetchall()
            connection.close()

            if results:
                print("последние", n, "запросов:")
                print("=" * 40)
                for result in results:
                    timestamp = result[1]
                    if isinstance(timestamp, float):
                        timestamp = datetime.fromtimestamp(timestamp)

                    formatted_time = timestamp.astimezone().strftime("%Y-%m-%d %H:%M:%S")
                    timezone_offset = timestamp.astimezone().strftime("%z")
                    formatted_timezone = f"{timezone_offset[:3]}:{timezone_offset[3:]}"

                    temperature = round(result[4])
                    feels_like = round(result[5])
                    wind_speed = round(result[6])

                    print("Текущее время:", formatted_time + formatted_timezone)
                    print("Название города:", result[2])
                    print("Погодные условия:", result[3])
                    print("Текущая температура:", temperature, "градусов по Цельсию")
                    print("Ощущается как:", feels_like, "градусов по Цельсию")
                    print("Скорость ветра:", wind_speed, "м/с")
                    print("=" * 40)
            else:
                print("история запросов пуста.")

    except ValueError:
        print("введите целое число для 'history'")
    except sqlite3.OperationalError:
        print("ошибка при работе с базой данных.")
    except sqlite3.Error:
        print("ошибка при работе с базой данных, попробуйте снова!")

menu_text = (
    "\nкоманды:\n1. погода по названию города\n2. погода по текущему местоположению\n"
    "3. просмотр истории запросов\n4. закрыть программу\n"
)

def main():
    try:
        while True:
            print(menu_text)
            user_input = input("\nвыберите одну из команд и введите её: ").strip()
            if user_input == '4':
                print("завершение программы")
                break
            elif user_input == '1':
                city = input("\nвведите название города: ").strip()
                get_weather_by_city(city)
            elif user_input == '2':
                get_weather_by_location()
            elif user_input == '3':
                n = input("\nвведите количество последних запросов: ").strip()
                print_history(n)
            else:
                print("введите корректную команду")
    except KeyboardInterrupt:
        print("\nПрограмма была прервана. Выход...")

if __name__ == "__main__":
    main()
