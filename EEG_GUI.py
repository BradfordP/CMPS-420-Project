# import sys
# import os
# import mne
# from PyQt5.QtCore import Qt, QTimer
# import pyqtgraph as pg
# from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QFileDialog, QCheckBox, QScrollArea, QGridLayout, QLabel, QLineEdit
# from PyQt5.QtGui import QDoubleValidator
# from pyqtgraph.Qt import QtGui
# from itertools import cycle

# class EEGAnalyzer(QMainWindow):
#     def __init__(self):
#         super().__init__()

#         self.initUI()

#         # Notification label with initial position at the bottom-right
#         self.notification_label = QLabel(self)
#         self.notification_label.setAlignment(Qt.AlignCenter)
#         self.notification_label.setStyleSheet("background-color: #2ecc71; color: white;")
#         self.notification_label.setFixedHeight(30)

#         # Calculate the position based on screen size
#         screen_size = QApplication.primaryScreen().availableGeometry()
#         label_size = self.notification_label.size()
#         new_x = screen_size.width() - label_size.width()
#         new_y = screen_size.height() - label_size.height()
#         self.notification_label.move(new_x, new_y)

#         self.notification_label.hide()

#         self.notification_timer = QTimer(self)
#         self.notification_timer.timeout.connect(self.clear_notification)

#     def initUI(self):
#         self.setWindowTitle("EEG Analyzer")
#         self.setGeometry(100, 100, 1000, 600)

#         self.central_widget = QWidget(self)
#         self.setCentralWidget(self.central_widget)

#         self.layout = QGridLayout(self.central_widget)

        
#         self.original_data = None  # Variable to store the original data


#         # Create a widget to hold the filter options
#         filter_options_widget = QWidget()

#         # Create a vertical layout for the filter options
#         filter_options_layout = QVBoxLayout(filter_options_widget)

#         # Create filter controls using text boxes
#         self.filter_low_label = QLabel("Low Frequency:")
#         self.filter_low_textbox = QLineEdit()
#         self.filter_low_textbox.setValidator(QDoubleValidator())

#         self.filter_high_label = QLabel("High Frequency:")
#         self.filter_high_textbox = QLineEdit()
#         self.filter_high_textbox.setValidator(QDoubleValidator())

#         self.apply_filter_button = QPushButton("Apply Filter", self)
#         self.apply_filter_button.clicked.connect(self.apply_bandpass_filter)



#         # Add filter controls to filter_options_layout
#         filter_options_layout.addWidget(self.filter_low_label)
#         filter_options_layout.addWidget(self.filter_low_textbox)
#         filter_options_layout.addWidget(self.filter_high_label)
#         filter_options_layout.addWidget(self.filter_high_textbox)
#         filter_options_layout.addWidget(self.apply_filter_button)

#         # Set a fixed width for filter_options_widget
#         filter_options_widget.setFixedWidth(250)

#         # Add filter_options_widget to the layout at (0, 0)
#         self.layout.addWidget(filter_options_widget, 0, 0)

#         # Add a button to remove the bandpass filter
#         self.remove_filter_button = QPushButton("Remove Filter", self)
#         self.remove_filter_button.clicked.connect(self.remove_bandpass_filter)

#         # Add remove_filter_button to filter_options_layout
#         filter_options_layout.addWidget(self.remove_filter_button)

#         # Create a widget to hold checkboxes with a fixed width
#         checkboxes_widget = QWidget()
#         checkboxes_widget.setFixedWidth(250)  # Set a fixed width

#         # Create a vertical layout for checkboxes
#         self.checkboxes_layout = QVBoxLayout(checkboxes_widget)

#         self.channel_scroll_area = QScrollArea()
#         self.channel_widget = QWidget()
#         self.channel_layout = QVBoxLayout(self.channel_widget)
#         self.channel_scroll_area.setWidget(self.channel_widget)
#         self.channel_scroll_area.setWidgetResizable(True)
#         self.checkboxes_layout.addWidget(self.channel_scroll_area)

#         # Add checkboxes_widget to the layout at (1, 0)
#         self.layout.addWidget(checkboxes_widget, 1, 0)

#         # Add the plot widget to the layout at (0, 1)
#         self.plot_widget = pg.PlotWidget()
#         self.layout.addWidget(self.plot_widget, 0, 1, 2, 1)

#         self.raw_data = None
#         self.channel_checkboxes = []
#         self.plotted_lines = []  # List to keep track of plotted lines
#         self.legend_items = {}  # Dictionary to map channel names to legend items

