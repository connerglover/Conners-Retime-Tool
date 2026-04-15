class BaseGUI:
    """Base class for all CRT GUIs.
    
    Subclasses must set self.window to a QDialog or QMainWindow instance.
    """

    def close(self):
        """Closes the window."""
        if hasattr(self, "window") and self.window is not None:
            self.window.close()

    def __enter__(self):
        """Context manager enter."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
