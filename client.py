import ipaddress
import webbrowser
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QMainWindow,
    QPushButton,
    QLineEdit,
    QLabel,
    QMessageBox,
)
from PyQt5.Qt import QUrl, QDesktopServices
import requests
import sys


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Client")
        self.setFixedSize(400, 400)
        self.label1 = QLabel("Enter your IP address:", self)
        self.text = QLineEdit(self)
        self.text.move(10, 30)
        self.button = QPushButton("Send", self)
        self.button.move(10, 200)
        self.label3 = QLabel("Entrez your Api_key", self)
        self.label3.move(10, 90)
        self.text2 = QLineEdit(self)
        self.text2.move(10, 120)
        self.label4 = QLabel("Entrez the hostname", self)
        self.label4.move(10, 150)
        self.text3 = QLineEdit(self)
        self.text3.move(10, 180)
        self.label2 = QLabel("E", self)
        self.label2.move(150, 150)


        self.button.clicked.connect(self.on_click)
        self.button.pressed.connect(self.on_click)

        self.show()

    def on_click(self):
        ipaddress = self.text.text()
        api_key = self.text2.text()
        hostname = self.text3.text()


        if hostname == "":
            QMessageBox.about(self, "Error", "Please fill the field")
        else:
            res = self.__query(hostname,api_key,ipaddress)
            if res:
                self.label2.setText("Answer : longitude %s latitude  %s" % (res["longitude"], res["latitude"]))
                self.label2.adjustSize()
                url1= "https://www.openstreetmap.org/?mlat=%s&mlon=%s#map=12" % (res["latitude"], res["longitude"])
                webbrowser.open(url1)
                self.show()

    def __query(self, hostname,api_key,ipaddress):
        url = "http://%s" % (hostname)+"/ip/%s" %(ipaddress)+ "?key=%s" % (api_key)
        QMessageBox.about(self, "url",url)

       # http://127.0.0.1:8000/ip/<ip>?key=<api key>
        r = requests.get(url)
        if r.status_code == requests.codes.NOT_FOUND:
            QMessageBox.about(self, "Error", "IP not found")
        if r.status_code == requests.codes.OK:
            return r.json()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = MainWindow()
    app.exec_()