class PhoneErrors(Exception):
    pass


class BracketError(PhoneErrors):
    pass


class DashErrors(PhoneErrors):
    pass


def checkPhoneNumber(phone):
    operators = [(910, 919), (980, 989), (920, 939), (902, 906), (960, 969)]
    phone = ''.join(phone.split())
    def check(s):
        counter = 0
        for i in range(1, len(s)):
            if s[i] == '(':
                counter += 1
            elif s[i] == ')':
                counter -= 1
            if counter < 0:
                raise BracketError()
        if counter != 0:
            raise BracketError()
        return counter == 0


    def check_dash(s):
        if s[0] == '-' or s[-1] == '-' or '--' in s:
            raise DashErrors()
        return True


    def check_phone_number(phone_number):
        try:
            check(phone_number)
        except BracketError:
            return "Incorrect format"
        try:
            check_dash(phone_number)
        except DashErrors:
            return "Incorrect format"
        phone_number = ''.join(phone_number.split('('))
        phone_number = ''.join(phone_number.split(')'))
        phone_number = ''.join(phone_number.split('-'))
        if len(phone_number) < 10:
            return "Invalid number of digits"
        if phone_number[0] == '+' and \
                (phone_number[1] == '1' or
                 phone_number[1:4] == "359" or
                 phone_number[1:3] == "55"):
            return phone_number
        if phone_number[0] != '+' and phone_number[0] != '8':
            return "Incorrect format"
        elif phone_number[0] == '+' and phone_number[1] != '7':
            return "Unknown mobile operator"
        if phone_number[0] == '8':
            phone_number = "+7" + phone_number[1:]
        if not phone_number[1:].isalnum():
            return "Incorrect format"
        if len(phone_number) != 12:
            return "Invalid number of digits"
        operator = 0
        for first, second in operators:
            if first <= int(phone_number[2:5]) <= second:
                operator = 1
                break
        if not operator:
            return "Unknown mobile operator"
        return phone_number


    return check_phone_number(phone)
