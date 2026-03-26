import sys
import sqlite3
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, QHeaderView
)
from PyQt6.QtCore import Qt

class BicycleProductManager(QWidget):
    def __init__(self):
        super().__init__()
        self.db_connection = sqlite3.connect('bicycle_products.db')
        self.create_table()
        self.init_ui()
        self.load_data()

    def create_table(self):
        cursor = self.db_connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS MyProduct (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                price REAL NOT NULL
            )
        ''')
        self.db_connection.commit()

    def init_ui(self):
        self.setWindowTitle('자전거 용품 관리')
        self.setGeometry(100, 100, 600, 400)

        layout = QVBoxLayout()

        # 입력 폼
        form_layout = QHBoxLayout()
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText('제품명')
        self.price_edit = QLineEdit()
        self.price_edit.setPlaceholderText('가격')
        form_layout.addWidget(QLabel('제품명:'))
        form_layout.addWidget(self.name_edit)
        form_layout.addWidget(QLabel('가격:'))
        form_layout.addWidget(self.price_edit)
        layout.addLayout(form_layout)

        # 버튼들
        button_layout = QHBoxLayout()
        self.add_button = QPushButton('입력')
        self.add_button.clicked.connect(self.add_product)
        self.edit_button = QPushButton('수정')
        self.edit_button.clicked.connect(self.edit_product)
        self.delete_button = QPushButton('삭제')
        self.delete_button.clicked.connect(self.delete_product)
        self.search_button = QPushButton('검색')
        self.search_button.clicked.connect(self.search_product)
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.edit_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.search_button)
        layout.addLayout(button_layout)

        # 테이블
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(['ID', '제품명', '가격'])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.itemSelectionChanged.connect(self.on_selection_changed)
        layout.addWidget(self.table)

        self.setLayout(layout)

    def load_data(self, search_term=None):
        cursor = self.db_connection.cursor()
        if search_term:
            cursor.execute('SELECT id, name, price FROM MyProduct WHERE name LIKE ?', ('%' + search_term + '%',))
        else:
            cursor.execute('SELECT id, name, price FROM MyProduct')
        rows = cursor.fetchall()
        self.table.setRowCount(len(rows))
        for row_idx, row in enumerate(rows):
            for col_idx, value in enumerate(row):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))

    def add_product(self):
        name = self.name_edit.text().strip()
        price_text = self.price_edit.text().strip()
        if not name or not price_text:
            QMessageBox.warning(self, '입력 오류', '제품명과 가격을 모두 입력하세요.')
            return
        try:
            price = float(price_text)
        except ValueError:
            QMessageBox.warning(self, '입력 오류', '가격은 숫자로 입력하세요.')
            return
        cursor = self.db_connection.cursor()
        cursor.execute('INSERT INTO MyProduct (name, price) VALUES (?, ?)', (name, price))
        self.db_connection.commit()
        self.name_edit.clear()
        self.price_edit.clear()
        self.load_data()

    def edit_product(self):
        selected_rows = set()
        for item in self.table.selectedItems():
            selected_rows.add(item.row())
        if len(selected_rows) != 1:
            QMessageBox.warning(self, '선택 오류', '수정할 항목을 하나 선택하세요.')
            return
        row = list(selected_rows)[0]
        id_item = self.table.item(row, 0)
        if not id_item:
            return
        product_id = int(id_item.text())
        name = self.name_edit.text().strip()
        price_text = self.price_edit.text().strip()
        if not name or not price_text:
            QMessageBox.warning(self, '입력 오류', '제품명과 가격을 모두 입력하세요.')
            return
        try:
            price = float(price_text)
        except ValueError:
            QMessageBox.warning(self, '입력 오류', '가격은 숫자로 입력하세요.')
            return
        cursor = self.db_connection.cursor()
        cursor.execute('UPDATE MyProduct SET name = ?, price = ? WHERE id = ?', (name, price, product_id))
        self.db_connection.commit()
        self.name_edit.clear()
        self.price_edit.clear()
        self.load_data()

    def delete_product(self):
        selected_rows = set()
        for item in self.table.selectedItems():
            selected_rows.add(item.row())
        if not selected_rows:
            QMessageBox.warning(self, '선택 오류', '삭제할 항목을 선택하세요.')
            return
        reply = QMessageBox.question(self, '삭제 확인', '선택된 항목을 삭제하시겠습니까?',
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            cursor = self.db_connection.cursor()
            for row in selected_rows:
                id_item = self.table.item(row, 0)
                if id_item:
                    product_id = int(id_item.text())
                    cursor.execute('DELETE FROM MyProduct WHERE id = ?', (product_id,))
            self.db_connection.commit()
            self.load_data()

    def search_product(self):
        search_term = self.name_edit.text().strip()
        self.load_data(search_term)

    def on_selection_changed(self):
        selected_rows = set()
        for item in self.table.selectedItems():
            selected_rows.add(item.row())
        if len(selected_rows) == 1:
            row = list(selected_rows)[0]
            name_item = self.table.item(row, 1)
            price_item = self.table.item(row, 2)
            if name_item and price_item:
                self.name_edit.setText(name_item.text())
                self.price_edit.setText(price_item.text())

    def closeEvent(self, event):
        self.db_connection.close()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = BicycleProductManager()
    window.show()
    sys.exit(app.exec())
