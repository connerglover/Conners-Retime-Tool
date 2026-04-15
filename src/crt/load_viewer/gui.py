# Standard library
from decimal import Decimal as d
from typing import NoReturn

# Third-party
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QScrollArea, QWidget, QFrame
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

# Local application
from crt.time import Time
from crt.base_gui import BaseGUI


class LoadViewerDialog(QDialog):
    """Dialog for viewing and managing loads."""

    def __init__(self, time: Time, content: dict, parent=None):
        super().__init__(parent)
        self.content = content
        self.setWindowTitle("Load Viewer")
        self.setFixedWidth(480)
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        self._build_ui(time, content)

    def _build_ui(self, time: Time, content: dict):
        c = content
        outer = QVBoxLayout(self)
        outer.setContentsMargins(16, 12, 16, 12)
        outer.setSpacing(8)

        # Title
        title = QLabel(c["Loads"])
        title.setFont(QFont("Helvetica", 18, QFont.Weight.Bold))
        outer.addWidget(title)

        # Scrollable load list
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        outer.addWidget(scroll)

        self._list_widget = QWidget()
        self._list_layout = QVBoxLayout(self._list_widget)
        self._list_layout.setContentsMargins(0, 0, 0, 0)
        self._list_layout.setSpacing(4)
        self._list_layout.addStretch()
        scroll.setWidget(self._list_widget)

        # Build load rows
        self._load_rows: dict[int, QWidget] = {}
        self._display_labels: dict[int, QLabel] = {}

        for index, load in enumerate(time.loads):
            load_time = round(d(load.length) / d(time.framerate), time.precision)
            self._add_load_row(index, load_time, c)

        # Resize to fit content (up to a max)
        row_height = 44
        max_visible = 8
        n = len(time.loads)
        content_height = min(n, max_visible) * row_height + 80
        self.setFixedHeight(content_height)

    def _add_load_row(self, index: int, load_time, content: dict):
        c = content
        row_widget = QWidget()
        row_widget.setObjectName(f"load_{index}")
        row_layout = QHBoxLayout(row_widget)
        row_layout.setContentsMargins(4, 2, 4, 2)
        row_layout.setSpacing(8)

        display_lbl = QLabel(f"{index + 1}: {load_time}")
        display_lbl.setObjectName(f"display_{index}")
        display_lbl.setFont(QFont("Helvetica", 14))
        row_layout.addWidget(display_lbl, stretch=1)

        btn_edit = QPushButton(c["Edit"])
        btn_edit.setObjectName(f"edit_{index}")
        btn_edit.setFont(QFont("Helvetica", 11))
        btn_edit.setFixedHeight(30)
        btn_edit.setFixedWidth(70)
        row_layout.addWidget(btn_edit)

        btn_delete = QPushButton(c["Delete"])
        btn_delete.setObjectName(f"delete_{index}")
        btn_delete.setFont(QFont("Helvetica", 11))
        btn_delete.setFixedHeight(30)
        btn_delete.setFixedWidth(70)
        row_layout.addWidget(btn_delete)

        # Insert before the stretch
        self._list_layout.insertWidget(self._list_layout.count() - 1, row_widget)
        self._load_rows[index] = row_widget
        self._display_labels[index] = display_lbl


class LoadViewerGUI(BaseGUI):
    """Wrapper around LoadViewerDialog to match the BaseGUI/event-loop interface."""

    def __init__(self, time: Time, content: dict):
        self.window = LoadViewerDialog(time, content)
        self._last_event = None
        self._last_values = {}
        self._connect_signals(time)

    def _connect_signals(self, time: Time):
        for index in range(len(time.loads)):
            edit_btn = self.window.findChild(QPushButton, f"edit_{index}")
            delete_btn = self.window.findChild(QPushButton, f"delete_{index}")
            if edit_btn:
                edit_btn.clicked.connect(lambda checked=False, i=index: self._emit(f"edit_{i}"))
            if delete_btn:
                delete_btn.clicked.connect(lambda checked=False, i=index: self._emit(f"delete_{i}"))

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
