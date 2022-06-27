import sqlite3
import sys
import os
import hashlib
from datetime import timedelta, datetime
from CheckPhoneNumber import checkPhoneNumber
from CheckPassword import checkPassword

from PyQt5 import uic
from PyQt5.QtCore import QTime, QTimer
from PyQt5.QtGui import QPixmap, QPalette, QBrush, QFontDatabase, QFont
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QTableWidgetItem, QAbstractItemView, QTableWidget, \
    QPushButton
from PyQt5.QtWidgets import QMainWindow


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.Load()

    def Load(self):
        uic.loadUi('Ui/Main.ui', self)
        self.setWindowTitle('Главная страница')
        # Подключение кнопок к фукнциям
        self.registration_button.clicked.connect(self.registrar)
        self.admin_button.clicked.connect(self.administrator)
        self.login_button.clicked.connect(self.login)
        # Прогрузка шрифтов и стилей
        self.loadFontFamilies()
        self.setBackground()
        self.setStylesForTheButtons()

    def loadFontFamilies(self):
        # Загрузка в базу необходимых шрифтов
        QFontDatabase.addApplicationFont("Font-families/Arkhip.ttf")
        QFontDatabase.addApplicationFont("Font-families/Evgenia Deco.ttf")

    def setBackground(self):
        # Установка заднего фона на главное окно
        # Создание экземпляра класса QPixmap
        background = QPixmap("Images/tab_background.jpg").scaled(self.width(), self.height())
        # Загрузка палитры главного окна
        palette = self.palette()
        # Установка кисти для палитры
        palette.setBrush(QPalette.Background, QBrush(background))
        # Установка палитры на главное окно
        self.setPalette(palette)
        self.setFixedSize(1024, 720)

    def setStylesForTheButtons(self):
        # Установка стилей для кнопок
        self.setStyleForTheButton(self.login_button)
        self.setStyleForTheButton(self.registration_button)
        self.setStyleForTheButton(self.admin_button)

    def setStyleForTheButton(self, button):
        # Установка шрифта для кнопки
        button.setFont(QFont("Arkhip", 8))
        # Установка стилей QSS
        button.setStyleSheet("QPushButton {background-color: white;"
                             "font-size: 14px;"
                             "color: #D1A961;"
                             "border-radius: 10px;"
                             "border: 2px solid #D1A961;}"

                             "QPushButton::hover{background-color : #222222;"
                             "color: #D1A961;}")

    def administrator(self):
        # Высвечивание нового окна и закрытие старого
        self.admin = WorkingWithCinemaTheatresWindow()
        self.admin.show()
        self.close()

    def registrar(self):
        # Высвечивание нового окна и закрытие старого
        self.registration = RegistrationWindow()
        self.registration.show()
        self.close()

    def login(self):
        # Высвечивание нового окна и закрытие старого
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()


