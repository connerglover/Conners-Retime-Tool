import PySimpleGUI as sg
from decimal import Decimal as d

from crt.core.time import Time
from crt.core.load import Load
from crt.gui.load_edit_window import LoadEditWindow

class LoadWindow:
    def __init__(self, time: Time, loads: list[Load]):
        if loads == []:
            raise ValueError("There are no loads to edit.")
        
        self.time = time
        self.loads = loads
        self.loads_to_delete = []
        self.window = self._create_window()

    def _create_window(self):
        load_layout = [
            [sg.Text("Loads", font=("Helvetica", 24))]
        ]

        for index, load in enumerate(self.loads):
            load_time = round(d(load.length / self.time.framerate), self.time.precision)
            next_cell = [sg.pin(sg.Col([[
                sg.Text(f"{index+1}: {load_time}", font=("Helvetica", 20), key=f"display_{index}"),
                sg.Button("Edit", font=("Helvetica", 14), key=f"edit_{index}"),
                sg.Button("Delete", font=("Helvetica", 14), key=f"delete_{index}")
            ]], key=f"load_{index}"))]
            load_layout.append(next_cell)

        return sg.Window("Load Viewer", load_layout, resizable=False, element_justification="left")

    def run(self):
        while True:
            event, values = self.window.read()
            
            if event == sg.WIN_CLOSED:
                break
            
            for index in range(len(self.loads)):
                if event == f"edit_{index}":
                    load = LoadEditWindow(self.loads[index], self.time.framerate)
                    load = load.run()
                    self.time.mutate_load(index, load.start_frame, load.end_frame)
                    load_time = round(d(load.length / self.time.framerate), self.time.precision)
                    self.window[f"display_{index}"].update(f"{index+1}: {load_time}")
                
                if event == f"delete_{index}":
                    self.loads_to_delete.append(index)
                    self.window[f"load_{index}"].update(visible=False)
                
            if len(self.loads_to_delete) == len(self.loads):
                break
                    
        self.window.close()
        self._cleanup()

    def _cleanup(self):
        self.loads_to_delete.sort(reverse=True)
        
        for index in self.loads_to_delete:
            del self.time.loads[index]
        
        self.time.recalculate()