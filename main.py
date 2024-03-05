import sys
from PyQt6.QtWidgets import QApplication, QMainWindow  # Add QMainWindow
from frontend.main_window import DataProfilingWidget  # Import your widget class
import multiprocessing
import os  # Import the os module
if multiprocessing.get_context() is None: 
    multiprocessing.set_start_method('spawn')

def start_dash_server():
    import dashboard
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(s.fileno())  # Print the file descriptor
    dashboard.app.run_server(debug=True, port=3000, dev_tools_hot_reload=False) 
    
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Data Profiling Application")  # Set a title

        # Create an instance of your main widget
        main_widget = DataProfilingWidget()

        # Set the central widget of your main window
        self.setCentralWidget(main_widget)

# ... your imports ...

if __name__ == '__main__':
    should_start_dash = True  

    # Execute PyQt6 Application
    app = QApplication(sys.argv)  
    window = MainWindow() 
    window.show() 

    if should_start_dash:
        print("main running") 
        dash_process = multiprocessing.Process(target=start_dash_server)
        dash_process.start()  
        should_start_dash = False  

    try:
        sys.exit(app.exec())
    finally:
        print("Terminating Dash Process...")
        dash_process.terminate()
        print("Waiting for Dash Process to Join...")
        dash_process.join()  
        print("Dash Process cleanup completed.") 

