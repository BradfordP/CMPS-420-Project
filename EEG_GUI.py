import sys
import os
import mne
import pyqtgraph as pg
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QFileDialog, QCheckBox, QScrollArea, QHBoxLayout
from pyqtgraph.Qt import QtGui
from itertools import cycle

class EEGAnalyzer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle("EEG Analyzer")
        self.setGeometry(100, 100, 1000, 600)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QHBoxLayout(self.central_widget)

        # Create a widget to hold checkboxes with a fixed width
        self.checkboxes_widget = QWidget()
        self.checkboxes_widget.setFixedWidth(200)  # Set a fixed width

        # Create a vertical layout for the checkboxes
        self.checkboxes_layout = QVBoxLayout(self.checkboxes_widget)

        self.upload_button = QPushButton("Upload EEG/EDF File", self)
        self.upload_button.clicked.connect(self.load_file)
        self.checkboxes_layout.addWidget(self.upload_button)

        self.channel_scroll_area = QScrollArea()
        self.channel_widget = QWidget()
        self.channel_layout = QVBoxLayout(self.channel_widget)
        self.channel_scroll_area.setWidget(self.channel_widget)
        self.channel_scroll_area.setWidgetResizable(True)
        self.checkboxes_layout.addWidget(self.channel_scroll_area)

        self.layout.addWidget(self.checkboxes_widget)

        self.plot_widget = pg.PlotWidget()
        self.layout.addWidget(self.plot_widget)

        self.raw_data = None
        self.channel_checkboxes = []
        self.plotted_lines = []  # List to keep track of plotted lines
        self.legend_items = {}  # Dictionary to map channel names to legend items

    def load_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly

        file_path, _ = QFileDialog.getOpenFileName(self, "Open EEG/EDF File", "", "EDF Files (*.edf);;All Files (*)", options=options)

        if file_path:
            self.load_data(file_path)
            self.create_channel_checkboxes()

    def create_channel_checkboxes(self):
        if self.raw_data is not None:
            channel_names = self.raw_data.ch_names


            # self.toggle_all_checkbox = QCheckBox('Toggle All')
            # self.toggle_all_checkbox.stateChanged.connect(self.update_plot)
            # self.toggle_all_checkbox.setChecked(False)
            # self.channel_checkboxes.append(self.toggle_all_checkbox)
            # self.channel_layout.addWidget(self.toggle_all_checkbox)
            # self.toggle_all_checkbox.stateChanged.connect(self.toggleAllCheckboxes)

            # Create checkboxes for each channel
            for name in channel_names:
                checkbox = QCheckBox(name)
                checkbox.stateChanged.connect(self.update_plot)
                self.channel_checkboxes.append(checkbox)
                self.channel_layout.addWidget(checkbox)
            

            # Check the first channel by default
            if self.channel_checkboxes:
                self.channel_checkboxes[0].setChecked(True)

            # Update the plot with the default channel
            self.update_plot()

    def update_plot(self):
        if self.raw_data is not None:
            data, times = self.raw_data[:, :]
            num_channels = data.shape[0]

            selected_channels = []
            colors = cycle(['b', 'g', 'r', 'c', 'm', 'y', 'k'])  # Define a list of colors for different lines

            # Remove previously plotted lines
            for line in self.plotted_lines:
                self.plot_widget.removeItem(line)
            self.plotted_lines.clear()

            # Update the legend items
            num_columns = 4  # Number of columns in the legend
            column_height = 30  # Height of each column
            current_column = 0  # Current column in the legend layout
            legend_items = []  # Temporary list for legend items
            legend_width = 0

            for i, checkbox in enumerate(self.channel_checkboxes):
                if checkbox.isChecked():
                    channel_name = checkbox.text()
                    selected_channels.append(channel_name)
                    color = next(colors)
                    channel_data = data[self.raw_data.ch_names.index(channel_name), :]
                    line = self.plot_widget.plot(times, channel_data, pen=pg.mkPen(color), name=channel_name)
                    self.plotted_lines.append(line)

                    if channel_name not in self.legend_items:
                        legend_item = self.plot_widget.addLegend(offset=(legend_width, current_column * column_height))
                        self.legend_items[channel_name] = legend_item
                        legend_items.append(legend_item)
                        legend_width += 200  # Adjust the legend width

                    current_column += 1
                    if current_column >= num_columns:
                        current_column = 0

            # Update the legend layout
            legend_height = ((len(legend_items) - 1) // num_columns + 1) * column_height
            self.plot_widget.legend.setGeometry(0, 0, legend_width, legend_height)

    def load_data(self, file_path):
        # Load the EDF file using MNE
        self.raw_data = mne.io.read_raw_edf(file_path, preload=True)


class OpeningWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('FIVE GUYS')
        
        self.setGeometry(100, 100, 400, 200)
        

        layout = QVBoxLayout()
        load_button = QPushButton('Load Data')
        load_button.clicked.connect(self.load_file)
        sample_button = QPushButton('Use Sample Data')
        
        layout.addWidget(load_button)
        layout.addWidget(sample_button)
        
        self.setLayout(layout)

    def open_secondary_window(self):
        self.secondary_window = EEGAnalyzer()
        self.secondary_window.show()

    def load_data(self, file_path):
        # Load the EDF file using MNE
        self.raw_data = mne.io.read_raw_edf(file_path, preload=True)

    def load_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly

        file_path, _ = QFileDialog.getOpenFileName(self, "Open EEG/EDF File", "", "EDF Files (*.edf);;All Files (*)", options=options)

        if file_path:
            openwindow.close()
            eeganalyzerInstance.show()
            eeganalyzerInstance.load_data(file_path)
            eeganalyzerInstance.create_channel_checkboxes()
            


if __name__ == '__main__':
    pg.setConfigOption('background', 'w')  # Set background color to white
    app = QApplication(sys.argv)
    eeganalyzerInstance = EEGAnalyzer()
    openwindow = OpeningWindow()
    openwindow.show()
    sys.exit(app.exec_())