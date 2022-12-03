class Bank:
    def __init__(self):
        self.bank_data = {}

    def create_account(self, card_num, pin_num, account, dollar):
        self.bank_data[card_num] = {'pin_num': pin_num, 'accounts': {account: dollar}}

    def add_account(self, card_num, account, dollar):
        if self.bank_data.get(card_num):
            self.bank_data[card_num]['accounts'][account] = dollar

    def check_pin_num(self, card_num, pin_num):
        if self.bank_data.get(card_num) and self.bank_data[card_num]['pin_num'] == pin_num:
            return self.bank_data[card_num]['accounts']
        else:
            return None

    def update_account(self, card_num, account, dollar):
        if self.bank_data[card_num]['accounts'].get(account):
            self.bank_data[card_num]['accounts'][account] = dollar


class Controller:
    def __init__(self, bank, dollar):
        self.bank = bank
        self.accounts = None
        self.balance = dollar

    def swipe(self, card_num, pin_num):
        self.accounts = self.bank.check_pin_num(card_num, pin_num)
        if self.accounts:
            return True, 'Welcome!'
        else:
            return False, 'Invalid card_num or Incorrect pin_num!'

    def account_select(self, account):
        return True if self.accounts.get(account) else False

    def account_actions(self, card_num, account, action, dollar=0):
        if action == 'Check The Balance':
            return self.accounts[account], 1
        elif action == 'Withdraw':
            if self.accounts[account] >= dollar and self.balance >= dollar:
                self.accounts[account] -= dollar
                self.bank.update_account(card_num, account, self.accounts[account])
                return self.accounts[account], 1
            else:
                return self.accounts[account], 0
        elif action == 'Deposit':
            self.accounts[account] += dollar
            self.bank.update_account(card_num, account, self.accounts[account])
            return self.accounts[account], 1
        else:
            return self.accounts[account], 2

    # Test function
    def __call__(self, card_num, pin_num, account, action_list):
        leave = False
        while not leave:
            v, m = self.swipe(card_num, pin_num)
            if not v:
                return m
            check = self.account_select(account)
            if not check:
                return 'Invalid Account!'
            for action in action_list:
                if action[0] == 'Leave':
                    return 'Thank you for using'
                balance, bit = self.account_actions(card_num, account, action[0], action[1])
                if bit == 2:
                    return 'Invalid action'
                if not bit:
                    print('Out of balance or out of money in the ATM')
            return 'Actions completed'


if __name__ == '__main__':
    empty_bank = Bank()
    # Test Empty Bank
    empty_atm = Controller(empty_bank, 0)
    _, message = empty_atm.swipe(0, 0)
    print('Test Invalid Message on Empty ATM Result -- {0}'.format(message))

    # Test Bank With Accounts
    test_bank = Bank()
    test_bank.create_account(123456789, 1234, 'kb', 1000)
    test_bank.add_account(123456789, 'shinhan', 1000)
    test_bank.create_account(987654321, 7321, 'kb', 5000)
    test_atm = Controller(test_bank, 10000)
    test_action_list = [('Check The Balance', 0), ('Withdraw', 40), ('Withdraw', 1000), ('Deposit', 100)]

    result = test_atm(987654321, 7321, 'kb', test_action_list)
    print('Test Success on Valid ATM Result - {0}'.format(result))

    # Tests whether ATM handles overdraft attempt without crashing
    result = test_atm(123456789, 1234, 'kb', test_action_list)
    print('Test Overdraft Result - {0}'.format(result))

    # Test incorrect Pin number
    result = test_atm(987654321, 1234, 'kb', test_action_list)
    print('Test Incorrect PIN Number Result - {0}'.format(result))

    # Test incorrect Account number
    result = test_atm(876504321, 1234, 'kb', test_action_list)
    print('Test Incorrect Acc Number Result - {0}'.format(result))

    test_bank2 = Bank()
    test_bank2.create_account(123456789, 1234, 'kb', 1000)
    test_bank2.add_account(123456789, 'shinhan', 30000)
    test_bank2.create_account(987654321, 7321, 'kb', 5000)
    test_atm2 = Controller(test_bank2, 10000)
    balance_over_action_list = [('Check The Balance', 0), ('Withdraw', 30000)]

    # Test excess dollar requests in the ATM
    result = test_atm2(123456789, 1234, 'shinhan', balance_over_action_list)
    print('Test dollar excess handling Result - {0}'.format(result))

    exit_action_list = [('Check The Balance', 0), ('Leave', 0)]
    result = test_atm2(123456789, 1234, 'shinhan', exit_action_list)
    print('Test exiting Result - {0}'.format(result))
