import database as dbl
import utils

from kivy.lang.builder import Builder
from kivymd.uix.boxlayout import BoxLayout
from kivymd.uix.list import OneLineListItem
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button.button import MDFlatButton
from kivy.metrics import dp
from kivy.uix.screenmanager import Screen

from widgets import MDTextFieldFuncIcon

from tkinter import filedialog
import tkinter as tk

Builder.load_file('./ui/choice_vault.kv')


class ChoiceVaultWindow(Screen):
    def __init__(self, *args, **kwargs):
        super(ChoiceVaultWindow, self).__init__(**kwargs)
        self.dialog = None
        self.current_element = ('', '')
        self.render_vaults_listview()
    
    def render_vaults_listview(self):
        self.ids.listview.clear_widgets()
        vaults = dbl.get_db_names('both')
        for dbname, udbname in vaults.items():
            list_item = OneLineListItem(id = f'list_item_{dbname}',
                                                    text=udbname, 
                                                    on_press = lambda x, db = dbname, udb = udbname: self._choice_list_element(db, udb))
            self.ids.listview.add_widget(list_item)
        self.current_element = ('', '')
        self._disable_buttons()
    
    def create_new_db(self):
        if self.dialog:
            return
        self.dialog = MDDialog(
            title = 'Создать новое хранилище',
            type = 'custom',
            content_cls = CreateNewDialogContent(),
            on_dismiss = self._clear_dialog,
            buttons = [
                MDFlatButton(text='Создать', on_release= self._create_new_db_dialog_agree),
                MDFlatButton(text='Отмена', on_release= self._dismiss_dialog)
            ]
        )
        self.dialog.open()
    
    def _create_new_db_dialog_agree(self, *args, **kwargs) -> None:
        dbname = self.dialog.content_cls.ids.createdb_dbname.text
        udbname = self.dialog.content_cls.ids.createdb_udbname.text
        dbl.create_db(dbname, udbname)
        self.render_vaults_listview()
        self._dismiss_dialog()

    def delete_db(self):
        if self.current_element == ('', ''):
            return
        dbl.delete_db(self.current_element[0])
        self.render_vaults_listview()
    
    def rename_db(self):
        if self.dialog or self.current_element == ('', ''):
            return
        self.dialog = MDDialog(
            title = 'Переименовать хранилище',
            type = 'custom',
            content_cls = RenameDBDialogContent(),
            on_dissmiss = self._clear_dialog,
            buttons = [
                MDFlatButton(text='Переименовать', on_release = self._rename_dialog_agree),
                MDFlatButton(text='Отмена', on_release = self._dismiss_dialog)
            ]
        )
        self.dialog.content_cls.ids.renamedb_dbname.text = self.current_element[0]
        self.dialog.content_cls.ids.renamedb_udbname.text = self.current_element[1]
        self.dialog.open()
    
    def _rename_dialog_agree(self, *args, **kwargs) -> None:
        dbname = self.dialog.content_cls.ids.renamedb_dbname.text
        udbname = self.dialog.content_cls.ids.renamedb_udbname.text
        if udbname != self.current_element[1]:
            dbl.rename_db(self.current_element[0], udbname, 'udbname')
        if dbname != self.current_element[0]:
            dbl.rename_db(self.current_element[0], dbname, 'dbname')
        self.render_vaults_listview()
        self._dismiss_dialog()

    def duplicate_db(self):
        if self.current_element == ('', ''):
            return
        dbl.duplicate_db(self.current_element[0])
        self.render_vaults_listview()

    def export_db(self):
        if self.dialog or self.current_element == ('', ''):
            return
        self.dialog = MDDialog(
            title = 'Экспорт базы данных',
            type = 'custom',
            content_cls = ExportDBDialogContent(),
            on_dismiss = self._clear_dialog,
            buttons = [
                MDFlatButton(text='Экспортировать', on_release = self._export_dialog_agree),
                MDFlatButton(text='Отмена', on_release = self._dismiss_dialog)
            ]
        )
        self.dialog.content_cls.ids.export_udbname_label.text = f'Экспорт "{self.current_element[1]}"'
        self.dialog.content_cls.ids.choice_path.bind(on_icon_press = self._get_user_path)
        self.dialog.open()
 
    def _export_dialog_agree(self, *args, **kwargs) -> None:
        path = self.dialog.content_cls.ids.choice_path.text
        filename = self.dialog.content_cls.ids.filename.text
        dbl.export_db(self.current_element[0], path, filename)
        self._dismiss_dialog()

    def import_db(self):
        if self.dialog:
            return
        self.dialog = MDDialog(
            title = 'Импорт хранилища',
            type = 'custom',
            content_cls = ImportDBDialogContent(),
            on_dismiss = self._clear_dialog,
            buttons = [
                MDFlatButton(text='Экспортировать', on_release = self._import_dialog_agree),
                MDFlatButton(text='Отмена', on_release = self._dismiss_dialog)
            ]
        )
        self.dialog.content_cls.ids.choice_path.bind(on_icon_press = self._get_user_file)
        self.dialog.open()

    def _import_dialog_agree(self, *args, **kwargs) -> None:
        path = self.dialog.content_cls.ids.choice_path.text
        dbl.import_db(path)
        self.render_vaults_listview()
        self._dismiss_dialog()

    def _get_user_path(self, *args) -> None:
        root = tk.Tk()
        root.withdraw()
        self.dialog.content_cls.ids.choice_path.text = filedialog.askdirectory()
        del root

    def _get_user_file(self, *args) -> None:
        root = tk.Tk()
        root.withdraw()
        self.dialog.content_cls.ids.choice_path.text = filedialog.askopenfilename()
        del root

    def _validate(self, instance, text) -> None:
        if not utils.filename_validator(text):
            instance.error = True
    def _choice_list_element(self, dbname: str, udbname: str) -> None:
        for listitem in self.ids.listview.children:
            if f'list_item_{self.current_element[0]}' == listitem.id:
                listitem.bg_color = (0, 0, 0, 0)
            if f'list_item_{dbname}' == listitem.id:
                listitem.bg_color = 'gainsboro'
        self.current_element = (dbname, udbname)
        self._enable_buttons()
    
    def work_with_db(self) -> None:
        if self.current_element == ('', ''):
            return
        self.manager.current = 'workspace'
    
    def _dismiss_dialog(self, *args, **kwargs) -> None:
        self.dialog.dismiss()
        self._clear_dialog()
    
    def _clear_dialog(self, *args, **kwargs) -> None:
        self.dialog = None

    def _enable_buttons(self) -> None:
        self.ids.rename_button.disabled = False
        self.ids.duplicate_button.disabled = False
        self.ids.export_button.disabled = False
        self.ids.edit_button.disabled = False
        self.ids.delete_button.disabled = False

    def _disable_buttons(self) -> None:
        self.ids.rename_button.disabled = True
        self.ids.duplicate_button.disabled = True
        self.ids.export_button.disabled = True
        self.ids.edit_button.disabled = True
        self.ids.delete_button.disabled = True


class CreateNewDialogContent(BoxLayout):
    pass


class RenameDBDialogContent(BoxLayout):
    pass


class ImportDBDialogContent(BoxLayout):
    pass


class ExportDBDialogContent(BoxLayout):
    pass