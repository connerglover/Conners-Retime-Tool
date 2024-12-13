import PySimpleGUI as sg
import json
import re
import darkdetect

from webbrowser import open as open_url
from requests import get as get_url
from decimal import Decimal as d

from crt._version import __version__
from crt.time import Time
from crt.load import Load
from crt.gui import MainWindow
from crt.load_viewer.app import LoadViewer
from crt.save_as.app import SaveAs
from crt.settings.app import SettingsApp

class App:
    """
    Main application for CRT.
    """
    def __init__(self):
        """
        Initializes the App class.
        """
        self.time = Time()
        self.file_path = None
        
        self.settings = SettingsApp()
        self.settings_dict = self.settings.config_to_dict()
        
        match self.settings_dict["theme"]:
            case "Automatic":
                if darkdetect.isDark():
                    sg.theme("DarkGrey15")
                else:
                    sg.theme("LightGray1")
            case "Dark":
                sg.theme("DarkGrey15")
            case "Light":
                sg.theme("LightGray1")
        
        if self.settings_dict["enable_updates"]:
            self._check_for_updates()
        
        self.window = MainWindow()
        
    def _check_for_updates(self):
        """
        Checks for updates.
        """
        response = get_url("https://api.github.com/repos/connerglover/Conners-Retime-Tool/releases/latest")
        if response.status_code == 200:
            latest_release = response.json()
            latest_version = latest_release["tag_name"]
            if str(latest_version) != str(__version__):
                confirmation = sg.popup_yes_no("Update Available", f"A new version of CRT is available: {latest_version}. Would you like to update?")
                if confirmation == "Yes":
                    open_url("https://github.com/connerglover/Conners-Retime-Tool/releases/latest")
    
    def _edit_loads(self):
        """
        Edits the loads.
        """
        if self.time.loads:
            try:
                load_window = LoadViewer(self.time)
                load_window.run()
            except ValueError as e:
                self._show_error(e)
            finally:
                self.window.window["loads_display"].update(self.time.iso_format(True))
        else:
            self._show_error("No loads to edit.")
    
    def _add_loads(self, values):
        """
        Adds the loads.
        
        Args:
            values (dict): The values from the main window.
        """
        start_frame = int(values["start_loads"])
        end_frame = int(values["end_loads"])
        
        try:
            self.time.add_load(start_frame, end_frame)
        except ValueError as e:
            self._show_error(e)
        else:
            self.window.window["start_loads"].update("0")
            self.window.window["end_loads"].update("0")
            sg.popup("Loads", "Load added successfully.")
    
    def debug_info_to_frame(self, time: Time, debug_info: str) -> int:
        """
        Converts debug info to a frame.
        
        Args:
            time (Time): The time.
            debug_info (str): The debug info.
        
        Returns:
            int: The frame.
        """
        debug_info = "{" + debug_info.split("{", 1)[-1]
        
        try:
            parsed_debug_info = json.loads(debug_info)
        except json.decoder.JSONDecodeError:
            raise ValueError("The debug info provided is invalid.\nPlease re-enter debug info.")
        
        try:
            cmt = parsed_debug_info["cmt"]
        except KeyError:
            raise ValueError("The debug info provided is invalid.\nPlease re-enter debug info.")
        
        output = d(cmt) * d(time.framerate)
        output = int(round(output, 0))
        
        return output

    def _handle_framerate(self, values: dict):
        """
        Handles the framerate.
        
        Args:
            values (dict): The values from the main window.
        """
        framerate = values["framerate"]
        framerate = self._clean_framerate(framerate)
        
        self.window.window["framerate"].update(framerate)
        self.time.mutate(framerate=framerate)
    
    def _handle_time(self, values: dict, key: str):
        """
        Handles the time.
        
        Args:
            values (dict): The values from the main window.
            key (str): The key of the time.
        """
        time = values[key]
        if time and time[-1] == "}":
            try:
                time_frame = self.debug_info_to_frame(self.time, time)
            except ValueError as e:
                if key == "start":
                    time_frame = self.time.start_frame
                elif key == "end":
                    time_frame = self.time.end_frame
                else:
                    raise ValueError("Invalid key provided.")
                self._show_error(e)
        else:
            time_frame = self.clean_frame(time)
        
        try:
            if key == "start":
                self.time.mutate(start_frame=time_frame)
            elif key == "end":
                self.time.mutate(end_frame=time_frame)
        except ValueError as e:
            self._show_error(e)
            time_frame = self.time.start_frame
        
        self.window.window[key].update(time_frame)
    
    def _handle_loads(self, values: dict, key: str):
        """
        Handles the loads.
        
        Args:
            values (dict): The values from the main window.
            key (str): The key of the loads.
        """
        loads = values[key]
        if loads and loads[-1] == "}":
            try:
                loads = self.debug_info_to_frame(self.time, loads)
            except ValueError as e:
                loads = 0
                self._show_error(e)
        else:
            loads = self.clean_frame(loads)
        
        self.window.window[key].update(loads)
    
    def _clean_framerate(self,framerate: str) -> d:
        cleaned_framerate = re.sub(r'[^0-9.]', '', framerate)
        
        if not re.search(r'[0-9]', cleaned_framerate):
            return "0"
        
        if cleaned_framerate.count('.') > 1:
            first_period_index = cleaned_framerate.find('.')
            cleaned_framerate = cleaned_framerate[:first_period_index + 1] + cleaned_framerate[first_period_index + 1:].replace('.', '')
        
        if cleaned_framerate.endswith('.'):
            cleaned_framerate += '0'
        
        cleaned_framerate = d(cleaned_framerate)
        
        return cleaned_framerate

    def clean_frame(self, frame: str) -> int:
        """
        Cleans the frame.
        
        Args:
            frame (str): The frame.
        
        Returns:
            int: The cleaned frame.
        """
        if any(char.isdigit() for char in frame):
            cleaned_frame = int(re.sub(r"[^0-9]", "", frame))
        else:
            cleaned_frame = 0
        
        return cleaned_frame
    
    def _paste_framerate(self, values: dict):
        """
        Pastes the framerate.
        
        Args:
            values (dict): The values from the main window.
        """
        framerate = sg.clipboard_get()
        framerate = self._clean_framerate(framerate)
        
        self.window.window["framerate"].update(framerate)
        self.time.mutate(framerate=framerate)
    
    def _paste_time(self, values: dict, key: str):
        """
        Pastes the time.
        
        Args:
            values (dict): The values from the main window.
            key (str): The key of the time.
        """
        time = sg.clipboard_get()
        if time and time[-1] == "}":
            try:
                time_frame = self.debug_info_to_frame(self.time, time)
            except ValueError as e:
                if key == "start":
                    time_frame = self.time.start_frame
                elif key == "end":
                    time_frame = self.time.end_frame
                else:
                    raise ValueError("Invalid key provided.")
                self._show_error(e)
        elif "." in time:
            time_frame = self.time.framerate * d(time)
            time_frame = int(round(time_frame, 0))
        else:
            time_frame = self.clean_frame(time)
        
        try:
            if key == "start":
                self.time.mutate(start_frame=time_frame)
            elif key == "end":
                self.time.mutate(end_frame=time_frame)
        except ValueError as e:
            self._show_error(e)
            time_frame = self.time.start_frame
        
        self.window.window[key].update(time_frame)
    
    def _paste_loads(self, values: dict, key: str):
        """
        Pastes the loads.
        
        Args:
            values (dict): The values from the main window.
            key (str): The key of the loads.
        """
        loads = sg.clipboard_get()
        if loads and loads[-1] == "}":
            try:
                loads = self.debug_info_to_frame(self.time, loads)
            except ValueError as e:
                loads = 0
                self._show_error(e)
        else:
            loads = self.clean_frame(loads)
        
        self.window.window[key].update(loads)
    
    def _new_time(self):
        """
        Creates a new time.
        """
        self.time = Time()
        
        self.window.window["framerate"].update(self.time.framerate)
        self.window.window["start"].update(self.time.start_frame)
        self.window.window["end"].update(self.time.end_frame)
        self.window.window["start_loads"].update("0")
        self.window.window["end_loads"].update("0")
    
    def _convert_to_dict(self) -> dict:
        """
        Converts the time to a JSON dictionary.
        
        Returns:
            dict: The JSON dictionary.
        """
        return {
            "start_frame": self.time.start_frame,
            "end_frame": self.time.end_frame,
            "framerate": self.time.framerate,
            "loads": [(load.start_frame, load.end_frame) for load in self.time.loads]
        }
    
    def _open_time(self):
        """
        Opens a time.
        """
        self.file_path = sg.popup_get_file("Open Time", file_types=(("Time Files", "*.json"),))
        if self.file_path:
            with open(self.file_path, "r") as file:
                try:
                    file_data = json.load(file)
                except json.decoder.JSONDecodeError:
                    self._show_error("The file provided is corrupted.\nPlease re-enter debug info.")
                    return
                
                loads = [Load(load[0], load[1]) for load in file_data["loads"]]
                self.time.mutate(start_frame=file_data["start_frame"], end_frame=file_data["end_frame"], framerate=file_data["framerate"])
                self.time.loads = loads
                
                self.window.window["start"].update(self.time.start_frame)
                self.window.window["end"].update(self.time.end_frame)
                self.window.window["framerate"].update(self.time.framerate)
                self.window.window["start_loads"].update("0")
                self.window.window["end_loads"].update("0")
                self.window.window["loads_display"].update(self.time.iso_format(False))
                self.window.window["without_loads_display"].update(self.time.iso_format(True))
            
    def _save_time(self):
        """
        Saves the time.
        """
        
        if self.file_path:
            with open(self.file_path, "w") as file:
                json.dump(self._convert_to_dict(), file)
            sg.popup("Save", "Time saved successfully.")
        else:
            self._save_as_time()
    
    def _settings(self):
        """
        Opens the settings.
        """
        self.settings.open_window()
        old_theme = self.settings_dict["theme"]
        self.settings_dict = self.settings.config_to_dict()
        
        if self.settings_dict["theme"] != old_theme:
            sg.popup_ok("Settings", "Please restart the application to apply the changes.")
    
    def _save_as_time(self):
        """
        Saves the time as a new time.
        """
        self.file_path = SaveAs().run()
        if self.file_path:
            with open(self.file_path, "w") as file:
                json.dump(self._convert_to_dict(), file)
    
    def run(self):
        """
        Runs the application.
        """
        
        while True:
            event, values = self.window.read()

            match event:
                case "New Time":
                    self._new_time()
                
                case "Open Time":
                    self._open_time()
                
                case "Save":
                    self._save_time()
                
                case "Save As":
                    self._save_as_time()
                
                case "Settings":
                    self._settings()
                
                case "Exit":
                    break
                
                case "Clear Loads":
                    self.time.clear_loads()
                
                case "Check for Updates":
                    self._check_for_updates()
                    
                case "Report Issue":
                    open_url("https://forms.gle/mnmbgt6cBeL6Dykk6")
                
                case "Suggest Feature":
                    open_url("https://forms.gle/V5bPaQbcFsk6Cijr5")
                
                case "About":
                    sg.popup("About", f"Conner's Retime Tool v{__version__}\n\nCreated by Conner Glover\n\n© 2024 Conner Glover")
                
                case "Edit Loads":
                    self._edit_loads()
                
                case "Add Loads":
                    self._add_loads(values)
                
                case "Copy Mod Note":
                    sg.clipboard_set(self.time.mod_note)
                
                case "framerate_paste":
                    self._paste_framerate(values)
                
                case "start_paste":
                    self._paste_time(values, "start")
                
                case "end_paste":
                    self._paste_time(values, "end")
                
                case "start_loads_paste":
                    self._paste_loads(values, "start_loads")
                
                case "end_loads_paste":
                    self._paste_loads(values, "end_loads")
                
                case "framerate":
                    self._handle_framerate(values)
                
                case "start":
                    self._handle_time(values, "start")
                
                case "end":
                    self._handle_time(values, "end")
                
                case "start_loads":
                    self._handle_loads(values, "start_loads")
                
                case "end_loads":
                    self._handle_loads(values, "end_loads")
                
                case "without_loads_display":
                    sg.clipboard_set(self.time.iso_format(True))
                
                case "loads_display":
                    sg.clipboard_set(self.time.iso_format(False))
                
                case sg.WIN_CLOSED:
                    break
            
            self.window.window["without_loads_display"].update(self.time.iso_format(True))
            self.window.window["loads_display"].update(self.time.iso_format(False))
        
        if self.file_path and sg.popup_yes_no("Exit", "Would you like to save?") == "Yes":
            self._save_time()
        
        self.window.close()

    def _show_error(self, message):
        """
        Shows the error.
        
        Args:
            message (str): The message to show.
        """
        sg.popup_error("Error", message, title="Error")