import sys
import time
from PyQt6.QtWidgets import QApplication, QMainWindow  # Add QMainWindow
from frontend.main_window import DataProfilingWidget  # Import your widget class
import os  # Import the os module
import zmq  # Import the ZeroMQ module
import threading

def start_dash_server():
    import dashboard

    # Create a ZeroMQ context
    context = zmq.Context()

    # Create a ZeroMQ SUB socket
    socket = context.socket(zmq.SUB)

    # Connect to the publisher
    socket.connect("tcp://localhost:5555")

    # Subscribe to all topics
    socket.setsockopt_string(zmq.SUBSCRIBE, "")

    # Run the Dash server
    dashboard.app.run_server(debug=True, port=3001, dev_tools_hot_reload=False, use_reloader=False)
    
class MainWindow(QMainWindow):
    def __init__(self, dash_thread):
        super().__init__()
        
        self.setWindowTitle("Data Profiling Application")  # Set a title

        # Create an instance of your main widget
        main_widget = DataProfilingWidget(dash_thread)

        # Set the central widget of your main window
        self.setCentralWidget(main_widget)



if __name__ == '__main__':
    # Execute PyQt6 Application
    app = QApplication(sys.argv)  

    # Start Dash server
    print("main running") 
    dash_thread = threading.Thread(target=start_dash_server)
    dash_thread.daemon = True  # Set the daemon attribute to True
    dash_thread.start()
    
    window = MainWindow(dash_thread) 
    window.show() 

    try:
        sys.exit(app.exec())
    finally:
        # Terminate the Dash server thread
        dash_thread.join()

