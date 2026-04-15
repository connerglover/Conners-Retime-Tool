# Standard library
from decimal import Decimal as d
from typing import NoReturn

# Third-party
from PySide6.QtWidgets import QPushButton, QLabel

# Local application
from crt.time import Time
from crt import load_editor
from crt.load_viewer.gui import LoadViewerGUI
from crt.language import Language


class LoadViewer:
    """Load viewer for CRT."""

    def __init__(self, time: Time, language: Language) -> NoReturn:
        """Initializes the LoadViewer class."""
        self.time = time
        self.language = language
        self.window = LoadViewerGUI(time, language.content)

        if not self.time.loads:
            raise ValueError("No loads to edit.")

        self.loads_to_delete = []

    def _edit_load(self, load_index: int) -> NoReturn:
        """Edits the load."""
        load = load_editor.LoadEditor(
            self.time.loads[load_index], self.time.framerate, self.language
        )
        load = load.run()
        self.time.mutate_load(load_index, load.start_frame, load.end_frame)
        load_time = round(d(load.length) / d(self.time.framerate), self.time.precision)

        # Update the display label
        lbl = self.window.window.findChild(QLabel, f"display_{load_index}")
        if lbl:
            lbl.setText(f"{load_index + 1}: {load_time}")

    def _delete_load(self, load_index: int) -> NoReturn:
        """Deletes the load."""
        self.loads_to_delete.append(load_index)
        # Hide the row widget
        from crt.load_viewer.gui import LoadViewerDialog
        row = self.window.window.findChild(type(self.window.window), f"load_{load_index}")
        # Use QWidget lookup by object name
        from PySide6.QtWidgets import QWidget
        row = self.window.window.findChild(QWidget, f"load_{load_index}")
        if row:
            row.setVisible(False)

    def _cleanup(self) -> NoReturn:
        """Cleans up the load viewer."""
        self.loads_to_delete.sort(reverse=True)
        for index in self.loads_to_delete:
            del self.time.loads[index]

    def run(self) -> Time:
        """Runs the load viewer."""
        while True:
            event, values = self.window.read()

            if event is None:
                break

            if '_' in str(event):
                parts = event.rsplit('_', 1)
                if len(parts) == 2:
                    action, load_index_str = parts
                    try:
                        load_index = int(load_index_str)
                    except ValueError:
                        continue

                    if action == "edit":
                        self._edit_load(load_index)
                    elif action == "delete":
                        self._delete_load(load_index)

        self.window.close()
        self._cleanup()
        return self.time
