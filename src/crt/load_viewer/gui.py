# Standard library
import json
import re
from decimal import Decimal as d
from typing import Callable, NoReturn

# Third-party
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QScrollArea, QWidget, QFrame, QLineEdit, QSizePolicy
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont, QGuiApplication

# Local application
from crt.time import Time
from crt.base_gui import BaseGUI


class LoadRow(QWidget):
    """A single load row that can toggle between display and inline-edit mode."""

    # Emitted when the user clicks Save: (index, start_frame_str, end_frame_str)
    save_requested = Signal(int, str, str)
    # Emitted when the user clicks Delete: (index,)
    delete_requested = Signal(int)

    def __init__(self, index: int, load, framerate: d, precision: int, content: dict, parent=None):
        super().__init__(parent)
        self.index = index
        self.load = load
        self.framerate = framerate
        self.precision = precision
        self.content = content
        self._editing = False
        self._build_ui()

    def _load_time_str(self) -> str:
        if self.framerate and self.framerate != 0:
            t = round(d(self.load.length) / d(self.framerate), self.precision)
        else:
            t = d(0)
        return str(t)

    def _build_ui(self):
        self._outer = QVBoxLayout(self)
        self._outer.setContentsMargins(4, 2, 4, 2)
        self._outer.setSpacing(4)

        # ── Display row ──────────────────────────────────────────────────────
        self._display_row = QWidget()
        dr = QHBoxLayout(self._display_row)
        dr.setContentsMargins(0, 0, 0, 0)
        dr.setSpacing(8)

        self._display_lbl = QLabel(f"{self.index + 1}: {self._load_time_str()}")
        self._display_lbl.setObjectName(f"display_{self.index}")
        self._display_lbl.setFont(QFont("Helvetica", 13))
        dr.addWidget(self._display_lbl, stretch=1)

        self._btn_edit = QPushButton(self.content.get("Edit", "Edit"))
        self._btn_edit.setObjectName(f"edit_{self.index}")
        self._btn_edit.setFont(QFont("Helvetica", 11))
        self._btn_edit.setFixedHeight(28)
        self._btn_edit.setFixedWidth(64)
        self._btn_edit.clicked.connect(self._enter_edit_mode)
        dr.addWidget(self._btn_edit)

        self._btn_delete = QPushButton(self.content.get("Delete", "Delete"))
        self._btn_delete.setObjectName(f"delete_{self.index}")
        self._btn_delete.setFont(QFont("Helvetica", 11))
        self._btn_delete.setFixedHeight(28)
        self._btn_delete.setFixedWidth(64)
        self._btn_delete.clicked.connect(lambda: self.delete_requested.emit(self.index))
        dr.addWidget(self._btn_delete)

        self._outer.addWidget(self._display_row)

        # ── Edit row (hidden by default) ─────────────────────────────────────
        self._edit_row = QWidget()
        self._edit_row.setVisible(False)
        er = QVBoxLayout(self._edit_row)
        er.setContentsMargins(8, 2, 8, 2)
        er.setSpacing(4)

        # Start frame input
        start_row = QHBoxLayout()
        start_row.setSpacing(6)
        start_lbl = QLabel(self.content.get("Start Frame", "Start Frame"))
        start_lbl.setFont(QFont("Helvetica", 12))
        start_lbl.setMinimumWidth(100)
        start_lbl.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        start_row.addWidget(start_lbl)
        self._start_input = QLineEdit(str(self.load.start_frame))
        self._start_input.setObjectName(f"start_{self.index}")
        self._start_input.setFont(QFont("Helvetica", 12))
        self._start_input.setFixedWidth(120)
        self._start_input.setFixedHeight(28)
        start_row.addWidget(self._start_input)
        self._start_paste = QPushButton(self.content.get("Paste", "Paste"))
        self._start_paste.setFont(QFont("Helvetica", 9))
        self._start_paste.setFixedWidth(50)
        self._start_paste.setFixedHeight(28)
        self._start_paste.clicked.connect(
            lambda: self._start_input.setText(QGuiApplication.clipboard().text())
        )
        start_row.addWidget(self._start_paste)
        start_row.addStretch()
        er.addLayout(start_row)

        # End frame input
        end_row = QHBoxLayout()
        end_row.setSpacing(6)
        end_lbl = QLabel(self.content.get("End Frame", "End Frame"))
        end_lbl.setFont(QFont("Helvetica", 12))
        end_lbl.setMinimumWidth(100)
        end_lbl.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        end_row.addWidget(end_lbl)
        self._end_input = QLineEdit(str(self.load.end_frame))
        self._end_input.setObjectName(f"end_{self.index}")
        self._end_input.setFont(QFont("Helvetica", 12))
        self._end_input.setFixedWidth(120)
        self._end_input.setFixedHeight(28)
        end_row.addWidget(self._end_input)
        self._end_paste = QPushButton(self.content.get("Paste", "Paste"))
        self._end_paste.setFont(QFont("Helvetica", 9))
        self._end_paste.setFixedWidth(50)
        self._end_paste.setFixedHeight(28)
        self._end_paste.clicked.connect(
            lambda: self._end_input.setText(QGuiApplication.clipboard().text())
        )
        end_row.addWidget(self._end_paste)
        end_row.addStretch()
        er.addLayout(end_row)

        # Save / Discard buttons
        action_row = QHBoxLayout()
        action_row.setSpacing(6)
        action_row.addStretch()
        self._btn_save = QPushButton(self.content.get("Save Edits", "Save Edits"))
        self._btn_save.setFont(QFont("Helvetica", 11))
        self._btn_save.setFixedHeight(28)
        self._btn_save.clicked.connect(self._on_save)
        action_row.addWidget(self._btn_save)
        self._btn_discard = QPushButton(self.content.get("Discard Changes", "Discard"))
        self._btn_discard.setFont(QFont("Helvetica", 11))
        self._btn_discard.setFixedHeight(28)
        self._btn_discard.clicked.connect(self._exit_edit_mode)
        action_row.addWidget(self._btn_discard)
        er.addLayout(action_row)

        self._outer.addWidget(self._edit_row)

        # Separator
        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setFrameShadow(QFrame.Shadow.Sunken)
        self._outer.addWidget(sep)

    def _enter_edit_mode(self):
        self._editing = True
        # Reset inputs to current load values
        self._start_input.setText(str(self.load.start_frame))
        self._end_input.setText(str(self.load.end_frame))
        self._display_row.setVisible(False)
        self._edit_row.setVisible(True)
        # Ask parent dialog to resize
        if self.parent():
            self.parent().adjustSize()

    def _exit_edit_mode(self):
        self._editing = False
        self._edit_row.setVisible(False)
        self._display_row.setVisible(True)
        if self.parent():
            self.parent().adjustSize()

    def _on_save(self):
        start_text = self._start_input.text()
        end_text = self._end_input.text()
        self.save_requested.emit(self.index, start_text, end_text)
        # Exit edit mode — display label will be updated by the controller
        self._exit_edit_mode()

    def refresh_display(self):
        """Refresh the display label after the load has been mutated."""
        self._display_lbl.setText(f"{self.index + 1}: {self._load_time_str()}")


