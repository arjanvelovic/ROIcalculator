import os

class ROICalculator():
    '''
    The ParkingGarage class will have the following attributes.
    -investments: dictionary of all investments
        -down payment: float of the downpayment
        -closing: float of closing cost
        -rehab: float of rehab cost
        -misc: float of any miscillaneous expenses
    -Income: dictionary of montly income
        -units: int of rental units for property
        -rent: list of floats of rent per property
        -laundry: float of monhtly laundry revenue
        -storage: float of monthly storage revenue
        -parking: float of monthly parking revenue
        -misc: float of any miscillaneous expenses
    - Expenses:
        -mortgage: float of monthly mortgage payment
        -tax: float of monthly tax payment
        -insurance: float of monthly insurance payment
        -utilities: dict of monthly utilities payment
            -electric: float of monthly electric payment
            -water: float of monthly water payment
            -sewage: float of monthly sewage payment
            -garbage: float of monthly garbage payment
            -gas: float of monthly gas payment
        -HOA: float of monthly HOA payment
        -landscaping: float of monthly landscaping payment
        -vacancy: float of monthly vacancy percentage, default = 5% rental income
        -repairs: float of monthly repairs payment, default = $50 per unit
        -capital: float of monthly capital payment, default = $50 per unit
        -property managment: float of monthly property managment percentage, default = 10% rental income
    '''
    # creating instance attributes, sets all values to None, used in logic later
    def __init__(self,
                investments = dict.fromkeys(['down payment', 'closing', 'rehab', 'misc']), 
                income =  {'units': None, 'rent': [], 'laundry': None, 'storage': None, 'parking': None, 'misc': None},
                expenses = {'mortgage': None,'tax': None,'insurance': None,
                    'utilities': dict.fromkeys(['electric', 'water', 'sewage', 'garbage', 'gas']),
                    'HOA': None, 'landscaping': None, 'repairs': None, 'capital': None, 'vacancy': None, 'property managment': None},
                investmentssum = None, incomesumsub = None, rentsum = None, expensesumsub = None, utilitiessum = None):
        self.investments = investments
        self.income = income
        self.expenses = expenses
        self.investmentssum = investmentssum
        self.incomesumsub = incomesumsub
        self.rentsum = rentsum
        self.expensesumsub = expensesumsub
        self.utilitiessum = utilitiessum

    def GetInvestments(self): #get investment information
        os.system('cls')
        self.investments.update(dict.fromkeys(['down payment', 'closing', 'rehab', 'misc'])) #resets to None for resubmission
        for key in self.investments.keys():
            while self.investments[key] == None:
                self.investments[key] = checkAndConvertFloat(input(f'What is the {key} cost for the property?\n$'), 0)
        self.investmentssum = sum(self.investments.values()) #sum of all investments

    def GetIncome(self): #get income information
        os.system('cls')
        self.income.update(dict.fromkeys(['units', 'laundry', 'storage', 'parking', 'misc'])) #resets to None for resumission
        self.income['rent'] = []
        self.incomesumsub = 0
        for key in self.income.keys():
            if key == 'units':
                while self.income[key] == None:
                    self.income[key] = checkAndConvertInt(input(f'How many units does the property have?\n'))
                    if self.income[key] >= 50: #ensures large value wasn't an error
                        while True:
                            alotOfUnits = input('Whoa that is alot of units, are you sure you have that many units?\n')
                            if alotOfUnits.lower() in ['yes', 'y', 'yeah', 'ye', '']:
                                self.income[key] = self.income[key]
                                break
                            elif alotOfUnits.lower() in ['no', 'n', 'nah']:
                                self.income[key] = None
                                break
                            else:
                                print('That was not a valid input\nPlease try again\n')      
            elif key == 'rent':
                for i in range(self.income['units']): #creates a list the same size as number as units
                    self.income[key].append(None)
                    while self.income[key][i] == None:
                        self.income[key][i] = checkAndConvertFloat(input(f'What is the rent revenue from unit {i+1}?\n$'), 0)
            else:
                while self.income[key] == None:
                    self.income[key] = checkAndConvertFloat(input(f'What is the monthly {key} revenue for the property?\n$'), 0)
                self.incomesumsub += self.income[key]
        self.rentsum = sum(self.income['rent'])
    
    def GetExpenses(self): #get expenses information
        os.system('cls')
        self.expenses.update(dict.fromkeys(['mortgage', 'tax', 'insurance', 'HOA', 'landscaping', 'repairs', 'capital', 'vacancy','property managment']))
        self.expenses['utilities'].update(dict.fromkeys(['electric', 'water', 'sewage', 'garbage', 'gas']))

        self.utilitiessum = 0
        self.expensesumsub = 0
        for key in self.expenses.keys():
            if key in ['mortgage', 'tax', 'insurance', 'HOA', 'landscaping']:
                while self.expenses[key] == None:
                    self.expenses[key] = checkAndConvertFloat(input(f'What is the monthly {key} cost for the property?\n$'), 0)
                self.expensesumsub += self.expenses[key]
            elif key == 'utilities':
                for key2 in self.expenses[key].keys(): #second for loop for utilities dictionary in expenses dictionary
                    while self.expenses[key][key2] == None:
                        self.expenses[key][key2] = checkAndConvertFloat(input(f'What is the monthly {key2} bill for the property?\n$'), 0)
                    self.utilitiessum += self.expenses[key][key2]
            elif key in ['repairs', 'capital']:
                while self.expenses[key] == None:
                    self.expenses[key] = checkAndConvertFloat(input(f'What is the monthly {key} cost per unit?\nThe deafult is set to $50 per unit\n$'), 50)
            else: #'vacany', 'propmanagement'
                while self.expenses[key] == None:
                    self.expenses[key] = checkAndConvertFloat(input(f'What is the {key} percentage of the property?\nThe deafult is set to %5\n%'), 5)

    def Calculations(self): #complete calculations and print report
        os.system('cls')
        if self.investmentssum == None:
            print('You still have to submit your investment costs\n')
        elif self.incomesumsub == None:
            print('You still have to submit your monthly income\n')
        elif self.expensesumsub == None:
            print('You still have to submit your monthly expenses\n')
        else:
            incomesum = self.incomesumsub + self.rentsum #sum of all income
            expensesum = self.expensesumsub + self.utilitiessum + (self.expenses['repairs'] + self.expenses['capital'])*self.income['units'] + (self.expenses['vacancy'] + self.expenses['property managment'])*0.01*self.rentsum #sum of all expenses

            monthlycashflow = incomesum - expensesum

            try: #use of try incase division of 0
                ROI = ((monthlycashflow*12)/self.investmentssum)*100
            except:
                print('You still have to submit your investment costs\n')

            if ROI < 0:
                ROIrating = 'Terrible'
            elif ROI >= 0 and ROI < 9:
                ROIrating = 'Bad'
            elif ROI >= 9 and  ROI < 15:
                ROIrating = 'Good'
            else:
                ROIrating = 'Amazing'

            #print of complete report
            print(
f'''HERE IS YOUR COMPLETE REPORT
----------------------------------------------------
Your Yearly Return on Investment:   {round(ROI,2)}%
Your ROI Rating: .................. {ROIrating}
Your Monthly Cashflow: ............ ${monthlycashflow}
Total Investment Cost: ............ ${self.investmentssum}
Total Monthly Income: ............. ${incomesum}
Total Monthly Expenses: ........... ${expensesum}
----------------------------------------------------
YOUR INVESTMENT COSTS:''')
            for key, value in self.investments.items():
                print(f'{key.capitalize()} Cost: ${value}')
            breakline()
            print('YOUR MONTHLY INCOME:')
            for key, value in self.income.items():
                if key == 'units':
                    print(f'Number of {key.capitalize()}: {value}')
                if key == 'rent':
                    print(f'Your Total {key.capitalize()}: ${self.rentsum}')
                    for i in range(len(self.income[key])):
                        print(f'    Unit {i+1} Rent: ${self.income[key][i]}')
                else:
                    print(f'{key.capitalize()} Revenue: ${value}')
            breakline()
            print('YOUR MONTHLY EXPENSES:')
            for key, value in self.expenses.items():
                if key == 'utilities':
                    print(f'Your Total {key.capitalize()}: ${self.utilitiessum}')
                    for key2, value2 in self.expenses[key].items():
                        print(f'    {key2.capitalize()} Cost: ${value2}')
                elif key in ['vacancy', 'property managment']:
                    print(f'{key.capitalize()} Percentage: {value}%')
                else:
                    print(f'{key.capitalize()} Cost: ${value}')
            breakline()
            waitinput = input('Press Enter to go back to the main menu\n')
    
    def mainMenu(self): #main menu for user interface
        os.system('cls')
        stay = True
        while stay:
            question = input('\nWelcome to the Return of Investment calculator\nPlease select the following options on the number pad:\n1) Input or edit investment costs\n2) Input or edit monthly income\n3) Input or edit monthly expenses\n4) Get ROI report\n5) Cancel\n')
            os.system('cls')
            if question == '1':
                self.GetInvestments()
            elif question == '2':
                self.GetIncome()
            elif question == '3':
                self.GetExpenses()
            elif question == '4':
                self.Calculations()
            elif question == '5':
                while True:
                    leavequestion = input('Are you sure you want to leave?\nAll of your data will be errassed if you do.\n')
                    os.system('cls')
                    if leavequestion.lower() in ['yes', 'y', 'yeah', 'ye', '']:
                        print('\nSee you later alligator!')
                        stay = False
                        break
                    elif leavequestion.lower() in ['no', 'n', 'nah']:
                        break
                    else:
                        print('That was not a valid input\nPlease try again\n')
            else:
                print('That was not a valid input\nPlease try again')

#create function to check if string is a float
def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False
    
def checkAndConvertFloat(input, default):
    if input.isnumeric() or isfloat(input):
        floatnum = float(input)
        if floatnum >= 0:
            return floatnum
        else:
            print('That was not a valid input\nPlease try again\n')
    elif input == '':
        return default
    else:
        print('That was not a valid input\nPlease try again\n')

def checkAndConvertInt(input):
    if input.isnumeric():
        intnum = int(input)
        if intnum >= 0:
            return intnum
        else:
            print('That was not a valid input\nPlease try again\n')
    else:
        print('That was not a valid input\nPlease try again\n')

def breakline():
    print('----------------------------------------------------')

Property1 = ROICalculator()
Property1.mainMenu()