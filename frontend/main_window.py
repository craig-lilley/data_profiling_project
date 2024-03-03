import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QVBoxLayout)
from PyQt6.QtCore import Qt
import pandas as pd
from backend.data_processing import read_data, count_missing_data
import plotly.graph_objects as go
from pyqtgraph import PlotWidget, GraphicsLayoutWidget 


class DataProfilingWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.drop_target = QLabel("Drop Your Data File Here")
        self.drop_target.setAcceptDrops(True)
        self.drop_target.setAlignment(Qt.AlignmentFlag.AlignCenter) # Center the text
        self.layout.addWidget(self.drop_target)
        
        self.plot_widget = QWidget()
        self.layout.addWidget(self.plot_widget)
        #print("plot_widget created:", self.plot_widget)

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
        # Implement your data profiling logic here
        #print("process_data_file called")
        try:
            df = read_data(file_path)  # Adjust based on your file type
            missing = count_missing_data(df)
            #print(type(missing), missing)

            fig = go.Figure(data=go.Heatmap(
                z=missing,  # Pass the missing data matrix here
                colorbar=dict(title="Missing Value Ratio")
            ))
            #print("fig created:", fig)
            fig.update_layout(title="Missing Data Heatmap")
            # Display the figure in the plot widget (using PyQtGraph)
            layout = QVBoxLayout()
            self.plot_widget.setLayout(layout)
            
            graphics_widget = GraphicsLayoutWidget(self.plot_widget) # Create a GraphicsLayoutWidget
            layout.addWidget(graphics_widget)  # Add it to your plot_widget's layout
            graphics_widget.addItem(fig)  # Add the Plotly figure to the GraphicsLayoutWidget

        
        except Exception as e:
            print(f"Error processing file: {e}")
    

if __name__ == '__main__': 
    app = QApplication(sys.argv)
    widget = DataProfilingWidget()
    widget.show()
    sys.exit(app.exec())
