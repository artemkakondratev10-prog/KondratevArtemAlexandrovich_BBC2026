x1 = int(input())
q = input()
x2 = int(input())

def plus(x1, x2):
    return x1 + x2
def minus(x1, x2):
    return x1 - x2
def multiply(x1, x2):
    return x1 * x2
def divide(x1, x2):
    if x2 == 0:
        return "На ноль делить нельзя!"
    else:
        return x1 / x2

if q == '+':
    print(plus(x1, x2))
elif q == '-':
    print(minus(x1, x2))
elif q == '*':
    print(multiply(x1, x2))
elif q == '/':
    print(divide(x1, x2))
    