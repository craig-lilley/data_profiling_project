import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QVBoxLayout)
from PyQt6.QtCore import Qt, QUrl
import pandas as pd
from backend.data_processing import read_data
import plotly.graph_objects as go
from pyqtgraph import PlotWidget, GraphicsLayoutWidget 
from PyQt6.QtWebEngineWidgets import QWebEngineView
import zmq
import time
    
class DataProfilingWidget(QWidget):
    def __init__(self, dash_thread):
        super().__init__()
        self.dash_thread = dash_thread
        self.setAcceptDrops(True)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.drop_target = QLabel("Drop Your Data File Here")
        self.drop_target.setAcceptDrops(True)
        self.drop_target.setAlignment(Qt.AlignmentFlag.AlignCenter) # Center the text
        self.layout.addWidget(self.drop_target)
        
        self.dash_view = QWebEngineView()
        self.layout.addWidget(self.dash_view)
        self.dash_view.load(QUrl('http://127.0.0.1:3001'))


    def dragEnterEvent(self, event):
        #print("dragEnterEvent triggered")
        #print(event.mimeData().formats())
        if event.mimeData().hasUrls():  # Check for file URLs
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        #rint("dropEvent triggered")
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                file_path = url.toLocalFile() # Get the local file path
                self.drop_target.setText("Processing File...")
                self.process_data_file(file_path)  # Call your profiling function
            event.accept()
        else: 
            event.ignore()

    def process_data_file(self, file_path):
        try:
            #print(f"Processing file: {file_path}")
            df = read_data(file_path) # Adapt the function name
            #print(f"Data: {df}")

            # ZeroMQ Setup
            print("Creating context")
            context = zmq.Context()
            print("Context created")
            socket = context.socket(zmq.PUB)  
            socket.bind("tcp://*:5556")
            print("Server started")
            
            time.sleep(1)
            # Send a test message
            socket.send_string("Test message")
              
            socket.send_json(df.to_json()) 
        except Exception as e:
            print(f"Error processing file: {e}")
        
    def closeEvent(self, event):
    # Stop the Dash server
        if self.dash_thread.is_alive():
            self.dash_thread.join()
            event.accept()
    


