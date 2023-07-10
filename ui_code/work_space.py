import database as dbl

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

Builder.load_file('./ui/work_space.kv')

class WorkspaceWindow(Screen):
    def __init__(self, *args, **kwargs):
        super(WorkspaceWindow, self).__init__(*args, **kwargs)
        self.ids.nav_bar.set_state('open')