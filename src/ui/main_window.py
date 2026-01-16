from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtGui import QClipboard, QIcon
from PyQt5.QtCore import Qt, QBuffer, QIODevice, QThread, pyqtSignal
import sys
import os
import time

# Ensure the path is correctly set
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir, os.pardir))
sys.path.append(parent_dir)

# Import the mdtolatex function
try:
    from src.mdtolatex import mdtolatex
except ImportError as e:
    print(f"Error importing mdtolatex: {e}")
    sys.exit(1)

unclicked_str = "📖"
processing_str = "✍️"


class Worker(QThread):
    result = pyqtSignal(str)

    def __init__(self):
        super().__init__()

    def run(self):
        time.sleep(0.1)  # Simulate a delay of 0.1 seconds
        clipboard = QApplication.clipboard()

        extracted_text = clipboard.text()  # Extract text from the clipboard

        converted_text = mdtolatex(extracted_text)
        self.result.emit(converted_text)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("mdtolatex GUI")
        self.setWindowIcon(QIcon('../images/icon.ico'))  # Set the window icon
        self.resize(840, 100)  # Set the window size to 400x400 pixels
        # self.setWindowFlags(Qt.FramelessWindowHint)  # Remove the title bar and frame
        self.move(0, 940)  # Set the window position to (100, 100)

        # self.quit_button = QPushButton("Quit", self)
        # self.quit_button.clicked.connect(self.quit_application)

        self.proceed_button = QPushButton(unclicked_str, self)
        self.proceed_button.setFixedSize(840, 80)  # Enlarge the proceed_button
        self.proceed_button.setStyleSheet("font-size: 50px;")  # Enlarge the button text
        self.proceed_button.clicked.connect(self.proceed_on_clipboard)

        layout = QVBoxLayout()
        layout.addWidget(self.proceed_button)
        # layout.addWidget(self.quit_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def proceed_on_clipboard(self):
        self.proceed_button.setText(processing_str)  # Change the button text while processing

        self.worker = Worker()
        self.worker.result.connect(self.display_result)
        self.worker.start()

    def display_result(self, text):
        clipboard = QApplication.clipboard()
        clipboard.setText(text)  # Copy the converted text to the clipboard
        self.proceed_button.setText(unclicked_str)  # Change the button text back to the original text

    # def quit_application(self):
    #     QApplication.quit()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())