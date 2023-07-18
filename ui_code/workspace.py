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
from kivymd.icon_definitions import md_icons
from kivymd.font_definitions import fonts
from widgets import MDTextFieldFuncIcon
import utils
from tkinter import filedialog
import tkinter as tk



Builder.load_file('./ui/workspace.kv')

class Tab(BoxLayout, MDTabsBase):
    pass

class SettingsTab(MDScrollView, MDTabsBase):
    def __init__(self, *args, **kwargs):
        super(SettingsTab, self).__init__(*args, **kwargs)
        self._build_menus()

    def _build_menus(self):
        self.export_templates_menu = MDDropdownMenu()
        
    
    def _choice_table_to_delete(self):
        print(2)

class AssistantTab(MDScrollView, MDTabsBase):
    def __init__(self, *args, **kwargs):
        super(AssistantTab, self).__init__(*args, **kwargs)


class WorkspaceWindow(Screen):
    def __init__(self, *args, **kwargs):
        super(WorkspaceWindow, self).__init__(*args, **kwargs)
        self.ids.nav_bar.set_state('open')
    
    def _open_settings_tab(self, **kwargs) -> None:
        self.ids.tabs.add_widget(SettingsTab(title=utils.build_reftitle('Настройки')))
    
    def _open_assistant_tab(self, **kwargs) -> None:
        self.ids.tabs.add_widget(AssistantTab(title=utils.build_reftitle('Ассистент')))
    
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