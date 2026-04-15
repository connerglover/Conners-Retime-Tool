# Standard library
import json
from decimal import Decimal as d
from typing import NoReturn

# Third-party
from PySide6.QtWidgets import QMessageBox, QLineEdit

# Local application
from crt.load import Load
from crt.load_editor.gui import LoadEditorGUI
from crt.language import Language


def _popup_error(title: str, message: str):
    """Shows an error popup."""
    box = QMessageBox()
    box.setWindowTitle(title)
    box.setText(str(message))
    box.setIcon(QMessageBox.Icon.Critical)
    box.setStandardButtons(QMessageBox.StandardButton.Ok)
    box.exec()


class LoadEditor:
    """Load editor for CRT."""

    def __init__(self, load: Load, framerate: d, language: Language) -> NoReturn:
        """Initializes the LoadEditor class."""
        self.load = load
        self.framerate = framerate
        self.window = LoadEditorGUI(load, framerate, language.content)

    def _handle_frame_input(self, values: dict, key: str) -> NoReturn:
        """Handles the frame input."""
        value = values[key]
        if value and value[-1] == "}":
            try:
                frame = self._debug_info_to_frame(value)
            except ValueError as e:
                frame = 0
                _popup_error("Error", e)
        else:
            frame = self._clean_frame(value)

        # Update the widget directly
        inp = self.window.window.findChild(QLineEdit, key)
        if inp:
            inp.blockSignals(True)
            inp.setText(str(int(frame)))
            inp.blockSignals(False)

    def _debug_info_to_frame(self, debug_info: str) -> int:
        """Converts debug info to a frame."""
        debug_info = "{" + debug_info.split("{", 1)[-1]

        try:
            parsed_debug_info = json.loads(debug_info)
        except json.decoder.JSONDecodeError:
            raise ValueError("The debug info provided is invalid.\nPlease re-enter debug info.")

        try:
            cmt = parsed_debug_info["cmt"]
        except KeyError:
            raise ValueError("The debug info provided is invalid.\nPlease re-enter debug info.")

        output = d(cmt) * d(self.framerate)
        output = int(round(output, 0))
        return output

    def _clean_frame(self, frame: str) -> int:
        """Cleans the frame."""
        digits = ''.join(char for char in frame if char.isdigit())
        return int(digits) if digits else 0

    def run(self) -> Load:
        """Runs the load editor."""
        from PySide6.QtWidgets import QApplication
        from PySide6.QtGui import QGuiApplication

        while True:
            event, values = self.window.read()

            match event:
                case "Save Edits":
                    self.load = Load(
                        int(values.get("start", 0) or 0),
                        int(values.get("end", 0) or 0)
                    )
                    break

                case "Discard Changes":
                    break

                case "start":
                    self._handle_frame_input(values, "start")

                case "end":
                    self._handle_frame_input(values, "end")

                case "start_paste":
                    text = QGuiApplication.clipboard().text()
                    self._handle_frame_input({"start": text}, "start")

                case "end_paste":
                    text = QGuiApplication.clipboard().text()
                    self._handle_frame_input({"end": text}, "end")

                case None:
                    # Window was closed
                    break

        self.window.close()
        return self.load
