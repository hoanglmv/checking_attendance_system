import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QLabel

app = QApplication(sys.argv)
window = QMainWindow()
tab_widget = QTabWidget()

tab1 = QWidget()
tab1_layout = QVBoxLayout(tab1)
tab1_layout.addWidget(QLabel("Tab 1"))

tab2 = QWidget()
tab2_layout = QVBoxLayout(tab2)
tab2_layout.addWidget(QLabel("Tab 2"))

tab_widget.addTab(tab1, "Tab 1")
tab_widget.addTab(tab2, "Tab 2")

window.setCentralWidget(tab_widget)
window.show()
sys.exit(app.exec())