import PySimpleGUI as sg

from crt.base_gui import BaseGUI

class SessionHistoryGUI(BaseGUI):
    """
    Session history GUI for CRT.
    """
    def __init__(self, past_file_paths: list[str], content: dict):
        """
        Initializes the SessionHistoryGUI class.
        """
        
        self.window = self._create_window(past_file_paths, content)

    
    def _create_window(self, past_file_paths: list[str], content: dict) -> sg.Window:
        """
        Creates the session history GUI.
        
        Returns:
            sg.Window: The session history GUI.
        """
        layout = [
            [sg.Listbox(values=past_file_paths, size=(50, 10), bind_return_key=True, key="session_history", font=("Helvetica", 14))],
        ]

        return sg.Window("Session History", layout, resizable=False)