from station import WeatherStation
from weather_plot import WeatherPlot

sitka = WeatherStation("data/sitka_2018_simple.csv")
death_valley = WeatherStation("data/death_valley_2018_simple.csv")

plot = WeatherPlot(sitka, [death_valley])
plot.plot()
