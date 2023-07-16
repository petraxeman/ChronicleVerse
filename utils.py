from kivymd.icon_definitions import md_icons
from kivymd.font_definitions import fonts



def filename_validator(string: str) -> bool:
    alphabet = list('qwertyuiopasdfghjklzxcvbnm_')
    for letter in string:
        if string not in alphabet:
            return False
    return True


def build_reftitle(title: str) -> str:
    return f'[ref="assistant"][font={fonts[-1]["fn_regular"]}]{md_icons["close"]}[/font][/ref] {title}'