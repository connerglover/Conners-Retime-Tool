import PySimpleGUI as sg

from crt.save_as.gui import SaveAsGUI

class SaveAs:
    """
    Save CRT as a time file.
    """
    def __init__(self):
        self.window = SaveAsGUI()
    
    def run(self):
        while True:
            event, values = self.window.read()
            
            match event:
                case "save":
                    file_path = values["file_name"]
                    break
                
                case "cancel":
                    file_path = None
                    break
                
                case sg.WIN_CLOSED:
                    file_path = None
                    break
        
        self.window.close()
        
        return file_path