class RegistrationWindow(Main):
    def Load(self):
        uic.loadUi('Ui/Registration for user.ui', self)
        self.setWindowTitle('Registration')

        self.connection = sqlite3.connect("Project_one.db")
        # Подключение функций к эвентам QLineEdit и QPushButton
        self.name.textChanged.connect(self.changeInNames)
        self.surname.textChanged.connect(self.changeInNames)
        self.phone.textChanged.connect(self.phoneCheck)
        self.password.textChanged.connect(self.passwordCheck)
        self.password_checking.textChanged.connect(self.passwordVCheck)
        self.login.textChanged.connect(self.loginCheck)
        self.registration.clicked.connect(self.registrar)
        # Вызов главных функций
        self.setConditions()
        self.loadFontFamilies()
        self.setBackground()
        self.setStylesForTheLabels()
        self.setStylesForTheLineEdits()
        self.setStylesForTheCircles()
        self.setStylesForThePasswordErrorsLabels()
        self.customizationOfTheButtons()

    def setConditions(self):
        # Установка начальных значений для переменных пользователя
        self.login_value = False
        self.name_value = False
        self.surname_value = False
        self.phone_value = False
        self.password_value = False
        self.password_check_value = False

    def customizationOfTheButtons(self):
        self.registration.setFont(QFont("Arkhip", 8))
        self.registration.setStyleSheet("QPushButton {background-color: white;"
                             "font-size: 14px;"
                             "color: #D1A961;"
                             "border-radius: 10px;"
                             "border: 2px solid #D1A961;}"

                             "QPushButton::hover{background-color : #222222;"
                             "color: #D1A961;}")
        self.registration.clicked.connect(self.registrar)

        self.come_back.setFont(QFont("Arkhip", 8))
        self.come_back.setStyleSheet("QPushButton {background-color: white;"
                                        "font-size: 14px;"
                                        "color: #D1A961;"
                                        "border-radius: 10px;"
                                        "border: 2px solid #D1A961;}"

                                        "QPushButton::hover{background-color : #222222;"
                                        "color: #D1A961;}")
        self.come_back.clicked.connect(self.comeBack)

    def setStylesForTheLabels(self):
        # Установка стилей для QLabels
        self.setStyleForTheLabel(self.label_login)
        self.setStyleForTheLabel(self.label_name)
        self.setStyleForTheLabel(self.label_surname)
        self.setStyleForTheLabel(self.label_phone)
        self.setStyleForTheLabel(self.label_password)
        self.setStyleForTheLabel(self.label_password_check)

    def setStyleForTheLabel(self, label):
        label.setFont(QFont("Arkhip", 10))
        label.setStyleSheet("color: #EBA606;"
                                   "font-families: Arkhip;")

    def setStylesForTheLineEdits(self):
        # Установка стилей для QLineEdits
        self.setStyleForTheLineEdit(self.login)
        self.setStyleForTheLineEdit(self.name)
        self.setStyleForTheLineEdit(self.surname)
        self.setStyleForTheLineEdit(self.phone)
        self.setStyleForTheLineEdit(self.password)
        self.setStyleForTheLineEdit(self.password_checking)

    def setStyleForTheLineEdit(self, lineEdit):
        lineEdit.setFont(QFont("Arkhip", 10))
        lineEdit.setStyleSheet("border: 0px solid #000000;"
                                "background-color: #f7f7f7;"
                                "background-image: url(Images/Background for label шаблон.svg);"
                                "padding-left: 32px;")

    def setStylesForTheCircles(self):
        # Установка начального стиля для свойственных кругов
        self.setDefaultCircle(self.circle_login)
        self.setDefaultCircle(self.circle_name)
        self.setDefaultCircle(self.circle_surname)
        self.setDefaultCircle(self.circle_phone)
        self.setDefaultCircle(self.circle_password)
        self.setDefaultCircle(self.circle_password_check)

    def setDefaultCircle(self, label):
        # Установка стандартного стиля круга
        label.setFixedSize(15, 15)
        label.setStyleSheet("border-image: url(Images/Circle.svg);"
                                       "text-align: left;")

    def setSuccessfullyCircle(self, label):
        # Установка стиля круга, для правильного резутата
        label.setFixedSize(15, 15)
        label.setStyleSheet("border-image: url(Images/Successfully circle.svg);"
                                       "text-align: left;")

    def setErrorCircle(self, label):
        # Установка стиля круга, для ошибки
        label.setFixedSize(15, 15)
        label.setStyleSheet("border-image: url(Images/Error circle.svg);"
                                       "text-align: left;")

    def setStylesForThePasswordErrorsLabels(self):
        # Установка стандартного стиля для полей пароля
        self.setDefault(self.length)
        self.setDefault(self.letter)
        self.setDefault(self.number)
        self.setDefault(self.three_letters)

    def setDefault(self, label):
        # Установка стандартного стиля для поля пароля
        font = QFont("Arkhip", 10)
        label.setFont(font)
        label.setStyleSheet("color: grey;"
                            "padding-left: 25px;")

    def setSuccessfully(self, label):
        # Установка стиля для поля пароля, в случае правильности условия
        font = QFont("Arkhip", 10)
        label.setFont(font)
        label.setStyleSheet("color: #3EFF00;"
                            "padding-left: 25px;")

    def setError(self, label):
        # Установка стиля для поля пароля, в случае неправильности условия
        font = QFont("Arkhip", 10)
        label.setFont(font)
        label.setStyleSheet("color: #FF1300;"
                            "padding-left: 25px;")

    def comeBack(self):
        # Вызыв главного окна и закрытие текущего
        ex.show()
        self.close()

    def loginCheck(self):
        # Проверка логина
        self.login_value = False
        # В случае пустого поля установка стандартного круга и отчистка поля ошибки для логина
        if not self.login.text():
            self.setDefaultCircle(self.circle_login)
            self.login_error.clear()
        else:
            # Получение всех логинов пользователей
            res = [el[0] for el in self.connection.cursor().execute("""SELECT login FROM Users""").fetchall()]
            # При наличии такого логина, вызывается ошибка "Username is busy"
            if self.login.text() in res:
                self.setErrorCircle(self.circle_login)
                self.login_error.setText("Username is busy.")
                self.setError(self.login_error)
                return False
            # В случае короткого логина, вызыв ошибки "Username is too short"
            elif len(self.login.text()) < 3:
                self.setErrorCircle(self.circle_login)
                self.login_error.setText("Username is too short.")
                self.setError(self.login_error)
                return False
            # В случае успеха присвоение переменной логина текста из соответствующего QLineEdit
            else:
                self.login_value = self.login.text()
                self.setSuccessfullyCircle(self.circle_login)
                self.login_error.clear()
        return True

    def changeInNames(self):
        if self.sender().objectName() == "name":
            self.name_value = False
            if len(self.sender().text()) > 3:
                self.name_value = self.name.text()
                self.setSuccessfullyCircle(self.circle_name)
            elif not len(self.sender().text()):
                self.setDefaultCircle(self.circle_name)
            else:
                self.setErrorCircle(self.circle_name)
        if self.sender().objectName() == "surname":
            self.surname_value = False
            if len(self.sender().text()) > 3:
                self.surname_value = self.surname.text()
                self.setSuccessfullyCircle(self.circle_surname)
            elif not len(self.sender().text()):
                self.setDefaultCircle(self.circle_surname)
            else:
                self.setErrorCircle(self.circle_surname)

    def phoneCheck(self):
        self.phone_value = False
        if not len(self.phone.text()):
            print(1)
            self.setDefaultCircle(self.circle_phone)
            self.phone_error.clear()
        else:
            answer = checkPhoneNumber(self.phone.text())
            if answer[0] == '+':
                self.phone_value = answer
                self.setSuccessfullyCircle(self.circle_phone)
                self.phone_error.clear()
            else:
                self.setErrorCircle(self.circle_phone)
                self.phone_error.setText(answer)
                self.setError(self.phone_error)

    def passwordCheck(self):
        self.passwordVCheck()
        self.password_value = False
        if not self.password.text():
            self.setDefaultCircle(self.circle_password)
            self.setStylesForThePasswordErrorsLabels()
        else:
            self.password_value = self.password.text()
            self.setSuccessfullyCircle(self.circle_password)
            self.setSuccessfully(self.length)
            self.setSuccessfully(self.letter)
            self.setSuccessfully(self.number)
            self.setSuccessfully(self.three_letters)
            answer = checkPassword(self.password.text())
            if answer:
                self.password_value = False
                self.setErrorCircle(self.circle_password)
                for element in answer:
                    if element == "Length":
                        self.setError(self.length)
                    if element == "No letter":
                        self.setError(self.letter)
                    if element == "No number":
                        self.setError(self.number)
                    if element == "Letters":
                        self.setError(self.three_letters)

    def passwordVCheck(self):
        self.password_check_value = False
        if not self.password_checking.text():
            self.setDefaultCircle(self.circle_password_check)
        elif self.password_checking.text() == self.password.text():
            self.password_check_value = True
            self.setSuccessfullyCircle(self.circle_password_check)
        else:
            self.setErrorCircle(self.circle_password_check)

    def registrar(self):
        if not self.login_value or not self.name_value or not self.surname_value or not \
                self.phone_value or not self.password_value or not self.password_check_value or not self.loginCheck():
            return
        salt = os.urandom(32) # Генерация соли в 32 байта
        key = hashlib.pbkdf2_hmac(
            'sha256', # Используемый алгоритм хэширования
            self.password_value.encode('utf-8'), # Конвектирование пароля в байты
            salt, # Предоставление соли
            100000,) # Производим 100000 итераций SHA-256
        self.connection.cursor().execute("INSERT INTO Users(login, name, surname, phone, salt, password) "
                                         "VALUES (?, ?, ?, ?, ?, ?)",
                                         (self.login_value, self.name_value, self.surname_value, self.phone_value, salt, key,))
        self.connection.commit()
        self.user_window = UserWindow()
        self.user_window.setName(self.login.text())
        self.user_window.show()
        self.close()


