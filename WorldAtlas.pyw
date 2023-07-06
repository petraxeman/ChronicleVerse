import sys
from PyQt6.QtWidgets import QMainWindow, QApplication, QListWidgetItem, QListWidget
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

        self.add_vaults_to_listwidget()

    def add_vaults_to_listwidget(self):
        with open('vaults', 'r', encoding='utf8') as file:
            vaults = [vaultname.strip() for vaultname in file.readlines()]
            self.list_of_vaults.addItems(vaults)

    def _on_press_create_button(self):
        pass
    
    def _on_press_raname_button(self):
        pass

    def _on_press_duplicate_button(self):
        pass
    
    def _on_press_delete_button(self):
        pass



if __name__ == '__main__':
    app = QApplication(sys.argv)
    choice_vault_window = ChoiceVaultWindow()
    app.exec()