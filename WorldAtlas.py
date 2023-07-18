from kivymd.app import MDApp as App
from kivy.core.window import Window

from kivy.lang.builder import Builder

from kivymd.uix.boxlayout import BoxLayout
from kivymd.uix.list import OneLineListItem
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button.button import MDFlatButton
from kivymd.uix.textfield.textfield import MDTextField
from kivy.metrics import dp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.behaviors import TouchBehavior

from tkinter import filedialog
import tkinter as tk 

from ui_code.choice_vault import ChoiceVaultWindow
from ui_code.workspace import WorkspaceWindow
import database as dbl



class WAScreenManager(ScreenManager):
    pass


class WorldAtlasApp(App):
    def build(self):
        wasm = WAScreenManager()
        wasm.add_widget(ChoiceVaultWindow())
        wasm.add_widget(WorkspaceWindow())
        wasm.current = 'choice_vault'
        Window.size = (1200, 600)
        return wasm

if __name__ == '__main__':
    WorldAtlasApp().run()