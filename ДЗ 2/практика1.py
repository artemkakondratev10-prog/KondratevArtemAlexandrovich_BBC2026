while True:
    print('Введите свою строку: ',end='')
    stroka = input()
    print('Введите уровень: ',end='')
    lvl = int(input())
    if lvl == 1:
        print(f'метод 1: {stroka.upper()}')
        print(f'метод 2: {stroka.lower()}')
        print(f'метод 3: {stroka.capitalize()}')

        print('Какой метод вы веберите: ', end='')
        metod = int(input())
        if metod == 1:
            print(stroka.upper())
        elif metod == 2:
            print(stroka.lower())
        else:
            print(stroka.capitalize())
    
    if lvl == 2:
        print('Ввведите номер метода который хотите использовать.')
        print(f'метод 1: Найти индекс слова.')
        print(f'метод 2: Заменить слово.')
        print(f'метод 3: Посчитать количество букв.')
        print('Какой метод вы веберите: ', end='')
        metod = int(input())
        if metod == 1:
            print('Напишите слово, индекс которого хотите найти: ', end='')
            slovo = input().lower()
            stroka.lower()
            print(stroka.find(slovo))
        elif metod == 2:
            print('Напишите слово, которое хотите заменить: ', end='')
            print('Напишите слово, на котрое хотите заменить: ', end='')                
            slovo1 = input().lower()
            slovo2 = input().lower()
            stroka.lower()
            print(stroka.replace(slovo1, slovo2))
        else:
            print('Напишите букву, колличество которой хотите найти: ', end='')
            bukva = input()
            print(stroka.count(bukva))
    if lvl == 3:
        print('Ввведите номер метода который хотите использовать.')
        print(f'метод 1: убрать символ разделителя между символами строки.')
        print(f'метод 2: соединить символы через разделитель.')
        print('Какой метод вы веберите: ', end='')
        metod = int(input())
        if metod == 1:
            print('Напишите разделитель символов, который хотите убрать: ', end='')
            razdelitel = input()
            stroka = stroka.split(razdelitel)
            print(''.join(stroka))
        else:
            print('Напишите разделитель, который хотите вставить между символами: ', end='')
            razdelitel = input()
            stroka = list(stroka)
            print(f'{razdelitel}'.join(stroka))
    if lvl == 4:
        print('Ввведите номер метода который хотите использовать.')
        print(f'метод 1: проверить, что строка состоит только из цифр.')
        print(f'метод 2: проверить, что строка состоит только из букв.')
        print(f'метод 3: убрать лишние пробелы с концов строки.')
        print(f'метод 4: вставить слово.')
        print('Какой метод вы веберите: ', end='')
        metod = int(input())
        if metod == 1:
            if stroka.isdigit():
                print('Строка состоит только из цифр.')
            else:
                print('Не состоит только из цифр.')
        elif metod == 2:
            if stroka.isdigit():
                print('Строка состоит только из букв.')
            else:
                print('Не состоит только из букв.')
        elif metod == 3:
            print(stroka.strip())
        else:
            print('Введите слово, которое хотить вставить: ', end='')
            slovo = input()
            print(r'Напишите вашу строку и в место, куда хотите вставить слово, напишите {}: ', end='')
            stroka = input()
            print(stroka.format(slovo))
    if lvl == 5:
        stroka = stroka.strip()
        stroka = stroka.lower()
        stroka = stroka.split(';')
        stroka = ' '.join(stroka)
        stroka = stroka.capitalize()
        print(stroka)
    input()