x1 = int(input())
q = input()
x2 = int(input())

if q == '+':
    print(x1 + x2)
elif q == '-':
    print(x1 - x2)
elif q == '*':
    print(x1 * x2)
elif q == '/':
    if x2 == 0:
        print("На ноль делить нельзя!")
    else:
        print(x1 / x2)
