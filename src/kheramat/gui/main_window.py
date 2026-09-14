import sys
import os
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QPlainTextEdit,
    QLineEdit, QTableWidget, QTableWidgetItem, QSplitter, QHeaderView,
    QTreeView, QFileSystemModel, QDockWidget, QToolBar, QStatusBar,
    QMessageBox, QApplication, QTabWidget, QFileDialog, QMenuBar, QMenu
)
from PySide6.QtCore import Qt, QSize, QModelIndex
from PySide6.QtGui import QFont, QAction, QIcon, QTextCursor

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

from ..runtime.interpreter import Interpreter
from ..services import ExecutionService, WorkspaceService
from ..toolbox.plotting import PlotManager
from .code_editor import CodeEditor

class PlotCanvas(FigureCanvas):
    def __init__(self, parent=None):
        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.axes = self.fig.add_subplot(111)
        super().__init__(self.fig)
        self.setParent(parent)

class CommandLineEdit(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.history = []
        self.history_idx = 0

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Up:
            if self.history and self.history_idx > 0:
                self.history_idx -= 1
                self.setText(self.history[self.history_idx])
            return
        elif event.key() == Qt.Key_Down:
            if self.history and self.history_idx < len(self.history) - 1:
                self.history_idx += 1
                self.setText(self.history[self.history_idx])
            elif self.history_idx >= len(self.history) - 1:
                self.history_idx = len(self.history)
                self.clear()
            return
        super().keyPressEvent(event)

class CommandWindow(QWidget):
    def __init__(self, interpreter: Interpreter, on_command_executed_cb=None):
        super().__init__()
        self.interpreter = interpreter
        self.on_command_executed_cb = on_command_executed_cb

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.display = QTextEdit()
        self.display.setReadOnly(True)
        self.display.setFont(QFont("Consolas", 10))
        self.display.setText("Vectra Desktop Environment (v0.1.0)\nType MATLAB commands or run scripts.\n\n")

        self.input_line = CommandLineEdit()
        self.input_line.setFont(QFont("Consolas", 10))
        self.input_line.setPlaceholderText(">> type command here...")
        self.input_line.returnPressed.connect(self.execute_command)

        layout.addWidget(self.display)
        layout.addWidget(self.input_line)

    def execute_command(self):
        cmd = self.input_line.text().strip()
        if not cmd:
            return

        self.input_line.clear()
        self.display.append(f">> {cmd}")
        self.input_line.history.append(cmd)
        self.input_line.history_idx = len(self.input_line.history)

        try:
            logs = self.interpreter.eval_code(cmd)
            for log in logs:
                self.display.append(log)
        except Exception as e:
            self.display.append(f"<font color='red'>Error: {e}</font>")

        if self.on_command_executed_cb:
            self.on_command_executed_cb()

class WorkspacePanel(QTableWidget):
    def __init__(self, interpreter: Interpreter):
        super().__init__(0, 3)
        self.interpreter = interpreter
        self.setHorizontalHeaderLabels(["Name", "Size", "Value"])
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.setEditTriggers(QTableWidget.NoEditTriggers)

    def refresh(self):
        self.setRowCount(0)
        infos = self.interpreter.workspace.get_info_list()
        for row_idx, info in enumerate(infos):
            self.insertRow(row_idx)
            self.setItem(row_idx, 0, QTableWidgetItem(info.name))
            self.setItem(row_idx, 1, QTableWidgetItem(info.size_str))
            self.setItem(row_idx, 2, QTableWidgetItem(info.value_str))

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Vectra — Scientific Computing & Engineering Desktop Environment")
        self.resize(1280, 800)

        self.interpreter = Interpreter()
        self.exec_service = ExecutionService(self.interpreter)
        self.ws_service = WorkspaceService(self.interpreter.workspace)
        self.is_dark_mode = True
        self._setup_ui()

    def _setup_ui(self):
        self.setDockNestingEnabled(True)
        self.setDockOptions(QMainWindow.AllowNestedDocks | QMainWindow.AnimatedDocks | QMainWindow.GroupedDragging | QMainWindow.AllowTabbedDocks)
        
        # Configure corners so bottom dock spans full width across bottom
        self.setCorner(Qt.TopLeftCorner, Qt.LeftDockWidgetArea)
        self.setCorner(Qt.BottomLeftCorner, Qt.BottomDockWidgetArea)
        self.setCorner(Qt.TopRightCorner, Qt.RightDockWidgetArea)
        self.setCorner(Qt.BottomRightCorner, Qt.BottomDockWidgetArea)

        # 1. Extreme Left: Current Folder Explorer
        self.file_model = QFileSystemModel()
        self.file_model.setRootPath(os.getcwd())
        self.tree_view = QTreeView()
        self.tree_view.setModel(self.file_model)
        self.tree_view.setRootIndex(self.file_model.index(os.getcwd()))
        self.tree_view.doubleClicked.connect(self._on_file_double_clicked)
        dock_files = QDockWidget("Current Folder", self)
        dock_files.setWidget(self.tree_view)
        dock_files.setObjectName("DockFiles")
        self.addDockWidget(Qt.LeftDockWidgetArea, dock_files)

        # 2. Center: Script Editor
        self.editor_tabs = QTabWidget()
        self.editor_tabs.setTabsClosable(True)
        self.editor_tabs.tabCloseRequested.connect(self._close_tab)
        self._add_new_editor_tab("Untitled.m", default_text=(
            "% Vectra Script Demonstration\n"
            "clc;\nclear;\n\n"
            "t = 0:0.001:0.1;\n"
            "m = sin(2*pi*10*t);\n"
            "s = ammod(m, 100, 1000);\n\n"
            "figure;\n"
            "subplot(2,1,1);\n"
            "plot(t, m);\n"
            "title('Message Signal m(t)');\n"
            "grid on;\n\n"
            "subplot(2,1,2);\n"
            "plot(t, s);\n"
            "title('AM Modulated Signal s(t)');\n"
            "grid on;\n"
        ))
        dock_editor = QDockWidget("Script Editor", self)
        dock_editor.setWidget(self.editor_tabs)
        dock_editor.setObjectName("DockEditor")
        self.addDockWidget(Qt.LeftDockWidgetArea, dock_editor)
        self.splitDockWidget(dock_files, dock_editor, Qt.Horizontal)

        # 3. Right Top: Figure Window
        plot_container = QWidget()
        plot_layout = QVBoxLayout(plot_container)
        plot_layout.setContentsMargins(0, 0, 0, 0)
        self.plot_canvas = PlotCanvas(self)
        self.plot_toolbar = NavigationToolbar(self.plot_canvas, self)
        plot_layout.addWidget(self.plot_toolbar)
        plot_layout.addWidget(self.plot_canvas)
        PlotManager.get_instance().set_canvas(self.plot_canvas)

        dock_plot = QDockWidget("Figure Window", self)
        dock_plot.setWidget(plot_container)
        dock_plot.setObjectName("DockPlot")
        self.addDockWidget(Qt.RightDockWidgetArea, dock_plot)

        self._create_menus()

        # 4. Right Bottom: Workspace Inspector
        self.workspace_panel = WorkspacePanel(self.interpreter)
        dock_ws = QDockWidget("Workspace Inspector", self)
        dock_ws.setWidget(self.workspace_panel)
        dock_ws.setObjectName("DockWorkspace")
        self.addDockWidget(Qt.RightDockWidgetArea, dock_ws)
        self.splitDockWidget(dock_plot, dock_ws, Qt.Vertical)

        # 5. Bottom: Command Window (Full Width)
        self.cmd_window = CommandWindow(self.interpreter, on_command_executed_cb=self._on_state_change)
        dock_cmd = QDockWidget("Command Window", self)
        dock_cmd.setWidget(self.cmd_window)
        dock_cmd.setObjectName("DockCommandWindow")
        self.addDockWidget(Qt.BottomDockWidgetArea, dock_cmd)

        # Set dock sizes proportion
        self.resizeDocks([dock_files, dock_editor, dock_plot], [220, 600, 460], Qt.Horizontal)
        self.resizeDocks([dock_plot, dock_ws], [480, 240], Qt.Vertical)
        self.resizeDocks([dock_editor, dock_cmd], [520, 280], Qt.Vertical)

        # Toolbar
        toolbar = QToolBar("Main Controls")
        self.addToolBar(toolbar)

        run_act = QAction("▶ Run Script", self)
        run_act.triggered.connect(self._run_current_script)
        toolbar.addAction(run_act)

        new_act = QAction("📄 New Script", self)
        new_act.triggered.connect(lambda: self._add_new_editor_tab("Untitled.m"))
        toolbar.addAction(new_act)

        save_act = QAction("💾 Save", self)
        save_act.triggered.connect(self._save_file)
        toolbar.addAction(save_act)

        clear_act = QAction("🧹 Clear Workspace", self)
        clear_act.triggered.connect(self._clear_workspace)
        toolbar.addAction(clear_act)

        self.is_dark_mode = True
        self.theme_act = QAction("☀️ Light Theme", self)
        self.theme_act.triggered.connect(self._toggle_theme)
        toolbar.addAction(self.theme_act)

        self._apply_theme()
        self.statusBar().showMessage("Vectra Ready.")

    def _toggle_theme(self):
        self.is_dark_mode = not self.is_dark_mode
        self.theme_act.setText("☀️ Light Theme" if self.is_dark_mode else "🌙 Dark Theme")
        self._apply_theme()

    def _apply_theme(self):
        # Notify editor tabs of theme change
        for i in range(self.editor_tabs.count()):
            editor = self.editor_tabs.widget(i)
            if isinstance(editor, CodeEditor):
                editor.set_dark_mode(self.is_dark_mode)

        if self.is_dark_mode:
            # Modern Slate / Catppuccin Dark Theme
            self.setStyleSheet("""
                QMainWindow {
                    background-color: #11111b;
                    color: #cdd6f4;
                }
                QWidget {
                    font-family: 'Segoe UI', 'SF Pro Display', Arial, sans-serif;
                    font-size: 13px;
                    color: #cdd6f4;
                }
                QDockWidget {
                    titlebar-close-icon: url();
                    titlebar-normal-icon: url();
                    font-weight: 600;
                    border: 1px solid #1e1e2e;
                }
                QDockWidget::title {
                    background: #181825;
                    padding: 8px 12px;
                    border-bottom: 1px solid #313244;
                    color: #b4befe;
                    font-size: 12px;
                    letter-spacing: 0.5px;
                }
                QPlainTextEdit, QTextEdit {
                    background-color: #1e1e2e;
                    color: #cdd6f4;
                    border: none;
                    selection-background-color: #45475a;
                    selection-color: #cdd6f4;
                }
                QLineEdit {
                    background-color: #181825;
                    color: #cdd6f4;
                    border: 1px solid #313244;
                    border-radius: 6px;
                    padding: 6px 10px;
                    font-family: 'Consolas', 'Fira Code', monospace;
                }
                QLineEdit:focus {
                    border: 1px solid #89b4fa;
                }
                QTableWidget {
                    background-color: #181825;
                    color: #cdd6f4;
                    gridline-color: #313244;
                    border: none;
                    alternate-background-color: #1e1e2e;
                }
                QHeaderView::section {
                    background-color: #11111b;
                    color: #89b4fa;
                    font-weight: 600;
                    padding: 6px;
                    border: none;
                    border-bottom: 2px solid #313244;
                }
                QTreeView {
                    background-color: #181825;
                    color: #cdd6f4;
                    border: none;
                    padding: 4px;
                }
                QTreeView::item:hover {
                    background-color: #313244;
                    border-radius: 4px;
                }
                QTreeView::item:selected {
                    background-color: #45475a;
                    color: #89b4fa;
                    border-radius: 4px;
                }
                QToolBar {
                    background-color: #181825;
                    border-bottom: 1px solid #313244;
                    spacing: 6px;
                    padding: 4px 8px;
                }
                QToolButton {
                    background-color: #313244;
                    color: #cdd6f4;
                    border: 1px solid #45475a;
                    border-radius: 6px;
                    padding: 6px 14px;
                    font-weight: 600;
                    font-size: 12px;
                }
                QToolButton:hover {
                    background-color: #45475a;
                    border-color: #89b4fa;
                    color: #ffffff;
                }
                QToolButton:pressed {
                    background-color: #89b4fa;
                    color: #11111b;
                }
                QTabWidget::pane {
                    border: 1px solid #313244;
                    background: #1e1e2e;
                }
                QTabBar::tab {
                    background: #181825;
                    color: #a6adc8;
                    padding: 8px 16px;
                    border-top-left-radius: 6px;
                    border-top-right-radius: 6px;
                    margin-right: 2px;
                    border: 1px solid #313244;
                    border-bottom: none;
                }
                QTabBar::tab:selected {
                    background: #1e1e2e;
                    color: #89b4fa;
                    font-weight: bold;
                    border-top: 2px solid #89b4fa;
                }
                QTabBar::tab:hover:!selected {
                    background: #313244;
                    color: #cdd6f4;
                }
                QSplitter::handle {
                    background: #313244;
                    width: 3px;
                    height: 3px;
                }
                QStatusBar {
                    background: #11111b;
                    color: #a6adc8;
                    border-top: 1px solid #313244;
                }
                QScrollBar:vertical {
                    background: #181825;
                    width: 10px;
                    margin: 0px;
                }
                QScrollBar::handle:vertical {
                    background: #45475a;
                    min-height: 20px;
                    border-radius: 5px;
                }
                QScrollBar::handle:vertical:hover {
                    background: #585b70;
                }
                QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                    height: 0px;
                }
            """)
        else:
            # Modern Clean Light Theme
            self.setStyleSheet("""
                QMainWindow {
                    background-color: #f3f4f6;
                    color: #1f2937;
                }
                QWidget {
                    font-family: 'Segoe UI', 'SF Pro Display', Arial, sans-serif;
                    font-size: 13px;
                    color: #1f2937;
                }
                QDockWidget {
                    titlebar-close-icon: url();
                    titlebar-normal-icon: url();
                    font-weight: 600;
                    border: 1px solid #e5e7eb;
                }
                QDockWidget::title {
                    background: #ffffff;
                    padding: 8px 12px;
                    border-bottom: 1px solid #e5e7eb;
                    color: #2563eb;
                    font-size: 12px;
                    letter-spacing: 0.5px;
                }
                QPlainTextEdit, QTextEdit {
                    background-color: #ffffff;
                    color: #1f2937;
                    border: none;
                    selection-background-color: #dbeafe;
                    selection-color: #1e40af;
                }
                QLineEdit {
                    background-color: #ffffff;
                    color: #1f2937;
                    border: 1px solid #d1d5db;
                    border-radius: 6px;
                    padding: 6px 10px;
                    font-family: 'Consolas', 'Fira Code', monospace;
                }
                QLineEdit:focus {
                    border: 1px solid #2563eb;
                }
                QTableWidget {
                    background-color: #ffffff;
                    color: #1f2937;
                    gridline-color: #f3f4f6;
                    border: none;
                    alternate-background-color: #f9fafb;
                }
                QHeaderView::section {
                    background-color: #f3f4f6;
                    color: #2563eb;
                    font-weight: 600;
                    padding: 6px;
                    border: none;
                    border-bottom: 2px solid #e5e7eb;
                }
                QTreeView {
                    background-color: #ffffff;
                    color: #1f2937;
                    border: none;
                    padding: 4px;
                }
                QTreeView::item:hover {
                    background-color: #f3f4f6;
                    border-radius: 4px;
                }
                QTreeView::item:selected {
                    background-color: #dbeafe;
                    color: #1e40af;
                    border-radius: 4px;
                }
                QToolBar {
                    background-color: #ffffff;
                    border-bottom: 1px solid #e5e7eb;
                    spacing: 6px;
                    padding: 4px 8px;
                }
                QToolButton {
                    background-color: #f3f4f6;
                    color: #374151;
                    border: 1px solid #e5e7eb;
                    border-radius: 6px;
                    padding: 6px 14px;
                    font-weight: 600;
                    font-size: 12px;
                }
                QToolButton:hover {
                    background-color: #e5e7eb;
                    border-color: #2563eb;
                    color: #111827;
                }
                QToolButton:pressed {
                    background-color: #2563eb;
                    color: #ffffff;
                }
                QTabWidget::pane {
                    border: 1px solid #e5e7eb;
                    background: #ffffff;
                }
                QTabBar::tab {
                    background: #f3f4f6;
                    color: #6b7280;
                    padding: 8px 16px;
                    border-top-left-radius: 6px;
                    border-top-right-radius: 6px;
                    margin-right: 2px;
                    border: 1px solid #e5e7eb;
                    border-bottom: none;
                }
                QTabBar::tab:selected {
                    background: #ffffff;
                    color: #2563eb;
                    font-weight: bold;
                    border-top: 2px solid #2563eb;
                }
                QTabBar::tab:hover:!selected {
                    background: #e5e7eb;
                    color: #1f2937;
                }
                QSplitter::handle {
                    background: #e5e7eb;
                    width: 3px;
                    height: 3px;
                }
                QStatusBar {
                    background: #ffffff;
                    color: #6b7280;
                    border-top: 1px solid #e5e7eb;
                }
                QScrollBar:vertical {
                    background: #f3f4f6;
                    width: 10px;
                    margin: 0px;
                }
                QScrollBar::handle:vertical {
                    background: #d1d5db;
                    min-height: 20px;
                    border-radius: 5px;
                }
                QScrollBar::handle:vertical:hover {
                    background: #9ca3af;
                }
                QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                    height: 0px;
                }
            """)

    def _add_new_editor_tab(self, title: str, default_text: str = "") -> CodeEditor:
        editor = CodeEditor(is_dark=self.is_dark_mode)
        if default_text:
            editor.setPlainText(default_text)
        idx = self.editor_tabs.addTab(editor, title)
        self.editor_tabs.setCurrentIndex(idx)
        return editor

    def _close_tab(self, index: int):
        if self.editor_tabs.count() > 1:
            self.editor_tabs.removeTab(index)

    def _run_current_script(self):
        curr_editor = self.editor_tabs.currentWidget()
        if isinstance(curr_editor, CodeEditor):
            code = curr_editor.toPlainText()
            try:
                self.interpreter.eval_code(code)
            except Exception as e:
                QMessageBox.critical(self, "Execution Error", str(e))
            self._on_state_change()

    def _save_file(self):
        curr_editor = self.editor_tabs.currentWidget()
        if isinstance(curr_editor, CodeEditor):
            file_path, _ = QFileDialog.getSaveFileName(self, "Save Script", "", "MATLAB Files (*.m);;All Files (*)")
            if file_path:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(curr_editor.toPlainText())
                filename = os.path.basename(file_path)
                self.editor_tabs.setTabText(self.editor_tabs.currentIndex(), filename)

    def _on_file_double_clicked(self, index: QModelIndex):
        file_path = self.file_model.filePath(index)
        if os.path.isfile(file_path) and file_path.endswith('.m'):
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            self._add_new_editor_tab(os.path.basename(file_path), content)

    def _on_state_change(self):
        self.workspace_panel.refresh()
        self.statusBar().showMessage("Execution finished cleanly.")

    def _clear_workspace(self):
        self.interpreter.workspace.clear()
        self._on_state_change()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if hasattr(self, 'plot_canvas') and self.plot_canvas:
            try:
                self.plot_canvas.fig.tight_layout()
                self.plot_canvas.draw_idle()
            except Exception:
                pass
