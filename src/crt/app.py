# Standard library
import json
import re
from decimal import Decimal as d
from webbrowser import open as open_url

# Third-party
import PySimpleGUI as sg
import darkdetect
from requests import get as get_url

# Local application
from crt._version import __version__
from crt.app_settings.app import Settings
from crt.decorators import error_handler, invalidate_cache
from crt.gui import MainWindow
from crt.load import Load
from crt.load_viewer.app import LoadViewer
from crt.save_as.app import SaveAs
from crt.session_history import SessionHistory
from crt.time import Time

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
        
        self.past_file_paths = []
        
        self.settings = Settings()
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
            
        self.language = self.settings.language
        
        self.window = MainWindow(self.language.content)
        
        self._cached_iso_formats = {
            'with_loads': None,
            'without_loads': None
        }
        self._cache_dirty = True
        
    def invalidate_caches(self):
        """
        Invalidates the caches.
        """
        self._cache_dirty = True
        self._update_displays()
    
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
    
    @error_handler
    def _edit_loads(self):
        """
        Edits the loads.
        """
        load_window = LoadViewer(self.time, self.language)
        load_window.run()
        self.window.window["loads_display"].update(self.time.iso_format(True))
    
    def _add_loads(self, values):
        """
        Adds the loads.
        
        Args:
            values (dict): The values from the main window.
        """
        start_frame = int(values["start_loads"])
        end_frame = int(values["end_loads"])
        
        if self.time.loads:
            if self._load_stats['total_loads'] != len(self.time.loads):
                self._load_stats['avg_length'] = sum(load.end_frame - load.start_frame for load in self.time.loads) / len(self.time.loads)
                self._load_stats['total_loads'] = len(self.time.loads)
            
            if (end_frame - start_frame) > self._load_stats['avg_length'] * 10:
                if sg.popup_yes_no("Woah!", "This load is concerningly long. Would you like to add the load anyway?") == "No":
                    return
        
        self.time.add_load(start_frame, end_frame)
        self.window.window["start_loads"].update("0")
        self.window.window["end_loads"].update("0")
        sg.popup("Loads", "Load added successfully.")
    
    def debug_info_to_frame(self, time: Time, debug_info: str) -> int:
        """Optimized debug info parsing"""
        try:
            # Find the starting position of the JSON object more efficiently
            start_pos = debug_info.find('{')
            if start_pos == -1:
                raise ValueError("The debug info provided is invalid.\nPlease re-enter debug info.")
            
            debug_info = debug_info[start_pos:]
            parsed_debug_info = json.loads(debug_info)
            cmt = parsed_debug_info["cmt"]
            
            # Optimize decimal calculations
            output = int(round(d(cmt) * d(time.framerate), 0))
            return output
        
        except (json.decoder.JSONDecodeError, KeyError):
            raise ValueError("The debug info provided is invalid.\nPlease re-enter debug info.")

    def _set_framerate(self, new_value: str):
        """
        Handles the framerate.
        
        Args:
            values (dict): The values from the main window.
        """
        framerate = new_value
        framerate = self._clean_framerate(framerate)
        
        self.window.window["framerate"].update(framerate)
        self.time.mutate(framerate=framerate)
    
    @error_handler
    @invalidate_cache
    def _set_time(self, key: str, new_value: str):
        """
        Handles the time.
        
        Args:
            values (dict): The values from the main window.
            key (str): The key of the time.
        """
        time = new_value
        if time and time[-1] == "}":
            time = self.debug_info_to_frame(self.time, time)
        else:
            time = self.clean_frame(time)
        
        match key:
            case "start":
                self.time.mutate(start_frame=time)
            case "end":
                self.time.mutate(end_frame=time)
        
        self.window.window[key].update(time)
    
    def _set_loads(self, key: str, new_value: str):
        """
        Handles the loads.
        
        Args:
            values (dict): The values from the main window.
            key (str): The key of the loads.
        """
        loads = new_value
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
        """Optimized frame cleaning"""
        # Use a more efficient method to check for digits
        if not frame or frame.isspace():
            return 0
        
        # Compile regex pattern once
        if not hasattr(self, '_digit_pattern'):
            self._digit_pattern = re.compile(r'\d+')
        
        match = self._digit_pattern.search(frame)
        return int(match.group()) if match else 0
    
    @invalidate_cache
    def _new_time(self):
        """
        Creates a new time.
        """
        self._save_as_time()
        self.time = Time()
        self._update_window_values({
            "framerate": self.time.framerate,
            "start": self.time.start_frame,
            "end": self.time.end_frame,
            "start_loads": "0",
            "end_loads": "0"
        })
    
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
        old_file_path = self.file_path
        new_file_path = sg.popup_get_file("Open Time", file_types=(("Time Files", "*.json"),))
        if new_file_path != old_file_path:
            self.file_path = new_file_path
            if old_file_path not in self.past_file_paths and old_file_path is not None:
                self.past_file_paths.append(old_file_path)
        
        if self.file_path and self.file_path != old_file_path:
            with open(self.file_path, "r") as file:
                try:
                    file_data = json.load(file)
                except json.decoder.JSONDecodeError:
                    raise ValueError("The file provided is corrupted.")
                
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
    
    @error_handler
    @invalidate_cache
    def _session_history(self):
        """
        Opens the session history.
        """
        
        old_file_path = self.file_path
        session_history = SessionHistory(self.language, self.past_file_paths)
        new_file_path = session_history.run()
        
        if old_file_path and sg.popup_yes_no("Save", "Would you like to save the current file?") == "Yes":
            self._save_time()
            
        if new_file_path and new_file_path != old_file_path:
            self.file_path = new_file_path
            if new_file_path in self.past_file_paths:
                self.past_file_paths.remove(new_file_path)
            if old_file_path and old_file_path not in self.past_file_paths:
                self.past_file_paths.append(old_file_path)
            
            try:
                with open(new_file_path, "r") as file:
                    file_data = json.load(file)
                    
                loads = [Load(load[0], load[1]) for load in file_data["loads"]]
                self.time.mutate(
                    start_frame=file_data["start_frame"],
                    end_frame=file_data["end_frame"],
                    framerate=file_data["framerate"]
                )
                self.time.loads = loads
                
                self._update_window_values({
                    "start": self.time.start_frame,
                    "end": self.time.end_frame,
                    "framerate": self.time.framerate,
                    "start_loads": "0",
                    "end_loads": "0"
                })
                
            except json.decoder.JSONDecodeError:
                raise ValueError("The file provided is corrupted.")
    
    def _settings(self):
        """
        Opens the settings.
        """
        old_settings_dict = self.settings_dict
        self.settings.open_window()
        self.settings_dict = self.settings.config_to_dict()
        
        if self.settings_dict != old_settings_dict:
            sg.popup_ok("Settings", "Please restart the application to apply the changes.")
    
    def _save_as_time(self):
        """
        Saves the time as a new time.
        """
        old_file_path = self.file_path
        new_file_path = SaveAs(self.language).run()
        if new_file_path != old_file_path:
            self.file_path = new_file_path
            if old_file_path not in self.past_file_paths and old_file_path is not None:
                self.past_file_paths.append(old_file_path)
            
        if self.file_path:
            with open(self.file_path, "w") as file:
                json.dump(self._convert_to_dict(), file)
    
    @property
    def _mod_note(self) -> str:
        """
        Gets the mod note.
        
        Returns:
            str: The mod note.
        """
        return self.settings_dict["mod_note_format"].format(
            time_with_loads=self.time.iso_format(False),
            time_without_loads=self.time.iso_format(True),
            hours=self.time.format_time_components(self.time.time)[0],
            minutes=self.time.format_time_components(self.time.time)[1],
            seconds=self.time.format_time_components(self.time.time)[2],
            milliseconds=self.time.format_time_components(self.time.time)[3],
            start_frame=self.time.start_frame,
            end_frame=self.time.end_frame,
            start_time=round((self.time.start_frame / self.time.framerate, self.time.precision)),
            end_time=round((self.time.end_frame / self.time.framerate, self.time.precision)),
            total_frames=self.time.length,
            fps=self.time.framerate,
            plug="[Conner's Retime Tool](https://github.com/connerglover/conners-retime-tool)",
        )
    
    
    def run(self):
        """
        Runs the application.
        """
        
        while True:
            event, values = self.window.read()

            match (event.split("::")[-1] if (isinstance(event, str) and "::" in event) else event):
                case "New Time":
                    self._new_time()
                
                case "Open Time":
                    self._open_time()
                    
                case "Session History":
                    self._session_history()
                
                case "Save":
                    self._save_time()
                
                case "Save As":
                    self._save_as_time()
                    
                case "Session History":
                    self._session_history()
                
                case "Settings":
                    self._settings()
                
                case "Clear Loads":
                    self.time.clear_loads()
                
                case "Check for Updates":
                    self._check_for_updates()
                    
                case "Report Issue":
                    open_url("https://forms.gle/mnmbgt6cBeL6Dykk6")
                
                case "Suggest Feature":
                    open_url("https://forms.gle/V5bPaQbcFsk6Cijr5")
                
                case "About":
                    sg.popup("About", f"Conner's Retime Tool v{__version__}\n\nCreated by Conner Glover\n\nCredits:\nMenzo: French and Polish Translations\nAmazinCris: Spanish Translations\n\n© 2024 Conner Glover")
                
                case "Edit Loads":
                    self._edit_loads()
                
                case "Add Loads":
                    self._add_loads(values)
                
                case "Copy Mod Note":
                    sg.clipboard_set(self._mod_note)
                
                case "framerate_paste":
                    self._set_framerate(sg.clipboard_get())
                
                case "start_paste":
                    self.set_time("start", sg.clipboard_get())
                
                case "end_paste":
                    self.set_time("end", sg.clipboard_get())
                
                case "start_loads_paste":
                    self._set_loads("start_loads", sg.clipboard_get())
                
                case "end_loads_paste":
                    self._set_loads("end_loads", sg.clipboard_get())
                
                case "framerate":
                    self._set_framerate(values["framerate"])
                
                case "start":
                    self._set_time("start", values["start"])
                
                case "end":
                    self._set_time("end", values["end"])
                
                case "start_loads":
                    self._set_loads("start_loads", values["start_loads"])
                
                case "end_loads":
                    self._set_loads("end_loads", values["end_loads"])
                
                case "without_loads_display":
                    sg.clipboard_set(self.time.iso_format(True))
                
                case "loads_display":
                    sg.clipboard_set(self.time.iso_format(False))
                
                case sg.WIN_CLOSED | "Exit":
                    break
                    
                case _ as e:
                    print(e)
            
            self._update_displays()
        
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

    def _update_displays(self):
        """Update time displays with caching"""
        if self._cache_dirty:
            self._cached_iso_formats['with_loads'] = self.time.iso_format(False)
            self._cached_iso_formats['without_loads'] = self.time.iso_format(True)
            self._cache_dirty = False
            
        self.window.window["without_loads_display"].update(self._cached_iso_formats['without_loads'])
        self.window.window["loads_display"].update(self._cached_iso_formats['with_loads'])

    def _update_window_values(self, updates: dict):
        """Batch window updates for better performance"""
        for key, value in updates.items():
            self.window.window[key].update(value)
            