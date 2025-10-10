from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt
from database import *

class UserTab(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Add language section
        add_group = QGroupBox("Add New Language")
        add_layout = QHBoxLayout(add_group)
        
        self.language_input = QLineEdit()
        self.language_input.setPlaceholderText("Language to learn (e.g., Spanish, French, Japanese)")
        add_layout.addWidget(self.language_input)
        
        add_btn = QPushButton("Add Language")
        add_btn.clicked.connect(self.add_language)
        add_layout.addWidget(add_btn)
        
        layout.addWidget(add_group)
        
        # Languages table
        self.user_table = QTableWidget()
        self.user_table.setColumnCount(9)
        self.user_table.setHorizontalHeaderLabels([
            "ID", "Language", "Level", "Words Learned", 
            "Speaking", "Writing", "Reading", "Listening", "Actions"
        ])
        self.user_table.setColumnHidden(0, True)
        layout.addWidget(self.user_table)
        
        # Table controls
        control_layout = QHBoxLayout()
        
        save_btn = QPushButton("Save All Changes")
        save_btn.clicked.connect(self.save_languages)
        control_layout.addWidget(save_btn)
        
        control_layout.addStretch()
        layout.addLayout(control_layout)
    
    def load_data(self):
        self.user_table.setRowCount(0)
        users = get_all_users()
        
        for user in users:
            row = self.user_table.rowCount()
            self.user_table.insertRow(row)
            
            # ID (hidden)
            id_item = QTableWidgetItem(str(user[0]))
            id_item.setFlags(id_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.user_table.setItem(row, 0, id_item)
            
            # Language
            self.user_table.setItem(row, 1, QTableWidgetItem(user[2]))
            
            # Level dropdown
            level_combo = QComboBox()
            level_combo.addItems(["Beginner", "Intermediate", "Advanced"])
            level_combo.setCurrentText(user[3])
            self.user_table.setCellWidget(row, 2, level_combo)
            
            # Words learned - UNEDITABLE and language-specific
            language = user[2]
            word_count = get_vocabulary_count_by_language(language)
            words_item = QTableWidgetItem(str(word_count))
            words_item.setFlags(words_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.user_table.setItem(row, 3, words_item)
            
            # Skills checkboxes
            for i, skill in enumerate([user[5], user[6], user[7], user[8]]):
                item = QTableWidgetItem()
                item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
                item.setCheckState(Qt.CheckState.Checked if skill == 1 else Qt.CheckState.Unchecked)
                self.user_table.setItem(row, 4 + i, item)
            
            # Delete button
            delete_btn = QPushButton("Delete")
            delete_btn.clicked.connect(lambda checked, row=row: self.delete_language(row))
            self.user_table.setCellWidget(row, 8, delete_btn)
    
    def add_language(self):
        username = get_username()
        language = self.language_input.text().strip()
        
        if not language:
            QMessageBox.warning(self, "Error", "Please enter a language")
            return
        
        add_user(username, language)
        self.language_input.clear()
        self.load_data()
        self.main_window.vocab_tab.update_category_combo()
        QMessageBox.information(self, "Success", f"Added {language} to your languages!")
    
    def delete_language(self, row):
        user_id = int(self.user_table.item(row, 0).text())
        language = self.user_table.item(row, 1).text()
        
        reply = QMessageBox.question(
            self, "Confirm Delete", 
            f"Remove {language} from your languages?"
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            delete_user(user_id)
            self.load_data()
            self.main_window.vocab_tab.update_category_combo()
    
    def save_languages(self):
        for row in range(self.user_table.rowCount()):
            user_id = int(self.user_table.item(row, 0).text())
            language = self.user_table.item(row, 1).text()
            level_widget = self.user_table.cellWidget(row, 2)
            level = level_widget.currentText()
            
            # Get the current word count for this specific language
            word_count = get_vocabulary_count_by_language(language)
            
            # Get skill checkboxes
            speaking = 1 if self.user_table.item(row, 4).checkState() == Qt.CheckState.Checked else 0
            writing = 1 if self.user_table.item(row, 5).checkState() == Qt.CheckState.Checked else 0
            reading = 1 if self.user_table.item(row, 6).checkState() == Qt.CheckState.Checked else 0
            listening = 1 if self.user_table.item(row, 7).checkState() == Qt.CheckState.Checked else 0
            
            update_user(user_id, language, level, word_count, speaking, writing, reading, listening)
        
        # Refresh the table to show updated word counts
        self.load_data()
        QMessageBox.information(self, "Saved", "All changes saved!")