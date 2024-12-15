# Third-party libraries
import PySimpleGUI as sg

# Local application
from crt.save_as.gui import SaveAsGUI
from crt.language import Language

class SaveAs:
    """
    Save CRT as a time file.
    """
    def __init__(self, language: Language):
        
        self.window = SaveAsGUI(language.content)
    
    def run(self):
        while True:
            event, values = self.window.read()
            
            match event:
                case "save":
                    file_path = values["file_name"]
                    break
                
                case "cancel" | sg.WIN_CLOSED:
                    file_path = None
                    break
        
        self.window.close()
        
        return file_path
    