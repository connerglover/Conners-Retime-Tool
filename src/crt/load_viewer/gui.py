# Standard library
from decimal import Decimal as d
from typing import NoReturn

# Third party
import PySimpleGUI as sg

# Local application
from crt.time import Time
from crt.base_gui import BaseGUI

class LoadViewerGUI(BaseGUI):
    """
    Load viewer GUI for CRT.
    """
    def __init__(self, time: Time, content: dict) -> NoReturn:
        """
        Initializes the LoadViewerGUI class.
        
        Args:
            time (Time): The time.
        """
        
        self.window = self._create_window(time, content)
    
    def _create_window(self, time: Time, content: dict) -> sg.Window:
        """
        Creates the load viewer GUI.
        
        Args:
            time (Time): The time.
        
        Returns:
            sg.Window: The load viewer GUI.
        """
        layout = [
            [sg.pin(sg.Col([[
                sg.Text(f"{index+1}: {round(d(load.length / time.framerate), time.precision)}", font=("Helvetica", 20), key=f"display_{index}"),
                sg.Button(content["Edit"], font=("Helvetica", 14), key=f"edit_{index}"),
                sg.Button(content["Delete"], font=("Helvetica", 14), key=f"delete_{index}")
            ]], key=f"load_{index}"))] for index, load in enumerate(time.loads)
        ]
        
        layout = [
            [sg.Text(content["Loads"], font=("Helvetica", 24))],
            *layout
        ]

        return sg.Window("Load Viewer", layout, resizable=False)