class BaseGUI:
    """Base class for all CRT GUIs
    """
    
    def read(self) -> tuple[str, dict]:
        """Reads the window
        """
        return self.window.read()
    
    def close(self):
        """Closes the window
        """
        self.window.close()
    
    def __enter__(self):
        """Context manager enter
        """
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit
        """
        self.close()
        