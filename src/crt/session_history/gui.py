import PySimpleGUI as sg

class SessionHistoryGUI:
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
    
    def read(self) -> tuple[str, dict]:
        """
        Reads the session history GUI.
        
        Returns:
            tuple[str, dict]: The event and values.
        """
        return self.window.read()
    
    def close(self):
        """
        Closes the session history GUI.
        """
        self.window.close()
    
    def __enter__(self):
        """
        Enters the session history GUI.
        """
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Exits the session history GUI.
        """
        self.close()
        