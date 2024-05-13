from collections import UserDict
import re


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        if not self.validate_phone(value):
            raise ValueError("Невірний формат номеру телефону. Номер повинен містити 10 цифр.")
        super().__init__(value)

    @staticmethod
    def validate_phone(value):
        return re.fullmatch(r"\d{10}", value)


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone, new_phone):
        for phone in self.phones:
            if phone.value == old_phone:
                phone.value = new_phone
                return True
        return False

    def find_phone(self, phone):
        for phone_record in self.phones:
            if phone_record.value == phone:
                return phone
        return False

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find_record(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]
            return True
        return False


def main():
    book = AddressBook()
    print("Welcome to your address book!")

    while True:
        user_input = input("Enter command (add, find, find_phone, delete, exit): ")
        if len(user_input) > 0 and user_input != '':
            if user_input.lower() == 'exit':
                break
            command, *args = user_input.split()
            try:
                if command.lower() == 'add':
                    name = input("Enter the contact name: ")
                    phone = input("Enter the phone number: ")
                    record = Record(name)
                    record.add_phone(phone)
                    book.add_record(record)
                    print("Contact added successfully.")

                elif command.lower() == 'find':
                    name = input("Enter the contact name to find: ")
                    record = book.find_record(name)
                    if record:
                        print(record)
                    else:
                        print("Contact not found.")

                elif command.lower() == 'delete':
                    name = input("Enter the contact name to delete: ")
                    if book.delete(name):
                        print("Contact deleted successfully.")
                    else:
                        print("Contact not found.")

                elif command.lower() == 'find_phone':
                    phone = input("Enter the phone number to find: ")
                    result = book.find_phone(phone)
                    print(result)

            except ValueError as e:
                print(e)
                continue
        else:
            print("Enter the command from the list")


def main_test():
    # Створення нової адресної книги
    book = AddressBook()

    # Створення запису для John
    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")

    # Додавання запису John до адресної книги
    book.add_record(john_record)

    # Створення та додавання нового запису для Jane
    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)

    # Виведення всіх записів у книзі
    for name, record in book.data.items():
        print(record)

    # Знаходження та редагування телефону для John
    john = book.find_record("John")
    john.edit_phone("1234567890", "1112223333")

    print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

    # Пошук конкретного телефону у записі John
    found_phone = john.find_phone("5555555555")
    print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

    # Видалення запису Jane
    book.delete("Jane")


if __name__ == '__main__':
    main()
	# main_test()