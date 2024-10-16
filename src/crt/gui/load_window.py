import PySimpleGUI as sg
from decimal import Decimal as d

from crt.core import Time
from crt.core import Load

from crt.gui.load_edit_window import create_load_edit_window

def create_load_window(time: Time, loads: list[Load]):
    if loads == []:
        raise ValueError("There are no loads to edit.")
    
    loads_to_delete = []
    
    load_layout = [
        [sg.Text("Loads", font=("Helvetica", 24))]
        ]

    for index, load in enumerate(loads):
        load_time = round(d(load.length / time.framerate), time.precision)
        next_cell = [sg.pin(sg.Col([[sg.Text(f"{index+1}: {load_time}", font=("Helvetica", 20), key=f"display_{index}"), sg.Button("Edit", font=("Helvetica", 14), key=f"edit_{index}"), sg.Button("Delete", font=("Helvetica", 14), key=f"delete_{index}")]], key=f"load_{index}"))]
        load_layout.append(next_cell)

    load_window = sg.Window("Load Viewer", load_layout, resizable=False, element_justification="left")
    
    while True:
        event, values = load_window.read()
        
        if event == sg.WIN_CLOSED:
            break
        
        for index in range(len(loads)):
            if event == f"edit_{index}":
                load = create_load_edit_window(loads[index])
                time.mutate_load(index, load.start_frame, load.end_frame)
                load_time = round(d(load.length / time.framerate), time.precision)
                load_window[f"display_{index}"].update(f"{index+1}: {load_time}")
            
            if event == f"delete_{index}":
                loads_to_delete.append(index)
                load_window[f"load_{index}"].update(visible=False)
            
        if len(loads_to_delete) == len(loads):
            break
                
    load_window.close()
    
    loads_to_delete.sort(reverse=True)
    
    for index in loads_to_delete:
        del time.loads[index]
    
    time.recalculate()