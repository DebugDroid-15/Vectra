import sys
import os

# 1. Initialize logging & crash handling early to capture module load errors
try:
    from ..logger import setup_logging, install_crash_handler, get_logger
    install_crash_handler()
    logger = get_logger("gui.app")
    logger.info("Initializing Vectra GUI application...")
except Exception:
    pass

# 2. Fix Conda / Windows DLL loading conflict for PySide6
if sys.platform == "win32":
    try:
        import PySide6
        pyside_dir = os.path.dirname(PySide6.__file__)
        # Add PySide6 directory to top of DLL search paths
        if hasattr(os, "add_dll_directory"):
            os.add_dll_directory(pyside_dir)
            plugins_dir = os.path.join(pyside_dir, "plugins")
            if os.path.exists(plugins_dir):
                os.add_dll_directory(plugins_dir)
        # Prepend PySide6 directory to system PATH to override Anaconda's Library\bin DLLs
        os.environ["PATH"] = pyside_dir + os.pathsep + os.path.join(pyside_dir, "plugins", "platforms") + os.pathsep + os.environ.get("PATH", "")
    except Exception as e:
        if 'logger' in locals():
            logger.warning(f"Could not configure PySide6 DLL directory: {e}")

from PySide6.QtWidgets import QSplashScreen, QApplication, QLabel, QVBoxLayout, QWidget
from PySide6.QtGui import QPixmap, QIcon, QFont, QColor
from PySide6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, QObject
from .main_window import MainWindow

class FadeSplashScreen(QSplashScreen):
    def __init__(self, pixmap):
        super().__init__(pixmap, Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setWindowOpacity(1.0)

def main():
    install_crash_handler()
    logger = get_logger("gui.app")
    logger.info("Initializing Vectra GUI application...")

    app = QApplication(sys.argv)
    app.setApplicationName("Vectra")
    app.setStyle("Fusion")

    icon_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "Vectra.png"))
    
    # 1. Create Splash Screen with Vectra.png
    splash = None
    if os.path.exists(icon_path):
        pixmap = QPixmap(icon_path)
        # Scaled pixmap with padding
        scaled_pixmap = pixmap.scaled(300, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        
        # Container splash widget
        splash_widget = QWidget()
        splash_widget.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.SplashScreen)
        splash_widget.setAttribute(Qt.WA_TranslucentBackground)
        
        layout = QVBoxLayout(splash_widget)
        layout.setAlignment(Qt.AlignCenter)
        
        img_label = QLabel()
        img_label.setPixmap(scaled_pixmap)
        img_label.setAlignment(Qt.AlignCenter)
        
        title_label = QLabel("VECTRA")
        title_label.setFont(QFont("Segoe UI", 18, QFont.Bold))
        title_label.setStyleSheet("color: white; letter-spacing: 4px;")
        title_label.setAlignment(Qt.AlignCenter)
        
        sub_label = QLabel("Scientific Computing Environment")
        sub_label.setFont(QFont("Segoe UI", 10))
        sub_label.setStyleSheet("color: #bdc3c7;")
        sub_label.setAlignment(Qt.AlignCenter)
        
        # Dark splash card background
        splash_widget.setStyleSheet("""
            QWidget {
                background-color: #1e1e2e;
                border-radius: 16px;
                padding: 20px;
            }
        """)
        
        layout.addWidget(img_label)
        layout.addWidget(title_label)
        layout.addWidget(sub_label)
        splash_widget.adjustSize()
        
        # Center splash on screen
        screen = app.primaryScreen().geometry()
        splash_widget.move(
            (screen.width() - splash_widget.width()) // 2,
            (screen.height() - splash_widget.height()) // 2
        )
        splash_widget.setWindowOpacity(1.0)
        splash_widget.show()
        app.processEvents()
        
        splash = splash_widget

    window = MainWindow()
    if os.path.exists(icon_path):
        window.setWindowIcon(QIcon(icon_path))

    def finish_splash():
        if splash:
            # Fade out animation over 600ms
            anim = QPropertyAnimation(splash, b"windowOpacity")
            anim.setDuration(600)
            anim.setStartValue(1.0)
            anim.setEndValue(0.0)
            anim.setEasingCurve(QEasingCurve.OutCubic)
            
            def show_main():
                splash.close()
                window.show()
                
            anim.finished.connect(show_main)
            anim.start(QPropertyAnimation.DeleteWhenStopped)
            # Keep reference to avoid garbage collection during animation
            splash.anim = anim
        else:
            window.show()

    # Hold splash screen visible for 3 seconds (3000 ms) before fading out
    QTimer.singleShot(3000, finish_splash)
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
