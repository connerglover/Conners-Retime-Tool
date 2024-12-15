# Standard library
import PySimpleGUI as sg

# Local application
from crt.session_history.gui import SessionHistoryGUI
from crt.language import Language

class SessionHistory:
    """
    Session history for CRT.
    """
    def __init__(self, language: Language, past_file_paths: list[str]):
        """
        Initializes the SessionHistory class.
        """
        
        if not past_file_paths:
            raise ValueError("No session history.")
        
        self.window = SessionHistoryGUI(past_file_paths, language.content)

    
    def run(self) -> str:
        """
        Runs the session history.
        
        Returns:
            str: The file path.
        """
        while True:
            event, values = self.window.read()
            
            match event:
                case "session_history":
                    file_path = values["session_history"][0]
                    break
                
                case sg.WIN_CLOSED:
                    file_path = None
                    break
        
        self.window.close()
        
        return file_path