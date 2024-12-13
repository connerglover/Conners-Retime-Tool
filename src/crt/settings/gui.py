import PySimpleGUI as sg

import re
from decimal import Decimal as d

class SettingsGUI:
    def __init__(self, enable_updates: bool, theme: str):
        self.window = self._create_window(enable_updates, theme)

    def _create_window(self, enable_updates: bool, theme: str):
        layout = [
            [sg.Text("CRT Settings", font=("Helvetica", 24))],
            [sg.Push(), sg.Checkbox("Automatically Check for Updates", default=enable_updates, key="enable_updates")],
            [sg.Push(), sg.Text("Theme", font=("Helvetica", 16)), sg.Combo(["Automatic", "Dark", "Light"], key="theme", default_value=theme)],
            [sg.HorizontalSeparator()],
            [sg.Button("Restore Defaults"), sg.Button("Apply"), sg.Button("Cancel")],
        ]
        return sg.Window("CRT Settings", layout, icon="icon.ico")
    
    def _clean_framerate(self,framerate: str) -> d:
        cleaned_framerate = re.sub(r'[^0-9.]', '', framerate)
        
        if not re.search(r'[0-9]', cleaned_framerate):
            return "0"
        
        if cleaned_framerate.count('.') > 1:
            first_period_index = cleaned_framerate.find('.')
            cleaned_framerate = cleaned_framerate[:first_period_index + 1] + cleaned_framerate[first_period_index + 1:].replace('.', '')
        
        if cleaned_framerate.endswith('.'):
            cleaned_framerate += '0'
        
        cleaned_framerate = d(cleaned_framerate)
        
        return cleaned_framerate
    
    def read(self):
        """
        Reads the main window.
        
        Returns:
            tuple[str, Any]: The event and values.
        """
        return self.window.read()
    
    def close(self):
        """
        Closes the main window.
        """
        self.window.close()
    
    def __enter__(self):
        """
        Enters the main window.
        
        Returns:
            MainWindow: The main window.
        """
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Exits the main window.
        """
        self.close()