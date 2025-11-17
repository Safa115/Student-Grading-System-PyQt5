import sys
from PyQt5.QtWidgets import QApplication
from views.interface import MainApp  # Import the GUI class from views folder

def main():
    # 1. Create the application instance
    app = QApplication(sys.argv)

    # 2. Create an instance of the Main Window and show it
    window = MainApp()
    window.show()

    # 3. Start the application event loop (keeps the window open)
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()