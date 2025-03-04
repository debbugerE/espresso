import sys
import sqlite3
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QVBoxLayout, QWidget, QStatusBar
from PyQt6 import uic


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        try:
            self.ui = uic.loadUi('main.ui', self)
        except FileNotFoundError:
            print("Файл интерфейса не найден.")
            sys.exit(1)

        layout = QVBoxLayout()
        container = QWidget()
        container.setLayout(layout)

        self.ui.label.setFixedHeight(40)
        self.ui.pushButton.setFixedHeight(40)

        layout.addWidget(self.ui.label)
        layout.addWidget(self.ui.tableWidget)
        layout.addWidget(self.ui.pushButton)
        self.setCentralWidget(container)

        self.ui.pushButton.clicked.connect(self.showData)

        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)

    def showData(self):
        try:
            conn = sqlite3.connect('coffee.sqlite')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM grade")
            rows = cursor.fetchall()
            conn.close()
        except sqlite3.Error as e:
            self.statusBar.showMessage(f"Ошибка базы данных: {e}")
            return

        try:
            self.ui.tableWidget.setRowCount(len(rows))
            self.ui.tableWidget.setColumnCount(len(rows[0]))
            self.ui.tableWidget.setHorizontalHeaderLabels(['ID', 'Name', 'Roast', 'Format', 'Taste', 'Price'])

            for row_num, row in enumerate(rows):
                for col_num, value in enumerate(row):
                    item = QTableWidgetItem(str(value))
                    self.ui.tableWidget.setItem(row_num, col_num, item)

            self.ui.tableWidget.resizeColumnsToContents()

            self.statusBar.showMessage(f"Нашлось {len(rows)} сортов кофе")
        except Exception as e:
            self.statusBar.showMessage(f"Ошибка отображения данных: {e}")


if __name__ == "__main__":
    try:
        app = QApplication(sys.argv)
        window = MainWindow()
        window.resize(800, 600)
        window.show()
        sys.exit(app.exec())
    except Exception as e:
        print(f"Ошибка запуска приложения: {e}")
