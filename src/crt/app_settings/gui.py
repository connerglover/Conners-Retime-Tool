# Standard library
import PySimpleGUI as sg
import re

# Third-party
from decimal import Decimal as d

# Local application
from crt.base_gui import BaseGUI

class SettingsGUI(BaseGUI):
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