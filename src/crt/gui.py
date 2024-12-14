import PySimpleGUI as sg

class MainWindow:
    """
    Main window for CRT.
    """
    def __init__(self, content: dict):
        """
        Initializes the MainWindow class.
        
        Args:
            language (str): The language of the window.
        """
        
        self.window = self._create_window(content)
    
    def _create_window(self, content: dict) -> sg.Window:
        """
        Creates the main window.
        
        Returns:
            sg.Window: The main window.
        """
        menu = [[content["File"], [content["New Time"]+"::New Time", "---", content["Open Time"]+"::Open Time", "---", content["Save"]+"::Save", content["Save As"]+"::Save As", "---", content["Settings"]+"::Settings", "---", content["Exit"]+"::Exit"]], 
                [content["Edit (Menu Bar)"], content["Copy Mod Note"]+"::Copy Mod Note", "---", content["Clear Loads"]+"::Clear Loads", content["Edit Loads"]+"::Edit Loads"],
                [content["Help"], [content["Check for Updates"]+"::Check for Updates", "---", content["Report Issue"]+"::Report Issue", content["Suggest Feature"]+"::Suggest Feature", "---", content["About"]+"::About"]]]
        
        layout = [
            [sg.Menu(menu)],
            [sg.Push(), sg.Text(content["Framerate"], font=("Helvetica", 16), justification="right"), sg.Input(default_text="60", key="framerate", enable_events=True, font=("Helvetica", 16), pad=((5, 0), (0, 0)), size=(12, 1)), sg.Button(content["Paste"], font=("Helvetica", 10), key="framerate_paste")],
            [sg.Push(), sg.Text(content["Start Frame"], font=("Helvetica", 16), justification="right"), sg.Input(default_text="0", key="start", enable_events=True, font=("Helvetica", 16), pad=((5, 0), (0, 0)), size=(12, 1)), sg.Button(content["Paste"], font=("Helvetica", 10), key="start_paste")],
            [sg.Push(), sg.Text(content["End Frame"], font=("Helvetica", 16), justification="right"), sg.Input(default_text="0", key="end", enable_events=True, font=("Helvetica", 16), pad=((5, 0), (0, 0)), size=(12, 1)), sg.Button(content["Paste"], font=("Helvetica", 10), key="end_paste")],
            [sg.Push(), sg.Text(content["Start Frame (Loads)"], font=("Helvetica", 16), justification="right"), sg.Input(default_text="0", key="start_loads", enable_events=True, font=("Helvetica", 16), pad=((5, 0), (0, 0)), size=(12, 1)), sg.Button(content["Paste"], font=("Helvetica", 10), key="start_loads_paste")],
            [sg.Push(), sg.Text(content["End Frame (Loads)"], font=("Helvetica", 16), justification="right"), sg.Input(default_text="0", key="end_loads", enable_events=True, font=("Helvetica", 16), pad=((5, 0), (0, 0)), size=(12, 1)), sg.Button(content["Paste"], font=("Helvetica", 10), key="end_loads_paste")],
            [sg.HorizontalSeparator()],
            [sg.Button(content["Copy Mod Note"], font=("Helvetica", 18), key="Copy Mod Note"), sg.Button(content["Add Loads"], font=("Helvetica", 18), key="Add Loads"), sg.Button(content["Edit Loads"], font=("Helvetica", 18), key="Edit Loads")],
            [sg.Text(f"{content["Without Loads"]}:", font=("Helvetica", 20), justification="right"), sg.StatusBar("00.000", key="without_loads_display", enable_events=True, font=("Helvetica", 20), size=(17,1), tooltip="Click to Copy Time")],
            [sg.Text(f"{content["With Loads"]}:", font=("Helvetica", 20), justification="right"), sg.StatusBar("00.000", key="loads_display", enable_events=True, font=("Helvetica", 20), size=(17,1), tooltip="Click to Copy Time")]
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