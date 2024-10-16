import PySimpleGUI as sg

from crt.core import Load
from crt.core import debug_info_to_frame
from crt.core import clean_frame

def create_load_edit_window(load: Load):
    load_edit_layout = [
        [sg.Text("Edit Load", font=("Helvetica", 24))],
        [sg.Push(), sg.Text(f"Start Frame", font=("Helvetica", 16), justification="right"), sg.Input(default_text=str(load.start_frame), key="start", enable_events=True, font=("Helvetica", 16), pad=((5, 0), (0, 0)), size=(12, 1)), sg.Button("Paste", font=("Helvetica", 10), key="start_paste")],
        [sg.Push(), sg.Text(f"End Frame", font=("Helvetica", 16), justification="right"), sg.Input(default_text=load.end_frame, key="end", enable_events=True, font=("Helvetica", 16), pad=((5, 0), (0, 0)), size=(12, 1)), sg.Button("Paste", font=("Helvetica", 10), key="end_paste")],
        [sg.Button("Save Edits", font=("Helvetica", 14)), sg.Button("Discard Changes", font=("Helvetica", 14))]
    ]
    
    load_edit_window = sg.Window("Load Editor", load_edit_layout, resizable=False)
    
    while True:
        event, values = load_edit_window.read()
        
        if event == sg.WIN_CLOSED:
            break
        
        if event == "Save Edits":
            start = int(values["start"])
            end = int(values["end"])
            load = Load(start, end)
            break
        
        if event == "Discard Changes":
            break
        
        if event == "start":
            start = values["start"]
            if start and start[-1] == "}":
                try:
                    start_frame = debug_info_to_frame(start)
                except ValueError as e:
                    start_frame = 0
                    sg.popup_error("Error", e, title="Error")
            else:
                start_frame = clean_frame(start)
            
            load_edit_window["start"].update(int(start_frame))
        
        if event == "end":
            end = values["end"]
            if end and end[-1] == "}":
                try:
                    end_frame = debug_info_to_frame(start)
                except ValueError as e:
                    end_frame = 0
                    sg.popup_error("Error", e, title="Error")
            else:
                end_frame = clean_frame(end)
            
            load_edit_window["end"].update(int(end_frame))
    
    load_edit_window.close()
    return load