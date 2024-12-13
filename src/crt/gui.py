import PySimpleGUI as sg

class MainWindow:
    """
    Main window for CRT.
    """
    def __init__(self, language: str = "en"):
        """
        Initializes the MainWindow class.
        
        Args:
            language (str): The language of the window.
        """
        
        match language:
            case "en":
                content = {
                    "menu": [["File", ["New Time", "---", "Open Time", "---", "Save", "Save As", "---", "Settings", "---", "Exit"]], 
                            ["Edit", ["Copy Mod Note", "Clear Loads", "---", "Add Loads", "Edit Loads"]], 
                            ["Help", ["Check for Updates", "---", "Report Issue", "Suggest Feature", "---", "About"]]],
                    "inputs": {
                        "framerate": "Framerate (FPS)",
                        "start": "Start Frame",
                        "end": "End Frame",
                        "start_loads": "Start Frame (Loads)",
                        "end_loads": "End Frame (Loads)"
                    },
                    "buttons": {
                        "paste": "Paste",
                        "copy_mod_note": "Copy Mod Note",
                        "add_loads": "Add Loads",
                        "edit_loads": "Edit Loads"
                    },
                    "outputs": {
                        "without_loads_display": "Without Loads:",
                        "loads_display": "With Loads:"
                    },
                    "tool_tips": {
                        "without_loads_display": "Click to Copy Time",
                        "loads_display": "Click to Copy Time"
                    }
                }
        
        self.window = self._create_window(content)
    
    def _create_window(self, content: dict) -> sg.Window:
        """
        Creates the main window.
        
        Returns:
            sg.Window: The main window.
        """
        menu = content["menu"]
        
        layout = [
            [sg.Menu(menu)],
            [sg.Push(), sg.Text(content["inputs"]["framerate"], font=("Helvetica", 16), justification="right"), sg.Input(default_text="60", key="framerate", enable_events=True, font=("Helvetica", 16), pad=((5, 0), (0, 0)), size=(12, 1)), sg.Button(content["buttons"]["paste"], font=("Helvetica", 10), key="framerate_paste")],
            [sg.Push(), sg.Text(content["inputs"]["start"], font=("Helvetica", 16), justification="right"), sg.Input(default_text="0", key="start", enable_events=True, font=("Helvetica", 16), pad=((5, 0), (0, 0)), size=(12, 1)), sg.Button(content["buttons"]["paste"], font=("Helvetica", 10), key="start_paste")],
            [sg.Push(), sg.Text(content["inputs"]["end"], font=("Helvetica", 16), justification="right"), sg.Input(default_text="0", key="end", enable_events=True, font=("Helvetica", 16), pad=((5, 0), (0, 0)), size=(12, 1)), sg.Button(content["buttons"]["paste"], font=("Helvetica", 10), key="end_paste")],
            [sg.Push(), sg.Text(content["inputs"]["start_loads"], font=("Helvetica", 16), justification="right"), sg.Input(default_text="0", key="start_loads", enable_events=True, font=("Helvetica", 16), pad=((5, 0), (0, 0)), size=(12, 1)), sg.Button(content["buttons"]["paste"], font=("Helvetica", 10), key="start_loads_paste")],
            [sg.Push(), sg.Text(content["inputs"]["end_loads"], font=("Helvetica", 16), justification="right"), sg.Input(default_text="0", key="end_loads", enable_events=True, font=("Helvetica", 16), pad=((5, 0), (0, 0)), size=(12, 1)), sg.Button(content["buttons"]["paste"], font=("Helvetica", 10), key="end_loads_paste")],
            [sg.HorizontalSeparator()],
            [sg.Button(content["buttons"]["copy_mod_note"], font=("Helvetica", 18)), sg.Button(content["buttons"]["add_loads"], font=("Helvetica", 18)), sg.Button(content["buttons"]["edit_loads"], font=("Helvetica", 18))],
            [sg.Text(content["outputs"]["without_loads_display"], font=("Helvetica", 20), justification="right"), sg.StatusBar("00.000", key="without_loads_display", enable_events=True, font=("Helvetica", 20), size=(17,1), tooltip=content["tool_tips"]["without_loads_display"])],
            [sg.Text(content["outputs"]["loads_display"], font=("Helvetica", 20), justification="right"), sg.StatusBar("00.000", key="loads_display", enable_events=True, font=("Helvetica", 20), size=(17,1), tooltip=content["tool_tips"]["loads_display"])]
        ]

        return sg.Window("Conner's Retime Tool", layout, icon="icon.ico")
    
    def read(self):
        """
        Reads the main window.
        
        Returns:
            tuple[str, Any]: The event and values.
        """
        return self.window.read()
    
    def close(self):
        """
        Closes the main window.
        """
        self.window.close()
    
    def __enter__(self):
        """
        Enters the main window.
        
        Returns:
            MainWindow: The main window.
        """
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Exits the main window.
        """
        self.close()