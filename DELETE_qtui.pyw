import sys
import database as dbl
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QMainWindow, QApplication, QDialog
from PyQt6 import uic



class ChoiceVaultWindow(QMainWindow):
    def __init__(self):
        super(ChoiceVaultWindow, self).__init__()
        uic.load_ui.loadUi('./ui/ChoiceVault.ui', self)
        self.show()

        self.create_button.clicked.connect(self._on_press_create_button)
        self.rename_button.clicked.connect(self._on_press_raname_button)
        self.duplicate_button.clicked.connect(self._on_press_duplicate_button)
        self.delete_button.clicked.connect(self._on_press_delete_button)

        self.render_vaults_listwidget()

    def render_vaults_listwidget(self):
        self.list_of_vaults.clear()
        vaults = dbl.get_database_dbnames()
        self.list_of_vaults.addItems(vaults)

    def _on_press_create_button(self):
        self._create_new_db_window = CreateNewDatabase()
        self._create_new_db_window.accepted_signal.connect(self.render_vaults_listwidget)
        self._create_new_db_window.show()
    
    def _on_press_raname_button(self):
        self._rename_db_window = RenameDatabase()
        self._rename_db_window.lineedit_old_dbname.setText(self.list_of_vaults.currentItem().text())
        self._rename_db_window.accepted_signal.connect(self.render_vaults_listwidget)
        self._rename_db_window.show()

    def _on_press_duplicate_button(self):
        dbl.duplicate_db(dbl.dbname_to_filename(self.list_of_vaults.currentItem().text()))
        self.render_vaults_listwidget()
    
    def _on_press_delete_button(self):
        dbname: str = self.list_of_vaults.currentItem().text()
        dbl.delete_db(dbl.dbname_to_filename(dbname))
        self.render_vaults_listwidget()
        

class CreateNewDatabase(QDialog):
    accepted_signal = pyqtSignal()
    def __init__(self):
        super(CreateNewDatabase, self).__init__()
        uic.load_ui.loadUi('./ui/create_new_database.ui', self)
        self.accepted.connect(self._on_accepted)
    
    def _on_accepted(self):
        if self.lineedit_filename.text() != '':
            if self.lineedit_databasename.text() != '':
                dbl.create_db(self.lineedit_filename.text(), self.lineedit_databasename.text())
            else:
                dbl.create_db(self.lineedit_filename.text(), None)
        else:
            self.close()
            return
        
        self.accepted_signal.emit()
        self.close()


class RenameDatabase(QDialog):
    accepted_signal = pyqtSignal()
    def __init__(self):
        super(RenameDatabase, self).__init__()
        uic.load_ui.loadUi('./ui/rename_database.ui', self)
        self.accepted.connect(self._on_accepted)
    
    def _on_accepted(self):
        db_filename = dbl.dbname_to_filename(self.lineedit_old_dbname.text())
        new_dbname = self.lineedit_new_dbname.text()
        dbl.rename_dbname(db_filename, new_dbname)

        self.accepted_signal.emit()
        self.close()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    choice_vault_window = ChoiceVaultWindow()
    app.exec()