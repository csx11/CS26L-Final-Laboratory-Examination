import sys
from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt
from database import *
from user_tab import UserTab
from vocab_tab import VocabularyTab

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CS26L Final Laboratory Examination")
        self.setFixedSize(1000, 700)
        
        init_db()
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Title
        title = QLabel("Language Learning Tracker")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: bold; margin: 20px;")
        layout.addWidget(title)
        
        # Setup username first
        self.setup_username_section(layout)
        
        # Tab widget
        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)
        
        # Create tabs
        self.user_tab = UserTab(self)
        self.vocab_tab = VocabularyTab(self)
        
        self.tabs.addTab(self.user_tab, "My Languages")
        self.tabs.addTab(self.vocab_tab, "Vocabulary")
        
        # Disable tabs until username is set
        self.tabs.setEnabled(False)
        
    def setup_username_section(self, layout):
        username_group = QGroupBox("Welcome! Please enter your name to get started")
        username_layout = QHBoxLayout(username_group)
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter your name")
        self.username_input.setMinimumWidth(200)
        username_layout.addWidget(self.username_input)
        
        start_btn = QPushButton("Start Learning!")
        start_btn.clicked.connect(self.start_app)
        username_layout.addWidget(start_btn)
        
        layout.addWidget(username_group)
        
        # Display current username if exists
        existing_username = get_username()
        if existing_username:
            self.username_input.setText(existing_username)
            self.start_app()  # Auto-start if username exists
    
    def start_app(self):
        username = self.username_input.text().strip()
        if not username:
            QMessageBox.warning(self, "Error", "Please enter your name to continue")
            return
        
        self.tabs.setEnabled(True)
        self.load_data()
    
    def load_data(self):
        self.user_tab.load_data()
        self.vocab_tab.load_data()