#         # Create a plot widget for the filtered data
#         self.filtered_plot_widget = pg.PlotWidget()
#         self.layout.addWidget(self.filtered_plot_widget, 0, 1, 2, 1)

#         # Initialize the list for filtered plotted lines
#         self.filtered_plotted_lines = []

#         # Create a button to toggle between displaying raw and filtered data
#         self.toggle_data_button = QPushButton("Show Filtered Data", self)
#         self.toggle_data_button.clicked.connect(self.toggle_data)

#         # Set the initial button as static
#         # self.toggle_data_button.setFixedWidth(120)  # Adjust the width as needed
#         self.layout.addWidget(self.toggle_data_button, 2, 1, 1, 1)

#         # Flag to track which data is currently displayed
#         self.show_filtered_data = False  # Set to True for the initial state

#         # Create color cycles for raw and filtered data
#         self.colors_raw = cycle(['b', 'g', 'r', 'c', 'm', 'y', 'k'])
#         self.colors_filtered = cycle(['b', 'g', 'r', 'c', 'm', 'y', 'k'])
    
#         # Initialize the color indices for raw and filtered data
#         self.color_index_raw = 0
#         self.color_index_filtered = 0
        
#         # Flag to track whether filtered data is available
#         self.filtered_data_available = False

#         # Hide the filtered plot widget initially
#         self.filtered_plot_widget.hide()

#     def load_file(self):
#         options = QFileDialog.Options()
#         options |= QFileDialog.ReadOnly

#         file_path, _ = QFileDialog.getOpenFileName(self, "Open EEG/EDF File", "", "EDF Files (*.edf);;All Files (*)", options=options)

#         if file_path:
#             self.load_data(file_path)
#             self.create_channel_checkboxes()

#     def create_channel_checkboxes(self):
#         if self.raw_data is not None:
#             channel_names = self.raw_data.ch_names

#             # Create checkboxes for each channel
#             for name in channel_names:
#                 checkbox = QCheckBox(name)
#                 checkbox.stateChanged.connect(self.update_plot)
#                 self.channel_checkboxes.append(checkbox)
#                 self.channel_layout.addWidget(checkbox)

#             # Check the first channel by default
#             if self.channel_checkboxes:
#                 self.channel_checkboxes[0].setChecked(True)

#             # Update the plot with the default channel
#             self.update_plot()


#     def apply_bandpass_filter(self):
#         if self.raw_data is not None:
#             try:
#                 low_freq = float(self.filter_low_textbox.text())
#                 high_freq = float(self.filter_high_textbox.text())
#             except ValueError:
#                 self.show_notification("Invalid Frequency Values", "Please enter valid numerical values for the frequency range.")
#                 return

#             print(f"Applying bandpass filter: Low Frequency = {low_freq}, High Frequency = {high_freq}")

#             # Check if the frequencies are within a reasonable range
#             if low_freq < 0 or high_freq < 0 or low_freq >= high_freq:
#                 self.show_notification("Invalid Frequency Range", "Please enter a valid frequency range.")
#                 return

#             # Apply bandpass filter to the filtered_data (not the raw_data)
#             self.filtered_data = self.original_data.copy()  # Create a copy of the original data
#             self.filtered_data.filter(l_freq=low_freq, h_freq=high_freq, method='fir', fir_window='hamming')

#             print("Bandpass filter applied successfully to filtered data.")

#             # Update the flag to indicate that filtered data is available
#             self.filtered_data_available = True

#             # Update the filtered plot
#             self.update_filtered_plot()

#             # Show a success message using a notification
#             self.show_notification("Success", "Bandpass filter applied successfully.")

#     def show_notification(self, title, message):
#         self.notification_label.setText(f"{title}: {message}")
#         self.notification_label.show()

#         # Calculate the position based on the window's position and size
#         window_size = self.size()
#         label_size = self.notification_label.size()
#         offset = 10  # Adjust the offset value as needed

#         new_x = window_size.width() - label_size.width() - offset  # Bottom-right corner with offset
#         new_y = window_size.height() - label_size.height() - offset
#         # Adjust the 'left' offset to move the label to the left
#         left_offset = 150  # Adjust the left offset as needed
#         new_x -= left_offset

#         # Set a fixed width (adjust the value as needed)
#         self.notification_label.setFixedWidth(250)  # Adjust the width as needed

#         self.notification_label.move(new_x, new_y)
#         self.notification_timer.start(5000)  # Display for 5 seconds

