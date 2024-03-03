import sys
from PyQt6.QtWidgets import QApplication, QMainWindow  # Add QMainWindow
from frontend.main_window import DataProfilingWidget  # Import your widget class

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Data Profiling Application")  # Set a title

        # Create an instance of your main widget
        main_widget = DataProfilingWidget()

        # Set the central widget of your main window
        self.setCentralWidget(main_widget)

if __name__ == '__main__': 
    app = QApplication(sys.argv)

    # Create a main window
    window = MainWindow() 
    window.show() 

    sys.exit(app.exec())
