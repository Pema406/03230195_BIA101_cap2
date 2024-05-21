class TaxCalculator:
    def __init__(self):
        self.name = input("Enter your name: ")
        self.org_type = input("Enter the type of organization you work for (Government/Private/Corporate): ").lower()
        self.employee_type = input("Enter your employment type (Regular/Contract): ").lower()
        self.age = int(input("Enter your age: "))
        self.marital_status = input("Enter your marital status (Single/Married): ").lower()
        self.num_children = int(input("Enter the number of children (0 if none): "))
        self.children_in_school = int(input("Enter the number of children going to school (0 if none): "))

        self.income = self.get_income_details()
        self.deductions = self.get_deduction_details()
        self.calculate_tax()

    def get_income_details(self):
        income = {}
        salary_income = float(input("Enter your annual salary income (0 if none): "))
        income["salary"] = salary_income
        rental_income = float(input("Enter your annual rental income (0 if none): "))
        income["rental"] = rental_income
        dividend_income = float(input("Enter your annual dividend income (0 if none): "))
        income["dividend"] = dividend_income
        other_income = float(input("Enter your annual income from other sources (0 if none): "))
        income["other"] = other_income

        if income["dividend"] > 0:
            income["dividend_loan_interest"] = float(input("Enter the interest paid on loans for shareholding: "))

        total_income = sum(income.values())
        income["bonus"] = 0.1 * total_income  # 10% bonus in every organization

        if self.org_type == "government" and self.employee_type == "contract":
            income["pf_contribution"] = 0
        elif self.org_type == "government" and self.employee_type == "regular":
            income["pf_contribution"] = 0.05 * income["salary"]  # 5% PF for government regular employees
        else:
            income["pf_contribution"] = 0.1 * income["salary"]  # 10% PF for other organizations

        return income

    def get_deduction_details(self):
        deductions = {}
        deductions["gis_contribution"] = float(input("Enter your annual Group Insurance Scheme (GIS) contribution: "))
        deductions["life_insurance_premium"] = float(input("Enter your annual life insurance premium: "))
        deductions["self_education_allowance"] = float(input("Enter your self-education allowance (up to Nu. 350,000): "))
        deductions["donations"] = float(input("Enter your donations (up to 5% of total adjusted gross income): "))
        deductions["sponsored_children_education"] = float(input("Enter your sponsored children education expense (up to Nu. 350,000 per child): "))
        return deductions

    def calculate_tax(self):
        taxable_income = self.income["bonus"] + sum(self.income.values()) - self.income["pf_contribution"] - self.deductions["gis_contribution"]

        education_allowance = min(350000 * self.children_in_school, taxable_income)
        taxable_income -= education_allowance

        taxable_income -= min(self.deductions["self_education_allowance"], 350000)
        taxable_income -= min(self.deductions["donations"], 0.05 * taxable_income)
        taxable_income -= min(self.deductions["sponsored_children_education"], 350000 * self.num_children)
        taxable_income -= self.deductions["life_insurance_premium"]

        if "rental" in self.income:
            rental_deduction = 0.2 * self.income["rental"]
            taxable_income -= rental_deduction

        if "dividend" in self.income:
            dividend_deduction = max(self.income["dividend"] - 30000 - self.income["dividend_loan_interest"], 0)
            taxable_income -= dividend_deduction

        if "other" in self.income:
            other_deduction = 0.3 * self.income["other"]
            taxable_income -= other_deduction

        tax_rates = [
            (0, 300000, 0),
            (300001, 400000, 0.1),
            (400001, 650000, 0.15),
            (650001, 1000000, 0.2),
            (1000001, 1500000, 0.25),
            (1500001, float('inf'), 0.3)
        ]

        tax_payable = 0
        remaining_income = taxable_income

        for min_income, max_income, rate in tax_rates:
            if remaining_income <= 0:
                break
            if remaining_income > max_income - min_income:
                tax_payable += (max_income - min_income) * rate
                remaining_income -= (max_income - min_income)
            else:
                tax_payable += remaining_income * rate
                remaining_income = 0

        if tax_payable >= 1000000:
            tax_payable *= 1.1

        print(f"Total tax payable by {self.name}: Nu. {tax_payable:.2f}")

# Create an instance of the TaxCalculator class
tax_calculator = TaxCalculator()
