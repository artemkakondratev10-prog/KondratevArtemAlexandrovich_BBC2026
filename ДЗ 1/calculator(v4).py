class Regular_Calculator:
    def __init__(self, arithmetic_operation):
        self.arithmetic_operation = arithmetic_operation

    def calculate(self):
        # Метод позволяет вычислять написанное пользователем арифметическое выражение
        # Делаем копию списка, чтобы не испортить исходный
        expr = self.arithmetic_operation

        # 1 Сначала проверяем на умножение и деление
        i = int(0)
        while i < len(expr):
            if expr[i] in ('*', '/'):
                left = expr[i - 1]
                op = expr[i]
                right = expr[i + 1]
                if op == '*':
                    res = left * right 
                else:
                    res = left / right
                # Заменяем три элемента [left, op, right] на res
                expr[i - 1:i + 2] = [res]
                # После срезa список уменьшился, возвращаемся на шаг назад
                i -= 1
            else:
                i += 1
    
        # 2 Проверяем на сложение и вычитание
        result = expr[0]
        for i in range(1, len(expr), 2):
            op = expr[i]               
            next_num = expr[i + 1]
            if op == '+':          # если +, то прибавляем к результату следующее число
                result += next_num
            elif op == '-':        # если -, то убавляем из результата следующее число
                result -= next_num
    
        return result              # выводим результат 

class Currency_Calculator:
    def __init__(self, cash):
        self.cash = cash
    # метод conver будет переводить из одной валюты в другую. По двум ключевым словам (названиям валют)
    # через elif метод будет определять нужный вариант перевода валюты 
    def conver(self, var_currency):
        if var_currency=='1':
            return self.cash/86.59
        elif var_currency=='2':
            return self.cash*86.59
        if var_currency=='3':
            return self.cash/100.56
        elif var_currency=='4':
            return self.cash*100.56
        if var_currency=='5':
            return self.cash/12.9
        elif var_currency=='6':
            return self.cash*12.9

class Tip_Calculator:
    def __init__(self, precent, value, people):     # получаем данные от пользователя
        self.precent = precent
        self.value = value 
        self.people = people
    def computeTip(self):                    # метод позволяет расчитать сумму чаевых на основе процента, итоговую сумму
        tip = self.value*(self.precent/100)  # и сумму к оплате с одного человека, если платят больше одного человека
        total_amount = self.value+tip
        if self.people > 1:
            print(f"Сумма чаевых: {tip}")
            print(f"Всего: {total_amount}")
            print(f"С одного человека: {total_amount/self.people}")
        else: 
            print(f"Сумма чаевых: {tip}")
            print(f"Всего: {total_amount}")
        
while True:
    print("Выберите режим работы калькулятора:")
    print("1. Обычный калькулятор.")
    print("2. Валютный калькулятор.")
    print("3. Калькулятор чаевых.")
    print('Ваш выбор: ',end='')
    mode = str(input())
    if mode == '1':           # переменная, которая хранит выбранный пользователем вариант калькулятора
        print("Вы выбрали обычный калькулятор.")
        print("Введите арифметическое выражение, так, чтобы каждый оператор и число были введены через пробел\
. Для завершения введите '=':")
        math_expression = [] 
        x = input().split()      # ввод данных пользователем для обычного калькулятора
        for i in x:              # цикл с помощью try и except позволяет добавить в список math_expression                          
            if i == '=':         # числа и операторы в типе int и str соответственно 
                break
            try:
                math_expression.append(int(i))
            except ValueError:
                math_expression.append(i)

        calculator = Regular_Calculator(math_expression)
        print(calculator.calculate())
        input()
    elif mode == '2':
        print("Выберите нужный вариант:")
        print("1. Перевод рубли в доллары.")
        print("2. Перевод доллары в рубли.")
        print("3. Перевод рубли в евро.")
        print("4. Перевод евро в рубли.")
        print("5. Перевод рубли в юани.")
        print("6. Перевод юани в рубли.")
        print("Ваш вариант: ", end='')
        y = input()
        print("Введите колличество ваших денег: ", end='')
        cash = int(input())
        currency_calculator = Currency_Calculator(cash)
        print(currency_calculator.conver(y))
        input()
    elif mode == "3":
        print("Пожалуйста, введите сумму к оплате: ", end='')
        sum = int(input())
        print("Пожалуйста, введите процент от суммы, который хотите оставить на чаевые: ", end='')
        pr = int(input())
        print("Пожалуйста, введите количество человек: ", end='')
        peop = int(input())
        tip = Tip_Calculator(pr, sum, peop)
        tip.computeTip()
        input()


