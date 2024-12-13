from crt.settings.gui import SettingsGUI

from configparser import ConfigParser

import os
import PySimpleGUI as sg

class SettingsApp:
    def __init__(self):
        self.config = ConfigParser()
        
        self.file_path = os.path.join(os.getenv('APPDATA'), "CRT", "settings.ini")
        
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        
        if not os.path.exists(self.file_path):
            self._restore_defaults()
        else:
            self.config.read(self.file_path)

    def _restore_defaults(self):
        with open(self.file_path, "w") as file:
            self.config.set("Settings", "enable_updates", "True")
            self.config.set("Settings", "theme", "Automatic")
            self.config.write(file)

    def _apply(self, values):
        self.config.set("Settings", "enable_updates", str(values["enable_updates"]))
        self.config.set("Settings", "theme", str(values["theme"]))
        self.config.write(open(self.file_path, "w"))
    
    def config_to_dict(self):
        return {
            "enable_updates": self.config.getboolean("Settings", "enable_updates"),
            "theme": self.config.get("Settings", "theme"),
        }
    
    def open_window(self):
        settings = self.config_to_dict()
        
        self.window = SettingsGUI(settings["enable_updates"], settings["theme"])
        
        while True:
            event, values = self.window.read()
            
            match event:
                case "Restore Defaults":
                    self._restore_defaults()
                
                case "Apply":
                    self._apply(values)
                    break
                
                case "Cancel":
                    break
                
                case sg.WIN_CLOSED:
                    break
        
        self.window.close()
