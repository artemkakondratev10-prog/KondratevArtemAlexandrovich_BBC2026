while True:
    x1 = int(input())
    q = input()
    x2 = int(input())

    def calculate(x1, q, x2):
        if q == '+':
            return x1 + x2
        elif q == '-':
            return x1 - x2
        elif q == '*':
            return x1 * x2
        elif q == '/':
            if x2 == 0:
                return "На ноль делить нельзя!"
            else:
                return x1 / x2
    print("=")
    print(calculate(x1, q, x2))

