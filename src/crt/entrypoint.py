import PySimpleGUI as sg

from crt.core import Time
from crt.core import debug_info_to_frame
from crt.core import clean_frame
from crt.core import clean_framerate

from crt.gui.main_window import create_main_window as app
from crt.gui.load_window import create_load_window

def run():
    sg.theme("DarkGrey15")
    
    main_window = app()

    time = Time()

    while True:
        event, values = main_window.read()
        if event == sg.WIN_CLOSED:
            break
        
        if event == "Edit Loads":
            try:
                create_load_window(time.loads)
            except ValueError as e:
                sg.popup_error("Error", e, title="Error")
            main_window["without_loads_display"].update(time.iso_format(True))
        
        if event == "Add Loads":
            start_frame = int(values["start_loads"])
            end_frame = int(values["end_loads"])
            
            try:
                time.add_load(start_frame, end_frame)
            except ValueError as e:
                sg.popup_error("Error", e, title = "Error")
            else:
                main_window["start_loads"].update("0")
                main_window["end_loads"].update("0")
                sg.popup("Loads", "Load added successfully.")
            
        if event == "Copy Mod Note":
            sg.clipboard_set(time.mod_note)

        if event == "framerate_paste":
            framerate = sg.clipboard_get()
            framerate = clean_framerate(framerate)
            
            main_window["framerate"].update(framerate)
            time.mutate(framerate=framerate)
        
        if event == "start_paste":
            start = sg.clipboard_get()
            if start and start[-1] == "}":
                try:
                    start_frame = debug_info_to_frame(start)
                except ValueError as e:
                    start_frame = time.start_frame
                    sg.popup_error("Error", e, title="Error")
            else:
                start_frame = clean_frame(start)
            
            try:
                time.mutate(start_frame=start_frame)
            except ValueError as e:
                sg.popup_error("Error", e, title = "Error")
                start_frame = time.start_frame
            
            main_window["start"].update(start_frame)

        if event == "end_paste":
            end = sg.clipboard_get()
            if end and end[-1] == "}":
                try:
                    end_frame = debug_info_to_frame(end)
                except ValueError as e:
                    end_frame = time.end_frame
                    sg.popup_error("Error", e, title="Error")
            else:
                end_frame = clean_frame(end)
                
            try:
                time.mutate(end_frame=end_frame)
            except ValueError as e:
                sg.popup_error("Error", e, title = "Error")
                end_frame = time.end_frame
        
        if event == "start_loads_paste":
            start = sg.clipboard_get()
            if start and start[-1] == "}":
                try:
                    start_frame = debug_info_to_frame(start)
                except ValueError as e:
                    start_frame = 0
                    sg.popup_error("Error", e, title="Error")
            else:
                start_frame = clean_frame(start)
            
            main_window["start_loads"].update(int(start_frame))
        
        if event == "end_loads_paste":
            end = sg.clipboard_get()
            if end and end[-1] == "}":
                try:
                    end_frame = debug_info_to_frame(end)
                except ValueError as e:
                    end_frame = 0
                    sg.popup_error("Error", e, title="Error")
            else:
                end_frame = clean_frame(end)
            
            main_window["end_loads"].update(end_frame)
        
        if event == "framerate":
            framerate = values["framerate"]
            framerate = clean_framerate(framerate)
            
            main_window["framerate"].update(framerate)
            time.mutate(framerate=framerate)

        if event == "start":
            start = values["start"]
            if start and start[-1] == "}":
                try:
                    start_frame = debug_info_to_frame(start)
                except ValueError as e:
                    start_frame = time.start_frame
                    sg.popup_error("Error", e, title="Error")
            else:
                start_frame = clean_frame(start)
            
            try:
                time.mutate(start_frame=start_frame)
            except ValueError as e:
                sg.popup_error("Error", e, title = "Error")
                start_frame = time.start_frame
            
            main_window["start"].update(start_frame)

        if event == "end":
            end = values["end"]
            if end and end[-1] == "}":
                try:
                    end_frame = debug_info_to_frame(end)
                except ValueError as e:
                    end_frame = time.end_frame
                    sg.popup_error("Error", e, title="Error")
            else:
                end_frame = clean_frame(end)
                
            try:
                time.mutate(end_frame=end_frame)
            except ValueError as e:
                sg.popup_error("Error", e, title = "Error")
                end_frame = time.end_frame
            
            main_window["end"].update(end_frame)
        
        if event == "start_loads":
            start = values["start_loads"]
            if start and start[-1] == "}":
                try:
                    start_frame = debug_info_to_frame(start)
                except ValueError as e:
                    start_frame = 0
                    sg.popup_error("Error", e, title="Error")
            else:
                start_frame = clean_frame(start)
            
            main_window["start_loads"].update(int(start_frame))

        if event == "end_loads":
            end = values["end_loads"]
            if end and end[-1] == "}":
                try:
                    end_frame = debug_info_to_frame(end)
                except ValueError as e:
                    end_frame = 0
                    sg.popup_error("Error", e, title="Error")
            else:
                end_frame = clean_frame(end)
            
            main_window["end_loads"].update(end_frame)
        
        if event == "without_loads_display":
            sg.clipboard_set(time.iso_format(True))
        
        if event == "loads_display":
            sg.clipboard_set(time.iso_format(False))
        
        main_window["without_loads_display"].update(time.iso_format(True))
        main_window["loads_display"].update(time.iso_format(False))

    main_window.close()