class LoginWindow(RegistrationWindow):
    def Load(self):
        uic.loadUi('Ui/LoginWindow.ui', self)
        self.setWindowTitle('Login')
        self.connection = sqlite3.connect("Project_one.db")

        self.login_button.clicked.connect(self.login)
        self.come_back.clicked.connect(self.comeBack)

        self.username.textChanged.connect(self.loginCleaner)
        self.password.textChanged.connect(self.passwordCleaner)

        self.loadFontFamilies()
        self.setBackground()
        self.setStylesForTheButtons()
        self.setStylesForTheLabels()
        self.setStylesForTheLineEdits()

    def setStylesForTheButtons(self):
        # Set styles for the PushButtons
        self.setStyleForTheButton(self.login_button)
        self.setStyleForTheButton(self.come_back)

    def setStylesForTheLabels(self):
        self.setStyleForTheLabel(self.label_login)
        self.setStyleForTheLabel(self.label_password)
        self.setStyleForTheLabel(self.login_error)
        self.setStyleForTheLabel(self.password_error)

    def setStylesForTheLineEdits(self):
        self.setStyleForTheLineEdit(self.username)
        self.setStyleForTheLineEdit(self.password)

    def login(self):
        try:
            # Запрос для получения соли и пароля введенного логина
            result = self.connection.cursor().execute("""SELECT salt, password FROM Users
                                                        WHERE login = ?""", (self.username.text(),)).fetchone()
            # Если данных не нашлось, выводится ошибка логина
            if not result:
                self.login_error.setText("Логин не найдет")
                self.setError(self.login_error)
                return
            new_key = hashlib.pbkdf2_hmac(
                'sha256',
                self.password.text().encode('utf-8'), # Предоставление введенного пароля
                result[0], # Получение соли из запроса
                100000
            )
            # Если пароли не сходятся, выводится ошибка пароля, иначе происходит переход на страницу пользователя
            if new_key != result[1]:
                self.password_error.setText("Неправильный пароль")
                self.setError(self.password_error)
                return
            self.login_window = UserWindow()
            self.login_window.setName(self.username.text())
            self.login_window.show()
            self.username.clear()
            self.password.clear()
            self.close()
        except Exception as Er:
            print(Er)

    def loginCleaner(self):
        self.login_error.clear()
        self.password_error.clear()

    def passwordCleaner(self):
        self.password_error.clear()


class UserWindow(RegistrationWindow):
    def __init__(self):
        super().__init__()
        self.Load()

    def Load(self):
        uic.loadUi("Ui/User Window.ui", self)
        self.setWindowTitle("Пользовательское окно")
        self.setFixedSize(1920, 1011)
        self.move(0, 40)
        self.connection = sqlite3.connect("Project_one.db")
        self.login = None

        self.schedule_button.clicked.connect(self.schedule)
        self.search_button.clicked.connect(self.search)
        self.buy_button.clicked.connect(self.buying)
        self.help_button.clicked.connect(self.helping)
        self.exit_button.clicked.connect(self.out)

        self.setBackground()
        self.loadFontFamilies()
        self.setStyleForTheButton(self.schedule_button)
        self.setStyleForTheButton(self.search_button)
        self.setStyleForTheButton(self.buy_button)
        self.setStyleForTheButton(self.exit_button)
        self.setStyleForTheButton(self.help_button)

    def setName(self, login):
        result = self.connection.cursor().execute("SELECT name, surname FROM Users WHERE login = ?",
                                                  (login,)).fetchone()
        self.names.setText(result[0] + ' ' + result[1])
        self.login = login

    def setBackground(self):
        # Set background for main window
        background = QPixmap("Images/tab_background - копия.jpg").scaled(self.width(), self.height())
        palete = self.palette()
        palete.setBrush(QPalette.Background, QBrush(background))
        self.setPalette(palete)
        # Set background for labels of usernames
        self.names.setAutoFillBackground(True)
        background = QPixmap("Images/Background for label answer.svg").scaled(self.names.width(), self.names.height())
        palete = self.names.palette()
        palete.setBrush(QPalette.Background, QBrush(background))
        self.names.setPalette(palete)
        self.names.setFont(QFont("Arkhip", 8))

    def schedule(self):
        self.movies = MonthSchedule()
        self.movies.setLogin(self.login)
        self.movies.show()

    def search(self):
        self.searcher = MoviesSearch()
        self.searcher.setLogin(self.login)
        self.searcher.show()

    def buying(self):
        self.buyer = BuyTickets()
        self.buyer.setLogin(self.login)
        self.buyer.show()

    def helping(self):
        self.help = HelpWindow()
        self.help.show()

    def out(self):
        ex.show()
        self.close()


