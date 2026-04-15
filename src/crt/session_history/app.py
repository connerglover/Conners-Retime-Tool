# Standard library
from typing import NoReturn

# Local application
from crt.session_history.gui import SessionHistoryGUI
from crt.language import Language


class SessionHistory:
    """Session history for CRT."""

    def __init__(self, language: Language, past_file_paths: list) -> NoReturn:
        """Initializes the SessionHistory class."""
        if not past_file_paths:
            raise ValueError("No session history.")

        self.window = SessionHistoryGUI(past_file_paths, language.content)

    def run(self) -> str:
        """Runs the session history dialog.

        Returns:
            str: The selected file path, or None if cancelled.
        """
        while True:
            event, values = self.window.read()

            match event:
                case "session_history":
                    selected = values.get("session_history", [])
                    file_path = selected[0] if selected else None
                    break

                case None:
                    file_path = None
                    break

        self.window.close()
        return file_path
