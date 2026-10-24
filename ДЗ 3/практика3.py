import time
import random
import os

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

class Room:
    def __init__(self, type, health=0, armor=0, sword=0, monster=0, attack_monster=0, trap=0):
        self.type = type
        self.health = health
        self.armor = armor
        self.sword = sword
        self.monster_health = monster
        self.attack_monster = attack_monster
        self.trap = trap
        
class Player:
    def __init__(self, health=100, armor=0, swords=None):
        if swords is None:
            swords = []
        self.health = health
        self.armor = armor
        self.swords = swords
        self.base_uron = 3  # базовый урон игрока без мечей

    def is_alive(self):
        return self.health > 0

    def permutation_sword(self):
        print('Какие два меча хотите поменять местами?')
        print('Ваш ответ (например 1,2): ', end='')
        otvet = [int(q - 1) for q in input().split(',')]
        self.sword[otvet[0]], self.sword[otvet[1]] = self.sword[otvet[1]], self.sword[otvet[0]]
        print() 


def generate_room(lab):
    for i in range(len(lab)):
        for j in range(len(lab[i])):
            room_type = random.choice(['p', 's', 'm', 'l']) #определение типа комнаты: p - пустая, s - сундук, m - монстр, l - ловушка
            room_health = random.randint(5, 20)  #в каждой комнате будет случайное количество здоровья, брони, мечей, монстров и ловушек
            room_armor = random.randint(10, 50)
            room_sword_numbers = random.randint(1, 3)
            room_monster_health = random.randint(60, 80)
            room_attack_monster = random.randint(5, 15)
            room_trap = random.randint(10, 20)
            room_sword = [random.randint(3, 15) for _ in range(room_sword_numbers)]              
            lab[i][j] = Room(type=room_type, health=room_health, armor=room_armor, sword=room_sword, monster=room_monster_health, attack_monster=room_attack_monster, trap=room_trap)

def otrisovka(x, y):
    lab2 = [['[ ]' for q in range(n)] for i in range(n)]
    lab2[x][y] = '[X]'
    for i in range(len(lab2)):
        for j in range(len(lab2[i])):
            print(lab2[i][j], end=' ')   # отрисовываем лаберинт двойным циклом, где [X] - это позиция игрока, а [ ] - это пустая комната
        print()

def move_player(x, y):
    print('Выберите куда сходить (w, s, a, d): ', end='')
    command = input().lower() #будем смотреть ввод от пользователя в нижнем регистре 
    if command == 'w' or command == 'ц':
        if x > 0:
            x -= 1
        else:
            print('Вы не можете идти дальше вверх.')
            time.sleep(2)
    elif command == 's' or command == 'ы':
        if x < n - 1:
            x += 1
        else:
            print('Вы не можете идти дальше вниз.')
            time.sleep(2)
    elif command == 'a' or command == 'ф':
        if y > 0:
            y -= 1
        else:
            print('Вы не можете идти дальше влево.')
            time.sleep(2)
    elif command == 'd' or command == 'в':
        if y < n - 1:
            y += 1
        else:
            print('Вы не можете идти дальше вправо.')
            time.sleep(2)
    else:
        print('Неверная команда. Попробуйте снова.')
        time.sleep(2)
    return x, y

def invent():
    print('Хотите заглянуть в инвентарь? (да/нет)')
    print('Ваш ответ: ', end='')
    otvet = input()
    if otvet == 'да':
        print('Инвентарь:')
        print(f'Здоровье: {player.health}')
        print(f'Броня: {player.armor}')
        print('Мечи: ', end='')
        print(player.swords if player.swords else 'пусто')
        time.sleep(1)
        print()
        if len(player.swords) > 0:
            print('Хотите поменять местами мечи? (да/нет)')
            print('Самый первый меч в списке будет являться основным.')
            print('Ваш ответ: ', end='')
            otvet = input()
            if otvet == 'да':
                player.permutation_sword()
                time.sleep(2)
            else:
                time.sleep(2)
    else:
        return True  # эта строка нужна для проверки, если пользователь решил не идти дальше и не захотел смотреть в инвентарь
        print()

