import PySimpleGUI as sg

import re
from decimal import Decimal as d

class SettingsGUI:
    def __init__(self, settings: dict, content: dict):
        enable_updates = settings["enable_updates"]
        theme = settings["theme"]
        language = settings["language"]
        mod_note_format = settings["mod_note_format"]
        
        self.window = self._create_window(enable_updates, theme, language, mod_note_format, content)

    def _create_window(self, enable_updates: bool, theme: str, language:str, mod_note_format: str, content: dict) -> sg.Window:
        layout = [
            [sg.Text(content["CRT Settings"], font=("Helvetica", 24))],
            [sg.Push(), sg.Checkbox(content["Automatically Check for Updates"], default=enable_updates, key="enable_updates")],
            [sg.Push(), sg.Text(content["Theme"], font=("Helvetica", 16)), sg.Combo([content["Automatic"], content["Dark"], content["Light"]], key="theme", default_value=theme)],
            [sg.Push(), sg.Text(content["Language"], font=("Helvetica", 16)), sg.Combo(["English", "Español", "Français", "Polski"], key="language", default_value=language)],
            [sg.Push(), sg.Text(content["Mod Note Format"], font=("Helvetica", 16)), sg.Input(key="mod_note_format", default_text=mod_note_format)],
            [sg.HorizontalSeparator()],
            [sg.Button(content["Restore Defaults"], key="Restore Defaults"), sg.Button(content["Apply"], key="Apply"), sg.Button(content["Cancel"], key="Cancel")],
        ]
        return sg.Window("CRT Settings", layout, resizable=False)
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