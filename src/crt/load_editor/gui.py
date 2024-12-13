import PySimpleGUI as sg
from decimal import Decimal as d

from crt.load import Load

class LoadEditorGUI:
    """
    Load editor GUI for CRT.
    """
    def __init__(self, load: Load, framerate: d):
        """
        Initializes the LoadEditorGUI class.
        
        Args:
            load (Load): The load.
            framerate (d): The framerate.
        """
        self.window = self._create_window(load, framerate)
    
    def _create_window(self, load: Load, framerate: d) -> sg.Window:
        """
        Creates the load editor GUI.
        
        Args:
            load (Load): The load.
            framerate (d): The framerate.
        
        Returns:
            sg.Window: The load editor GUI.
        """
        layout = [
            [sg.Text("Edit Load", font=("Helvetica", 24))],
            [sg.Push(), sg.Text(f"Start Frame", font=("Helvetica", 16), justification="right"), 
             sg.Input(default_text=str(load.start_frame), key="start", enable_events=True, 
                     font=("Helvetica", 16), pad=((5, 0), (0, 0)), size=(12, 1)), 
             sg.Button("Paste", font=("Helvetica", 10), key="start_paste")],
            [sg.Push(), sg.Text(f"End Frame", font=("Helvetica", 16), justification="right"), 
             sg.Input(default_text=str(load.end_frame), key="end", enable_events=True, 
                     font=("Helvetica", 16), pad=((5, 0), (0, 0)), size=(12, 1)), 
             sg.Button("Paste", font=("Helvetica", 10), key="end_paste")],
            [sg.Button("Save Edits", font=("Helvetica", 14)), 
             sg.Button("Discard Changes", font=("Helvetica", 14))]
        ]

        return sg.Window("Editing Load", layout, resizable=False, element_justification="left")
    
    def read(self) -> tuple[str, dict]:
        """
        Reads the load editor GUI.
        
        Returns:
            tuple[str, dict]: The event and values.
        """
        return self.window.read()
    
    def close(self):
        """
        Closes the load editor GUI.
        """
        self.window.close()
    
    def __enter__(self):
        """
        Enters the load editor GUI.
        
        Returns:
            LoadEditorGUI: The load editor GUI.
        """ 
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Exits the load editor GUI.
        """
        self.close()
        