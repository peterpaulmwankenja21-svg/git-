import sys
import requests
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QLabel, QPushButton, QWidget, QLineEdit

class currencyConverter(QWidget):
    def __init__(self):
        super().__init__()
        self.currency_converter_label = QLabel("Currency Exchange(USD to TZS):", self)
        self.amount_input = QLineEdit(self)
        self.convert_btn = QPushButton("Convert", self)
        self.Result_label = QLabel("Amount:", self)

        self.initUI()


    def initUI(self):
        self.setWindowTitle("Currency converter App")
        self.setGeometry(400, 200, 500, 200)

        vbox = QVBoxLayout()
        vbox.addWidget( self.currency_converter_label)
        vbox.addWidget( self.amount_input)

        vbox.addWidget( self.convert_btn)
        vbox.addWidget(self.Result_label)


        self.setLayout(vbox)
        self.amount_input.setPlaceholderText("Enter amount(USD)")





        self.setStyleSheet("""
        QPushButton{
        background-color: #00BFFF;
        font-size: 30px;
        }
        QLabel{
        font-style: bold;
        font-size: 20px;
        }
        QLineEdit{
        font-size: 20px;
        }
        """)
        self.convert_btn.clicked.connect(self.get_currency)




    def get_currency(self):
        try:
            amount = float(self.amount_input.text())
        except ValueError:
            self.Result_label.setText("Please enter a valid number")
            return



        api_key = "927edd19f240839c74642c0f"
        from_currency = "USD"
        to_currency = "TZS"
        url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/{from_currency}"
        response = requests.get(url)
        data = response.json()

        exchange_rate = data['conversion_rates'][f'{to_currency}']

        converted_rate = exchange_rate * amount

        self.Result_label.setText(f"{amount} {from_currency} = {converted_rate} {to_currency}")



if __name__ == "__main__":
    app = QApplication(sys.argv)
    currency = currencyConverter()
    currency.show()
    exit(app.exec_())