class MoviesSearch(LoginWindow):
    def Load(self):
        uic.loadUi("Ui/MovieSearch.ui", self)
        self.setWindowTitle("Поиск фильма")
        self.connection = sqlite3.connect("Project_one.db")

        self.movies.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.search.clicked.connect(self.searcher)
        self.buy_button.clicked.connect(self.buy)

        self.title.textChanged.connect(self.cleanerError)
        self.date.dateChanged.connect(self.cleanerError)

        self.loadFontFamilies()
        self.setBackground()
        self.setStylesForTheLabels()
        self.setStyleForTheLineEdit(self.title)
        self.setStyleForTheLineEdit(self.date)
        self.setStyleForTheButton(self.search)
        self.setStyleForTheButton(self.buy_button)

    def setStylesForTheLabels(self):
        self.setStyleForTheLabel(self.label_title)
        self.setStyleForTheLabel(self.label_date)
        self.any.setFont(QFont("Arkhip"))

    def setLogin(self, login):
        self.login = login

    def searcher(self):
        if not self.title.text() and self.any.isChecked():
            return
        result = self.connection.cursor().execute("""SELECT title, begin, end, duration, age_limit, hall FROM Movies""").fetchall()
        movies = result.copy()
        result.clear()
        # Отсеиваются фильмы, в которых нет введенных пользователем символов
        for movie in movies:
            if self.title.text().lower() in movie[0].lower():
                result.append(movie)
        # Если выбран поиск по дате, отсеиваются неподходящие фильмы
        if not self.any.isChecked():
            date = self.date.date().toString("yyyy-MM-dd")
            movies = result.copy()
            result.clear()
            for movie in movies:
                if date == movie[1].split()[0]:
                    result.append(movie)
        if not result:
            self.error.setText("Фильмов не найдено")
            self.error.setStyleSheet("color: red")
            return
        self.loadTable(result)

    def loadTable(self, movies):
        self.movies.setColumnCount(6)
        self.movies.setRowCount(0)
        # Заполним заголовки для столбцов
        self.movies.setHorizontalHeaderLabels(["Название", "Начало", "Конец", "Продолжительность",
                                               "Возрастное ограничение", "Зал"])
        # Заполняем таблицу элементами
        for i, row in enumerate(movies):
            self.movies.setRowCount(
                self.movies.rowCount() + 1)
            for j, elem in enumerate(row):
                self.movies.setItem(
                    i, j, QTableWidgetItem(str(elem)))
        self.movies.setFont(QFont("Arkhip", 8))
        self.movies.setColumnWidth(0, 200)
        self.movies.setCurrentItem(self.movies.item(-1, -1))

    def cleanerError(self):
        self.error.clear()

    def buy(self):
        if self.movies.currentRow() == -1:
            return
        result = self.connection.cursor().execute("""SELECT x, y, busy FROM Places
                                                                WHERE movie = (SELECT id FROM Movies
                                                                WHERE begin = ? AND hall = ?)""",
                                                  (self.movies.item(self.movies.currentRow(), 1).text(),
                                                   self.movies.item(self.movies.currentRow(), 5).text(),)).fetchall()
        id = self.connection.cursor().execute("""SELECT id FROM Movies
                                                                WHERE begin = ? AND hall = ?""",
                                              (self.movies.item(self.movies.currentRow(), 1).text(),
                                               self.movies.item(self.movies.currentRow(), 5).text(),)).fetchone()


        class ShowPlaces(LoginWindow):
            def Load(self):
                self.setWindowTitle("Просмотр мест")
                self.setFixedSize(1024, 711)
                self.connection = sqlite3.connect("Project_one.db")
                self.id = None
                self.login = None

                self.dict_of_buy = {}

                self.buy = QPushButton("Купить", self)
                self.buy.move(800, 580)
                self.buy.clicked.connect(self.buyer)

                self.loadFontFamilies()
                self.setBackground()
                self.setStyleForTheButton(self.buy)

            def showPlaces(self, places, id, login):
                self.id = id
                self.login = login
                for place in places:
                    button = QPushButton(self)
                    button.resize(30, 30)
                    button.move(place[0], place[1])
                    button.clicked.connect(self.marker)
                    button.setStyleSheet("QPushButton {background-color: white;"
                                         "border-radius: 10px;"
                                         "border: 1px solid gold}"
                                         "QPushButton:hover {background-color: grey}")
                    if place[2] != "False":
                        if place[2] == self.login:
                            button.setStyleSheet("QPushButton {background-color: green;"
                                                 "border-radius: 10px;"
                                                 "border: 1px solid black}")
                        else:
                            button.setStyleSheet("QPushButton {background-color: red;"
                                                 "border-radius: 10px;"
                                                 "border: 1px solid black}")
                        button.setEnabled(False)

            def marker(self):
                if (self.sender().x(), self.sender().y()) not in self.dict_of_buy.keys():
                    self.sender().setStyleSheet("QPushButton {background-color: #28F7B2;"
                                                "border-radius: 10px;"
                                                "border: 1px solid gold}"
                                                "QPushButton:hover {background-color: grey}")
                    self.dict_of_buy[(self.sender().x(), self.sender().y())] = self.sender()
                else:
                    self.sender().setStyleSheet("QPushButton {background-color: white;"
                                                "border-radius: 10px;"
                                                "border: 1px solid gold}"
                                                "QPushButton:hover {background-color: grey}")
                    self.dict_of_buy.pop((self.sender().x(), self.sender().y()))

            def buyer(self):
                if not self.dict_of_buy:
                    return
                for place in self.dict_of_buy.keys():
                    self.connection.cursor().execute("""UPDATE Places
                                                                SET busy = ?
                                                                WHERE movie = ?
                                                                AND x = ? AND y = ?""",
                                                     (self.login, self.id, place[0], place[1],))
                    self.dict_of_buy[place].setStyleSheet("QPushButton {background-color: green;"
                                                          "border-radius: 10px;"
                                                          "border: 1px solid black}")
                    self.dict_of_buy[place].setEnabled(False)
                self.connection.commit()
                self.dict_of_buy.clear()


        self.shower = ShowPlaces()
        self.shower.showPlaces(result, *id, self.login)
        self.shower.show()


class MonthSchedule(MoviesSearch):
    def Load(self):
        self.setFixedSize(1024, 711)
        self.setWindowTitle("Расписание на месяц")
        self.connection = sqlite3.connect("Project_one.db")

        self.movies = QTableWidget(self)
        self.movies.resize(550, 500)
        self.movies.move(450, 100)
        self.movies.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.buy_button = QPushButton("Купить билеты", self)
        self.buy_button.resize(140, 30)
        self.buy_button.move(850, 630)
        self.buy_button.clicked.connect(self.buy)

        self.setBackground()
        self.loadFontFamilies()
        self.loadTable()
        self.setStyleForTheButton(self.buy_button)

    def loadTable(self):
        # Получим результат запроса фильмов на месяц
        res = self.connection.cursor().execute("""SELECT title, begin, end, duration, age_limit, hall FROM Movies
                                                    WHERE begin <= ?""",
                                               (datetime.now().date() + timedelta(days=30),)).fetchall()
        res.sort(key=lambda x: x[1])
        # Заполним размеры таблицы
        self.movies.setColumnCount(6)
        self.movies.setRowCount(0)
        # Заполним заголовки для столбцов
        self.movies.setHorizontalHeaderLabels(["Название", "Начало", "Конец", "Продолжительность",
                                               "Возрастное ограничение", "Кинозал"])
        # Заполняем таблицу элементами
        for i, row in enumerate(res):
            self.movies.setRowCount(
                self.movies.rowCount() + 1)
            for j, elem in enumerate(row):
                self.movies.setItem(
                    i, j, QTableWidgetItem(str(elem)))
        self.movies.setFont(QFont("Arkhip", 8))


