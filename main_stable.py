import sys
import os
import json
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QToolBar, QAction,
    QLineEdit, QPushButton, QWidget, QVBoxLayout, QLabel, QComboBox
)
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl

class SettingsWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("💖 Settings 💖")
        self.setGeometry(300, 300, 300, 150)
        self.layout = QVBoxLayout()

        self.label = QLabel("Select Default Search Engine:")
        self.combo = QComboBox()
        self.combo.addItem("Google", "https://www.google.com/search?q=")
        self.combo.addItem("DuckDuckGo", "https://duckduckgo.com/?q=")
        self.combo.addItem("Vyntr", "https://vyntr.com/search?q=")
        self.combo.addItem("Bing", "https://www.bing.com/search?q=")

        self.load_settings()

        save_btn = QPushButton("💾 Save")
        save_btn.clicked.connect(self.save_settings)

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.combo)
        self.layout.addWidget(save_btn)
        self.setLayout(self.layout)

    def load_settings(self):
        try:
            with open("settings.json", "r") as f:
                data = json.load(f)
                url = data.get("default_search_engine", "")
                idx = self.combo.findData(url)
                if idx != -1:
                    self.combo.setCurrentIndex(idx)
        except FileNotFoundError:
            pass

    def save_settings(self):
        with open("settings.json", "w") as f:
            json.dump({
                "default_search_engine": self.combo.currentData()
            }, f)
        self.close()

class FemboyBrowser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("💖 Femboy Browser - Stable 💖")
        self.setGeometry(100, 100, 1000, 700)

        self.settings = self.load_settings()
        self.default_engine = self.settings.get("default_search_engine", "https://www.google.com/search?q=")

        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.setCentralWidget(self.tabs)

        self.init_toolbar()
        self.setStyleSheet(self.femboy_theme())

        start_page = os.path.abspath("start_page.html")
        self.add_tab(QUrl.fromLocalFile(start_page))

    def init_toolbar(self):
        navtb = QToolBar("Navigation")
        navtb.setMovable(False)
        self.addToolBar(navtb)

        back_btn = QAction("◀", self)
        back_btn.triggered.connect(lambda: self.current_web().back())
        navtb.addAction(back_btn)

        forward_btn = QAction("▶", self)
        forward_btn.triggered.connect(lambda: self.current_web().forward())
        navtb.addAction(forward_btn)

        reload_btn = QAction("⟳", self)
        reload_btn.triggered.connect(lambda: self.current_web().reload())
        navtb.addAction(reload_btn)

        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        navtb.addWidget(self.url_bar)

        go_btn = QPushButton("✨ Go ✨")
        go_btn.clicked.connect(self.navigate_to_url)
        navtb.addWidget(go_btn)

        new_tab_btn = QPushButton("➕ Tab")
        new_tab_btn.clicked.connect(lambda: self.add_tab(QUrl("https://www.google.com")))
        navtb.addWidget(new_tab_btn)

        settings_btn = QPushButton("⚙️ Settings")
        settings_btn.clicked.connect(self.open_settings)
        navtb.addWidget(settings_btn)

    def current_web(self):
        return self.tabs.currentWidget()

    def add_tab(self, url):
        browser = QWebEngineView()
        browser.setUrl(url)
        i = self.tabs.addTab(browser, "🌐 New Tab")
        self.tabs.setCurrentIndex(i)
        browser.urlChanged.connect(lambda u: self.url_bar.setText(u.toString()))

    def close_tab(self, i):
        if self.tabs.count() > 1:
            self.tabs.removeTab(i)

    def navigate_to_url(self):
        text = self.url_bar.text()
        if not text.startswith("http"):
            text = self.default_engine + text
        self.current_web().setUrl(QUrl(text))

    def load_settings(self):
        try:
            with open("settings.json", "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {"default_search_engine": "https://www.google.com/search?q="}

    def open_settings(self):
        self.settings_window = SettingsWindow()
        self.settings_window.show()

    def femboy_theme(self):
        return """
        QMainWindow {
            background-color: #fff0f8;
        }
        QToolBar {
            background: #ffe6f7;
            border-bottom: 2px solid #e0b0ff;
        }
        QTabWidget::pane {
            background: #fff;
            border: 2px solid #ffb6c1;
        }
        QTabBar::tab {
            background: #ffc9ec;
            border-radius: 10px;
            padding: 10px 30px;
            min-width: 150px;
            font-family: 'Comic Sans MS';
            font-size: 14px;
        }
        QTabBar::tab:selected {
            background: #ff94d7;
            font-weight: bold;
        }
        QLineEdit, QPushButton {
            background-color: #ffe0f7;
            border: 1px solid #ffb6c1;
            border-radius: 10px;
            padding: 5px 10px;
            font-family: 'Comic Sans MS';
            font-size: 14px;
        }
        QPushButton:hover {
            background-color: #ffccf9;
        }
        """
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FemboyBrowser()
    window.show()
    sys.exit(app.exec_())
