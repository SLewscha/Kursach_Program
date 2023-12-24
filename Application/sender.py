# Импортируем модуль системных функций и параметров
import sys
# Импортируем из фреймворка PyQt5 модули, необходимые для создания графического интерфейса приложения
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QVBoxLayout, QPushButton, QLineEdit
# Импортируем модуль, предоставляющий функционал для работы с сетевыми сокетами
import socket
# Импортируем модуль, необходимый для работы с данными в формате JSON
import json
# Импортируем модуль, предоставляющий функционал для взаимодействия с системой через Windows Management Instrumentation
import wmi

# Создаем класс SenderWindow, наследник QMainWindow
class SenderWindow(QMainWindow):
    def __init__(self):
        # Вызываем конструктор родительского класса QMainWindow, от которого наследуется класс SenderWindow, тем самым позволяя использовать функционал и свойства, определенные в классе QMainWindow
        super().__init__()

        # Указываем заголовок данного окна
        self.setWindowTitle("Отправитель")
        # Указываем размер окна
        self.setFixedSize(350, 200)

        # Создаем экземпляр класса QWidget
        central_widget = QWidget(self)
        # Устанавливаем центральный виджет для данного окна, который будет содержать другие элементы интерфейса
        self.setCentralWidget(central_widget)

        # Создаем экземпляр класса QVBoxLayout
        layout = QVBoxLayout()
        # Выстраиваем элементы внутри центрального виджета данного окна в вертикальном расположении
        central_widget.setLayout(layout)

        # Создаем виджет для текста
        label = QLabel("Окно отправителя")
        # Устанавливаем виджет в соответствии с ранее установленным расположением
        layout.addWidget(label)

        # Аналогично предыдущему блоку, но с другим текстом
        label = QLabel("Введите IP-адрес удаленного компьютера:")
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

        # Создаем кнопку с помощью конструктора QPushButton
        send_button = QPushButton("Отправить")
        # Устанавливаем соединение между сигналом нажатия кнопки и вызовом метода destination (см. блок ниже)
        send_button.clicked.connect(self.destination)
        layout.addWidget(send_button)

    # Определяем метод, получающий введенные значения IP-адреса и порта, а также вызывающий метод отправки собранной информации
    def destination(self):
        # Создаем переменную, которая сохраняет текст, введенный пользователем в виджет QLineEdit с именем ip_input (соответствует IP-адресу удаленного компьютера)
        receiver_ip = self.ip_input.text()
        # Создаем переменную, которая сохраняет преобразованный в число текст, введенный пользователем в виджет QLineEdit с именем port_input (соответствует номеру порта)
        receiver_port = int(self.port_input.text())
        # Создаем переменную, в которую сохраняется возвращаемое значение вызванного метода get_system_info
        data = self.get_system_info()
        # Вызываем метод передачи данных получателю, который принимает в качестве аргументов IP-адрес удаленного компьютера, порт и системную информацию
        self.send_data_to_receiver(receiver_ip, receiver_port, data)

    # Определяем метод, собирающий информацию о конфигурации компьютера
    def get_system_info(self):
        # Создаем экземпляр wmi для доступа к функциям, предоставляемым данным классом
        c = wmi.WMI()

        # Получаем информацию о процессоре с помощью WMI
        # Сперва создаем переменную для сохранения информации о процессоре, затем сохраняем в нее информацию о первом процессоре из списка
        processor_info = c.Win32_Processor()[0]
        # Записываем имя процессора из переменной processor_info
        processor_name = processor_info.Name
        # Записываем архитектуру процессора
        processor_architecture = processor_info.Architecture
        # записываем количество ядер процессора
        processor_cores = processor_info.NumberOfCores

        # Аналогично предыдущему блоку, но для видеокарты
        gpu_info = c.Win32_VideoController()[0]
        gpu_name = gpu_info.Name
        gpu_resolution = (gpu_info.CurrentHorizontalResolution, gpu_info.CurrentVerticalResolution)
        
        # Аналогично предыдущему блоку, но для ОС
        os_info = c.Win32_OperatingSystem()[0]
        os_name = os_info.Caption
        os_version = os_info.Version

        # Создаем словарь с полученными данными
        system_info = {
            "Processor": {
                "Name": processor_name,
                "Architecture": processor_architecture,
                "Cores": processor_cores
            },
            "GPU": {
                "Name": gpu_name,
                "Resolution": gpu_resolution
            },
            "OS": {
                "Name": os_name,
                "Version": os_version
            }
        }

        # Устанавливаем словарь на роль возвращаемого значения
        return system_info

    # Определяем метод, который отправляет данные по сети на указанный IP-адрес и порт получателя
    def send_data_to_receiver(self, receiver_ip, receiver_port, data):
        # Создаем сокет с атрибутами socket.AF_INET, указывающим на использование семейства адресов IPv4, и socket.SOCK_STREAM, указывающим на использование протокола TCP
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Устанавливаем соединение с указанным IP-адресом и портом получателя
        sock.connect((receiver_ip, receiver_port))
        # Преобразуем собранные данные в формат JSON и передаем их переменной data_json
        data_json = json.dumps(data)
        # Отправляем данные в формате JSON через установленное соединение в виде байтов
        sock.sendall(data_json.encode())
        # Закрываем соединение с получателем
        sock.close()

# Блок, оставленный на случай отдельного тестирования данной программы
if __name__ == "__main__":
    app = QApplication(sys.argv)
    sender_window = SenderWindow()
    sender_window.show()
    sys.exit(app.exec_())