#     def clear_notification(self):
#         self.notification_label.clear()
#         self.notification_label.hide()
#         self.notification_timer.stop()

#     # def resizeEvent(self):
#     #     # Calculate the new position of the notification label
#     #     label_size = self.notification_label.size()
#     #     screen_size = QApplication.primaryScreen().availableGeometry()
#     #     new_x = screen_size.width() - label_size.width()
#     #     new_y = screen_size.height() - label_size.height()

#     #     # Set the new position
#     #     self.notification_label.move(new_x, new_y)

#     def toggle_data(self):
#         if self.show_filtered_data:
#             self.show_filtered_data = False
#             self.toggle_data_button.setText("Show Filtered Data")
#         else:
#             self.show_filtered_data = True
#             self.toggle_data_button.setText("Show Raw Data")

#         # Update the visibility of the plot widgets
#         self.plot_widget.setVisible(not self.show_filtered_data)
#         self.filtered_plot_widget.setVisible(self.show_filtered_data)

#     def update_filtered_plot(self):
#         if self.filtered_data is not None and self.filtered_data_available:
#             data, times = self.filtered_data[:, :]
#             num_channels = data.shape[0]
#             legend_items = []

#             # Remove previously plotted lines for filtered data
#             for line in self.filtered_plotted_lines:
#                 self.filtered_plot_widget.removeItem(line)

#             # Reset color index to the beginning
#             self.color_index_filtered = 0

#             for i, checkbox in enumerate(self.channel_checkboxes):
#                 if checkbox.isChecked():
#                     channel_name = checkbox.text()

#                     # Get the color from the current index and update the index
#                     color = self.get_next_color(self.color_index_filtered, is_filtered=True)
#                     self.color_index_filtered += 1

#                     channel_data = data[self.filtered_data.ch_names.index(channel_name), :]
#                     line = self.filtered_plot_widget.plot(times, channel_data, pen=pg.mkPen(color), name=channel_name)
#                     self.filtered_plotted_lines.append(line)
#                     legend_items.append((line, channel_name))

#             # Update the legend for the filtered plot
#             self.filtered_plot_widget.addLegend(items=legend_items)
    


#     def remove_bandpass_filter(self):
#         if self.original_data is not None:
#             # Restore the original data
#             self.raw_data = self.original_data.copy()

#             print("Bandpass filter removed successfully.")

#             # After removing the filter, update the plot
#             self.update_plot()


#     def update_plot(self):
#         if self.raw_data is not None:
#             data, times = self.raw_data[:, :]
#             num_channels = data.shape[0]
#             selected_channels = []
#             legend_items = []

#             # Remove previously plotted lines (for both raw and filtered data)
#             for line in self.plotted_lines:
#                 self.plot_widget.removeItem(line)

#             # Reset color index to the beginning
#             self.color_index_raw = 0

#             for i, checkbox in enumerate(self.channel_checkboxes):
#                 if checkbox.isChecked():
#                     channel_name = checkbox.text()
#                     selected_channels.append(channel_name)

#                     # Get the color from the current index and update the index
#                     color = self.get_next_color(self.color_index_raw, is_filtered=False)
#                     self.color_index_raw += 1

#                     channel_data = data[self.raw_data.ch_names.index(channel_name), :]
#                     line = self.plot_widget.plot(times, channel_data, pen=pg.mkPen(color), name=channel_name)
#                     self.plotted_lines.append(line)
#                     legend_items.append((line, channel_name))

#             # Update the legend for raw data
#             self.plot_widget.addLegend(items=legend_items)

#             # Update the legend for filtered data if it's currently shown
#             if self.show_filtered_data:
#                 self.update_filtered_plot()

#             # Hide or show the filtered plot based on the toggle button
#             self.filtered_plot_widget.setVisible(self.show_filtered_data)
#             self.plot_widget.setVisible(not self.show_filtered_data)

#     def get_next_color(self, index, is_filtered=False):
#         # Define color cycles for raw and filtered data
#         raw_colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
#         filtered_colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']

#         colors = filtered_colors if is_filtered else raw_colors

#         # Get the color based on the index and reset if necessary
#         if index < len(colors):
#             return colors[index]
#         else:
#             return colors[index % len(colors)]
        

#     def load_data(self, file_path):
#         # Load the EDF file using MNE
#         self.raw_data = mne.io.read_raw_edf(file_path, preload=True)
#         self.original_data = self.raw_data.copy()  # Save a copy of the original data


# class OpeningWindow(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle('FIVE GUYS')
        
