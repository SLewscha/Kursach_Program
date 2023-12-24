# Импортируем модуль системных функций и параметров
import sys
# Импортируем из фреймворка PyQt5 модули, необходимые для создания графического интерфейса приложения
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QVBoxLayout, QPushButton, QTextEdit, QLineEdit
# Импортируем модуль, предоставляющий функционал для работы с сетевыми сокетами
import socket
# Импортируем модуль, необходимый для работы с данными в формате JSON
import json

# Создаем класс ReceiverWindow, наследник QMainWindow
class ReceiverWindow(QMainWindow):
    def __init__(self):
        # Вызываем конструктор родительского класса QMainWindow, от которого наследуется класс ReceiverWindow, тем самым позволяя использовать функционал и свойства, определенные в классе QMainWindow
        super().__init__()

        # Указываем заголовок данного окна
        self.setWindowTitle("Получатель")
        # Указываем размер окна
        self.setFixedSize(350, 400)

        # Создаем экземпляр класса QWidget
        central_widget = QWidget(self)
        # Устанавливаем центральный виджет для данного окна, который будет содержать другие элементы интерфейса
        self.setCentralWidget(central_widget)

        # Создаем экземпляр класса QVBoxLayout
        layout = QVBoxLayout()
        # Выстраиваем элементы внутри центрального виджета данного окна в вертикальном расположении
        central_widget.setLayout(layout)

        # Создаем виджет для текста
        label = QLabel("Окно получателя")
        # Устанавливаем виджет в соответствии с ранее установленным расположением
        layout.addWidget(label)

        # Аналогично предыдущему блоку, но с другим текстом
        label = QLabel("Введите IP-адрес вашего компьютера:")
        layout.addWidget(label)

        # Создаем экземпляр класса виджета QLineEdit, предназначенного для ввода строки текста
        self.ip_input = QLineEdit()
        layout.addWidget(self.ip_input)

        # Вновь виджет для отображения строки текста
        label = QLabel("Введите порт:")
        layout.addWidget(label)

        # Вновь виджет для ввода строки текста
        self.port_input = QLineEdit()
        layout.addWidget(self.port_input)

        # Вновь строка текста
        label = QLabel("Информация о системе:")
        layout.addWidget(label)

        # Создаем экземпляр класса виджета QTextEdit, предназначенного для отображения и редактирования текста
        self.system_info_text = QTextEdit()
        # Устанавливает режим только для чтения
        self.system_info_text.setReadOnly(True)
        layout.addWidget(self.system_info_text)

        # Создаем кнопку с помощью конструктора QPushButton
        receive_button = QPushButton("Получить данные")
        # Устанавливаем соединение между сигналом нажатия кнопки и вызовом метода process_data
        receive_button.clicked.connect(self.process_data)
        layout.addWidget(receive_button)

    #Определяем метод, получающий введенные значения IP-адреса и порта, а также вызывающий методы receive_data_from_sender и show_system_info (см. блоки ниже)
    def process_data(self):
        # Создаем переменную, которая сохраняет текст, введенный пользователем в виджет QLineEdit с именем ip_input (соответствует IP-адресу компьютера-получателя)
        receiver_ip = self.ip_input.text()
        # Создаем переменную, которая сохраняет преобразованный в число текст, введенный пользователем в виджет QLineEdit с именем port_input (соответствует номеру порта)
        receiver_port = int(self.port_input.text())
        #Вызываем метод получения и обработки данных отправителя, который принимает в качестве аргументов IP-адрес компьютера-получателя и порт
        system_info = self.receive_data_from_sender(receiver_ip, receiver_port)
        # #Вызываем метод, который принимает в качестве аргумента полученные от отправителя данные и выводит их на экран
        self.show_system_info(system_info)

    # Определяем метод, который получает данные по сети на указанный IP-адрес и порт
    def receive_data_from_sender(self, receiver_ip, receiver_port):
        # Создаем сокет с атрибутами socket.AF_INET, указывающим на использование семейства адресов IPv4, и socket.SOCK_STREAM, указывающим на использование протокола TCP
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Связываем созданный сокет с указанными IP-адресом и портом, тем самым позволяя сокету прослушивать входящие соединения на данном адресе и порту
        sock.bind((receiver_ip, receiver_port))
        # Назначаем сокету режим прослушивания входящих соединений, ограничивая максимальное их количество одним
        sock.listen(1)
        # Принимаем входящее соединение и создаем для него новый сокет conn, который будет использоваться для взаимодействия с удаленным компьютером, а также сохраняем информацию об адресе и порте
        conn, addr = sock.accept()
        # Принимаем данные размером до 2048 байт из соединения conn, декодируем байты в читаемый текст и сохраняем данные в переменную data_json
        data_json = conn.recv(2048).decode()
        # Преобразуем полученный JSON-текст в соответствующую структуру данных
        data = json.loads(data_json)
        # Закрываем соединение conn
        conn.close()
        # Закрываем сокет sock
        sock.close()

        # Устанавливаем полученный текст с конфигурацией удаленного компьютера на роль возвращаемого значения
        return data

    # Определяем метод, выводящий данные на экран
    def show_system_info(self, system_info):
        # Преобразуем системную информацию в формат JSON, добавив отступ в 4 пробела
        system_info_str = json.dumps(system_info, indent=4)
        # Присваиваем переменной system_info_text, являющейся объектом виджета, предназначенного для вывода строк, значение JSON-текста, содержащего системную информацию удаленного компьютера
        self.system_info_text.setPlainText(system_info_str)

# Блок, оставленный на случай отдельного тестирования данной программы
if __name__ == "__main__":
    app = QApplication(sys.argv)
    receiver_window = ReceiverWindow()
    receiver_window.show()
    sys.exit(app.exec_())
