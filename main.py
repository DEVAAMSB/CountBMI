import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, \
     QTableWidget, QTableWidgetItem, QInputDialog
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QIcon
import matplotlib.pyplot as plt
import pandas as pd

class CountBMI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.users_data = {}

    def initUI(self):
        self.setWindowIcon(QIcon('bmi.png'))
        self.setWindowTitle('Count BMI')

        # Create layout
        layout = QVBoxLayout()

        # Weight input
        self.weight_label = QLabel('Weight (kg):')
        self.weight_input = QLineEdit(self)
        layout.addWidget(self.weight_label)
        layout.addWidget(self.weight_input)

        # Height input
        self.height_label = QLabel('Height (cm):')
        self.height_input = QLineEdit(self)
        layout.addWidget(self.height_label)
        layout.addWidget(self.height_input)

        # Calculate button
        self.calc_button = QPushButton('Calculate BMI', self)
        self.calc_button.clicked.connect(self.calculate_bmi)
        layout.addWidget(self.calc_button)

        # Result label
        self.result_label = QLabel('')
        layout.addWidget(self.result_label)

        # User data table
        self.data_table = QTableWidget()
        self.data_table.setColumnCount(3)
        self.data_table.setHorizontalHeaderLabels(['Name', 'BMI', 'Date'])
        layout.addWidget(self.data_table)

        # Set layout
        self.setLayout(layout)

    @pyqtSlot()
    def calculate_bmi(self):
        weight = float(self.weight_input.text())
        height = float(self.height_input.text()) / 100  # Convert cm to meters
        bmi = weight / (height ** 2)
        self.result_label.setText(f'Your BMI is: {bmi:.2f}')

        # Store data
        name, okPressed = QInputDialog.getText(self, "Get name","Your name:", QLineEdit.Normal, "")
        if okPressed and name != '':
            if name not in self.users_data:
                self.users_data[name] = []
            self.users_data[name].append((bmi, pd.Timestamp.now()))

            # Update table
            self.update_table()

    def update_table(self):
        self.data_table.setRowCount(0)
        for name, data in self.users_data.items():
            for bmi, date in data:
                row_position = self.data_table.rowCount()
                self.data_table.insertRow(row_position)
                self.data_table.setItem(row_position, 0, QTableWidgetItem(name))
                self.data_table.setItem(row_position, 1, QTableWidgetItem(f'{bmi:.2f}'))
                self.data_table.setItem(row_position, 2, QTableWidgetItem(date.strftime('%Y-%m-%d %H:%M:%S')))

    def show_bmi_trend(self, name):
        if name in self.users_data:
            data = pd.DataFrame(self.users_data[name], columns=['BMI', 'Date']).set_index('Date')
            data['BMI'].plot(title=f'BMI Trend for {name}')
            plt.show()
        else:
            QMessageBox.information(self, 'Error', 'No data for this user.')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CountBMI()
    ex.show()
    sys.exit(app.exec_())
