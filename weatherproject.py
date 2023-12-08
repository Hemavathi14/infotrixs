import requests
import time
import json
import nametemplate


class WeatherApp:  # define a class
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"
        self.favorite_cities = []

    def get_weather_by_city(self, city_name):  # this func is for checking weather details
        params = {
            'q': city_name,
            'appid': self.api_key,
            'units': 'metric'  # You can change the units as per your preference
        }

        try:
            response = requests.get(self.base_url, params=params)  # sending http request
            data = response.json()  # the data we want json format

            if response.status_code == 200:  # if status code 200 means it is successful
                return data
            else:
                print(f"Error: {data['message']}")
                return None

        except requests.RequestException as e:
            print(f"Request Error: {e}")
            return None

    def add_favorite_city(self, city_name):  # func for add fav cities
        if city_name not in self.favorite_cities:
            self.favorite_cities.append(city_name)  # adding cities to the empty list
            print(f"{city_name} added to favorites.")

    def remove_favorite_city(self, city_name):
        if city_name in self.favorite_cities:  # removing city from fav as per user choice
            self.favorite_cities.remove(city_name)
            print(f"{city_name} removed from favorites.")
        else:
            print(f"{city_name} is not in favorites.")

    def list_favorite_cities(self):  # printing fav cities in the list
        print("Favorite Cities:")
        for city in self.favorite_cities:
            print(f"- {city}")

    def auto_refresh(self, interval_sec):
        for _ in range(5):  # auto refresh func , it will work 5 times otherwise it will become infinite loop
            for city in self.favorite_cities:
                weather_data = self.get_weather_by_city(city)
                if weather_data:
                    print(f"Weather in {city}: {weather_data['weather'][0]['description']}, "
                          f"Temperature: {weather_data['main']['temp']}°C")
            time.sleep(interval_sec)


if __name__ == "__main__":
    API_KEY = "2ea093abcc2844411e39b20734286dac"
    weather_app = WeatherApp(API_KEY)
    print(nametemplate.welcome_note)

    while True:

        print("\n*********************************************")
        print("Options:")
        print("1. Check weather by city")
        print("2. Add favorite city")
        print("3. Remove favorite city")
        print("4. List favorite cities")
        print("5. Auto refresh favorite cities")
        print("6. Quit")
        print("*********************************************\n")

        choice = input("Enter your choice (1-6): ")  # users choice

        # checking users choice
        if choice == "1":
            city_name = input("Enter city name: ").lower().strip()
            weather_data = weather_app.get_weather_by_city(city_name)  # passing city name to the function
            if weather_data:
                print(f"Weather in {city_name}: {weather_data['weather'][0]['description']}, "
                      f"Temperature: {weather_data['main']['temp']}°C")

        elif choice == "2":
            city_name = input("Enter city name to add to favorites: ")
            weather_app.add_favorite_city(city_name)

        elif choice == "3":
            city_name = input("Enter city name to remove from favorites: ")
            weather_app.remove_favorite_city(city_name)

        elif choice == "4":
            weather_app.list_favorite_cities()

        elif choice == "5":
            interval_sec = int(input("Enter auto-refresh interval in seconds (e.g., 15): "))
            weather_app.auto_refresh(interval_sec)

        elif choice == "6":
            print("Quitting the application. Goodbye!")
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 6.")
