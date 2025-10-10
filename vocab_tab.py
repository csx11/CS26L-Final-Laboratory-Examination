from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt
from database import *

class VocabularyTab(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Add vocabulary section
        add_group = QGroupBox("Add New Word")
        add_layout = QHBoxLayout(add_group)
        
        self.word_input = QLineEdit()
        self.word_input.setPlaceholderText("Word")
        self.word_input.setMinimumWidth(150)
        add_layout.addWidget(self.word_input)
        
        self.definition_input = QLineEdit()
        self.definition_input.setPlaceholderText("Definition")
        self.definition_input.setMinimumWidth(250)
        add_layout.addWidget(self.definition_input)
        
        self.category_combo = QComboBox()
        self.category_combo.setPlaceholderText("Language Category")
        self.category_combo.setMinimumWidth(150)
        add_layout.addWidget(self.category_combo)
        
        add_vocab_btn = QPushButton("Add Word")
        add_vocab_btn.clicked.connect(self.add_vocabulary)
        add_layout.addWidget(add_vocab_btn)
        
        layout.addWidget(add_group)
        
        # Vocabulary table
        self.vocab_table = QTableWidget()
        self.vocab_table.setColumnCount(4)
        self.vocab_table.setHorizontalHeaderLabels(["ID", "Word", "Definition", "Category"])
        self.vocab_table.setColumnHidden(0, True)
        self.vocab_table.itemSelectionChanged.connect(self.on_vocab_selected)
        layout.addWidget(self.vocab_table)
        
        # Vocabulary controls
        vocab_control_layout = QHBoxLayout()
        
        update_vocab_btn = QPushButton("Update Selected Word")
        update_vocab_btn.clicked.connect(self.update_vocabulary)
        vocab_control_layout.addWidget(update_vocab_btn)
        
        delete_vocab_btn = QPushButton("Delete Selected Word")
        delete_vocab_btn.clicked.connect(self.delete_vocabulary)
        vocab_control_layout.addWidget(delete_vocab_btn)
        
        clear_btn = QPushButton("Clear Form")
        clear_btn.clicked.connect(self.clear_vocab_form)
        vocab_control_layout.addWidget(clear_btn)
        
        vocab_control_layout.addStretch()
        layout.addLayout(vocab_control_layout)
    
    def load_data(self):
        self.load_vocabulary()
        self.update_category_combo()
    
    def load_vocabulary(self):
        self.vocab_table.setRowCount(0)
        vocab_items = get_all_vocabulary()
        
        for vocab in vocab_items:
            row = self.vocab_table.rowCount()
            self.vocab_table.insertRow(row)
            
            # ID (hidden)
            id_item = QTableWidgetItem(str(vocab[0]))
            id_item.setFlags(id_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.vocab_table.setItem(row, 0, id_item)
            
            # Word, Definition, Category
            self.vocab_table.setItem(row, 1, QTableWidgetItem(vocab[1]))
            self.vocab_table.setItem(row, 2, QTableWidgetItem(vocab[2] or ""))
            self.vocab_table.setItem(row, 3, QTableWidgetItem(vocab[3] or ""))
    
    def update_category_combo(self):
        self.category_combo.clear()
        self.category_combo.addItem("")
        languages = get_user_languages()
        for lang in languages:
            self.category_combo.addItem(lang)
    
    def add_vocabulary(self):
        word = self.word_input.text().strip()
        definition = self.definition_input.text().strip()
        category = self.category_combo.currentText()
        
        if not word:
            QMessageBox.warning(self, "Error", "Please enter a word")
            return
        
        add_vocabulary(word, definition, category)
        self.clear_vocab_form()
        self.load_vocabulary()
        self.main_window.user_tab.save_languages()  # Update word counts
    
    def on_vocab_selected(self):
        current_row = self.vocab_table.currentRow()
        if current_row >= 0:
            self.word_input.setText(self.vocab_table.item(current_row, 1).text())
            self.definition_input.setText(self.vocab_table.item(current_row, 2).text())
            
            category = self.vocab_table.item(current_row, 3).text()
            index = self.category_combo.findText(category)
            if index >= 0:
                self.category_combo.setCurrentIndex(index)
    
    def update_vocabulary(self):
        current_row = self.vocab_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Error", "Please select a word to update")
            return
        
        vocab_id = int(self.vocab_table.item(current_row, 0).text())
        word = self.word_input.text().strip()
        definition = self.definition_input.text().strip()
        category = self.category_combo.currentText()
        
        if not word:
            QMessageBox.warning(self, "Error", "Word cannot be empty")
            return
        
        update_vocabulary(vocab_id, word, definition, category)
        self.load_vocabulary()
        self.main_window.user_tab.save_languages()  # Update word counts
        QMessageBox.information(self, "Updated", f"Updated: {word}")
    
    def delete_vocabulary(self):
        current_row = self.vocab_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Error", "Please select a word to delete")
            return
        
        vocab_id = int(self.vocab_table.item(current_row, 0).text())
        word = self.vocab_table.item(current_row, 1).text()
        
        reply = QMessageBox.question(
            self, "Confirm Delete", 
            f"Delete the word '{word}'?"
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            delete_vocabulary(vocab_id)
            self.clear_vocab_form()
            self.load_vocabulary()
            self.main_window.user_tab.save_languages()  # Update word counts
    
    def clear_vocab_form(self):
        self.word_input.clear()
        self.definition_input.clear()
        self.category_combo.setCurrentIndex(0)
        self.vocab_table.clearSelection()