class BuyTickets(LoginWindow):
    def Load(self):
        uic.loadUi("Ui/Buy tickets.ui", self)
        self.setWindowTitle("Покупка билетов.")
        self.connection = sqlite3.connect("Project_one.db")
        self.login = None

        self.title.textChanged.connect(self.loadTable)
        self.look_button.clicked.connect(self.buyer)

        self.movies.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.loadFontFamilies()
        self.setBackground()
        self.setStyleForTheLabel(self.label_name)
        self.setStyleForTheLineEdit(self.title)
        self.setStyleForTheButton(self.look_button)
        self.loadTable()
        self.movies.setFont(QFont("Arkhip", 8))

    def setLogin(self, login):
        self.login = login

    def loadTable(self):
        title = "%"
        if self.title.text():
            title = '%' + self.title.text() + '%'
        result = self.connection.cursor().execute("""SELECT title, begin, end, duration, age_limit, hall FROM Movies
                                                    WHERE title LIKE ?""", (title,)).fetchall()
        self.movies.setColumnCount(6)
        self.movies.setRowCount(0)
        self.movies.setHorizontalHeaderLabels(["Название", "Начало", "Конец", "Продолжительность",
                                               "Возрастное ограничение", "Кинозал"])
        for i, row in enumerate(result):
            self.movies.setRowCount(
                self.movies.rowCount() + 1)
            for j, elem in enumerate(row):
                self.movies.setItem(
                    i, j, QTableWidgetItem(str(elem)))
        self.movies.setCurrentItem(self.movies.item(-1, -1))

    def buyer(self):
        if self.movies.currentRow() == -1:
            return
        result = self.connection.cursor().execute("""SELECT x, y, busy FROM Places
                                                        WHERE movie = (SELECT id FROM Movies
                                                        WHERE begin = ? AND hall = ?)""",
                                                  (self.movies.item(self.movies.currentRow(), 1).text(),
                                                        self.movies.item(self.movies.currentRow(), 5).text(),)).fetchall()
        id = self.connection.cursor().execute("""SELECT id FROM Movies
                                                        WHERE begin = ? AND hall = ?""",
                                              (self.movies.item(self.movies.currentRow(), 1).text(),
                                                        self.movies.item(self.movies.currentRow(), 5).text(),)).fetchone()


        class ShowPlaces(LoginWindow):
            def Load(self):
                self.setWindowTitle("Просмотр мест")
                self.setFixedSize(1024, 711)
                self.connection = sqlite3.connect("Project_one.db")
                self.id = None
                self.login = None

                self.dict_of_buy = {}

                self.buy = QPushButton("Купить", self)
                self.buy.move(800, 580)
                self.buy.clicked.connect(self.buyer)

                self.loadFontFamilies()
                self.setBackground()
                self.setStyleForTheButton(self.buy)

            def showPlaces(self, places, id, login):
                self.id = id
                self.login = login
                for place in places:
                    button = QPushButton(self)
                    button.resize(30, 30)
                    button.move(place[0], place[1])
                    button.clicked.connect(self.marker)
                    button.setStyleSheet("QPushButton {background-color: white;"
                                         "border-radius: 10px;"
                                         "border: 1px solid gold}"
                                         "QPushButton:hover {background-color: grey}")
                    if place[2] != "False":
                        if place[2] == self.login:
                            button.setStyleSheet("QPushButton {background-color: green;"
                                                 "border-radius: 10px;"
                                                 "border: 1px solid black}")
                        else:
                            button.setStyleSheet("QPushButton {background-color: red;"
                                                 "border-radius: 10px;"
                                                 "border: 1px solid black}")
                        button.setEnabled(False)

            def marker(self):
                if (self.sender().x(), self.sender().y()) not in self.dict_of_buy.keys():
                    self.sender().setStyleSheet("QPushButton {background-color: #28F7B2;"
                                             "border-radius: 10px;"
                                             "border: 1px solid gold}"
                                             "QPushButton:hover {background-color: grey}")
                    self.dict_of_buy[(self.sender().x(), self.sender().y())] = self.sender()
                else:
                    self.sender().setStyleSheet("QPushButton {background-color: white;"
                                         "border-radius: 10px;"
                                         "border: 1px solid gold}"
                                         "QPushButton:hover {background-color: grey}")
                    self.dict_of_buy.pop((self.sender().x(), self.sender().y()))

            def buyer(self):
                if not self.dict_of_buy:
                    return
                for place in self.dict_of_buy.keys():
                    self.connection.cursor().execute("""UPDATE Places
                                                        SET busy = ?
                                                        WHERE movie = ?
                                                        AND x = ? AND y = ?""",
                                                     (self.login, self.id, place[0], place[1],))
                    self.dict_of_buy[place].setStyleSheet("QPushButton {background-color: green;"
                                                 "border-radius: 10px;"
                                                 "border: 1px solid black}")
                    self.dict_of_buy[place].setEnabled(False)
                self.connection.commit()
                self.dict_of_buy.clear()


        self.shower = ShowPlaces()
        self.shower.showPlaces(result, *id, self.login)
        self.shower.show()


class HelpWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.Load()

    def Load(self):
        uic.loadUi("Ui/HelpWindow.ui", self)
        self.setFixedSize(1024, 711)
        self.setWindowTitle("Помощь")

        self.loadFontFamilies()
        self.setStyleForTheHeader()
        self.setStyleForTheText()

    def loadFontFamilies(self):
        QFontDatabase.addApplicationFont("Font-families/Arkhip.ttf")

    def setStyleForTheHeader(self):
        self.header.setFont(QFont("Arkhip", 20))

    def setStyleForTheText(self):
        self.text.setFont(QFont("Arkhip", 8))


class WorkingWithCinemaTheatresWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.Load()

    def Load(self):
        uic.loadUi('Ui/Working.ui', self)
        self.setWindowTitle('Work with cinema theatres')
        self.setFixedSize(1920, 1011)
        self.move(0, 40)

        self.come_back.clicked.connect(self.comeBack)
        self.good_working.setText("Good work.")

        self.new_cinema_theatre.clicked.connect(self.createCinemaTheatre)
        self.new_hall.clicked.connect(self.createHall)
        self.add_movie.clicked.connect(self.newMovie)

        self.delete_cinema_theatre.clicked.connect(self.uninstallerCinemaTheatre)
        self.delete_hall.clicked.connect(self.uninstallerHall)
        self.delete_movie.clicked.connect(self.uninstallerMovie)

        self.loadFontFamilies()
        self.setBackground()
        self.create_clock()
        self.setStylesForTheAdditionalButton()
        self.setStylesForTheMainButtons()

    def create_clock(self):
        # Creating the label
        self.label = QLabel(self)
        # Resizing the label
        self.label.resize(700, 500)
        # Set the font to the label
        self.label.setFont(QFont('Evgenia Deco', 120))
        # Moving the label
        self.label.move(55, 625)
        # Set color for the text of the label
        self.label.setStyleSheet("color: white")

        # Creating the timer
        timer = QTimer(self)
        # Connecting the timer with the function
        timer.timeout.connect(self.showTime)
        # Starting the timer
        timer.start(1000)

        # Calling the function
        self.showTime()

    def showTime(self):
        currentTime = QTime.currentTime()
        displayTxt = currentTime.toString('hh:mm:ss')
        self.label.setText(displayTxt)

    def loadFontFamilies(self):
        # Downloading the fonts
        QFontDatabase.addApplicationFont("Font-families/Evgenia Deco.ttf")
        QFontDatabase.addApplicationFont("Font-families/Arkhip.ttf")
        QFontDatabase.addApplicationFont("Font-families/Pobeda Bold.ttf")

    def setBackground(self):
        # Set background for main window
        background = QPixmap("Images/Arministrator_background_three.jpg").scaled(1920, 1011)
        palette = self.palette()
        palette.setBrush(QPalette.Background, QBrush(background))
        self.setPalette(palette)

    def setStyleForTheMainButton(self, button):
            font = QFont("Arkhip", 50)
            button.setFont(font)
            button.setStyleSheet("QPushButton {background-color: #222222;"
                                 "font-size: 18px;"
                                 "color: white;"
                                 "border-radius: 22px;"
                                 "border: 2px solid #999999;}"

                                 "QPushButton::hover{background-color : white;"
                                 "color: black;}")

    def setStylesForTheAdditionalButton(self):
        # Set style for the button of come back
        self.come_back.setStyleSheet("QPushButton {background-color: #222222;"
                                     "font-size: 18px;"
                                     "color: white;"
                                     "border-radius: 18px;"
                                     "border: 2px solid #999999;}"

                                     "QPushButton::hover{background-color : white;"
                                     "color: black;}")
        # Set styles for the PushButtons
        font = QFont('Pobeda', 70)
        self.good_working.setFont(font)
        self.good_working.setStyleSheet("color: white")

    def setStylesForTheMainButtons(self):
        # Set style for the main buttons
        # Buttons for adding
        self.setStyleForTheMainButton(self.new_cinema_theatre)
        self.setStyleForTheMainButton(self.new_hall)
        self.setStyleForTheMainButton(self.add_movie)
        # Buttons for uninstalling
        self.setStyleForTheMainButton(self.delete_cinema_theatre)
        self.setStyleForTheMainButton(self.delete_hall)
        self.setStyleForTheMainButton(self.delete_movie)

    def createCinemaTheatre(self):
        self.creator = CreatorOfCinemaTheatre()
        self.creator.show()

    def uninstallerCinemaTheatre(self):
        self.uninstaller = UninstallerOfCinemaTheatre()
        self.uninstaller.show()

    def createHall(self):
        self.creator = CreatorOfHall()
        self.creator.show()

    def uninstallerHall(self):
        self.uninstaller = UninstallerOfHall()
        self.uninstaller.show()

    def newMovie(self):
        self.creator = AddingMovie()
        self.creator.show()

    def uninstallerMovie(self):
        self.uninstaller = UninstallerOfMovie()
        self.uninstaller.show()

    def comeBack(self):
        self.admin = Main()
        self.admin.show()
        self.close()


class CreatorOfCinemaTheatre(QWidget):
    def __init__(self):
        super().__init__()
        self.Load()

    def Load(self):
        uic.loadUi("Ui/CreatingTheatre.ui", self)
        self.setWindowTitle("Creating a cinema theatre")
        self.connection = sqlite3.connect("Project_one.db")

        self.create.clicked.connect(self.creator)
        self.title.textChanged.connect(self.errorsClear)
        self.setStyleForThePushButton(self.create)

        self.loadFontFamilies()
        self.setBackground()
        self.setStylesForTheLabels()
        self.setStylesForTheLineEdits()
        self.setStylesForTheSpinBoxes()

    def loadFontFamilies(self):
        QFontDatabase.addApplicationFont("Font-families/Arkhip.ttf")

    def setBackground(self):
        # Set background for main window
        background = QPixmap("Images/CinemaTheatreBackground.jpg").scaled(640, 480)
        palette = self.palette()
        palette.setBrush(QPalette.Background, QBrush(background))
        self.setPalette(palette)
        self.setFixedSize(640, 480)

    def setStylesForTheLabels(self):
        self.setStyleForTheLabel(self.label_title)
        self.setStyleForTheLabel(self.label_count)

    def setStyleForTheLabel(self, label):
        label.setFont(QFont("Arkhip", 8))
        label.setStyleSheet("color: white;")

    def setStyleForThePushButton(self, button):
        button.setFont(QFont("Arkhip", 8))
        button.setStyleSheet("QPushButton {border-image:url(Images/Background for button.svg);}"
                             "QPushButton:hover {border-image:url(Images/Background for button hover.svg);"
                                                    "color: white;}")

    def setStylesForTheLineEdits(self):
        self.setStyleForTheLineEdit(self.title)

    def setStyleForTheLineEdit(self, lineEdit):
        lineEdit.setFont(QFont("Arkhip", 8))
        lineEdit.setStyleSheet("border: 2px solid white;"
                                  "border-radius: 6px;"
                                  "background-color: #e7ce89;")

    def setStylesForTheSpinBoxes(self):
        self.setStyleForTheSpinBox(self.count)

    def setStyleForTheSpinBox(self, spinBox):
        spinBox.setFont(QFont("Arkhip", 8))
        spinBox.setStyleSheet( "QSpinBox {border: 2px solid white;"
                                    "border-radius: 6px;"
                                    "background-color: #e7ce89;}"
                                    "QSpinBox::up-arrow {background-color: blue;}")
        spinBox.setButtonSymbols(2)

    def errorsClear(self):
        self.error.clear()

    def creator(self):
        if not self.title.text() or not self.count.value():
            return
        result = self.connection.cursor().execute("""SELECT title, max_count_of_halls, current_count_of_halls FROM Cinemas
                                                    WHERE title = ?""", (self.title.text(),)).fetchone()
        if result:
            self.error.setText("The title already exists.")
            self.error.setStyleSheet("color: red;")
            return
        self.connection.cursor().execute("""INSERT INTO Cinemas VALUES (?, ?, ?)""",
                                         (self.title.text(), self.count.value(), 0,))
        self.connection.commit()
        self.error.setText("Successfully created the cinema theatre.")
        self.error.setStyleSheet("color: green")


