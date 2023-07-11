def filename_validator(string: str) -> bool:
    alphabet = list('qwertyuiopasdfghjklzxcvbnm_')
    for letter in string:
        if string not in alphabet:
            return False
    return True