#         self.setGeometry(100, 100, 400, 200)
        

#         layout = QVBoxLayout()
#         load_button = QPushButton('Load Data')
#         load_button.clicked.connect(self.load_file)
#         sample_button = QPushButton('Use Sample Data')
        
#         layout.addWidget(load_button)
#         layout.addWidget(sample_button)
        
#         self.setLayout(layout)

#     def open_secondary_window(self):
#         self.secondary_window = EEGAnalyzer()
#         self.secondary_window.show()

#     def load_data(self, file_path):
#         # Load the EDF file using MNE
#         self.raw_data = mne.io.read_raw_edf(file_path, preload=True)

#     def load_file(self):
#         options = QFileDialog.Options()
#         options |= QFileDialog.ReadOnly

#         file_path, _ = QFileDialog.getOpenFileName(self, "Open EEG/EDF File", "", "EDF Files (*.edf);;All Files (*)", options=options)

#         if file_path:
#             openwindow.close()
#             eeganalyzerInstance.show()
#             eeganalyzerInstance.load_data(file_path)
#             eeganalyzerInstance.create_channel_checkboxes()
            


# if __name__ == '__main__':
#     pg.setConfigOption('background', 'w')  # Set background color to white
#     app = QApplication(sys.argv)
#     eeganalyzerInstance = EEGAnalyzer()
#     openwindow = OpeningWindow()
#     openwindow.show()
#     sys.exit(app.exec_())



import sys
import os
import mne
from mne.preprocessing import ICA
from mne.channels import make_standard_montage, make_dig_montage
import numpy as np
from PyQt5.QtCore import Qt, QTimer
import pyqtgraph as pg
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QFileDialog, QCheckBox, QScrollArea, QGridLayout, QLabel, QLineEdit, QAction
from PyQt5.QtGui import QDoubleValidator
from pyqtgraph.Qt import QtGui
from itertools import cycle

