import database as dbl

from kivy.lang.builder import Builder
from kivymd.uix.boxlayout import BoxLayout
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.list import OneLineListItem
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button.button import MDFlatButton
from kivy.metrics import dp
from kivy.uix.screenmanager import Screen
from kivymd.uix.tab.tab import MDTabsBase
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.icon_definitions import md_icons
from kivymd.font_definitions import fonts
from widgets import MDTextFieldFuncIcon
import utils
from tkinter import filedialog
import tkinter as tk



Builder.load_file('./ui/workspace.kv')
Builder.load_file('./ui/work_with_tables.kv')

class Tab(BoxLayout, MDTabsBase):
    pass


class CreateTableTab(MDScrollView, MDTabsBase):
    def __init__(self, **kwargs):
        super(CreateTableTab, self).__init__(**kwargs)
        #self.do_scroll_x = True
        #self.do_scroll_y = False
        self.cols = 3
        self.rows = 2

    def _add_new_field(self, **kwargs):
        self.ids.field_container.add_widget(FieldsContainer())


class FieldsContainer(MDGridLayout):
    def __init__(self, **kwargs):
        super(FieldsContainer, self).__init__(**kwargs)
        self.height = self.minimum_height

    def get_data(self):
        return True



class SettingsTab(MDScrollView, MDTabsBase):
    def __init__(self, *args, **kwargs):
        super(SettingsTab, self).__init__(*args, **kwargs)
        self.custom_parent = None
        self._build_menus()
        self._render_delete_table()
        self._render_import_template()

    def _build_menus(self):
        self.table_to_delete_menu = MDDropdownMenu(caller= self.ids.delete_tablename, position="center",width_mult=4)
        self.table_to_delete_menu.bind()

        self.import_template_menu = MDDropdownMenu(caller= self.ids.delete_tablename, position="center",width_mult=4)
        self.import_template_menu.bind()
    
    def _render_delete_table(self):
        pass
    
    def _render_import_template(self):
        self.import_template_menu.items = [{'viewclass':'OneLineListItem', 'text': name, 'on_release': lambda n=name: self._import_set_item(n)} for name in utils.get_import_templates()]

    def _import_set_item(self, item_name: str) -> None:
        self.ids.import_tables.text = item_name
        self.import_template_menu.dismiss()

    def _choice_table_to_delete(self):
        print(2)
    
    def _open_create_table_tab(self, **kwargs):
        self.custom_parent._open_create_table_tab()


class AssistantTab(MDScrollView, MDTabsBase):
    def __init__(self, *args, **kwargs):
        super(AssistantTab, self).__init__(*args, **kwargs)


class WorkspaceWindow(Screen):
    def __init__(self, *args, **kwargs):
        super(WorkspaceWindow, self).__init__(*args, **kwargs)
        self.ids.nav_bar.set_state('open')
    
    def _open_settings_tab(self, **kwargs) -> None:
        widget = SettingsTab(title=utils.build_reftitle('Настройки'))
        widget.custom_parent = self
        self.ids.tabs.add_widget(widget)
    
    def _open_assistant_tab(self, **kwargs) -> None:
        self.ids.tabs.add_widget(AssistantTab(title=utils.build_reftitle('Ассистент')))
    
    def _open_create_table_tab(self, **kwargs) -> None:
        self.ids.tabs.add_widget(CreateTableTab(title=utils.build_reftitle('Создание таблицы')))

    def _exit(self, **kwargs) -> None:
        self.manager.current = 'choice_vault'
    
    def on_ref_press(self,
                     instance_tabs,
                     instance_tab_label,
                     instance_tab,
                     instance_tab_bar,
                     instance_carousel):
        for instance_tab in instance_carousel.slides:
            if instance_tab.title == instance_tab_label.text:
                instance_tabs.remove_widget(instance_tab_label)
                break