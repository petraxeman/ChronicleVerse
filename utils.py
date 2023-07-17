from kivymd.icon_definitions import md_icons
from kivymd.font_definitions import fonts
#from kivymd.uix.label import MDLabel
from kivy.core.text import Label as CoreLabel


def filename_validator(string: str) -> bool:
    alphabet = list('qwertyuiopasdfghjklzxcvbnm_')
    for letter in string:
        if string not in alphabet:
            return False
    return True


def build_reftitle(title: str) -> str:
    return f'[ref="assistant"][font={fonts[-1]["fn_regular"]}]{md_icons["close"]}[/font][/ref] {title}'


def fontsize_in_pixels(fontsize: int, text: str = 'A') -> int:
    return CoreLabel(font_size=fontsize).get_extents(text)