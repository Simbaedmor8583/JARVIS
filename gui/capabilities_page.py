"""Searchable operational view of the real dynamic capability registry."""
import time

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QSplitter,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from gui.widgets.hud import HudPanel


class CapabilitiesPage(QWidget):
    def __init__(self, gui_controller, parent=None):
        super().__init__(parent)
        self.gc = gui_controller
        self._records = []
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        controls = HudPanel("Capability Registry Filters", compact=True)
        top = QHBoxLayout()
        self.summary = QLabel("Waiting for capability scan")
        self.summary.setObjectName("dataValue")
        self.search = QLineEdit()
        self.search.setPlaceholderText("Search name, detail, permission…")
        self.search.textChanged.connect(self._filter)
        self.filters = {}
        for key, label in (
            ("category", "All categories"), ("status", "All statuses"),
            ("permission", "All permissions"), ("risk", "All risks"),
        ):
            combo = QComboBox()
            combo.addItem(label, "")
            combo.currentIndexChanged.connect(self._filter)
            self.filters[key] = combo
            top.addWidget(combo)
        self.refresh_button = QPushButton("REFRESH")
        self.refresh_button.clicked.connect(self.refresh)
        self.selftest_button = QPushButton("SELF TEST")
        self.selftest_button.clicked.connect(self.refresh)
        top.insertWidget(0, self.summary)
        top.insertStretch(1, 1)
        top.insertWidget(2, self.search)
        top.addWidget(self.refresh_button)
        top.addWidget(self.selftest_button)
        controls.content.addLayout(top)
        root.addWidget(controls)

        splitter = QSplitter(Qt.Horizontal)
        table_panel = HudPanel("Registered Capabilities")
        self.table = QTableWidget(0, 8)
        self.table.setHorizontalHeaderLabels((
            "Capability", "Category", "Status", "Permission", "Risk",
            "Connected", "Last Check", "Detail",
        ))
        self.table.setSortingEnabled(True)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.itemSelectionChanged.connect(self._show_selected)
        self.table.horizontalHeader().setStretchLastSection(True)
        table_panel.content.addWidget(self.table)
        splitter.addWidget(table_panel)

        detail_panel = HudPanel("Capability Details")
        self.details = {}
        form = QFormLayout()
        for label, key in (
            ("NAME", "capability_id"), ("CATEGORY", "category"),
            ("STATUS", "status"), ("CONNECTED", "connected"),
            ("RISK", "risk"), ("PERMISSION", "permission"),
            ("REQUIRED SOFTWARE", "dependencies"),
            ("CONFIGURATION", "detail"), ("VOICE EXAMPLES", "voice_examples"),
            ("GUI EXAMPLES", "gui_examples"), ("LAST SUCCESS", "last_success"),
            ("LAST FAILURE", "last_failure"),
        ):
            value = QLabel("Unavailable")
            value.setObjectName("dataValue")
            value.setWordWrap(True)
            value.setTextInteractionFlags(Qt.TextSelectableByMouse)
            self.details[key] = value
            form.addRow(label, value)
        detail_panel.content.addLayout(form)
        self.test_button = QPushButton("TEST CAPABILITY HEALTH")
        self.test_button.clicked.connect(self.refresh)
        detail_panel.content.addWidget(self.test_button)
        splitter.addWidget(detail_panel)
        splitter.setStretchFactor(0, 4)
        splitter.setStretchFactor(1, 2)
        root.addWidget(splitter, 1)

    def refresh(self):
        self.summary.setText("Scanning capabilities…")
        self.refresh_button.setEnabled(False)
        self.selftest_button.setEnabled(False)
        self.test_button.setEnabled(False)
        self.gc.run_async(self.gc.controller.start_capability_scan)

    def set_report(self, report):
        report = report if isinstance(report, dict) else {}
        self._records = list(report.get("capabilities", []))
        counts = report.get("counts", {})
        self.summary.setText(
            f"{report.get('total', 0)} total · "
            + ", ".join(f"{key}: {value}" for key, value in sorted(counts.items()))
        )
        self._populate_filters()
        self.refresh_button.setEnabled(True)
        self.selftest_button.setEnabled(True)
        self.test_button.setEnabled(True)
        self._filter()

    def _populate_filters(self):
        mappings = {
            "category": {record.get("skill", "") for record in self._records},
            "status": {record.get("status", "") for record in self._records},
            "permission": {record.get("permission", "") for record in self._records},
            "risk": {record.get("risk", "") for record in self._records},
        }
        for key, values in mappings.items():
            combo = self.filters[key]
            selected = combo.currentData()
            combo.blockSignals(True)
            while combo.count() > 1:
                combo.removeItem(1)
            for value in sorted(item for item in values if item):
                combo.addItem(str(value), str(value))
            index = combo.findData(selected)
            combo.setCurrentIndex(max(0, index))
            combo.blockSignals(False)

    def _filter(self):
        query = self.search.text().strip().lower()
        selected = {key: combo.currentData() for key, combo in self.filters.items()}
        records = []
        for record in self._records:
            category = record.get("skill", "")
            values = {
                "category": category,
                "status": record.get("status", ""),
                "permission": record.get("permission", ""),
                "risk": record.get("risk", ""),
            }
            haystack = " ".join(str(value) for value in record.values()).lower()
            if query and query not in haystack:
                continue
            if any(selected[key] and str(values[key]) != str(selected[key]) for key in selected):
                continue
            records.append(record)
        self.table.setSortingEnabled(False)
        self.table.setRowCount(len(records))
        for row, record in enumerate(records):
            checked = record.get("last_checked") or 0
            values = (
                record.get("capability_id", ""),
                record.get("skill", ""),
                record.get("status", "Unavailable"),
                record.get("permission", "UNASSIGNED"),
                record.get("risk", "unknown"),
                "Yes" if record.get("connected") else "No",
                time.strftime("%H:%M:%S", time.localtime(checked)) if checked else "Never",
                record.get("detail", ""),
            )
            for column, value in enumerate(values):
                item = QTableWidgetItem(str(value))
                item.setData(Qt.UserRole, record)
                self.table.setItem(row, column, item)
        self.table.setSortingEnabled(True)
        if records:
            self.table.selectRow(0)
        else:
            self._show_record({})

    def _show_selected(self):
        item = self.table.item(self.table.currentRow(), 0)
        self._show_record(item.data(Qt.UserRole) if item else {})

    def _show_record(self, record):
        record = record if isinstance(record, dict) else {}
        record = dict(record)
        record.setdefault("category", record.get("skill", "Unavailable"))
        for key, label in self.details.items():
            value = record.get(key)
            if key in {"last_success", "last_failure"}:
                value = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(value)) if value else "Never"
            elif isinstance(value, (list, tuple)):
                value = "\n".join(map(str, value)) or "None"
            elif key == "connected":
                value = "Yes" if value else "No"
            label.setText(str(value if value not in (None, "") else "Unavailable"))