class EEGAnalyzer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.showing_ica_data = False  # Flag to track whether ICA data is currently displayed
        self.show_ica_data_button = None


        self.initUI()

        # Notification label with initial position at the bottom-right
        self.notification_label = QLabel(self)
        self.notification_label.setAlignment(Qt.AlignCenter)
        self.notification_label.setStyleSheet("background-color: #2ecc71; color: white;")
        self.notification_label.setFixedHeight(30)

        # Calculate the position based on screen size
        screen_size = QApplication.primaryScreen().availableGeometry()
        label_size = self.notification_label.size()
        new_x = screen_size.width() - label_size.width()
        new_y = screen_size.height() - label_size.height()
        self.notification_label.move(new_x, new_y)

        self.notification_label.hide()

        self.notification_timer = QTimer(self)
        self.notification_timer.timeout.connect(self.clear_notification)

    def initUI(self):
        self.setWindowTitle("EEG Analyzer")
        self.setGeometry(100, 100, 1000, 600)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QGridLayout(self.central_widget)

        
        self.original_data = None  # Variable to store the original data



        
        # Create a menu bar
        menubar = self.menuBar()
        file_menu = menubar.addMenu('File')
        
        # Add a new menu for ICA Preprocessing
        ica_menu = menubar.addMenu('ICA Preprocessing')
        ica_menu.setToolTipsVisible(True)

        ica_action = QAction('Run Automatic ICA', self)
        ica_action.setToolTip('Applies basic ICA preprocessing for\nsimplified use.')

        #ica_action.triggered.connect(self.run_ica)

        ica_menu.addAction(ica_action)

        # Add actions to the File menu
        load_action = QAction('Load Data', self)
        load_action.triggered.connect(self.load_file)
        file_menu.addAction(load_action)

        sample_action = QAction('Use Sample Data', self)
        file_menu.addAction(sample_action)
        
        # Create a button for Tranform
        transform_menu = menubar.addMenu('Transform')
        transform_menu.setToolTipsVisible(True)
        
        LOGX_action = QAction('Log X', self)
        LOGX_action.setToolTip('Transforms the graph using the Log x function')
        
        LOGY_action = QAction('Log Y', self)
        LOGY_action.setToolTip('Transforms the graph using the Log y function')
        
        
        transform_menu.addAction(LOGX_action)
        transform_menu.addAction(LOGY_action)
        










        # Create a widget to hold the filter options
        filter_options_widget = QWidget()

        # Create a vertical layout for the filter options
        filter_options_layout = QVBoxLayout(filter_options_widget)

        # Create filter controls using text boxes
        self.filter_low_label = QLabel("Low Frequency:")
        self.filter_low_textbox = QLineEdit()
        self.filter_low_textbox.setValidator(QDoubleValidator())

        self.filter_high_label = QLabel("High Frequency:")
        self.filter_high_textbox = QLineEdit()
        self.filter_high_textbox.setValidator(QDoubleValidator())

        self.apply_filter_button = QPushButton("Apply Filter", self)
        self.apply_filter_button.clicked.connect(self.apply_bandpass_filter)



        # Add filter controls to filter_options_layout
        filter_options_layout.addWidget(self.filter_low_label)
        filter_options_layout.addWidget(self.filter_low_textbox)
        filter_options_layout.addWidget(self.filter_high_label)
        filter_options_layout.addWidget(self.filter_high_textbox)
        filter_options_layout.addWidget(self.apply_filter_button)

        # Set a fixed width for filter_options_widget
        filter_options_widget.setFixedWidth(250)

        # Add filter_options_widget to the layout at (0, 0)
        self.layout.addWidget(filter_options_widget, 0, 0)

        # Add a button to remove the bandpass filter
        self.remove_filter_button = QPushButton("Remove Filter", self)
        self.remove_filter_button.clicked.connect(self.remove_bandpass_filter)

        # Add remove_filter_button to filter_options_layout
        filter_options_layout.addWidget(self.remove_filter_button)

        # Create a widget to hold checkboxes with a fixed width
        checkboxes_widget = QWidget()
        checkboxes_widget.setFixedWidth(250)  # Set a fixed width

        # Create a vertical layout for checkboxes
        self.checkboxes_layout = QVBoxLayout(checkboxes_widget)

        self.channel_scroll_area = QScrollArea()
        self.channel_widget = QWidget()
        self.channel_layout = QVBoxLayout(self.channel_widget)
        self.channel_scroll_area.setWidget(self.channel_widget)
        self.channel_scroll_area.setWidgetResizable(True)
        self.checkboxes_layout.addWidget(self.channel_scroll_area)

        # Add checkboxes_widget to the layout at (1, 0)
        self.layout.addWidget(checkboxes_widget, 1, 0)

        # Add the plot widget to the layout at (0, 1)
        self.plot_widget = pg.PlotWidget()
        self.layout.addWidget(self.plot_widget, 0, 1, 2, 1)


        self.create_ica_button()








        self.raw_data = None
        self.channel_checkboxes = []
        self.plotted_lines = []  # List to keep track of plotted lines
        self.legend_items = {}  # Dictionary to map channel names to legend items

        # Create a plot widget for the filtered data
        self.filtered_plot_widget = pg.PlotWidget()
        self.layout.addWidget(self.filtered_plot_widget, 0, 1, 2, 1)

        # Initialize the list for filtered plotted lines
        self.filtered_plotted_lines = []

        # Create a button to toggle between displaying raw and filtered data
        self.toggle_data_button = QPushButton("Show Filtered Data", self)
        self.toggle_data_button.clicked.connect(self.toggle_data)

        # Set the initial button as static
        # self.toggle_data_button.setFixedWidth(120)  # Adjust the width as needed
        self.layout.addWidget(self.toggle_data_button, 2, 1, 1, 1)

        # Flag to track which data is currently displayed
        self.show_filtered_data = False  # Set to True for the initial state

        # Create color cycles for raw and filtered data
        self.colors_raw = cycle(['b', 'g', 'r', 'c', 'm', 'y', 'k'])
        self.colors_filtered = cycle(['b', 'g', 'r', 'c', 'm', 'y', 'k'])
    
        # Initialize the color indices for raw and filtered data
        self.color_index_raw = 0
        self.color_index_filtered = 0
        
        # Flag to track whether filtered data is available
        self.filtered_data_available = False

        # Hide the filtered plot widget initially
        self.filtered_plot_widget.hide()

