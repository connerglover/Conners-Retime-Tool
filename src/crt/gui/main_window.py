import PySimpleGUI as sg
from os import path

class MainWindow:
    def __init__(self):
        self.window = self._create_window()
    
    def _create_window(self) -> sg.Window:
        layout = [
            [sg.Push(), sg.Text("Framerate (FPS)", font=("Helvetica", 16), justification="right"), sg.Input(default_text="60", key="framerate", enable_events=True, font=("Helvetica", 16), pad=((5, 0), (0, 0)), size=(12, 1)), sg.Button("Paste", font=("Helvetica", 10), key="framerate_paste")],
            [sg.Push(), sg.Text("Start Frame", font=("Helvetica", 16), justification="right"), sg.Input(default_text="0", key="start", enable_events=True, font=("Helvetica", 16), pad=((5, 0), (0, 0)), size=(12, 1)), sg.Button("Paste", font=("Helvetica", 10), key="start_paste")],
            [sg.Push(), sg.Text("End Frame", font=("Helvetica", 16), justification="right"), sg.Input(default_text="0", key="end", enable_events=True, font=("Helvetica", 16), pad=((5, 0), (0, 0)), size=(12, 1)), sg.Button("Paste", font=("Helvetica", 10), key="end_paste")],
            [sg.Push(), sg.Text("Start Frame (Loads)", font=("Helvetica", 16), justification="right"), sg.Input(default_text="0", key="start_loads", enable_events=True, font=("Helvetica", 16), pad=((5, 0), (0, 0)), size=(12, 1)), sg.Button("Paste", font=("Helvetica", 10), key="start_loads_paste")],
            [sg.Push(), sg.Text("End Frame (Loads)", font=("Helvetica", 16), justification="right"), sg.Input(default_text="0", key="end_loads", enable_events=True, font=("Helvetica", 16), pad=((5, 0), (0, 0)), size=(12, 1)), sg.Button("Paste", font=("Helvetica", 10), key="end_loads_paste")],
            [sg.HorizontalSeparator()],
            [sg.Button("Copy Mod Note", font=("Helvetica", 18)), sg.Button("Add Loads", font=("Helvetica", 18)), sg.Button("Edit Loads", font=("Helvetica", 18))],
            [sg.Text("Without Loads:", font=("Helvetica", 20), justification="right"), sg.StatusBar("00.000", key="without_loads_display", enable_events=True, font=("Helvetica", 20), size=(17,1), tooltip="Click to Copy Time")],
            [sg.Text("Loads:", font=("Helvetica", 20), justification="right"), sg.StatusBar("00.000", key="loads_display", enable_events=True, font=("Helvetica", 20), size=(17,1), tooltip="Click to Copy Time")]
        ]

        return sg.Window("Conner's Retime Tool", layout, icon="icon.ico")
    
    def read(self):
        return self.window.read()
    
    def close(self):
        self.window.close()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()