def sword_delete(swords):
    print('Ваши мечи: ', end='')
    for i in range(len(swords)):
        print(f'{i + 1} меч с уроном {swords[i]}')
    
    while True:
        otvet1 = input('Напишите номер меча, который хотите выбросить или напишите 0, если не хотите ничего выбрасывать', end='')
        if otvet1 == '0':
            break
        del swords[otvet1 - 1]
        
def sword_add(swords, lab1):  # функция добавления мечей
    while True:
        print('1. Добавить меч.')
        print('2. Выбросить меч.')
        print('3. Ничего не делать.')
        print('Выберите, что хотите сделать(номер операции): ',end='')
        otvet = input()
        if otvet == '3':
            break
        elif otvet == '1':
            print(f'Напишите номер(а) меча или мечей, которые хотите забрать: ')
            for i in range(len(lab1[x][y].sword)):
                print(f'{i + 1}. Меч с уроном {lab1[x][y].sword[i]}')

            print('Ваш выбор (пишите через запятую с пробелом): ', end='')
            result = [int(q - 1) for q in input().split(', ')]
            for i in result:
                swords.append(lab1[x][y].sword[i])
        elif otvet == '2':
            sword_delete(swords)

# def information(invent):
#     print(f'1. Ваше здоровье: {invent[0]}')
#     print(f'2. Ваша броня: {invent[1]}')
#     if len(invent[2]) != 0:
#         print('3. Ваши мечи: ', end=' ')
#         for sword in invent[2]:
#             print(f'{sword},', end=' ')
#     else:
#         print('3. Ваши мечи: нет')

#     if len(invent[3]) != 0:
#         print('4. Ваша частицы брони: ', end=' ')
#         for bron in invent[3]:
#             print(f'{bron},', end=' ')

# def dobav(invent, komnata): #тут мы добавляем в инвентарь предметы из комнаты
#     invent[0] += komnata[1] #здоровье из комнаты добавляем в здоровье игрока
#     invent[1] += komnata[2] #броню из комнаты добавляем в броню игрока
#     invent[2].append(komnata[3]) #мечи из комнаты добавляем в инвентарь игрока
#     invent[3].append(komnata[2]) #частицы брони из комнаты добавляем в инвентарь игрока

# def sunduk(komnata):
#     print('Вы нашли сундук!')
#     print(f'В сундуке лежит: {komnata[1]} здоровья, {komnata[2]} брони и {komnata[3]} мечей.')
#     print('Хотите забрать предметы из сундука? (да/нет)')
#     otvet = input()
#     if otvet == 'да':
#         return dobav(invent, komnata)
#     else:
#         print('Вы решили оставить предметы в сундуке.')





# базовые константы игры           
x = 0
y = 0
n = 10
ogr_sword = 3 #ограничение на количество мечей, которые может носить игрок
proshlie_komnati = [(0, 0)] #список, в котором будут храниться координаты комнат, которые игрок уже посещал
lab1 = [[[] for q in range(n)] for i in range(n)]
generate_room(lab1)
player = Player()   # создаание игрока с начальными характеристиками здоровья, брони и мечей

# for i in range(len(lab1)):
#     for j in range(len(lab1[i])):
#         print(f'Комната {i+1}, {j+1}: тип - {lab1[i][j].type}, здоровье - {lab1[i][j].health}, броня - {lab1[i][j].armor}, мечи - {lab1[i][j].sword}, монстр - {lab1[i][j].monster}, атака монстра - {lab1[i][j].attack_monster}, ловушка - {lab1[i][j].trap}')
# invent = [[] for i in range(4)]

