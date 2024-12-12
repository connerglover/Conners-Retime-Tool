import PySimpleGUI as sg
from decimal import Decimal as d

from crt.time import Time

class LoadViewerGUI:
    """
    Load viewer GUI for CRT.
    """
    def __init__(self, time: Time):
        """
        Initializes the LoadViewerGUI class.
        
        Args:
            time (Time): The time.
        """
        self.window = self._create_window(time)
    
    def _create_window(self, time: Time) -> sg.Window:
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
                sg.Button("Edit", font=("Helvetica", 14), key=f"edit_{index}"),
                sg.Button("Delete", font=("Helvetica", 14), key=f"delete_{index}")
            ]], key=f"load_{index}"))] for index, load in enumerate(time.loads)
        ]
        
        layout = [
            [sg.Text("Loads", font=("Helvetica", 24))],
            *layout
        ]

        return sg.Window("Load Viewer", layout, resizable=False, element_justification="left")
    
    def read(self) -> tuple[str, dict]:
        """
        Reads the load viewer GUI.
        
        Returns:
            tuple[str, dict]: The event and values.
        """
        return self.window.read()
    
    def close(self):
        """
        Closes the load viewer GUI.
        """
        self.window.close()
    
    def __enter__(self):
        """
        Enters the load viewer GUI.
        """
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Exits the load viewer GUI.
        """
        self.close()
