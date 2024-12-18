# Standard library
from decimal import Decimal as d
from typing import NoReturn

# Third-party
import PySimpleGUI as sg

# Local application
from crt.load import Load
from crt.base_gui import BaseGUI

class LoadEditorGUI(BaseGUI):
    """
    Load editor GUI for CRT.
    """
    def __init__(self, load: Load, framerate: d, content: dict) -> NoReturn:
        """
        Initializes the LoadEditorGUI class.
        
        Args:
            load (Load): The load.
            framerate (d): The framerate.
        """
        
        self.window = self._create_window(load, framerate, content)
    
    def _create_window(self, load: Load, framerate: d, content: dict) -> sg.Window:
        """
        Creates the load editor GUI.
        
        Args:
            load (Load): The load.
            framerate (d): The framerate.
        
        Returns:
            sg.Window: The load editor GUI.
        """
        layout = [
            [sg.Text(content["Edit Load"], font=("Helvetica", 24))],
            [sg.Push(), sg.Text(content["Start Frame"], font=("Helvetica", 16), justification="right"), 
             sg.Input(default_text=str(load.start_frame), key="start", enable_events=True, 
                     font=("Helvetica", 16), pad=((5, 0), (0, 0)), size=(12, 1)), 
             sg.Button(content["Paste"], font=("Helvetica", 10), key="start_paste")],
            [sg.Push(), sg.Text(content["End Frame"], font=("Helvetica", 16), justification="right"), 
             sg.Input(default_text=str(load.end_frame), key="end", enable_events=True, 
                     font=("Helvetica", 16), pad=((5, 0), (0, 0)), size=(12, 1)), 
             sg.Button(content["Paste"], font=("Helvetica", 10), key="end_paste")],
            [sg.Button(content["Save Edits"], font=("Helvetica", 14), key="Save Edits"), 
             sg.Button(content["Discard Changes"], font=("Helvetica", 14), key="Discard Changes")],
        ]

        return sg.Window("Editing Load", layout, resizable=False)