import PySimpleGUI as sg
import json
import re

from decimal import Decimal as d

from crt.load import Load
from crt.load_editor.gui import LoadEditorGUI
from crt.language import Language

class LoadEditor:
    """
    Load editor for CRT.
    """
    def __init__(self, load: Load, framerate: d, language: Language):
        """
        Initializes the LoadEditor class.
        
        Args:
            load (Load): The load.
            framerate (d): The framerate.
        """
        self.load = load
        self.framerate = framerate
        self.window = LoadEditorGUI(load, framerate, language.content)
    
    def _handle_frame_input(self, values: dict, key: str):
        """
        Handles the frame input.
        
        Args:
            values (dict): The values from the main window.
            key (str): The key of the frame.
        """
        value = values[key]
        if value and value[-1] == "}":
            try:
                frame = self._debug_info_to_frame(value)
            except ValueError as e:
                frame = 0
                sg.popup_error("Error", e, title="Error")
        else:
            frame = self._clean_frame(value)

        self.window.window[key].update(int(frame))
    
    def _debug_info_to_frame(self, debug_info: str) -> int:
        """
        Converts debug info to a frame.
        
        Args:
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
        
        output = d(cmt) * d(self.framerate)
        output = int(round(output, 0))
        
        return output
    
    def _clean_frame(self, frame: str) -> int:
        """
        Cleans the frame.
        
        Args:
            frame (str): The frame.
        
        Returns:
            int: The cleaned frame.
        """
        digits = ''.join(char for char in frame if char.isdigit())
        return int(digits) if digits else 0
    
    def run(self):
        """
        Runs the load editor.
        """
        while True:
            event, values = self.window.read()
            
            match event:
                case "Save Edits":
                    self.load = Load(values["start"], values["end"])
                    break
                
                case "Discard Changes":
                    break
                
                case "start":
                    self._handle_frame_input(values, "start")
                    
                case "end":
                    self._handle_frame_input(values, "end")
                
                case sg.WIN_CLOSED:
                    break
        
        self.window.close()
        return self.load
    