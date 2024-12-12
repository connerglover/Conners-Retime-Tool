import PySimpleGUI as sg
import json
import re

from decimal import Decimal as d

from crt.core.load import Load
from crt.core.time import Time

class LoadEditWindow:
    def __init__(self, load: Load, framerate: d):
        self.load = load
        self.framerate = framerate
        self.window = None
        
    def create_layout(self):
        return [
            [sg.Text("Edit Load", font=("Helvetica", 24))],
            [sg.Push(), sg.Text(f"Start Frame", font=("Helvetica", 16), justification="right"), 
             sg.Input(default_text=str(self.load.start_frame), key="start", enable_events=True, 
                     font=("Helvetica", 16), pad=((5, 0), (0, 0)), size=(12, 1)), 
             sg.Button("Paste", font=("Helvetica", 10), key="start_paste")],
            [sg.Push(), sg.Text(f"End Frame", font=("Helvetica", 16), justification="right"), 
             sg.Input(default_text=self.load.end_frame, key="end", enable_events=True, 
                     font=("Helvetica", 16), pad=((5, 0), (0, 0)), size=(12, 1)), 
             sg.Button("Paste", font=("Helvetica", 10), key="end_paste")],
            [sg.Button("Save Edits", font=("Helvetica", 14)), 
             sg.Button("Discard Changes", font=("Helvetica", 14))]
        ]
    
    def handle_frame_input(self, values, key):
        value = values[key]
        if value and value[-1] == "}":
            try:
                frame = self.debug_info_to_frame(value)
            except ValueError as e:
                frame = 0
                sg.popup_error("Error", e, title="Error")
        else:
            frame = self.clean_frame(value)

        self.window[key].update(int(frame))
    
    def debug_info_to_frame(self, debug_info: str) -> int:
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
    
    def clean_frame(self, frame: str) -> int:
        if any(char.isdigit() for char in frame):
            cleaned_frame = int(re.sub(r"[^0-9]", "", frame))
        else:
            cleaned_frame = 0
        
        return cleaned_frame
    
    def run(self):
        self.window = sg.Window("Load Editor", self.create_layout(), resizable=False)
        
        while True:
            event, values = self.window.read()
            
            if event == sg.WIN_CLOSED:
                break
            
            if event == "Save Edits":
                start = int(values["start"])
                end = int(values["end"])
                self.load = Load(start, end)
                break
            
            if event == "Discard Changes":
                break
            
            if event == "start":
                self.handle_frame_input(values, "start")
            
            if event == "end":
                self.handle_frame_input(values, "end")
        
        self.window.close()
        return self.load