from kivymd.app import MDApp as App
from kivy.core.window import Window

from kivy.uix.screenmanager import ScreenManager

from uic.storages import StoragesWindow
from uic.workspace import WorkspaceWindow
import cvlib.database as dbl
import cvlib.utils as utils



class CVScreenManager(ScreenManager):
    pass


class ChronicleVerseApp(App):
    def build(self):
        self.title = 'ChronicleVerse Foal [0.0.7.002]'
        cvsm = CVScreenManager()
        cvsm.add_widget(StoragesWindow())
        cvsm.add_widget(WorkspaceWindow())
        cvsm.current = 'storages'
        Window.size = (1200, 675)
        return cvsm

if __name__ == '__main__':
    utils.check_folders()
    ChronicleVerseApp().run()