from random import sample, choices
import sqlite3

# SQL queries section
create_table_card = """CREATE TABLE IF NOT EXISTS card (
               id INTEGER PRIMARY KEY AUTOINCREMENT, 
               number TEXT, 
               pin TEXT, 
               balance INTEGER DEFAULT 0)"""

insert_card = "INSERT INTO card (number, pin) VALUES(?, ?)"
select_number = "SELECT number FROM card WHERE number = ?"
select_pin = "SELECT pin FROM card WHERE number = ?"
select_balance = "SELECT balance FROM card WHERE number = ?"
add_income = "UPDATE card SET Balance = Balance + ? WHERE number = ?"
outcome_balance = "UPDATE card SET Balance = Balance - ? WHERE number = ?"
close_account = "DELETE FROM card WHERE number = ?"
# SQL DB section
conn = sqlite3.connect('card.s3db')
cur = conn.cursor()
cur.execute("DROP TABLE IF EXISTS card")
conn.commit()
cur.execute(create_table_card)
conn.commit()

transfer_card_check_return: list[str] = ['You can\'t transfer money to the same account!',
                                         'Probably you made a mistake in the card number. Please try again!',
                                         'Such a card does not exist.']


class BankingSystem:
    def __init__(self):
        self.cards = {}

    def menu(self):
        while True:
            print("1. Create an account\n2. Log into account\n0. Exit")
            choice = input()
            if choice == '1':
                self.create_account()
            elif choice == '2':
                self.login()
            elif choice == '0':
                print('Bye!')
                exit()
            else:
                print('Unknown option.')

    @staticmethod
    def luhn(iin, acc_id):
        card_num = [int(x) for x in list(iin + acc_id)]
        for i in range(0, len(card_num), 2):
            card_num[i] = card_num[i] * 2
        card_num = [x - 9 if x > 9 else x for x in card_num]
        if sum(card_num) % 10 == 0:
            card_num.append(0)
            return str(0)
        else:
            return str(10 - sum(card_num) % 10)

    @staticmethod
    def luhn_check(number):
        card_num = [int(x) for x in list(number)]
        checksum = card_num[-1]
        card_num = card_num[:-1]
        for i in range(0, len(card_num), 2):
            card_num[i] = card_num[i] * 2
        card_num = [x - 9 if x > 9 else x for x in card_num]
        if (sum(card_num) + checksum) % 10 == 0:
            return True
        else:
            return False

    @staticmethod
    def generate_numbers(self):
        while True:
            random_pin = ''.join([str(n) for n in sample(range(9), 4)])
            iin = '400000'
            acc_id = ''.join([str(n) for n in choices(range(9), k=9)])
            checksum = self.luhn(iin, acc_id)
            random_card = iin + acc_id + checksum
            yield random_card, random_pin

    def create_account(self):
        card, pin = next(self.generate_numbers(self))
        self.insert_card(card, pin)
        print('\nYour card has been created')
        print(f'Your card number:\n{card}')
        print(f'Your card PIN:\n{pin}\n')

    def login(self):
        card = input('Enter your card number:\n')
        pin = input('Enter your PIN:\n')
        entered_login = self.select_number(card)
        if entered_login != 0:
            entered_pin = self.select_pin(entered_login)
            if entered_pin == pin:
                print('You have successfully logged in!\n')
                self.account(card)
            else:
                print('Wrong card number or PIN\n')
        else:
            print('Wrong card number or PIN\n')

    def account(self, card):
        while True:
            print('1. Balance\n2. Add income\n3. Do transfer\n4. Close account\n5. Log Out\n0. Exit')
            choice = input()
            if choice == '1':
                print(f"\nBalance: {self.select_balance(card)}\n")
            elif choice == '2':
                print('Enter income:\n')
                income = int(input())
                self.add_income(card, income)
                print('Income was added!\n')
            elif choice == '3':
                print('Transfer\nEnter card number:\n')
                card_to_transfer = input()
                if self.transfer_card_check(self, card_to_transfer, card) != 3:
                    print(transfer_card_check_return[self.transfer_card_check(self, card_to_transfer, card)])
                else:
                    print('Enter how much money you want to transfer:\n')
                    money = int(input())
                    if money > self.select_balance(card):
                        print('Not enough money!\n')
                    else:
                        self.outcome(card, money)
                        self.add_income(card_to_transfer, money)
                        print('Success!\n')

            elif choice == '4':
                self.delete_account(card)
                print('The account has been closed!\n')
                return
            elif choice == '5':
                print('You have successfully logged out!\n')
                return
            elif choice == '0':
                print('Bye!')
                exit()
            else:
                print('Unknown option.\n')

    @staticmethod
    def insert_card(card, pin):
        cur.execute(insert_card, (card, pin))
        conn.commit()

    @staticmethod
    def select_number(number):
        cur.execute(select_number, (number,))
        conn.commit()
        try:
            return cur.fetchone()[0]
        except TypeError:
            return 0

    @staticmethod
    def select_pin(number):
        cur.execute(select_pin, (number,))
        conn.commit()
        return cur.fetchone()[0]

    @staticmethod
    def select_balance(number):
        cur.execute(select_balance, (number,))
        conn.commit()
        return cur.fetchone()[0]

    @staticmethod
    def add_income(number, income):
        cur.execute(add_income, (income, number))
        conn.commit()

    @staticmethod
    def outcome(number, outcome):
        cur.execute(outcome_balance, (outcome, number))
        conn.commit()

    @staticmethod
    def delete_account(number):
        cur.execute(close_account, (number,))
        conn.commit()

    @staticmethod
    def transfer_card_check(self, card_to_transfer, account):
        if card_to_transfer == account:
            return 0
        elif not self.luhn_check(card_to_transfer):
            return 1
        elif self.select_number(card_to_transfer) == 0:
            return 2
        else:
            return 3


BankingSystem().menu()
