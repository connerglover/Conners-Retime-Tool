# Standard Library
from typing import NoReturn

# Third-party
import PySimpleGUI as sg

# Local application
from crt.base_gui import BaseGUI

class SaveAsGUI(BaseGUI):
    """Save CRT as a time file GUI for CRT.
    """
    def __init__(self, content: dict) -> NoReturn:
        """Initializes the SaveAsGUI class.
        """
        
        self.window = self._create_window(content)

    
    def _create_window(self, content: dict) -> sg.Window:
        """Creates the save as GUI.
        
        Returns:
            sg.Window: The save as GUI.
        """
        layout = [
            [sg.Text(content["Save As"], font=("Helvetica", 24))],
            [sg.Text(content["File Name"], font=("Helvetica", 14), key = "File "), sg.SaveAs(key="file_name", file_types=(("Load Files", "*.json"),))],
            [sg.Button(content["Save"], font=("Helvetica", 14), key="save"), sg.Button(content["Cancel"], font=("Helvetica", 14), key="cancel")]
        ]

        return sg.Window("Save As", layout, resizable=False)