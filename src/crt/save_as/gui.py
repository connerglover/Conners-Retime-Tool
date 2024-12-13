import PySimpleGUI as sg
from decimal import Decimal as d

class SaveAsGUI:
    """
    Save CRT as a time file GUI for CRT.
    """
    def __init__(self):
        """
        Initializes the SaveAsGUI class.
        """
        self.window = self._create_window()
    
    def _create_window(self) -> sg.Window:
        """
        Creates the save as GUI.
        
        Returns:
            sg.Window: The save as GUI.
        """
        layout = [
            [sg.Text("Save As", font=("Helvetica", 24))],
            [sg.Text("File Name", font=("Helvetica", 14)), sg.SaveAs(key="file_name", file_types=(("Load Files", "*.json"),))],
            [sg.Button("Save", font=("Helvetica", 14), key="save"), sg.Button("Cancel", font=("Helvetica", 14), key="cancel")]
        ]

        return sg.Window("Save As", layout, resizable=False, element_justification="left")
    
    def read(self) -> tuple[str, dict]:
        """
        Reads the save as GUI.
        
        Returns:
            tuple[str, dict]: The event and values.
        """
        return self.window.read()
    
    def close(self):
        """
        Closes the save as GUI.
        """
        self.window.close()
    
    def __enter__(self):
        """
        Enters the save as GUI.
        """
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Exits the save as GUI.
        """
        self.close()