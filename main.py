#input: curr. age, curr. net worth, salary, salary hikes annually, sign on bonus, yearly bonus
# input contd: company issued stocks, percentage to save, prop of saving to 401K+stocks, prop of saving to bank

class NetWorthEstimator:
    def __init__(self, pre_tax, raise_percentage, yearly_bonus, company_equity, to_save, curr_age, fin_age, house, house_start_age):
        self.pre_tax_income = pre_tax
        self.post_tax_income = 0
        self.salary_raise_percent = raise_percentage
        self.yearly_bonus = yearly_bonus # percent
        self.company_equity = company_equity # RSUs: set to 45k usually
        self.percent_to_save = to_save # percent
        self.save_to_stocks = 30
        self.save_to_bank = self.percent_to_save - self.save_to_stocks
        self.start = curr_age
        self.end = fin_age
        self.bank_account = 50000
        self.stock_account = 10000
        self.property_worth = house # val for example, 300,000
        self.first_property_date = house_start_age


    def calculate_seattle_taxes(self):
        # Federal income tax rates for 2021 (Single Filing Status)
        tax_brackets = {
            9950: 0.10,
            40525: 0.12,
            86375: 0.22,
            164925: 0.24,
            209425: 0.32,
            523600: 0.35,
            float('inf'): 0.37
        }

        tax_owed = 0
        remaining_income = self.pre_tax_income

        # Calculate tax for each bracket
        for bracket, rate in tax_brackets.items():
            if remaining_income <= 0:
                break

            taxable_amount = min(remaining_income, bracket)
            tax_owed += taxable_amount * rate
            remaining_income -= taxable_amount
            self.post_tax_income = self.pre_tax_income - tax_owed

        return tax_owed

    def setPreTax(self, num):
        self.pre_tax_income = num
        return

    def getPostTax(self):
        self.calculate_seattle_taxes()
        return self.post_tax_income

    def calc_pre_tax_till_end(self):
        lst = [self.pre_tax_income]
        x = self.pre_tax_income
        for i in range(self.start + 1, self.end + 1):
            if i >= 26:
                x = x + self.company_equity
            x = x * (1 + (self.salary_raise_percent / 100))
            lst.append(x)
        return lst

    def calc_post_tax_till_end(self):
        pre_tax_incomes = self.calc_pre_tax_till_end()
        post_tax_incomes = []

        for income in pre_tax_incomes:
            self.setPreTax(income)  # Update the pre-tax income
            post_tax_income = self.getPostTax()  # Calculate the post-tax income
            post_tax_incomes.append(post_tax_income)

        return post_tax_incomes

    def all_accounts(self):
        try:
            b = self.property_value()
            a = self.calc_post_tax_till_end()
            for i in a:
                self.bank_account = self.bank_account + (i * (self.save_to_bank / 100))
                self.stock_account = self.stock_account + (i * (self.save_to_stocks / 100))

            self.stock_account = self.stock_account * (1.05) ** (self.end - self.start)
            self.stock_account += b
            return f'Net Worth is: {self.bank_account + self.stock_account}'

        except Exception as e:
            return f'An error occurred: {str(e)}'

    def property_value(self):
        property_tax = 0.05*self.property_worth
        fin_prop_val = self.property_worth *(1.1)**(self.end-self.first_property_date)
        fin_prop_val-=(property_tax(self.end-self.first_property_date))
        return self.property_worth





income = NetWorthEstimator(125000, 3, 12, 40000, 40, 22, 50, 100000, 24)
print(income.calc_pre_tax_till_end())
print(income.calc_post_tax_till_end())
print(income.all_accounts())
