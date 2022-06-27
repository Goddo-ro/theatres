def checkPassword(password):
    russian_letters = {"й": 1, "ц": 2, "у": 3, "к": 4, "е": 5, "н": 6, "г": 7,
                       "ш": 8, "щ": 9, "з": 10, "х": 11, "ъ": 12, "ф": 13,
                       "ы": 14, "в": 15, "а": 16, "п": 17, "р": 18, "о": 19,
                       "л": 20, "д": 21, "ж": 22, "э": 23, "я": 24, "ч": 25,
                       "с": 26, "м": 27, "и": 28, "т": 29, "ь": 30, "б": 31, "ю": 32,
                       "ё": 12124}
    english_letters = {"q": 1, "w": 2, "e": 3, "r": 4, "t": 5, "y": 6,
                       "u": 7, "i": 8, "o": 9, "p": 10, "a": 11, "s": 12,
                       "d": 13, "f": 14, "g": 15, "h": 16, "j": 17,
                       "k": 18, "l": 19, "z": 20, "x": 21, "c": 22, "v": 23,
                       "b": 24, "n": 25, "m": 26}
    ru_lower = "йцукенгшщзхъфывапролджэячсмитьбю"
    ru_upper = ru_lower.upper()
    en_lower = "qwertyuiopasdfghjklzxcvbnm"
    en_upper = en_lower.upper()

    def number_in_password(password):
        for i in range(10):
            if str(i) in password:
                return True
        return False

    def letter_in_password(password):
        upper_flag = 0
        lower_flag = 0
        for symbol in password:
            if symbol in ru_lower or symbol in en_lower:
                lower_flag = 1
            if symbol in ru_upper or symbol in en_upper:
                upper_flag = 1
        if upper_flag and lower_flag:
            return True
        return False

    def three_consecutive_russian_letters(password):
        password = password.lower()
        for i in range(10):
            password.replace(str(i), '')
        for i in range(2, len(password)):
            if password[i - 2] not in russian_letters or \
                    password[i - 1] not in russian_letters or \
                    password[i] not in russian_letters or \
                    password[i - 2] == 'ъ' and password[i - 1] == 'ф' or \
                    password[i - 1] == 'ъ' and password[i] == 'ф' or \
                    password[i - 2] == 'э' and password[i - 1] == 'я' or \
                    password[i - 1] == 'э' and password[i] == 'я':
                continue
            if russian_letters[password[i - 1]] - russian_letters[password[i - 2]] == 1 and \
                    russian_letters[password[i]] - russian_letters[password[i - 1]] == 1 or \
                    password[i - 2] == 'ж' and password[i - 1] == 'э' and password[i] == 'ё':
                return True
        return False

    def three_consecutive_english_letters(password):
        password = password.lower()
        for i in range(10):
            password.replace(str(i), '')
        for i in range(2, len(password)):
            if password[i - 2] not in english_letters or \
                    password[i - 1] not in english_letters or \
                    password[i] not in english_letters or \
                    password[i - 2] == 'p' and password[i - 1] == 'a' or \
                    password[i - 1] == 'p' and password[i] == 'a' or \
                    password[i - 2] == 'l' and password[i - 1] == 'z' or \
                    password[i - 1] == 'l' and password[i] == 'z':
                continue
            if english_letters[password[i - 1]] - english_letters[password[i - 2]] == 1 and \
                    english_letters[password[i]] - english_letters[password[i - 1]] == 1:
                return True
        return False

    def password_check(password):
        errors = []
        try:
            assert len(password) > 8
        except AssertionError:
            errors.append("Length")
        try:
            assert letter_in_password(password)
        except AssertionError:
            errors.append("No letter")
        try:
            assert number_in_password(password)
        except AssertionError:
            errors.append("No number")
        try:
            if three_consecutive_russian_letters(password) or \
                    three_consecutive_english_letters(password):
                raise Exception()
        except Exception:
            errors.append("Letters")
        return errors

    return password_check(password)
