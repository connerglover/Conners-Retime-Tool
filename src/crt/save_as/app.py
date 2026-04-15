# Standard Library
from typing import NoReturn

# Local application
from crt.save_as.gui import SaveAsGUI
from crt.language import Language


class SaveAs:
    """Save CRT as a time file."""

    def __init__(self, language: Language) -> NoReturn:
        """Initializes the SaveAs class."""
        self.window = SaveAsGUI(language.content)

    def run(self) -> str:
        """Runs the save as dialog.

        Returns:
            str: The file path, or None if cancelled.
        """
        while True:
            event, values = self.window.read()

            match event:
                case "save":
                    file_path = values.get("file_name") or None
                    break

                case "cancel" | None:
                    file_path = None
                    break

        self.window.close()
        return file_path
