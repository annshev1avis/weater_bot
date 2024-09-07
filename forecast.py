import requests
import vulnarable_info

# прогноз погоды для определенного города. start_hour-end_hour - часы для прогноза
class Forecast:
    api_key = vulnarable_info.weather_api_key  # ключ из моего личного аккаунта weatherapi.com

    def __init__(self, city, start_hour, end_hour):
        params = {"key": Forecast.api_key, "q": city, "days": 1}

        self.forecast = requests.get("http://api.weatherapi.com/v1/forecast.json", params=params).json()["forecast"]["forecastday"][0]
        self.start_hour = start_hour
        self.end_hour = end_hour

    @property
    def forecast_by_hours(self):
        # list of <dict характеристики часа>
        return self.forecast["hour"][self.start_hour:self.end_hour + 1]

    def temp_by_hours(self):
        # возвращает словарь вида <str время>: <int температура по С>
        return {h['time'].split()[1]: int(h["temp_c"]) for h in self.forecast_by_hours}

    def min_temp(self):
        temp = self.temp_by_hours()
        return min(temp.values())

    def max_temp(self):
        temp = self.temp_by_hours()
        return max(temp.values())

    def main_cloud_type(self):
        cloud_types = [h['condition']['text'] for h in self.forecast_by_hours]
        cloud_types_freq = {t: cloud_types.count(t) for t in cloud_types}
        most_popular_type = cloud_types[0]
        for c_t, freq in cloud_types_freq.items():
            if freq > cloud_types_freq[most_popular_type]:
                most_popular_type = c_t
        return most_popular_type

    def rainy_hours(self):
        # list of <str время>
        rainy_h = filter(lambda x: x["will_it_rain"] or x["will_it_snow"], self.forecast_by_hours)
        return list(h['time'].split()[1] for h in rainy_h)

    def get_sunset(self):
        # <str время>
        return self.forecast["astro"]["sunset"]

    def day_summary_str(self):
        res = f"облачность: {self.main_cloud_type()}\n"

        if self.rainy_hours():
            res += f"осадки ожидаются в: {' '.join(self.rainy_hours())}\n"
        else:
            res += "осадки не ожидаются\n"

        res += f"температура от {self.min_temp()} до {self.max_temp()}:\n"

        temp_by_hours_str = "\n".join([f'{h}: {str(t)} °C' for h, t in self.temp_by_hours().items()])
        res += temp_by_hours_str

        return res