#Remember this shit for when you try to do layouts later on:
#addWidget(self, a0: QWidget, row: int, column: int, rowSpan: int, columnSpan: int, alignment: Union[Qt.Alignment, Qt.AlignmentFlag] = Qt.Alignment()) <-- This is what the numbers mean next to self.layout.addWidget(xyz, 2, 0, 1, 1)
###
# Big block underneath goes here
###

    






    def create_ica_button(self):
        self.show_ica_data_button = QPushButton("Show ICA Data", self)
        self.show_ica_data_button.clicked.connect(self.run_ica)  # Connect to the run_ica method

        self.layout.addWidget(self.show_ica_data_button, 2, 0, 1, 1)
        self.show_ica_data_button.show()  # Hide the button initially


    def run_ica(self):
        if self.raw_data is not None:
            # Apply ICA
            ica = ICA(n_components=len(self.raw_data.ch_names), random_state=97, max_iter=800)
            ica.fit(self.raw_data)

            # Get the ICA components
            ica_components = ica.get_sources(self.raw_data)  # Pass the raw data to get_sources

            # Update the plot widget with ICA components
            self.update_plot_with_ica(ica_components)

            # Set the flag to indicate that ICA data is currently displayed
            self.show_ica_data = True

    def update_plot_with_ica(self, ica_components):
        # Clear the existing plot
        self.plot_widget.clear()

        # Plot ICA components on the existing plot widget
        num_components = ica_components.info['nchan']
        times = ica_components.times
        data = ica_components.get_data()

        legend_items = []

        for i in range(num_components):
            color = self.get_next_color(i, is_filtered=False)
            channel_data = data[i, :]
            line = self.plot_widget.plot(times, channel_data, pen=pg.mkPen(color), name=f'ICA Component {i + 1}')
            legend_items.append((line, f'ICA Component {i + 1}'))

        # Add legend to the plot
        self.plot_widget.addLegend(items=legend_items)


































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


    def apply_bandpass_filter(self):
        if self.raw_data is not None:
            try:
                low_freq = float(self.filter_low_textbox.text())
                high_freq = float(self.filter_high_textbox.text())
            except ValueError:
                self.show_notification("Invalid Frequency Values", "Please enter valid numerical values for the frequency range.")
                return

            print(f"Applying bandpass filter: Low Frequency = {low_freq}, High Frequency = {high_freq}")

            # Check if the frequencies are within a reasonable range
            if low_freq < 0 or high_freq < 0 or low_freq >= high_freq:
                self.show_notification("Invalid Frequency Range", "Please enter a valid frequency range.")
                return

            # Apply bandpass filter to the filtered_data (not the raw_data)
            self.filtered_data = self.original_data.copy()  # Create a copy of the original data
            self.filtered_data.filter(l_freq=low_freq, h_freq=high_freq, method='fir', fir_window='hamming')

            print("Bandpass filter applied successfully to filtered data.")

            # Update the flag to indicate that filtered data is available
            self.filtered_data_available = True

            # Update the filtered plot
            self.update_filtered_plot()

            # Show a success message using a notification
            self.show_notification("Success", "Bandpass filter applied successfully.")

    def show_notification(self, title, message):
        self.notification_label.setText(f"{title}: {message}")
        self.notification_label.show()

        # Calculate the position based on the window's position and size
        window_size = self.size()
        label_size = self.notification_label.size()
        offset = 10  # Adjust the offset value as needed

        new_x = window_size.width() - label_size.width() - offset  # Bottom-right corner with offset
        new_y = window_size.height() - label_size.height() - offset
        # Adjust the 'left' offset to move the label to the left
        left_offset = 150  # Adjust the left offset as needed
        new_x -= left_offset

        # Set a fixed width (adjust the value as needed)
        self.notification_label.setFixedWidth(250)  # Adjust the width as needed

        self.notification_label.move(new_x, new_y)
        self.notification_timer.start(5000)  # Display for 5 seconds

    def clear_notification(self):
        self.notification_label.clear()
        self.notification_label.hide()
        self.notification_timer.stop()

    # def resizeEvent(self):
    #     # Calculate the new position of the notification label
    #     label_size = self.notification_label.size()
    #     screen_size = QApplication.primaryScreen().availableGeometry()
    #     new_x = screen_size.width() - label_size.width()
    #     new_y = screen_size.height() - label_size.height()

    #     # Set the new position
    #     self.notification_label.move(new_x, new_y)

    def toggle_data(self):
        if self.show_filtered_data:
            self.show_filtered_data = False
            self.toggle_data_button.setText("Show Filtered Data")
        else:
            self.show_filtered_data = True
            self.toggle_data_button.setText("Show Raw Data")

        # Update the visibility of the plot widgets
        self.plot_widget.setVisible(not self.show_filtered_data)
        self.filtered_plot_widget.setVisible(self.show_filtered_data)

    def update_filtered_plot(self):
        if self.filtered_data is not None and self.filtered_data_available:
            data, times = self.filtered_data[:, :]
            num_channels = data.shape[0]
            legend_items = []

            # Remove previously plotted lines for filtered data
            for line in self.filtered_plotted_lines:
                self.filtered_plot_widget.removeItem(line)

            # Reset color index to the beginning
            self.color_index_filtered = 0

            for i, checkbox in enumerate(self.channel_checkboxes):
                if checkbox.isChecked():
                    channel_name = checkbox.text()

                    # Get the color from the current index and update the index
                    color = self.get_next_color(self.color_index_filtered, is_filtered=True)
                    self.color_index_filtered += 1

                    channel_data = data[self.filtered_data.ch_names.index(channel_name), :]
                    line = self.filtered_plot_widget.plot(times, channel_data, pen=pg.mkPen(color), name=channel_name)
                    self.filtered_plotted_lines.append(line)
                    legend_items.append((line, channel_name))

            # Update the legend for the filtered plot
            self.filtered_plot_widget.addLegend(items=legend_items)
    


    def remove_bandpass_filter(self):
        if self.original_data is not None:
            # Restore the original data
            self.raw_data = self.original_data.copy()

            print("Bandpass filter removed successfully.")

            # After removing the filter, update the plot
            self.update_plot()


    def update_plot(self):
        if self.raw_data is not None:
            data, times = self.raw_data[:, :]
            num_channels = data.shape[0]
            selected_channels = []
            legend_items = []

            # Remove previously plotted lines (for both raw and filtered data)
            for line in self.plotted_lines:
                self.plot_widget.removeItem(line)

            # Reset color index to the beginning
            self.color_index_raw = 0

            for i, checkbox in enumerate(self.channel_checkboxes):
                if checkbox.isChecked():
                    channel_name = checkbox.text()
                    selected_channels.append(channel_name)

                    # Get the color from the current index and update the index
                    color = self.get_next_color(self.color_index_raw, is_filtered=False)
                    self.color_index_raw += 1

                    channel_data = data[self.raw_data.ch_names.index(channel_name), :]
                    line = self.plot_widget.plot(times, channel_data, pen=pg.mkPen(color), name=channel_name)
                    self.plotted_lines.append(line)
                    legend_items.append((line, channel_name))

            # Update the legend for raw data
            self.plot_widget.addLegend(items=legend_items)

            # Update the legend for filtered data if it's currently shown
            if self.show_filtered_data:
                self.update_filtered_plot()

            # Hide or show the filtered plot based on the toggle button
            self.filtered_plot_widget.setVisible(self.show_filtered_data)
            self.plot_widget.setVisible(not self.show_filtered_data)

    def get_next_color(self, index, is_filtered=False):
        # Define color cycles for raw and filtered data
        raw_colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
        filtered_colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']

        colors = filtered_colors if is_filtered else raw_colors

        # Get the color based on the index and reset if necessary
        if index < len(colors):
            return colors[index]
        else:
            return colors[index % len(colors)]
        








    def load_data(self, file_path):
        # Load the EDF file using MNE
        self.raw_data = mne.io.read_raw_edf(file_path, preload=True)

        # Extract the channel names from the raw data
        channel_names_raw = self.raw_data.ch_names

        # Create a standard 10-20 montage
        standard_montage = mne.channels.make_standard_montage('standard_1020')

        # Extract the channel names from the standard montage
        channel_names_montage = standard_montage.ch_names

        # Find the intersection of channel names between raw data and montage
        included_channels = list(set(channel_names_raw) & set(channel_names_montage))

        # Check if digitization points are available
        if not self.raw_data.info['dig']:
            print("No digitization points found. Creating a default montage.")
            
            # Manually set the channel types for each channel in raw_data
            for channel in self.raw_data.info['chs']:
                if channel['ch_name'] in included_channels:
                    channel['kind'] = mne.io.constants.FIFF.FIFFV_EEG_CH

            # Set the standard montage to None
            standard_montage = None

        # Ensure that channel names in raw_data match the montage exactly
        self.raw_data.pick_channels(included_channels)

        self.raw_data.set_montage(standard_montage)

        self.original_data = self.raw_data.copy()  # Save a copy of the original data

















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

















    
    # def apply_auto_ica(self):
    #     # Check if raw data is available
    #     if self.raw_data is not None:
    #         # Create an ICA object
    #         ica = ICA(n_components=len(self.raw_data.ch_names), random_state=97, max_iter=800)

    #         # Manually create a DigMontage based on the channel positions in your raw data
    #         ch_pos = dict(zip(self.raw_data.ch_names, self.raw_data.get_channel_positions()))
    #         dig_montage = mne.channels.DigMontage(ch_pos=ch_pos)

    #         # Set the montage
    #         self.raw_data.set_montage(dig_montage)

    #         # Fit the ICA model to the raw data
    #         ica.fit(self.raw_data)

    #         # Plot the ICA components for manual inspection (optional)
    #         ica.plot_components()

    #         # Automatically select and remove artifacts
    #         ica.exclude = []  # Set to exclude the components identified automatically
    #         ica.apply(self.raw_data)

    #         print("Automatic ICA preprocessing completed.")

    #         # Update the plot after preprocessing
    #         self.update_plot()
    #     else:
    #         print("No raw data available for ICA preprocessing.")















    # def apply_auto_ica(self):
    #     if self.raw_data is not None:
    #         # Create an ICA object
    #         ica = ICA(n_components=len(self.raw_data.ch_names), random_state=97, max_iter=800)

    #         # Fit the ICA model to the raw data
    #         ica.fit(self.raw_data)

    #         # Automatically exclude a fixed number or percentage of components
    #         # n_components_to_exclude = 5  # Adjust this number as needed
    #         # OR
    #         percentage_to_exclude = 20  # Adjust this percentage as needed

    #         # Set the components to exclude
    #         # ica.exclude = list(range(n_components_to_exclude))
    #         # OR
    #         ica.exclude = list(range(int(len(ica.mixing_matrix_) * (percentage_to_exclude / 100))))

    #         # Apply ICA with the specified exclusions
    #         ica.apply(self.raw_data)

    #         print("Automatic ICA preprocessing completed.")

    #     else:
    #         print("No raw data available for ICA preprocessing.")







    # def run_ica(self):
    #     # Apply automatic ICA preprocessing
    #     self.apply_auto_ica()

    #     # Check if the ICA button is not already created
    #     if self.show_ica_data_button is None:
    #         # Create the button to show ICA data
    #         self.create_ica_button()

    #         # Show the ICA button
    #         self.show_ica_data_button.show()

    #         # Call the method to show the ICA data plot
    #         self.show_ica_data_plot()
    #     if self.showing_ica_data:
    #         self.show_ica_data_plot()
    #     else:
    #         self.update_plot()




    #     # Add your actual ICA preprocessing logic here
    #     # Once the ICA preprocessing is done, you can call the method to show the ICA data plot
    #     # self.show_ica_data_plot()


    # def create_ica_button(self):
    #     self.show_ica_data_button = QPushButton("Show ICA Data", self)
    #     self.show_ica_data_button.clicked.connect(self.toggle_ICA_data_view)  # Connect to the toggle_data_view method
    #     self.layout.addWidget(self.show_ica_data_button, 2, 0, 1, 1)
    #     self.show_ica_data_button.hide()  # Hide the button initially


    # def toggle_ICA_data_view(self):
    #     self.showing_ica_data = not self.showing_ica_data

    #     if self.showing_ica_data:
    #         self.toggle_data_button.setText("Show Raw Data")
    #         self.show_ica_data_plot()
    #     else:
    #         self.toggle_data_button.setText("Show ICA Data")
    #         self.update_plot()





    # def show_ica_data_plot(self):
    #     # Check if ICA data is available
    #     if hasattr(self.raw_data, 'ica_') and self.raw_data.ica_ is not None:
    #         ica_data = self.raw_data.ica_.get_sources()

    #         # Plot ICA data
    #         data, times = ica_data[:, :]
    #         num_channels = data.shape[0]
    #         legend_items = []

    #         # Remove previously plotted lines for ICA data
    #         for line in self.filtered_plotted_lines:
    #             self.filtered_plot_widget.removeItem(line)

    #         # Reset color index to the beginning
    #         self.color_index_filtered = 0

    #         for i, checkbox in enumerate(self.channel_checkboxes):
    #             if checkbox.isChecked():
    #                 channel_name = checkbox.text()

    #                 # Get the color from the current index and update the index
    #                 color = self.get_next_color(self.color_index_filtered, is_filtered=True)
    #                 self.color_index_filtered += 1

    #                 channel_data = data[self.raw_data.ch_names.index(channel_name), :]
    #                 line = self.filtered_plot_widget.plot(times, channel_data, pen=pg.mkPen(color), name=channel_name)
    #                 self.filtered_plotted_lines.append(line)
    #                 legend_items.append((line, channel_name))

    #         # Update the legend for the ICA plot
    #         self.filtered_plot_widget.addLegend(items=legend_items)
    #     else:
    #         print("ICA data not available. Run automatic ICA preprocessing first.")