#Weather App Api using python
import sys
import requests
from PyQt5.QtWidgets import QApplication, QPushButton, QWidget, QLabel, QVBoxLayout, QLineEdit
from PyQt5.QtCore import Qt

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.city_label = QLabel("Enter the city", self)
        self.city_input = QLineEdit(self)
        self.temperature_label = QPushButton("Get temperature", self)
        self.emoji_label = QLabel(self)
        self.weather_description = QLabel(self)

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Weather App")

        vbox = QVBoxLayout()
        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.temperature_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.weather_description)

        self.setLayout(vbox)

        self.setStyleSheet("""
        QPushButton{
        border-radius: 50px;
        background-color: #FF5733;
        font-size: 25px;
        }
        QLabel{
        font-size: 35px;
        font-style: Bold;
        }
        QLineEdit{
        font-size: 20px;
        }
        
        """)
        self.setGeometry(100, 100, 400, 200)

        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        #self.temperature_label.setAlignment(Qt.AlignTop)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.weather_description.setAlignment(Qt.AlignCenter)



        self.temperature_label.clicked.connect(self.get_weather)

    def get_weather(self):
        try:
            api_key = "27804c083aeadbc141867d60911a5ecd"
            city = self.city_input.text()
            url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            if data['cod'] == 200:
                self.display_weather(data)


        except requests.exceptions.HTTPError as httpError:
            match response.status_code:
                case 400:
                    self.display_error("Bad request:\nplease check your input")
                case 401:
                  self.display_error("Unauthorized:\nInvalid API key")
                case 403:
                    self.display_error("Forbidden:\nAccess denied")
                case 404:
                    self.display_error("Not found:\ncity not found")
                case 500:
                    self.display_error("Internal sever error:\nplease try again")
                case 502:
                    self.display_error("Bad gateway:\nInvalid response from the server")
                case 503:
                    self.display_error("service unavailable:\nservice down")
                case 504:
                    self.display_error("Bad request:\nplease check your input")
                case _:
                   self.display_error(f"httpError occurred\n{httpError}")

        except requests.exceptions.ConnectionError:
            self.display_error("No connection:\nCheck your connection")



    def display_error(self, message):
        self.temperature_label.setText(message)
        self.emoji_label.setText("")



    def display_weather(self, data):
        temp_k = data['main']['temp']
        temp_c = temp_k - 273.15
        weather_id = data['weather'][0]['id']
        desc = data['weather'][0]['description']

        self.temperature_label.setText(f"{temp_c:.0f}°C")
        self.emoji_label.setText(self.get_weather_emoji(weather_id))
        self.weather_description.setText(f"{desc}")

    @staticmethod
    def get_weather_emoji(weather_id):
        if 200 <= weather_id < 300:
            return "⛈️"
        elif 300 <= weather_id < 400:
            return "🌦️"
        elif 500 <= weather_id < 600:
            return "🌧️"
        elif 600 <= weather_id < 700:
            return "❄️"
        elif 700 <= weather_id < 800:
            return "🌫️"
        elif weather_id == 800:
            return "☀️"
        elif 801 <= weather_id <= 804:
            return "☁️"
        else:
            return "🌈"


if __name__ == '__main__':
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    exit(app.exec_())


