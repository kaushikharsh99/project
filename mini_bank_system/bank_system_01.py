import datetime

class BankAccount:
    def __init__(self, account_holder, account_number, initial_balance=0):
        self.account_holder = account_holder
        self.account_number = account_number
        self._balance = initial_balance        
        self._transactions = []                
        self._record_transaction("Account Created", initial_balance)

    

    def deposit(self, ammount):
        if ammount > 0:
            self._balance += ammount
            self._record_transaction("Deposit", ammount)
            print(f" Deposited: ₹{ammount:.2f}")
        else:
            print(" Deposit ammount must be positive.")

    def withdraw(self, ammount):
        if ammount <= 0:
            print(" Withdrawal ammount must be positive.")
        elif ammount > self._balance:
            print(" Insufficient funds.")
        else:
            self._balance -= ammount
            self._record_transaction("Withdraw", -ammount)
            print(f" Withdrew: ₹{ammount:.2f}")

    def get_balance(self):
        return self._balance

    def account_info(self):
        return f" Account Holder: {self.account_holder} |  Account No: {self.account_number} | Balance: ₹{self._balance:.2f}"

    

    def _record_transaction(self, transaction_type, ammount):
        """Store transaction with timestamp"""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self._transactions.append((timestamp, transaction_type, ammount, self._balance))

    def show_transactions(self):
        print(f"\n Transaction History for {self.account_holder}:")
        if not self._transactions:
            print("No transactions found.")
        else:
            for t in self._transactions:
                time, t_type, ammount, bal = t
                print(f"[{time}] {t_type:12}  ₹{ammount:8.2f}  →  Balance: ₹{bal:.2f}")
        print("-" * 60)

# Manage multiple accounts in one place

class BankSystem:
    def __init__(self):
        self.accounts = {}

    def create_account(self):
        name = input("Enter account holder name: ")
        number = input("Enter account number: ")
        if number in self.accounts:
            print(" Account number already exists!")
            return
        initial = float(input("Enter initial deposit (₹): "))
        self.accounts[number] = BankAccount(name, number, initial)
        print(" Account created successfully!\n")

    def get_account(self):
        number = input("Enter account number: ")
        acc = self.accounts.get(number)
        if acc:
            return acc
        else:
            print(" Account not found.")
            return None

    def main_menu(self):
        while True:
            print("\n =====  Demo Bank  =====")
            print("1  Create Account")
            print("2 Deposit Money")
            print("3  Withdraw Money")
            print("4  Check Balance")
            print("5  Show Transaction History")
            print("6  Show Account Info")
            print("7  Exit")

            choice = input("Select option (1-7): ")

            if choice == "1":
                self.create_account()

            elif choice == "2":
                acc = self.get_account()
                if acc:
                    amt = float(input("Enter ammount to deposit: "))
                    acc.deposit(amt)

            elif choice == "3":
                acc = self.get_account()
                if acc:
                    amt = float(input("Enter ammount to withdraw: "))
                    acc.withdraw(amt)

            elif choice == "4":
                acc = self.get_account()
                if acc:
                    print(f" Current Balance: ₹{acc.get_balance():.2f}")

            elif choice == "5":
                acc = self.get_account()
                if acc:
                    acc.show_transactions()

            elif choice == "6":
                acc = self.get_account()
                if acc:
                    print(acc.account_info())

            elif choice == "7":
                print(" Thank you for using Python Bank. Goodbye!")
                break

            else:
                print(" Invalid choice. Please try again.")


if __name__ == "__main__":
    bank = BankSystem()
    bank.main_menu()
