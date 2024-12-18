# Standard library
import os
from configparser import ConfigParser
from typing import NoReturn, Optional

# Third-party
import PySimpleGUI as sg
import appdirs

# Local application
from crt.language import Language
from crt.app_settings.gui import SettingsGUI

class Settings:
    """Settings for CRT.
    """
    def __init__(self) -> NoReturn:
        """Initializes the Settings class.
        """        
        self.config = ConfigParser()
        
        self.file_path = os.path.join(appdirs.user_config_dir("CRT"), "settings.ini")
        self.defaults = {
            "enable_updates": "True",
            "theme": "Automatic",
            "language": "en",
            "mod_note_format": "Mod Note {time_without_loads} without loads, and {time_with_loads} with loads at {fps} FPS using {plug}"
        }
        
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        
        if not os.path.exists(self.file_path):
            self._restore_defaults(False)
        else:
            self.config.read(self.file_path)
        
        self._settings_cache = None
        self._sync_missing_settings()
        
        self.language = Language(self.config.get("Settings", "language"))

    def _restore_defaults(self, prompt: Optional[bool] = True) -> NoReturn:
        """Restores the settings back to the defautls.
        """        
        if prompt:
            confirmation = sg.popup_yes_no("Are you sure you want to restore the default settings?", title="Restore Defaults")
            
            if confirmation == "No":
                return
        
        self.config = ConfigParser()
        self.config.add_section("Settings")
        for key, value in self.defaults.items():
            self.config.set("Settings", key, value)
        with open(self.file_path, "w") as file:
            self.config.write(file)
        self._settings_cache = None

    def _apply_theme(self, theme: str) -> NoReturn:
        """Applies the theme to the settings.

        Args:
            theme (str): Name of the theme.
        """        
        en_theme = self.language.translate(self.language.language, "en", theme)
        self.config.set("Settings", "theme", str(en_theme))
    
    def _apply(self, values: dict) -> NoReturn:
        """Applies the settings.

        Args:
            values (dict): The values from the settings window.
        """        
        with open(self.file_path, "w") as file:
            self.config.set("Settings", "enable_updates", str(values["enable_updates"]))
            self._apply_theme(values["theme"])
            self.config.set("Settings", "language", str(values["language"]))
            self.config.set("Settings", "mod_note_format", str(values["mod_note_format"]))
            self.config.write(file)
        self._settings_cache = None
    
    def config_to_dict(self) -> dict:
        """Converts the settings into a dictionary.

        Returns:
            dict: The dictionary of settings.
        """        
        if self._settings_cache is None:
            self._settings_cache = {
                "enable_updates": self.config.getboolean("Settings", "enable_updates"),
                "theme": self.config.get("Settings", "theme"),
                "language": self.config.get("Settings", "language"),
                "mod_note_format": self.config.get("Settings", "mod_note_format")
            }
        return self._settings_cache
    
    def _sync_missing_settings(self) -> NoReturn:
        """Syncs the settings that aren't present in the config file.
        """        
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
    
    def open_window(self) -> NoReturn:
        """Opens the settings window.
        """        
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
