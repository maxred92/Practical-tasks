import math
from datetime import datetime

import requests
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

bot = Bot(token="6033243937:AAEm3U12TBBN5HSNcUTWHKMtuPTLHAufJi4")
dp = Dispatcher(bot)

WEATHER_API_TOKEN = "6667b026a2ba09a5004fe2e4b5f3762d"


@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.reply(
        "Hello! Write me the name of the city and I will send a weather report."
    )


@dp.message_handler()
async def get_weather(message: types.Message):
    try:
        response = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={message.text}&lang=en&units=metric&APPID={WEATHER_API_TOKEN}"
        )
        data = response.json()
        city = data["name"]
        cur_temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]
        sunrise_timestamp = datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_timestamp = datetime.fromtimestamp(data["sys"]["sunset"])
        length_day = datetime.fromtimestamp(
            data["sys"]["sunset"]
        ) - datetime.fromtimestamp(data["sys"]["sunrise"])
        code_to_smile = {
            "Clear": "Clear \U00002600",
            "Clouds": "Clouds \U00002601",
            "Rain": "Rain \U00002614",
            "Drizzle": "Drizzle \U00002614",
            "Thunderstorm": "Thunderstorm \U000026A1",
            "Snow": "Snow \U0001F328",
            "Mist": "Mist \U0001F32B",
        }
        weather_description = data["weather"][0]["main"]
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = "Look out the window. I don't understand what the weather now"
        await message.reply(
            f"{datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
            f"City weather: {city}\nTemperature: {cur_temp}°C {wd}\n"
            f"Air humidity: {humidity}%\nPressure: {math.ceil(pressure/1.333)} mm\nWind: {wind} m/s \n"
            f"Sunrise: {sunrise_timestamp}\nSunset: {sunset_timestamp}\nDay length: {length_day}\n"
            f"------------------------\n"
            f"Have a nice day!"
        )
    except Exception as e:
        await message.reply("Check the city name!")


if __name__ == "__main__":
    executor.start_polling(dp)