class LoadViewerDialog(QDialog):
    """Dialog for viewing and managing loads with inline editing."""

    def __init__(self, time: Time, content: dict, parent=None):
        super().__init__(parent)
        self._time = time
        self.content = content
        self.setWindowTitle(content.get("Loads", "Load Viewer"))
        self.setMinimumWidth(500)
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        self._load_rows: dict[int, LoadRow] = {}
        self._build_ui(time, content)

    def _build_ui(self, time: Time, content: dict):
        outer = QVBoxLayout(self)
        outer.setContentsMargins(16, 12, 16, 12)
        outer.setSpacing(8)

        # Title
        title = QLabel(content.get("Loads", "Loads"))
        title.setFont(QFont("Helvetica", 18, QFont.Weight.Bold))
        outer.addWidget(title)

        # Scrollable load list
        self._scroll = QScrollArea()
        self._scroll.setWidgetResizable(True)
        self._scroll.setFrameShape(QFrame.Shape.NoFrame)
        outer.addWidget(self._scroll)

        self._list_widget = QWidget()
        self._list_layout = QVBoxLayout(self._list_widget)
        self._list_layout.setContentsMargins(0, 0, 0, 0)
        self._list_layout.setSpacing(0)
        self._list_layout.addStretch()
        self._scroll.setWidget(self._list_widget)

        for index, load in enumerate(time.loads):
            row = LoadRow(index, load, time.framerate, time.precision, content, self._list_widget)
            self._list_layout.insertWidget(self._list_layout.count() - 1, row)
            self._load_rows[index] = row

        # Done button
        done_row = QHBoxLayout()
        done_row.addStretch()
        self._btn_done = QPushButton(content.get("Done", "Done"))
        self._btn_done.setFont(QFont("Helvetica", 12))
        self._btn_done.setMinimumHeight(32)
        self._btn_done.setMinimumWidth(80)
        done_row.addWidget(self._btn_done)
        outer.addLayout(done_row)

        # Size to content
        n = len(time.loads)
        row_h = 48
        max_vis = 8
        self._scroll.setFixedHeight(min(n, max_vis) * row_h + 8)
        self.adjustSize()


class LoadViewerGUI(BaseGUI):
    """Wrapper around LoadViewerDialog to match the BaseGUI/event-loop interface."""

    def __init__(self, time: Time, content: dict):
        self.window = LoadViewerDialog(time, content)
        self._last_event = None
        self._last_values = {}
        self._connect_signals()

    def _connect_signals(self):
        for index, row in self.window._load_rows.items():
            row.save_requested.connect(self._on_save)
            row.delete_requested.connect(self._on_delete)
        self.window._btn_done.clicked.connect(lambda: self._emit("done"))

    def _on_save(self, index: int, start_text: str, end_text: str):
        self._last_event = f"save_{index}"
        self._last_values = {
            "index": index,
            "start": start_text,
            "end": end_text,
        }

    def _on_delete(self, index: int):
        self._emit(f"delete_{index}")

    def _emit(self, event: str):
        self._last_event = event
        self._last_values = {}

    def read(self) -> tuple:
        """Blocking read: shows the dialog and returns (event, values)."""
        from PySide6.QtWidgets import QApplication
        self._last_event = None
        self.window.show()
        while self._last_event is None and self.window.isVisible():
            QApplication.processEvents()
        event = self._last_event
        values = self._last_values
        return event, values

    def close(self):
        if self.window:
            self.window.close()

    def refresh_row(self, index: int):
        """Refresh the display label of a load row after mutation."""
        row = self.window._load_rows.get(index)
        if row:
            row.refresh_display()

    def hide_row(self, index: int):
        """Hide a load row (after deletion)."""
        row = self.window._load_rows.get(index)
        if row:
            row.setVisible(False)