class UninstallerOfCinemaTheatre(CreatorOfCinemaTheatre):
    def Load(self):
        uic.loadUi("Ui/DeleteTheatre.ui", self)
        self.setWindowTitle("Delete a cinema theatre.")
        self.connection = sqlite3.connect("Project_one.db")

        self.delete_button.clicked.connect(self.uninstaller)

        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.createTable("""SELECT title, max_count_of_halls, 
                                current_count_of_halls FROM Cinemas""",
                         ["Навание", "Макс. кол-во кинозалов", "Кол-во кинозалов"], 3)

        self.loadFontFamilies()
        self.setBackground()
        self.setStyleForTheTable()
        self.setStyleForThePushButton(self.delete_button)

    def createTable(self, condition, header, column_count):
        result = self.connection.cursor().execute(condition).fetchall()
        # Заполним размеры таблицы
        self.table.setColumnCount(column_count)
        self.table.setRowCount(0)
        self.table.setHorizontalHeaderLabels(header)
        # Задаем размеры столбцам
        self.table.setColumnWidth(0, 200)
        self.table.setColumnWidth(1, 130)
        self.table.setColumnWidth(2, 130)
        # Заполняем таблицу элементами
        for i, row in enumerate(result):
            self.table.setRowCount(
                self.table.rowCount() + 1)
            for j, elem in enumerate(row):
                self.table.setItem(
                    i, j, QTableWidgetItem(str(elem)))
        self.table.setCurrentItem(self.table.item(-1, -1))

    def setStyleForTheTable(self):
        self.table.setFont(QFont("Arkhip"))
        self.table.setStyleSheet("QTableWidget"
                                 "{"
                                 "background: #222222;"
                                 "border: none;"
                                 "font-size: 12px;"
                                 "color: #D1A961"
                                 "}"
                                 "QTableWidget:item"
                                 "{"
                                 "border-bottom: 1px solid #eef1f7;"
                                 "}"
                                 "QTableWidget:item:selected"
                                 "{"
                                 "color: white;"
                                 "background: #111111;"
                                 "}"
                                 "QHeaderView::section"
                                 "{"
                                 "background-color: #333333;"
                                 "color: #999999;"
                                 "border-radius: 14px;"
                                 "}")

    def uninstaller(self):
        if self.table.currentRow() == -1:
            return
        title = self.table.item(self.table.currentRow(), 0).text()
        ids = self.connection.cursor().execute("""SELECT id FROM Movies 
                                                    WHERE hall IN (SELECT title FROM Halls
                                                    WHERE cinema = ?)""", (title,)).fetchall()
        for element in ids:
            self.uninstallerOfPlaces(*element)
        self.connection.cursor().execute("""DELETE FROM Movies
                                             WHERE Hall IN (SELECT title FROM Halls WHERE cinema = ?)""", (title,))
        self.connection.cursor().execute("""DELETE FROM Halls
                                                WHERE cinema = ?""", (title,))
        self.connection.cursor().execute("""DELETE FROM Cinemas
                                                WHERE title = ?""", (title,))
        self.connection.commit()
        self.createTable("""SELECT title, max_count_of_halls,
                                        current_count_of_halls FROM Cinemas""",
                         ["Навание", "Макс. кол-во кинозалов", "Кол-во кинозалов"], 3)

    def uninstallerOfPlaces(self, movie):
        self.connection.cursor().execute("""DELETE from Places
                                        WHERE movie = ?""", (movie,))
        self.connection.commit()


class CreatorOfHall(UninstallerOfCinemaTheatre):
    def Load(self):
        uic.loadUi("Ui/CreatingHall.ui", self)
        self.setWindowTitle("Create a hall.")
        self.connection = sqlite3.connect("Project_one.db")

        self.create.clicked.connect(self.creator)
        self.title.textChanged.connect(self.errorsClear)

        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.setBackground()
        self.loadFontFamilies()
        self.createTable("""SELECT title, max_count_of_halls, 
                                        current_count_of_halls FROM Cinemas""",
                         ["Навание", "Макс. кол-во кинозалов", "Кол-во кинозалов"], 3)
        self.setStyleForTheTable()
        self.setStyleForTheLabel(self.label_title)
        self.setStyleForTheLabel(self.select)
        self.setStyleForTheLineEdit(self.title)
        self.setStyleForThePushButton(self.create)

    def creator(self):
        if self.table.currentRow() == -1 or not self.title.text():
            return
        halls = self.connection.cursor().execute("""SELECT title FROM Halls
                                                        WHERE title = ?""", (self.title.text(),)).fetchone()
        if halls:
            self.error.setText("Название уже существует.")
            self.error.setStyleSheet("color: red;")
            return
        result = self.connection.cursor().execute("""SELECT max_count_of_halls, current_count_of_halls FROM Cinemas
                                                                WHERE title = ?""",
                                                  (self.table.item(self.table.currentRow(),
                                                                0).text(),)).fetchone()
        if result[0] == result[1]:
            self.error.setText("Колличество залов в кинотеатре заполнено.")
            self.error.setStyleSheet("color: red;")
            return
        self.connection.cursor().execute("""INSERT INTO Halls VALUES (?, ?, ?)""",
                                            (self.title.text(), 0,
                                             self.table.item(self.table.currentRow(),
                                                             0).text()))
        self.connection.cursor().execute("""UPDATE Cinemas
                                            SET current_count_of_halls = current_count_of_halls + 1
                                            WHERE title = ?""",
                                         (self.table.item(self.table.currentRow(), 0).text(),))
        self.connection.commit()
        self.error.setText("Кинозал успешно добавлен.")
        self.error.setStyleSheet("color: green")
        self.createTable("""SELECT title, max_count_of_halls, 
                                        current_count_of_halls FROM Cinemas""",
                         ["Навание", "Макс. кол-во кинозалов", "Кол-во кинозалов"], 3)


