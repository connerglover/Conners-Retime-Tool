from crt.app_settings.gui import SettingsGUI

from configparser import ConfigParser
import os
import appdirs

import PySimpleGUI as sg

from crt.language import Language

class SettingsApp:
    def __init__(self):
        self.config = ConfigParser()
        
        self.file_path = os.path.join(appdirs.user_config_dir("CRT"), "settings.ini")
        self.defaults = {
            "enable_updates": "True",
            "theme": "Automatic",
            "language": "en",
        }
        
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        
        if not os.path.exists(self.file_path):
            self._restore_defaults()
        else:
            self.config.read(self.file_path)
        
        self._settings_cache = None
        self._sync_missing_settings()
        
        self.language = Language(self.config.get("Settings", "language"))

    def _restore_defaults(self):
        self.config = ConfigParser()
        self.config.add_section("Settings")
        for key, value in self.defaults.items():
            self.config.set("Settings", key, value)
        with open(self.file_path, "w") as file:
            self.config.write(file)
        self._settings_cache = None

    def _apply_theme(self, theme):
        en_theme = self.language.translate(self.language.language, "en", theme)
        self.config.set("Settings", "theme", str(en_theme))
    
    def _apply(self, values):
        with open(self.file_path, "w") as file:
            self.config.set("Settings", "enable_updates", str(values["enable_updates"]))
            self._apply_theme(values["theme"])
            self.config.set("Settings", "language", str(values["language"]))
            self.config.write(file)
        self._settings_cache = None
    
    def config_to_dict(self):
        if self._settings_cache is None:
            self._settings_cache = {
                "enable_updates": self.config.getboolean("Settings", "enable_updates"),
                "theme": self.config.get("Settings", "theme"),
                "language": self.config.get("Settings", "language"),
            }
        return self._settings_cache
    
    def _sync_missing_settings(self):
        """Ensure all default settings are present in the config file."""
        if not self.config.has_section("Settings"):
            self.config.add_section("Settings")
        
        updated = False
        for key, value in self.defaults.items():
            if not self.config.has_option("Settings", key):
                self.config.set("Settings", key, value)
                updated = True
        
        if updated:
            with open(self.file_path, "w") as file:
                self.config.write(file)
            self._settings_cache = None
    
    def open_window(self):
        settings = self.config_to_dict()
        
        self.window = SettingsGUI(settings, self.language.content)
        
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
