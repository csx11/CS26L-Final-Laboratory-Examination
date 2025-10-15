import sys
from PyQt6.QtWidgets import *
from database import *
from PyQt6.QtCore import Qt
from user_tab import UserTab
from vocab_tab import VocabularyTab

class MainWindow(QMainWindow):
    """
    Main application window for the Language Learning Progress Tracker.
    It initializes the database, sets up the interface layout, and manages navigation tabs.
    """
    def __init__(self):
        super().__init__()
        # Window 
        self.setWindowTitle("CS26L Final Laboratory Examination")
        self.setFixedSize(873, 700)
        
        # Initialize database
        init_db()
        
        #widget & main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        title = QLabel("Language Learning Progress Tracker")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("""
            background-color: #1abc9c;
            color: white;
            font-size: 26px;
            font-weight: bold;
            padding: 20px;
            border-radius: 10px;
        """)
        layout.addWidget(title)


        # Username input section (top)
        self.setup_username_section(layout)
        
        # Tabs for User and Vocabulary sections
        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)
        
        # Create and attach custom tab widgets
        self.user_tab = UserTab(self)
        self.vocab_tab = VocabularyTab(self)
        
        # Add tabs to the interface
        self.tabs.addTab(self.user_tab, "My Languages")
        self.tabs.addTab(self.vocab_tab, "Vocabulary")

        # Tabs are disabled until username is provided
        self.tabs.setEnabled(False)
        
    def setup_username_section(self, layout):
        """
        Creates a section at the top where the user can enter their name.
        If a username already exists in the database, it auto-fills and proceeds.
        """
        username_group = QGroupBox("Please enter your name to get started")
        username_layout = QHBoxLayout(username_group)
        
        # Input field for username
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter your name")
        self.username_input.setMinimumWidth(200)
        username_layout.addWidget(self.username_input)
        
        # Start button to confirm username
        start_btn = QPushButton("Start")
        start_btn.clicked.connect(self.start_app)
        username_layout.addWidget(start_btn)
        
        # Add the group box to the main layout
        layout.addWidget(username_group)
        
        # Auto-load username if previously saved in database
        existing_username = get_username()
        if existing_username:
            self.username_input.setText(existing_username)
            self.start_app()  # Auto-start app if username exists
    
    def start_app(self):
        """
        Triggered when the Start button is pressed or username is detected.
        Enables the tabs and loads user data.
        """
        username = self.username_input.text().strip()
        if not username:
            QMessageBox.warning(self, "Error", "Please enter your name to continue")
            return
        
        # Enable the main tabs after username is set
        self.tabs.setEnabled(True)
        self.load_data()
    
    def load_data(self):
        """
        Loads data for both User and Vocabulary tabs.
        """
        self.user_tab.load_data()
        self.vocab_tab.load_data()