class UninstallerOfHall(UninstallerOfCinemaTheatre):
    def Load(self):
        uic.loadUi("Ui/DeleteTheatre.ui", self)
        self.setWindowTitle("Удаление зала.")
        self.connection = sqlite3.connect("Project_one.db")
        self.delete_button.clicked.connect(self.uninstaller)

        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.createTable("""SELECT * FROM Halls""",
                         ["Название", "Число фильмов", "Кинотеатр"], 3)
        self.setStyleForTheTable()
        self.loadFontFamilies()
        self.setBackground()
        self.setStyleForThePushButton(self.delete_button)

    def uninstaller(self):
        if self.table.currentRow() == -1:
            return
        title = self.table.item(self.table.currentRow(), 0).text()
        theatre = self.table.item(self.table.currentRow(), 2).text()
        ids = self.connection.execute("""SELECT id FROM Movies
                                            WHERE hall = ?""", (title,)).fetchall()
        for element in ids:
            self.uninstallerOfPlaces(element[0])
        self.connection.cursor().execute("""DELETE FROM Halls
                                                WHERE title = ?""", (title,))
        self.connection.cursor().execute("""DELETE FROM Movies
                                                WHERE hall = ?""", (title, ))
        self.connection.cursor().execute("""UPDATE Cinemas
                                            SET current_count_of_halls = current_count_of_halls - 1
                                            WHERE title = ?""", (theatre,))
        self.connection.commit()
        self.createTable("""SELECT * FROM Halls""",
                         ["Название", "Число фильмов", "Кинотеатр"], 3)


class AddingMovie(CreatorOfHall):
    def Load(self):
        uic.loadUi("Ui/AddingMovie.ui", self)
        self.setWindowTitle("Adding a movie")
        self.connection = sqlite3.connect("Project_one.db")

        self.add.clicked.connect(self.adding)

        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.loadFontFamilies()
        self.setBackground()
        self.createTable("SELECT * FROM Halls", ["Название", "Кол-во фильмов", "Кинотеатр"], 3)
        self.setStyleForTheTable()
        self.setStylesForTheLabels()
        self.setStylesForTheLineEdits()
        self.setStyleForThePushButton(self.add)
        self.setStyleForTheSpinBox(self.duration)
        self.setStyleForTheSpinBox(self.age_limit)

    def setStylesForTheLabels(self):
        self.setStyleForTheLabel(self.label_title)
        self.setStyleForTheLabel(self.label_begin)
        self.setStyleForTheLabel(self.label_duration)
        self.setStyleForTheLabel(self.label_age)
        self.setStyleForTheLabel(self.select)

    def setStylesForTheLineEdits(self):
        self.setStyleForTheLineEdit(self.title)
        self.setStyleForTheLineEdit(self.begin)
        self.begin.setMinimumDate(datetime.today().date())
        self.begin.setMinimumTime(datetime.today().time())

    def adding(self):
        if not self.title.text() or self.table.currentRow() == -1:
            return
        date = self.begin.dateTime()
        begin = datetime(date.date().year(), date.date().month(), date.date().day(),
                         date.time().hour(), date.time().minute())
        duration = timedelta(minutes=self.duration.value())
        end = begin + duration
        movies = self.connection.cursor().execute("""SELECT begin, end, id FROM Movies
                                                    WHERE hall = ?""",
                                                  (self.table.item(self.table.currentRow(), 0).text(),)).fetchall()
        for el in movies:
            interval_begin = datetime.strptime(el[0], "%Y-%m-%d %H:%M:%S")
            interval_end = datetime.strptime(el[1], "%Y-%m-%d %H:%M:%S")
            if interval_begin <= begin <= interval_end or begin <= interval_begin <= end:
                self.error.setText("Error: Time is busy.")
                self.error.setStyleSheet("color: red")
                return
        ids = [el[0] for el in self.connection.cursor().execute("""SELECT id FROM Movies""").fetchall()]
        id = 1
        if ids:
            id = max(ids) + 1
        self.connection.cursor().execute("""INSERT INTO Movies VALUES (?, ?, ?, ?, ?, ?, ?)""",
                                         (id,
                                          self.title.text(),
                                          begin,
                                          end,
                                          self.duration.value(),
                                          self.age_limit.value(),
                                          self.table.item(self.table.currentRow(), 0).text()), )
        self.connection.cursor().execute("""UPDATE Halls
                                            SET current_count_of_films = current_count_of_films + 1
                                            WHERE title = ?""",
                                         (self.table.item(self.table.currentRow(), 0).text(),))
        for y in range(100, 521, 60):
            for x in range(440, 881, 40):
                self.connection.cursor().execute("""INSERT INTO Places VALUES (?, ?, ?, ?)""",
                                                 (x, y, id, "False",))
        self.connection.commit()
        self.error.setText(f"Successfully add a movie into the hall "
                           f"\"{self.table.item(self.table.currentRow(), 0).text()}\".")
        self.error.setStyleSheet("color: green")
        self.createTable("SELECT * FROM Halls", ["Название", "Кол-во фильмов", "Кинотеатр"], 3)


class UninstallerOfMovie(UninstallerOfCinemaTheatre):
    def Load(self):
        uic.loadUi("Ui/DeleteTheatre.ui", self)
        self.setWindowTitle("Удаление фильма.")
        self.connection = sqlite3.connect("Project_one.db")

        self.delete_button.clicked.connect(self.uninstaller)

        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.createTable("""SELECT title, begin, end, duration, age_limit, hall FROM Movies""",
                         ["Название", "Начало", "Конец", "Продолжительность", "Возрастное ограничение", "Зал"], 6)
        self.setStyleForTheTable()
        self.loadFontFamilies()
        self.setBackground()
        self.setStyleForThePushButton(self.delete_button)

    def uninstaller(self):
        if self.table.currentRow() == -1:
            return
        result = self.connection.cursor().execute("""SELECT id FROM Movies
                                                    WHERE begin = ? AND hall = ?""",
                                                  (self.table.item(self.table.currentRow(), 1).text(),
                                                    self.table.item(self.table.currentRow(), 5).text(),)).fetchone()
        self.connection.execute("""DELETE FROM Movies
                                     WHERE begin = ? AND hall = ?""",
                                (self.table.item(self.table.currentRow(), 1).text(),
                                 self.table.item(self.table.currentRow(), 5).text(),))
        self.connection.execute("""UPDATE Halls
                                    SET current_count_of_films = current_count_of_films - 1
                                    WHERE title = ?""",
                                (self.table.item(self.table.currentRow(), 5).text(),))

        self.uninstallerOfPlaces(result[0])
        self.connection.commit()
        self.createTable("""SELECT title, begin, end, duration, age_limit, hall FROM Movies""",
                         ["Название", "Начало", "Конец", "Продолжительность", "Возрастное ограничение", "Зал"], 6)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Main()
    ex.show()
    sys.exit(app.exec())
