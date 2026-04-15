# Third-party libraries
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QFrame, QMenuBar, QMenu,
    QSizePolicy, QApplication
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QAction, QFont

# Local application
from crt.base_gui import BaseGUI


class ClickableLabel(QLabel):
    """A QLabel that emits a clicked signal."""
    clicked = Signal()

    def mousePressEvent(self, event):
        self.clicked.emit()
        super().mousePressEvent(event)


class MainWindow(QMainWindow):
    """The main QMainWindow for CRT."""

    def __init__(self, content: dict):
        super().__init__()
        self.content = content
        self.setWindowTitle("Conner's Retime Tool")
        self.setFixedSize(560, 440)
        self._build_ui()

    def _build_ui(self):
        c = self.content

        # ── Menu bar ──────────────────────────────────────────────────────────
        menubar = self.menuBar()

        # File menu
        file_menu = menubar.addMenu(c["File"])
        self._add_action(file_menu, c["New Time"],       "New Time")
        file_menu.addSeparator()
        self._add_action(file_menu, c["Open Time"],      "Open Time")
        self._add_action(file_menu, c["Session History"],"Session History")
        file_menu.addSeparator()
        self._add_action(file_menu, c["Save"],           "Save")
        self._add_action(file_menu, c["Save As"],        "Save As")
        file_menu.addSeparator()
        self._add_action(file_menu, c["Settings"],       "Settings")
        file_menu.addSeparator()
        self._add_action(file_menu, c["Exit"],           "Exit")

        # Edit menu
        edit_menu = menubar.addMenu(c["Edit (Menu Bar)"])
        self._add_action(edit_menu, c["Copy Mod Note"],  "Copy Mod Note")
        edit_menu.addSeparator()
        self._add_action(edit_menu, c["Clear Loads"],    "Clear Loads")
        self._add_action(edit_menu, c["Edit Loads"],     "Edit Loads")

        # Help menu
        help_menu = menubar.addMenu(c["Help"])
        self._add_action(help_menu, c["Check for Updates"], "Check for Updates")
        help_menu.addSeparator()
        self._add_action(help_menu, c["Report Issue"],   "Report Issue")
        self._add_action(help_menu, c["Suggest Feature"],"Suggest Feature")
        help_menu.addSeparator()
        self._add_action(help_menu, c["About"],          "About")

        # ── Central widget ────────────────────────────────────────────────────
        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setContentsMargins(16, 12, 16, 12)
        root.setSpacing(8)

        # Input rows
        self._inputs = {}
        rows = [
            ("framerate",    c["Framerate"],           "60"),
            ("start",        c["Start Frame"],         "0"),
            ("end",          c["End Frame"],            "0"),
            ("start_loads",  c["Start Frame (Loads)"], "0"),
            ("end_loads",    c["End Frame (Loads)"],   "0"),
        ]
        for key, label_text, default in rows:
            root.addLayout(self._make_input_row(key, label_text, default, c["Paste"]))

        # Separator
        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setFrameShadow(QFrame.Shadow.Sunken)
        root.addWidget(sep)

        # Action buttons row
        btn_row = QHBoxLayout()
        btn_row.setSpacing(8)
        self.btn_copy_mod_note = QPushButton(c["Copy Mod Note"])
        self.btn_copy_mod_note.setObjectName("Copy Mod Note")
        self.btn_add_loads = QPushButton(c["Add Loads"])
        self.btn_add_loads.setObjectName("Add Loads")
        self.btn_edit_loads = QPushButton(c["Edit Loads"])
        self.btn_edit_loads.setObjectName("Edit Loads")
        for btn in (self.btn_copy_mod_note, self.btn_add_loads, self.btn_edit_loads):
            btn.setFont(QFont("Helvetica", 13))
            btn.setMinimumHeight(38)
            btn_row.addWidget(btn)
        root.addLayout(btn_row)

        # Display rows
        self.without_loads_display = self._make_display_row(
            root, f"{c['Without Loads']}:", "without_loads_display", "00.000",
            tooltip=c.get("Click to Copy Time", "Click to Copy Time")
        )
        self.loads_display = self._make_display_row(
            root, f"{c['With Loads']}:", "loads_display", "00.000",
            tooltip=c.get("Click to Copy Time", "Click to Copy Time")
        )

    def _add_action(self, menu: QMenu, text: str, key: str) -> QAction:
        action = QAction(text, self)
        action.setData(key)
        menu.addAction(action)
        return action

    def _make_input_row(self, key: str, label_text: str, default: str, paste_label: str) -> QHBoxLayout:
        row = QHBoxLayout()
        row.setSpacing(6)

        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        row.addWidget(spacer)

        lbl = QLabel(label_text)
        lbl.setFont(QFont("Helvetica", 13))
        lbl.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        lbl.setMinimumWidth(180)
        row.addWidget(lbl)

        inp = QLineEdit(default)
        inp.setObjectName(key)
        inp.setFont(QFont("Helvetica", 13))
        inp.setFixedWidth(140)
        inp.setFixedHeight(30)
        row.addWidget(inp)
        self._inputs[key] = inp

        paste_btn = QPushButton(paste_label)
        paste_btn.setObjectName(f"{key}_paste")
        paste_btn.setFont(QFont("Helvetica", 9))
        paste_btn.setFixedWidth(54)
        paste_btn.setFixedHeight(30)
        row.addWidget(paste_btn)

        return row

    def _make_display_row(self, parent_layout: QVBoxLayout, label_text: str,
                          key: str, default: str, tooltip: str) -> ClickableLabel:
        row = QHBoxLayout()
        row.setSpacing(6)

        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        row.addWidget(spacer)

        lbl = QLabel(label_text)
        lbl.setFont(QFont("Helvetica", 15, QFont.Weight.Bold))
        lbl.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        row.addWidget(lbl)

        display = ClickableLabel(default)
        display.setObjectName(key)
        display.setFont(QFont("Helvetica", 15))
        display.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        display.setToolTip(tooltip)
        display.setMinimumWidth(160)
        display.setFixedHeight(32)
        display.setFrameShape(QFrame.Shape.StyledPanel)
        display.setFrameShadow(QFrame.Shadow.Sunken)
        display.setContentsMargins(6, 0, 6, 0)
        row.addWidget(display)

        parent_layout.addLayout(row)
        return display


class MainGUI(BaseGUI):
    """Main window for CRT."""

    def __init__(self, content: dict):
        self.window = MainWindow(content)
