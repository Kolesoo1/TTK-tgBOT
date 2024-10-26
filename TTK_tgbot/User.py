class User:
    number = '000000000'
    count = 1

    def __init__(self, phone_number, address):
        self.__phone_number = phone_number
        self.__address = address
        self.__reg_number = User.number[:-(User.count % 10) - 1] + str(User.count)
        User.count += 1

    def get_phone_number(self):
        return self.__phone_number

    def get_address(self):
        return self.__address

    def get_reg_number(self):
        return self.__reg_number