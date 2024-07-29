import requests

# class OpenWeatherAPI:
#     _API_KEY = "63b3bb20a705ea1272d166545564dea1"

class WeatherWrapper:

    def __init__(self, city):
        self.city = city
        self.API_KEY = "63b3bb20a705ea1272d166545564dea1"
        self.URL = f"https://api.openweathermap.org/data/2.5/weather?q={self.city}&appid={self.API_KEY}"
        self.__data = eval(requests.get(self.URL).text)

    def get_temperature(self):
        return round((self.__data['main']['temp'] - 273.15), 2)


    def get_temp_feel(self):
        return round((self.__data['main']['feels_like'] - 273.15), 2)

    def get_data(self):
        return self.__data

    def get_weather(self):
        return self.__data['weather'][0]['main']

    def get_humidity(self):
        return self.__data['main']['humidity']


    def get_visibility(self):
        return self.__data['visibility']

    def get_wind(self):
        return self.__data['wind']['speed']

    def get_wind_direct(self):
        return self.__data['wind']['deg']

    def __str__(self):
        return (f"The weather in {self.city} is mostly {self.__data['weather'][0]['main']},"
                f"the temperature is {round((self.__data['main']['feels_like'] - 273.15), 2)}°C,"
                f"and you can feel it like {round((self.__data['main']['feels_like'] - 273.15), 2)}°C,"
                f"the humidity is {self.__data['main']['humidity']}%,"
                f"the visibility is at least {self.__data['visibility']}m,"
                f"the speed of wind is {self.__data['wind']['speed']} m/sec,"
                f"the direction of wind is {self.__data['wind']['deg']}°")
#
#
# city = 'Poltava'
# weather = CurrentWeatherData(city=city)
#
# print(weather.__str__())


