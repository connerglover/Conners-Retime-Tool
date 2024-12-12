import PySimpleGUI as sg
import json
import re

from decimal import Decimal as d

from crt.time import Time
from crt.gui import MainWindow
from crt.load_viewer.app import LoadViewer

class App:
    """
    Main application for CRT.
    """
    def __init__(self):
        """
        Initializes the App class.
        """
        self.time = Time()
        
        sg.theme("DarkGrey15")
        self.main_window = MainWindow()
    
    def _edit_loads(self):
        """
        Edits the loads.
        """
        try:
            load_window = LoadViewer(self.time)
            load_window.run()
        except ValueError as e:
            self._show_error(e)
        finally:
            self.main_window.window["loads_display"].update(self.time.iso_format(True))
    
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
            self.main_window.window["start_loads"].update("0")
            self.main_window.window["end_loads"].update("0")
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
        
        self.main_window.window["framerate"].update(framerate)
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
        
        self.main_window.window[key].update(time_frame)
    
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
        
        self.main_window.window[key].update(loads)
    
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
        
        self.main_window.window["framerate"].update(framerate)
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
        
        self.main_window.window[key].update(time_frame)
    
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
        
        self.main_window.window[key].update(loads)
        
    def run(self):
        """
        Runs the application.
        """
        while True:
            event, values = self.main_window.read()
            
            match event:
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
            
            self.main_window.window["without_loads_display"].update(self.time.iso_format(True))
            self.main_window.window["loads_display"].update(self.time.iso_format(False))
        
        self.main_window.close()

    def _show_error(self, message):
        """
        Shows the error.
        
        Args:
            message (str): The message to show.
        """
        sg.popup_error("Error", message, title="Error")