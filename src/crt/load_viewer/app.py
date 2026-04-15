# Standard library
import json
import re
from decimal import Decimal as d, InvalidOperation
from typing import NoReturn

# Third-party
from PySide6.QtWidgets import QMessageBox

# Local application
from crt.time import Time
from crt.load_viewer.gui import LoadViewerGUI
from crt.language import Language


def _popup_error(title: str, message: str):
    box = QMessageBox()
    box.setWindowTitle(title)
    box.setText(str(message))
    box.setIcon(QMessageBox.Icon.Critical)
    box.setStandardButtons(QMessageBox.StandardButton.Ok)
    box.exec()


def _parse_frame(text: str, framerate: d) -> int:
    """Parse a frame input string following the full validation spec."""
    text = str(text).strip()

    # Debug info detection
    if '{' in text and '"cmt"' in text:
        start = text.find('{')
        try:
            parsed = json.loads(text[start:])
            cmt = parsed["cmt"]
            fps = d(str(framerate)) if framerate and framerate != 0 else d('1')
            return int(round(d(str(cmt)) * fps, 0))
        except (json.JSONDecodeError, KeyError, InvalidOperation):
            pass

    # Strip non-numeric/non-decimal characters
    cleaned = re.sub(r'[^0-9.]', '', text)

    if not cleaned or not re.search(r'[0-9]', cleaned):
        return 0

    # Collapse multiple decimal points
    if cleaned.count('.') > 1:
        idx = cleaned.find('.')
        cleaned = cleaned[:idx + 1] + cleaned[idx + 1:].replace('.', '')

    # Decimal → timestamp conversion
    if '.' in cleaned:
        try:
            fps = d(str(framerate)) if framerate and framerate != 0 else d('1')
            return int(round(d(cleaned) * fps, 0))
        except (InvalidOperation, ValueError):
            return 0

    try:
        return int(cleaned)
    except ValueError:
        return 0


class LoadViewer:
    """Load viewer for CRT — handles inline editing of all loads at once."""

    def __init__(self, time: Time, language: Language) -> NoReturn:
        if not time.loads:
            raise ValueError("No loads to edit.")

        self.time = time
        self.language = language
        self.window = LoadViewerGUI(time, language.content)
        self._loads_to_delete: list[int] = []

    def _save_all(self, rows_data: dict) -> list[str]:
        """Validate and save all edited rows. Returns a list of error messages."""
        errors = []
        for index_str, data in rows_data.items():
            index = int(index_str)
            if index >= len(self.time.loads):
                continue
            start_frame = _parse_frame(data.get("start", "0"), self.time.framerate)
            end_frame = _parse_frame(data.get("end", "0"), self.time.framerate)

            if start_frame == end_frame:
                errors.append(f"Load {index + 1}: duration is 0 (start equals end)")
                continue
            if start_frame > end_frame:
                errors.append(f"Load {index + 1}: end frame is before start frame")
                continue

            self.time.loads[index].start_frame = start_frame
            self.time.loads[index].end_frame = end_frame

        return errors

    def _delete_load(self, index: int) -> NoReturn:
        """Marks a load for deletion and hides its row."""
        self._loads_to_delete.append(index)
        self.window.hide_row(index)

    def _cleanup(self) -> NoReturn:
        """Removes deleted loads from the time object (highest index first)."""
        for index in sorted(set(self._loads_to_delete), reverse=True):
            if 0 <= index < len(self.time.loads):
                del self.time.loads[index]

    def run(self) -> Time:
        """Runs the load viewer event loop."""
        while True:
            event, values = self.window.read()

            if event is None:
                break

            elif event == "save_all":
                rows_data = values.get("rows", {})
                errors = self._save_all(rows_data)
                if errors:
                    _popup_error("Validation Error", "\n".join(errors))
                else:
                    break

            elif event == "discard":
                # Inputs already reset by the GUI; just close
                break

            elif isinstance(event, str) and event.startswith("delete_"):
                try:
                    index = int(event.split("_", 1)[1])
                    self._delete_load(index)
                except (ValueError, IndexError):
                    pass

        self.window.close()
        self._cleanup()
        return self.time
