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
    """Parse a frame input string.

    Rules (same as App._parse_frame_input):
    1. If it contains JSON debug info, extract cmt * framerate.
    2. Strip non-numeric/non-decimal characters.
    3. Empty → 0.
    4. Contains decimal → treat as seconds timestamp, convert to frame.
    5. Otherwise → plain integer.
    """
    text = str(text).strip()

    # 1 — debug info
    if '{' in text and '"cmt"' in text:
        start = text.find('{')
        try:
            parsed = json.loads(text[start:])
            cmt = parsed["cmt"]
            fps = d(str(framerate)) if framerate and framerate != 0 else d('1')
            return int(round(d(str(cmt)) * fps, 0))
        except (json.JSONDecodeError, KeyError, InvalidOperation):
            pass

    # 2 — strip non-numeric/non-decimal
    cleaned = re.sub(r'[^0-9.]', '', text)

    # 3 — empty
    if not cleaned or not re.search(r'[0-9]', cleaned):
        return 0

    # Collapse multiple decimal points
    if cleaned.count('.') > 1:
        idx = cleaned.find('.')
        cleaned = cleaned[:idx + 1] + cleaned[idx + 1:].replace('.', '')

    # 4 — decimal → timestamp
    if '.' in cleaned:
        try:
            fps = d(str(framerate)) if framerate and framerate != 0 else d('1')
            return int(round(d(cleaned) * fps, 0))
        except (InvalidOperation, ValueError):
            return 0

    # 5 — plain integer
    try:
        return int(cleaned)
    except ValueError:
        return 0


class LoadViewer:
    """Load viewer for CRT — handles inline editing without a separate LoadEditor."""

    def __init__(self, time: Time, language: Language) -> NoReturn:
        """Initializes the LoadViewer class."""
        if not time.loads:
            raise ValueError("No loads to edit.")

        self.time = time
        self.language = language
        self.window = LoadViewerGUI(time, language.content)
        self._loads_to_delete: list[int] = []

    def _save_load(self, index: int, start_text: str, end_text: str) -> NoReturn:
        """Validates and saves an inline-edited load."""
        start_frame = _parse_frame(start_text, self.time.framerate)
        end_frame = _parse_frame(end_text, self.time.framerate)

        # Validate manually (bypassing the decorator's broken arg-position logic)
        if start_frame == end_frame:
            raise ValueError("The duration of the load is 0.000")
        if start_frame > end_frame:
            raise ValueError("The load time ends before it starts.")

        # Directly mutate the load (skip @validate_load to avoid the args[0]=index bug)
        self.time.loads[index].start_frame = start_frame
        self.time.loads[index].end_frame = end_frame

        # Refresh the display label in the GUI
        self.window.refresh_row(index)

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

            if event is None or event == "done":
                break

            if isinstance(event, str) and event.startswith("save_"):
                try:
                    index = int(event.split("_", 1)[1])
                    self._save_load(index, values.get("start", "0"), values.get("end", "0"))
                except (ValueError, IndexError) as e:
                    _popup_error("Error", str(e))

            elif isinstance(event, str) and event.startswith("delete_"):
                try:
                    index = int(event.split("_", 1)[1])
                    self._delete_load(index)
                except (ValueError, IndexError):
                    pass

        self.window.close()
        self._cleanup()
        return self.time
