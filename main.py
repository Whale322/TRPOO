import datetime
import json
import sys
from urllib.request import urlopen

from PyQt6 import uic, QtCore, QtGui
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from pygismeteo import Gismeteo
import sqlite3
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('цэ.ui', self)
        url = 'http://ipinfo.io/json'
        self.connection = sqlite3.connect("Gismeteo.db")
        response = urlopen(url)
        self.setFixedSize(self.size())
        self.data = json.load(response)
        self.test_schetchik = 0
        self.test_flag = False
        self.update_()
        self.working_clock = QtCore.QTimer()
        self.working_clock.setInterval(10000)
        self.working_clock.timeout.connect(self.update_)
        self.working_clock.start()


    def diary(self):
        self.test_flag = True
        uic.loadUi('цэ1.ui', self)
        self.working_clock.stop()
        self.label_2.show()
        self.label_3.show()
        self.label_4.show()
        self.label_5.show()
        self.gif.setScaledSize(QtCore.QSize(800, 1000))
        self.label.setMovie(self.gif)
        self.label.resize(800, 600)
        self.gif.start()
        self.pushButton.clicked.connect(self.back)
        pixmap = QtGui.QPixmap(f'photo\{self.hour3_icon}.png')
        self.label_10.setPixmap(pixmap)

        self.label_6.setFont(QFont('Yu Gothic UI Light', 16))
        self.label_7.setFont(QFont('Yu Gothic UI Light', 16))
        self.label_8.setFont(QFont('Yu Gothic UI Light', 16))
        self.label_6.setText(self.hour3_time)
        self.label_7.setText(self.hour6_time)
        self.label_8.setText(self.hour9_time)

        pixmap = QtGui.QPixmap(f'photo\{self.hour3_icon}.png')
        self.label_11.setPixmap(pixmap)

        pixmap = QtGui.QPixmap(f'photo\{self.hour3_icon}.png')
        self.label_12.setPixmap(pixmap)

        self.label_13.setText(f"{str(self.hour3_temperature)}°")
        self.label_14.setText(f"💦 {str(self.hour3_humidity)}%")
        self.label_15.setText(f"↓ {str(self.hour3_pressure)} мм")

        self.label_16.setText(f"↓ {str(self.hour6_pressure)} мм")
        self.label_17.setText(f"💦 {str(self.hour6_humidity)}%")
        self.label_18.setText(f"{str(self.hour6_temperature)}°")

        self.label_19.setText(f"↓ {str(self.hour9_pressure)} мм")
        self.label_20.setText(f"💦 {str(self.hour9_humidity)}%")
        self.label_21.setText(f"{str(self.hour9_temperature)}°")

        self.person = (self.connection.cursor().execute(f"""SELECT user FROM Users""").fetchall())[0][0]
        self.count = self.connection.cursor().execute(f"""SELECT * FROM Diary""").fetchall()
        if len(self.count) < 5:
            self.label_22.setText(f"Вы ещё не успели заполнить дневник!\n Осталось немного\n Заполняйте его еще {5-len(self.count)} дня, чтобы мы могли давать\n Вам рекомендации!")
        else:
            f = False
            cur_davlenie = self.current.pressure.mm_hg_atm
            cur_vlaznost = self.current.humidity.percent
            cur_tempereture = self.current.temperature.air.c
            print(cur_tempereture, cur_vlaznost, cur_davlenie)
            for elem in self.count:
                print(elem[10])
                if (abs(float(cur_davlenie) - float(elem[10])) < 11) and (abs(float(cur_tempereture) - float(elem[8]) < 6)) and (abs(float(cur_vlaznost) - float(elem[9])) <= 11):
                    print(elem[4], elem[5], elem[6])
                    f = True
                    f1 = elem[4]
                    f2 = elem[5]
                    f3 = elem[6]
                    break
            if f:
                if f1 and f2 and f3:
                    if (f1 == "3" or f1 == "2") and f2 == "1" and f3 == "1":
                        self.label_22.setText(
                        f"Ваш прогноз на сегодня:\n Сегодня вас ждет хорошее расположение духа.\n Ухудшений самочувствия не ожидается.")
                    elif f1 == "1" and f2 == "2" and f3 == "2":
                        self.label_22.setText(
                            f"Ваш прогноз на сегодня:\n Ухудшение состояния.\n Советуем воздержаться от работы.")
                    elif (f1 == "3" or f1 == "2") and (f2 == "2" or f2 == "3") and f3 == "1":
                        self.label_22.setText(
                            f"Ваш прогноз на сегодня:\n Возможны головные боли и апатия.")
                    else:
                        self.label_22.setText(
                            f"Ваш прогноз на сегодня:\n Возможны головные боли и слабость.\n Советуем делать перерывы в работе и\n проветривать помещение")
            else:
                self.label_22.setText("Недостаточно данных для прогноза")
        self.label_9.setText(f"Здравствуйте, {self.person}")
        self.label_22.resize(self.label_22.sizeHint())

    def back(self):
        self.working_clock.start()
        uic.loadUi('цэ.ui', self)
        self.test_flag = False
        self.update_()

    def test3(self):
        self.test_window.pushButton_7.setEnabled(True)
        self.test_window.pushButton_8.setEnabled(True)
        self.test_window.pushButton_9.setEnabled(True)
        self.test_window.pushButton_7.show()
        self.test_window.pushButton_8.show()
        self.test_window.pushButton_9.show()
        self.test_window.pushButton_4.hide()
        self.test_window.pushButton_5.hide()
        self.test_window.pushButton_6.hide()
        self.test_window.pushButton_4.setEnabled(False)
        self.test_window.pushButton_5.setEnabled(False)
        self.test_window.pushButton_6.setEnabled(False)
        self.test_window.label.setText("Ощущаете ли вы усталость?")
        self.test_window.pushButton_7.setText("Сильную")
        self.test_window.pushButton_8.setText("Слабую")
        self.test_window.pushButton_9.setText("Нет")
        self.test_window.pushButton_7.setFont(QFont('Yu Gothic UI Light', 12))
        self.test_window.pushButton_7.resize(71, 61)
        self.test_window.pushButton_8.resize(71, 61)
        self.test_window.pushButton_9.resize(71, 61)
        self.test_window.pushButton_8.setFont(QFont('Yu Gothic UI Light', 12))
        self.test_window.pushButton_9.setFont(QFont('Yu Gothic UI Light', 12))
        self.test_window.pushButton_7.clicked.connect(self.test3_1)
        self.test_window.pushButton_8.clicked.connect(self.test3_2)
        self.test_window.pushButton_9.clicked.connect(self.test3_3)

    def test_zapolnenie(self):
        print(self.test_sostyanie, self.test_bol, self.test_ustal)
        self.person = (self.connection.cursor().execute(f"""SELECT user FROM Users""").fetchall())[-1][0]
        self.connection.cursor().execute('INSERT INTO Diary VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);',
                (str(self.test_time[2]), str(self.test_time[1]), str(self.test_time[0]), self.label_3.text(), self.test_sostyanie, self.test_bol, self.test_ustal,
                                          self.person, self.temperature, self.humidity, self.pressure))
        self.connection.commit()
        self.test_window.close()

    def test3_1(self):
        self.test_ustal = 3
        self.test_zapolnenie()

    def test3_2(self):
        self.test_ustal = 2
        self.test_zapolnenie()

    def test3_3(self):
        self.test_ustal = 1
        self.test_zapolnenie()

    def test2(self):
        self.test_window.pushButton_4.setEnabled(True)
        self.test_window.pushButton_5.setEnabled(True)
        self.test_window.pushButton_6.setEnabled(True)
        self.test_window.label.setText("Ощущаете ли вы головную боль?")
        self.test_window.pushButton_4.setText("Сильную")
        self.test_window.pushButton_5.setText("Слабую")
        self.test_window.pushButton_6.setText("Нет")
        self.test_window.pushButton.hide()
        self.test_window.pushButton_2.hide()
        self.test_window.pushButton_3.hide()
        self.test_window.pushButton.setEnabled(False)
        self.test_window.pushButton_2.setEnabled(False)
        self.test_window.pushButton_3.setEnabled(False)
        self.test_window.pushButton_4.setFont(QFont('Yu Gothic UI Light', 12))
        self.test_window.pushButton_4.resize(71, 61)
        self.test_window.pushButton_5.resize(71, 61)
        self.test_window.pushButton_6.resize(71, 61)
        self.test_window.pushButton_5.setFont(QFont('Yu Gothic UI Light', 12))
        self.test_window.pushButton_6.setFont(QFont('Yu Gothic UI Light', 12))
        self.test_window.pushButton_4.clicked.connect(self.test2_1)
        self.test_window.pushButton_5.clicked.connect(self.test2_2)
        self.test_window.pushButton_6.clicked.connect(self.test2_3)

        self.test_window.pushButton_4.show()
        self.test_window.pushButton_5.show()
        self.test_window.pushButton_6.show()

    def test2_1(self):
        self.test_bol = 3
        self.test3()

    def test2_2(self):
        self.test_bol = 2
        self.test3()

    def test2_3(self):
        self.test_bol = 1
        self.test3()

    def test(self):
        self.test_window = QMainWindow()
        uic.loadUi('цэ2.ui', self.test_window)
        self.test_window.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)
        self.test_window.setWindowOpacity(0.9)
        self.test_window.label.setFont(QFont('Yu Gothic UI Light', 14))
        self.test_window.label.move(65, 60)
        self.test_window.pushButton.setIcon(QIcon('good.png'))
        self.test_window.pushButton.setIconSize(QtCore.QSize(58, 58))
        self.test_window.pushButton_2.setIcon(QIcon(r'very_good.png'))
        self.test_window.pushButton_2.setIconSize(QtCore.QSize(65, 65))
        self.test_window.pushButton_3.setIcon(QIcon(r'so_so.png'))
        self.test_window.pushButton_3.setIconSize(QtCore.QSize(85, 85))
        self.test_window.pushButton.clicked.connect(self.test_1)
        self.test_window.pushButton_2.clicked.connect(self.test_2)
        self.test_window.pushButton_3.clicked.connect(self.test_3)
        self.test_window.pushButton_4.setEnabled(False)
        self.test_window.pushButton_5.setEnabled(False)
        self.test_window.pushButton_6.setEnabled(False)
        self.test_window.pushButton_7.setEnabled(False)
        self.test_window.pushButton_8.setEnabled(False)
        self.test_window.pushButton_9.setEnabled(False)

        self.test_window.pushButton_4.hide()
        self.test_window.pushButton_5.hide()
        self.test_window.pushButton_6.hide()
        self.test_window.pushButton_7.hide()
        self.test_window.pushButton_8.hide()
        self.test_window.pushButton_9.hide()
        self.test_window.show()

    def test_1(self):
        self.test_sostyanie = 3
        self.test2()

    def test_2(self):
        self.test_sostyanie = 2
        self.test2()

    def test_3(self):
        self.test_sostyanie = 1
        self.test2()


    def registration(self):
        self.registration_window = QMainWindow()
        uic.loadUi('registration.ui', self.registration_window)
        self.registration_window.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)
        self.registration_window.setWindowOpacity(0.75)
        self.registration_window.pushButton_2.hide()
        self.registration_window.pushButton_3.hide()
        self.registration_window.pushButton_4.hide()
        self.registration_window.pushButton_2.setEnabled(False)
        self.registration_window.pushButton_3.setEnabled(False)
        self.registration_window.pushButton_4.setEnabled(False)
        self.registration_window.pushButton_5.hide()
        self.registration_window.pushButton_5.setEnabled(False)
        self.registration_window.pushButton_6.hide()
        self.registration_window.pushButton_6.setEnabled(False)
        self.registration_window.pushButton.clicked.connect(self.registration1)
        self.registration_window.lineEdit.hide()
        self.registration_window.show()

    def registration1(self):
        self.registration_window.label.setText("Как вас называть?")
        self.registration_window.label_2.setText("")
        self.registration_window.lineEdit.show()
        self.registration_window.pushButton_2.show()
        self.registration_window.pushButton_2.setEnabled(True)
        self.registration_window.pushButton.hide()
        self.registration_window.pushButton.setEnabled(False)
        self.registration_window.pushButton_2.clicked.connect(self.registration2_1)

    def registration2_1(self):
        self.person = self.registration_window.lineEdit.text()
        print([self.person])
        self.registration_window.lineEdit.hide()
        self.registration_window.label.setText("Имеются ли у вас заболевания?")
        self.registration_window.lineEdit.setText("")
        self.registration_window.pushButton_2.hide()
        self.registration_window.pushButton_2.setEnabled(False)
        self.registration_window.pushButton_5.show()
        self.registration_window.pushButton_5.setEnabled(True)
        self.registration_window.pushButton_6.show()
        self.registration_window.pushButton_6.setEnabled(True)
        self.registration_window.pushButton_5.clicked.connect(self.registration2_2)
        self.registration_window.pushButton_6.clicked.connect(self.registration3_1)

    def registration2_2(self):
        self.registration_window.lineEdit.show()
        self.registration_window.lineEdit.setText("")
        self.registration_window.pushButton_3.show()
        self.registration_window.pushButton_3.setEnabled(True)
        self.registration_window.pushButton_5.hide()
        self.registration_window.pushButton_5.setEnabled(False)
        self.registration_window.pushButton_6.hide()
        self.registration_window.pushButton_6.setEnabled(False)
        self.registration_window.label.setText("Какие у вас заболевания?")
        self.registration_window.pushButton_3.clicked.connect(self.registration3_1)

    def registration3_1(self):
        self.bolezn = self.registration_window.lineEdit.text()
        self.registration_window.lineEdit.hide()
        self.registration_window.label.setText("Имеются ли у вас аллергия?")
        self.registration_window.lineEdit.setText("")
        self.registration_window.pushButton_3.hide()
        self.registration_window.pushButton_3.setEnabled(False)
        self.registration_window.pushButton_5.show()
        self.registration_window.pushButton_5.setEnabled(True)
        self.registration_window.pushButton_6.show()
        self.registration_window.pushButton_6.setEnabled(True)
        self.registration_window.pushButton_5.clicked.connect(self.registration3_2)
        self.registration_window.pushButton_6.clicked.connect(self.zapolnenie)

    def registration3_2(self):
        self.registration_window.lineEdit.show()
        self.registration_window.pushButton_4.show()
        self.registration_window.pushButton_4.setEnabled(True)
        self.registration_window.lineEdit.setText("")
        self.registration_window.pushButton_5.hide()
        self.registration_window.pushButton_5.setEnabled(False)
        self.registration_window.pushButton_6.hide()
        self.registration_window.pushButton_6.setEnabled(False)
        self.registration_window.label.setText("На что у вас аллергия?")
        self.registration_window.pushButton_4.clicked.connect(self.zapolnenie)

    def zapolnenie(self):
        self.registration_window.pushButton_5.hide()
        self.registration_window.pushButton_5.setEnabled(False)
        self.registration_window.pushButton_6.hide()
        self.registration_window.pushButton_6.setEnabled(False)
        self.allergy = self.registration_window.lineEdit.text()
        self.connection.cursor().execute('INSERT INTO Users VALUES (?, ?, ?);',
                                         (self.person, self.allergy, self.bolezn))
        self.connection.commit()
        self.registration_window.close()
        self.test()

    def okno(self):
        self.test_clock = QtCore.QTimer()
        self.test_clock.setInterval(3000)
        self.test_clock.timeout.connect(self.okno)
        self.test_clock.start()
        if self.test_schetchik == 1:
            self.test_clock.start()
            count = self.connection.cursor().execute(f"""SELECT user FROM Users""").fetchall()
            if count:
                self.test()
            else:
                self.registration()
        self.test_schetchik += 1



    def update_(self):
        self.pushButton.clicked.connect(self.close)
        self.pushButton_2.setIcon(QIcon('icon.png'))
        self.pushButton_2.setIconSize(QtCore.QSize(128, 128))
        self.pushButton_2.clicked.connect(self.diary)

        count = self.connection.cursor().execute(f"""SELECT * FROM Diary""").fetchall()
        self.test_time = str(datetime.datetime.now())[:10].split("-")
        if len(count) == 0:
            self.okno()
        elif ((int(count[-1][0]) != int(self.test_time[2])) or (int(count[-1][1]) != int(self.test_time[1])) or (int(count[-1][2]) != int(self.test_time[0]))):
            self.okno()


        gismeteo = Gismeteo()
        search_results = gismeteo.search.by_query(self.data['city'])
        # search_results = gismeteo.search.by_query('Нигер')
        city_id = search_results[0]
        r = city_id.name
        # print(r)
        # print(city_id.name)
        city_id = search_results[0].id
        self.current = gismeteo.current.by_id(city_id)
        hour3 = gismeteo.step3.by_id(city_id, days=1)
       # print(current)

        self.time = str(datetime.datetime.now().time())[:5].split(":")

        k = (int(self.time[0]) + 3) // 3
        if k > 7:
            hour3 = gismeteo.step3.by_id(city_id, days=2)
            k = k % 8


        self.hour3_temperature = hour3[k].temperature.air.c
        self.hour3_humidity = hour3[k].humidity.percent
        self.hour3_pressure = hour3[k].pressure.mm_hg_atm
        self.hour3_icon = hour3[k].icon
        self.hour3_time = ((hour3[k].date.local).split()[1][:5])

        if k+2 > 7:
            hour3 = gismeteo.step3.by_id(city_id, days=2)
            k = k % 8

        if k+1 > 7:
            hour3 = gismeteo.step3.by_id(city_id, days=2)
            k = k % 8

        self.hour6_temperature = hour3[k+1].temperature.air.c
        self.hour6_humidity = hour3[k+1].humidity.percent
        self.hour6_pressure = hour3[k+1].pressure.mm_hg_atm
        self.hour6_icon = hour3[k+1].icon
        self.hour6_time = ((hour3[k+1].date.local).split()[1][:5])

        self.hour9_temperature = hour3[k+2].temperature.air.c
        self.hour9_humidity = hour3[k+2].humidity.percent
        self.hour9_pressure = hour3[k+2].pressure.mm_hg_atm
        self.hour9_icon = hour3[k+2].icon
        self.hour9_time = ((hour3[k+2].date.local).split()[1][:5])

        weekd = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']
        month = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь',
                 'Ноябрь', 'Декабрь']
        self.label.setText(str(r))
        self.label.resize(self.label.sizeHint())
        self.label.move(740 - self.label.width(), 25)
        self.temperature = str(self.current.temperature.air.c)
        self.humidity = str(self.current.humidity.percent)
        self.pressure = str(self.current.pressure.mm_hg_atm)
        self.label_2.setText(f'{str(self.current.temperature.air.c)}°')
        self.label_2.resize(self.label_2.sizeHint())
        self.label_4.setText(f"💦 {str(self.current.humidity.percent)}%")
        #a = (str(datetime.datetime.now()).split())[1]
        #time = (a.split('.'))[0]
        self.label_5.setText(f"↓ {str(self.current.pressure.mm_hg_atm)} мм")
        self.label_6.setText(str(datetime.datetime.now().time())[:5])

        #print(self.time)
        # self.label_6.setText('22:15')
        description = str(self.current.description.full)
        self.label_8.setText('')
        if 'Ясно' in description:
            self.label_9.setStyleSheet(
                "QLabel {background-color: qlineargradient(spread: pad, x1:0, y1:0.5, x2:1, y2:0.5, stop:0 rgba(15, 147, 255, 150), stop:1 rgba(250 , 250, 250, 150)); border-radius: 35%}")
            self.gif = QMovie("photo\gifgivecom.gif")
        if 'Пасмурно' in description:
            self.label_9.setStyleSheet(
                "QLabel {background-color: qlineargradient(spread: pad, x1:0, y1:0.5, x2:1, y2:0.5, stop:0 rgba(125, 125, 125, 150), stop:1 rgba(250 , 250, 250, 150)); border-radius: 35%}")
            self.gif = QMovie("photo\ChM.gif")
            self.gif.setSpeed(50)
        if 'блачно' in description:
            self.label_9.setStyleSheet(
                "QLabel {background-color: qlineargradient(spread: pad, x1:0, y1:0.5, x2:1, y2:0.5, stop:0 rgba(219, 239, 255, 150), stop:1 rgba(250 ,250, 250, 150)); border-radius: 35%}")
            self.gif = QMovie("photo\облачно.gif")
            self.gif.setSpeed(50)
        if ',' in description:
            description, description1 = str(self.current.description.full).split(', ')[:2]
            self.label_8.setText(description1)
            self.label_8.resize(self.label_8.sizeHint())
            self.label_3.setText(description)
            self.label_3.resize(self.label_3.sizeHint())
            self.label_3.move(385 - (self.label_3.width()) // 2, 250)
            self.label_8.move(385 - (self.label_8.width()) // 2, 280)
            if 'дождь' in description1:
                self.gif = QMovie("photo\дождь.gif")
                self.gif.setSpeed(50)
            if 'гроза' in description1:
                self.gif = QMovie("photo\OtZ.gif")
        else:
            self.label_3.setText(description)
            self.label_3.resize(self.label_3.sizeHint())
            self.label_3.move(385 - (self.label_3.width()) // 2, 270)
        self.label_3.setText(description)
        self.label_3.resize(self.label_3.sizeHint())
        self.label_11.setText(
            f"{weekd[datetime.datetime.today().weekday()]}, {datetime.datetime.now().day} {month[datetime.datetime.now().month - 1]}")
        self.label_11.resize(self.label_11.sizeHint())
        self.label_11.move(740 - self.label_11.width(), self.label_11.y())
        self.label_8.resize(self.label_8.sizeHint())
        self.gif.setScaledSize(QtCore.QSize(800, 1000))
        self.label_7.setMovie(self.gif)
        self.label_7.resize(800, 600)
        self.gif.start()
        self.show()
        pixmap = QtGui.QPixmap(f'photo\{self.current.icon}.png')
        self.label_10.setPixmap(pixmap)
        self.label_10.setScaledContents(True)
        self.label_10.resize(130, 85)

    def display_clock(self):
        self.label_6.setText(str(datetime.datetime.now()))


if __name__ == '__main__':
    app = QApplication(sys.argv)
ex = MainWindow()
ex.show()
sys.exit(app.exec())
con.slose()
