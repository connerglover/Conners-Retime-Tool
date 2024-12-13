import PySimpleGUI as sg
from decimal import Decimal as d

from crt.time import Time
from crt import load_editor

from crt.load_viewer.gui import LoadViewerGUI

class LoadViewer:
    """
    Load viewer for CRT.
    """
    def __init__(self, time: Time):
        """
        Initializes the LoadViewer class.
        
        Args:
            time (Time): The time.
        """
        self.time = time
        self.window = LoadViewerGUI(time)
        
        self.loads_to_delete = []

    def _edit_load(self, load_index: int):
        """
        Edits the load.
        
        Args:
            load_index (int): The index of the load.
        """
        load = load_editor.LoadEditor(self.time.loads[load_index], self.time.framerate)
        load = load.run()
        self.time.mutate_load(load_index, load.start_frame, load.end_frame)
        load_time = round(d(load.length / self.time.framerate), self.time.precision)
        self.window.window[f"display_{load_index}"].update(f"{load_index+1}: {load_time}")

    def _delete_load(self, load_index: int):
        """
        Deletes the load.
        
        Args:
            load_index (int): The index of the load.
        """
        self.loads_to_delete.append(load_index)
        self.window.window[f"load_{load_index}"].update(visible=False)


    def _cleanup(self):
        """
        Cleans up the load viewer.
        """
        self.loads_to_delete.sort(reverse=True)
        
        for index in self.loads_to_delete:
            del self.time.loads[index]

    def run(self):
        """
        Runs the load viewer.
        """
        while True:
            event, values = self.window.read()
            
            if event == sg.WIN_CLOSED:
                break
            
            # Extract load index from event name if it exists
            if '_' in str(event):
                action, load_index = event.split('_')
                load_index = int(load_index)
                
                if action == "edit":
                    self._edit_load(load_index)
                elif action == "delete":
                    self._delete_load(load_index)
            
        self.window.close()
        self._cleanup()
        
        return self.time
    