# #information(invent)
while True:
    if x == n - 1 and y == n - 1:   #если игрок дошел до конца лабиринта, то выводим сообщение о победе и выходим из цикла
        print('Поздравляем! Вы нашли выход из лабиринта.')
        break

    otrisovka(x, y) 
    x, y = move_player(x, y)   # блок отрисовки лабиринта на терминале
    clear_screen()
    otrisovka(x, y)        
    


    if (x, y) not in proshlie_komnati:   # оснновной блок условия тела игры, который проверяет был ли игрок в комнате ранее
        if lab1[x][y].type == 'p':                 # проверка 1 комнаты (пустая)
            print('Вы вошли в пустую комнату.')
            time.sleep(1)

        elif lab1[x][y].type == 's':               # проверка 2 комнаты (сундук)
            print('Вы вошли в комнату с сундуком.')
            time.sleep(1)
            print(f'В сундуке лежит: {lab1[x][y].health} здоровья, {lab1[x][y].armor} единицы брони и {len(lab1[x][y].sword)} меча.')
            print('Хотите забрать предметы из сундука? (да/нет)')
            print('Ваш ответ: ', end='')
            otvet = input()
            if otvet == 'да':
                player.health += lab1[x][y].health
                player.armor = min(80, player.armor + lab1[x][y].armor) # сделаем ограничение на броню
                if ogr_sword - len(player.swords) >= len(lab1[x][y].sword):
                    player.swords.extend(lab1[x][y].sword)
                    print('Вы забрали предметы из сундука.')
                    print()
                else:
                    print('Вы не можете забрать все мечи из сундука.')
                    print(f'Вы можете забрать только {ogr_sword - len(player.swords)} меча.')
                    print('Хотите забрать только часть мечей из сундука или выбросить лишние? (да/нет)')
                    print('Ваш ответ: ', end='')
                    otvet = input()                                                              
                    print()                                                                
                    if otvet == 'да':        
                        sword_add(player.swords, lab1)                                             
            else:
                print('Вы решили оставить предметы в сундуке.')
                print()


        elif lab1[x][y].type == 'm':               # проверка 3 комнаты (монстр)
            print('Вы вошли в комнату с монстром.')
            time.sleep(1)
            print(f'Монстр имеет {lab1[x][y].monster_health} здоровья и наносит {lab1[x][y].attack_monster} урона.')
            print()
            while lab1[x][y].monster_health > 0 and player.is_alive():   # цикл до тех пор, пока оба живы
                if len(player.swords) > 0: # проверка на наличие меча в инвенторе
                    sword_damage = player.swords[0] # используем первый меч из инвентаря (он по умолчанию является основным)
                    print(f'Вы нанесли {sword_damage} урона монстру. У монстра осталось ', end ='')
                    print('0 здоровья' if lab1[x][y].monster_health - sword_damage <= 0 else f'{round(lab1[x][y].monster_health - sword_damage)} здоровья.')
                    lab1[x][y].monster_health -= sword_damage

                else:     # если меча нет, то игрок бьется руками (player.base_uron)
                    print(f'Вы нанесли {player.base_uron} урона монстру. У монстра осталось ', end='')
                    print('0 здоровья' if lab1[x][y].monster_health - player.base_uron <= 0 else f'{round(lab1[x][y].monster_health - player.base_uron)} здоровья.')
                    lab1[x][y].monster_health -= player.base_uron

                if lab1[x][y].monster_health > 0:        
                    uron = lab1[x][y].attack_monster * (1 - player.armor / 100)
                    print(f'Монстр атакует вас и наносит {uron} урона. У вас осталось ', end='')
                    print('0 здоровья' if player.health - uron <= 0 else f'{round(player.health - uron)} здоровья.')
                    player.health -= uron  # уменьшаем здоровье игрока с учетом брони
                    input()
 
            if player.is_alive():
                print('Вы победили монстра!')
                print(f'У вас осталось {player.health} здоровья.')
                print()
            else:
                print('Вы были убиты монстром. Игра окончена.')
                break
        elif lab1[x][y].type == 'l':               # проверка 4 комнаты (ловушка)
            print('Вы вошли в комнату с ловушкой.')
            time.sleep(1)
            uron_lowushki = lab1[x][y].trap * (1 - player.armor / 100)
            player.health -= uron_lowushki  # уменьшаем здоровье игрока с учетом брони
            print(f'Ловушка сработала и нанесла вам {uron_lowushki} урона. У вас осталось {player.health} здоровья.')
            time.sleep(1)
            if not player.is_alive():
                print('Вы были убиты ловушкой. Игра окончена.')
                break

        invent()
            
        print('Хотите продолжить идти дальше? (да/нет)')
        print('Ваш ответ: ', end='')
        otvet = input()
        if otvet == 'да':
            time.sleep(1)
            pass
        else:
            if invent():
                print('Вы решили закончить игру.')
                time.sleep(1.5)
                break

        clear_screen()
        proshlie_komnati.append((x, y))  # добавляем координаты комнаты в список посещенных комнат
    else:
        clear_screen()