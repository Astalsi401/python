class Category:
    def __init__(self, name):
        self.ledger = []
        self.name = name

    def __str__(self):
        res = self.name.center(30, '*') + '\n'
        for a in self.ledger:
            res += '%-23s' % (a['description'][0:23]) + '%7s' % (format(a['amount'], '.2f')) + '\n'
        res += 'Total: %.2f' % (self.get_balance())
        return res

    def get_balance(self):
        total = 0
        for a in self.ledger:
            total += a['amount']
        return total

    def check_funds(self, amount):
        return self.get_balance() >= amount

    def get_spent(self):
        spent = 0
        for a in self.ledger:
            if a['amount'] < 0:
                spent += float(abs(a['amount']))
        return spent

    def deposit(self, amount, description=''):
        self.ledger.append({"amount": amount, "description": description})

    def withdraw(self, amount, description=''):
        if self.check_funds(amount):
            self.ledger.append({"amount": -amount, "description": description})
            return True
        else:
            return False

    def transfer(self, amount, category):
        if self.check_funds(amount):
            self.ledger.append({'amount': -amount, 'description': f'Transfer to {category.name}'})
            category.ledger.append({'amount': amount, 'description': f'Transfer from {self.name}'})
            return True
        else:
            return False


def create_spend_chart(categories):
    if len(categories) > 4:
        return 'Max Categories 4'
    res = 'Percentage spent by category\n'
    for p in range(100, -10, -10):
        res += '%3d|' % (p)
        spent = [c.get_spent() for c in categories]
        spent = [round(s / sum(spent) * 100) for s in spent]
        for s in spent:
            if s >= p:
                res += ' o '
            else:
                res += '   '
        res += ' \n'
    res += ' ' * 4 + '-' * 3 * len(categories) + '-\n'
    xtitle = [len(c.name) for c in categories]
    for r in range(0, max(xtitle)):
        res += ' ' * 4
        for i in range(0, len(categories)):
            try:
                res += ' %s ' % categories[i].name[r]
            except:
                res += '   '
        if r != max(xtitle) - 1:
            res += ' \n'
        else:
            res += ' '
    return res


food = Category("Food")
entertainment = Category("Entertainment")
business = Category("Business")
food.deposit(900, "deposit")
food.deposit(45.56)
food.deposit(900, "deposit")
food.withdraw(45.67, "milk, cereal, eggs, bacon, bread")
food.deposit(900, "deposit")
good_withdraw = food.withdraw(45.67)
food.deposit(900, "deposit")
food.withdraw(45.67, "milk, cereal, eggs, bacon, bread")
food.deposit(900, "deposit")
food.withdraw(45.67, "milk, cereal, eggs, bacon, bread")
transfer_amount = 20
food_balance_before = food.get_balance()
entertainment_balance_before = entertainment.get_balance()
good_transfer = food.transfer(transfer_amount, entertainment)
food_balance_after = food.get_balance()
entertainment_balance_after = entertainment.get_balance()
food.deposit(10, "deposit")
food.deposit(100, "deposit")
good_withdraw = food.withdraw(100.10)
food.deposit(100, "deposit")
good_transfer = food.transfer(200, entertainment)
food.deposit(900, "deposit")
food.withdraw(45.67, "milk, cereal, eggs, bacon, bread")
food.transfer(20, entertainment)
food.deposit(900, "deposit")
entertainment.deposit(900, "deposit")
business.deposit(900, "deposit")
food.withdraw(105.55)
entertainment.withdraw(33.40)
business.withdraw(10.99)

print(create_spend_chart([business, food, entertainment]))
print(create_spend_chart([business, food, entertainment]))
