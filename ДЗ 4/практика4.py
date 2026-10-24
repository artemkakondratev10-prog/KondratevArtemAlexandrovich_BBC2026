import pandas as pd
import numpy as np

df = pd.read_csv('C:/Users/Привет/Downloads/tested.csv', sep = ',')
#n = int(input())  # сами выбираем сколько строк из начала взять
#print(df.head(n))  # выполнение пункта 7

#print(df.tail())   # выполнение пункта 8

# print(df.shape[0], df.shape[1])  # выполнение пункта 9, выводит кол-во строк и столбцов

#print(*list(df.columns)) # выполнение пункта 10, отображение названия столбцов

#print(df.dtypes)  # выполение пункта 11

# пункт 12 категориальные признаки: PassengerId, Survived, Pclass, Name, Sex, Ticket, Cabin, Embarked
# числовые признаки: Age,SibSp,Parch,Fare

# выполнение пункта 13
#print(f'{df.columns[5]}: {df[df.columns[5]].mean()}, {df[df.columns[5]].median()},\
# {df[df.columns[5]].min()}, {df[df.columns[5]].max()}, {df[df.columns[5]].std()}')
#print(f'{df.columns[6]}: {df[df.columns[6]].mean()}, {df[df.columns[6]].median()},\
# {df[df.columns[6]].min()}, {df[df.columns[6]].max()}, {df[df.columns[6]].std()}')  # весь этот блок кода выводит 
#print(f'{df.columns[7]}: {df[df.columns[7]].mean()}, {df[df.columns[7]].median()},\
# {df[df.columns[7]].min()}, {df[df.columns[7]].max()}, {df[df.columns[7]].std()}')  # среднее, медиану, минимум, максимум
#print(f'{df.columns[9]}: {df[df.columns[9]].mean()}, {df[df.columns[9]].median()},\
# {df[df.columns[9]].min()}, {df[df.columns[9]].max()}, {df[df.columns[9]].std()}')  # и стандартное отклонение числовых признаков

#print(df[df.columns[2]].value_counts()) # пункт 14, функция выводит кол-во пассажиров в каждом классе

#print(df[df.columns[11]].nunique()) # пункт 15, функция возвращает кол-во уникальных значений

# Ответ на вопрос: потому что Pclass содержит информацию только о классе пассажира, ничего полезного
# от среднего значения, медианы и т.д. мы не получим

# print(df.isna().sum())  # пункт 16, метод isna() создает DataFrame с True (если NaN) и False значениями, а sum() считает кол-во для каждого столбца и выводит Series

# series1 = df.isna().sum()
# print(series1 / df.shape[0] * 100)  # пункт 17, мы можем делить и умножать сразу весь series

# print(df.isna().sum().idxmax())  # пункт 18, метод idxmax() позволяет найти индекс самого большого значения (выводит именно индекс!)

age_before = df.iloc[:, 5].median()
z_do = [df[df.columns[5]].mean(), df[df.columns[5]].median(), df[df.columns[5]].min(), df[df.columns[5]].max(), df[df.columns[5]].std(), df[df.columns[5]].count()]
#print(f'{df.columns[5]}: {', '.join(z_do)}')
df.iloc[:, 5] = df.iloc[:, 5].fillna(age_before)   # пункт 19-21, смотрим старые параметры, заполняем пропуски, смотрим новые параметры
z_po = [df[df.columns[5]].mean(), df[df.columns[5]].median(), df[df.columns[5]].min(), df[df.columns[5]].max(), df[df.columns[5]].std(), df[df.columns[5]].count()] 
#print(f'{df.columns[5]}: {', '.join(z_po)}')

df1 = pd.DataFrame({
    'До обработки' : z_do,        # пункт 22, создаем таблицу с значениями до и после заполнения пустых ячеек
    'После обработки' : z_po   
}, index = ['Среднее арифметическое', 'Медиана', 'Минимальный возраст', 'Максимальный возраст', 'Стандартное отклонение', 'Количество известных значений'])
print(df1)

shape1 = df.shape  # пункт 26, кол-во строк и стобцов до обработки
df = df.dropna(subset='Embarked')   # пункт 23, удаляем те строки, в которых значение Embarked NaN
if (df.shape[0] / df.iloc[:, 10].isna().sum() * 100) > 50:   # пункт 24, смотрим на процент пропусков от всех строк и удаляем столбец, если больше 50%
    df = df.drop('Cabin', axis = 1)
shape2 = df.shape   # пункт 26, кол-во строк и стобцов после обработки
# print(df.isna().sum())  # пункт 25, проверка на пропуски после обаботки

# print(shape1, shape2)  # пункт 26, вывод кол-ва строк и столбцов до и после обработки

# ответы на контрольные вопросы
# пункт 27: Потому что медиана менее чувствительна к выбросам — слишком большим или маленьким значениям
# пункт 28: После заполнения пропусков увеличилось количество известных значений. 
# Среднее и стандартное отклонение могут измениться. Медиана, минимум и максимум остаются прежними.
# пункт 29: стандартное отклоение может измениться, так как добавление значений равных медианы изменяет разброс относительного среднего значения
# пункт 30: Исходное распределение не сохраняется полностью, поскольку заполнение пропусков медианой 
# искусственно увеличивает количество значений, равных медиане, и изменяет частоты возрастов.

survived = df.iloc[:,1].to_numpy()
maska = survived == 1
#print(np.sum(maska) / maska.shape[0] * 100) # пункт 31, нашли кол-во выживших и их процент от общего числа человек

# пункт 32, находим процент выживших среди мужчин и женщин
sex = df['Sex'].to_numpy()
maska_man = (survived == 1) & (sex == 'male')   # используем маску
maska_woman = (survived == 1) & (sex == 'female')
pr_man = np.sum(maska_man) / maska.shape[0] * 100
pr_woman = np.sum(maska_woman) / maska.shape[0] * 100
# print(np.sum(maska_man) / maska.shape[0] * 100)   
# print(np.sum(maska_woman) / maska.shape[0] * 100)

# пункт 33
age = df['Age'].to_numpy()
sex = df['Sex'].to_numpy()
maska_man = sex == 'male'
maska_woman = sex == 'female'
mean_man = np.mean(age[maska_man])
mean_woman = np.mean(age[maska_woman])
# print(mean_man)
# print(mean_woman)


age = df['Age'].to_numpy()
sex = df['Sex'].to_numpy()
survived = df['Survived'].to_numpy()
maska_man_1 = (sex == 'male') & (survived == 0)
maska_man_2 = (sex == 'male') & (survived == 1)   # пункт 34
maska_woman_1 = (sex == 'female') & (survived == 0)
maska_woman_2 = (sex == 'female') & (survived == 1)
man_1 = np.mean(age[maska_man_1])
man_2 = np.nan if age[maska_man_2].size == 0 else np.mean(age[maska_man_2])
woman_1 = np.nan if age[maska_woman_1].size == 0 else np.mean(age[maska_woman_1])
woman_2 = np.mean(age[maska_woman_2])


fare = df['Fare'].to_numpy()
fare_min = np.nanmin(fare)
fare_max = np.nanmax(fare)      # пункт 35
fare_midle = np.nanmean(fare)
#print(fare_min, fare_max, fare_midle)

std_age = np.std(df['Age'].to_numpy())   # пункт 36
#print(std_age)

# df2 = pd.DataFrame({
#     'Мужчины' : [pr_man, mean_man, man_2, man_1],
#     'Женщины' : [pr_woman, mean_woman, woman_2, woman_1]           # Результат в виде таблицы 31-34
# }, index = ['Процент выживших', 'Средний возраст', 'Средний возраст выживших', 'Средний возраст погибших'])
# print(df2.fillna('Значение неизвестно'))

# ответ на котрольный вопрос: Как оказалось, среди мужчин нет ни одного выжившего человека. Поэтому нельзя посчитать средний вораст для выживших мужчин.
# Но также нет ни одиной умершей женщины, поэтому посчитать средний возраст среди умерших женщин так же нельзя.

filtr1 = df[(df['Sex'] == 'male') & (df['Age'] > 30) & (df['Pclass'] == 1)]
#print(filtr1.shape[0], filtr1.head(10), sep='\n')                                  # фильтрация данных задание 1

filtr2 = df[((df['Age'] < 18) | ((df['Sex'] == 'female')) & (df['Survived'] == 1))]  # фильтрация данных задание 2
#print(filtr2.shape[0])

filtr3 = df[(df['Pclass'] == 3) & (df['Fare'] > fare_midle)]    # фильтрация данных задание 3, пассажиры найдены


filtr4 = df[(df['Age'] >= 20) & (df['Age'] <= 40) & (df['Embarked'] == 'S')]  # фильтрация данных задание 4, пассажиры найдены

# ответ на контрольный вопрос: при фильтрации с помощью "И" мы отбираем только тех пассажиров, которые соответствуют обоим условиям
# при фильтрации с помощью "ИЛИ" мы отбираем только тех пассажиров, которые соответствуют хотя бы одному условию


df3 = df.groupby(['Pclass', 'Sex']).agg(
    size = ('Age', 'size'),
    mean_age = ('Age', 'mean'),                  # пункт 37, группируем данные и агрегируем их с помощью agg
    survived_percent = ('Survived', lambda x : x.mean() * 100),
    mean_fare = ('Fare', 'mean')
)
# print(df3)

df4 = df.groupby('Embarked').agg(         # пункт 38
    size = ('Age', 'size'),
    survived_percent = ('Survived', lambda x : x.mean() * 100)
)
# print(df4)

df5 = df.groupby('Pclass')['Survived'].mean() * 100        # пункт 39, вывод класса с наибольшим кол-вом выживших
# max_Pclass = df5.idxmax()            
# print(max_Pclass)

# ответ на контрольный вопрос, группировка позволяет быстро узнать статистические данные в случае, когда понадобилось бы много масок.
# например для Pclass и Sex понадобилось бы писать 6 масок и долго считать, в то время как группировка с агрегацией позволила быстро вычислить все необходимые данные.

# df.to_csv(
#     r'C:/Users/Привет/OneDrive/Рабочий стол/Homework python/ДЗ 4/titanic_processed.csv',
#     index=False
# )

# df3.to_csv(
#     r'C:/Users/Привет/OneDrive/Рабочий стол/Homework python/ДЗ 4/titanic_statistics.csv',
# )

data1 = pd.read_csv(r'C:/Users/Привет/OneDrive/Рабочий стол/Homework python/ДЗ 4/titanic_processed.csv')
data2 = pd.read_csv(r'C:/Users/Привет/OneDrive/Рабочий стол/Homework python/ДЗ 4/titanic_statistics.csv')

# print(data1.head())
# print(data2.head())

# ответы на итоговые вопросы: 
# 1. Столбец Age содержал 86 пропусков (20% от всех значений), столбец Cabin содержал 327 пропусков (78% от всех значений)
# 2. После обработки пропусков столбец Cabin был удален, то есть было удалено 418 значений.
# Еще после обработки пропусков в Age умньшился средний возраст (было 30,2, стало 29,5) и уменьшилось стандартное отклонение (было 14,18 стало 12,70)
# причина в том, что мы заполняли пропуски медианой, существенно уменьшая стандартное отклонение (стало больше усредненных значений, что уменьшило разброс в возрасте)
# средний возраст уменьшился, так как он был больше чем значение медианы, таким образом, добавление медианы заставило уменьшится средний возраст.
# 3. Исходный Titanic dataset содержал сведения только о мертвых мужчинах и о живых женщинах, не удивительно, что средний возраст выживших мужчин и умерших женщин
# в таблице пункта 31-34 является неизвестынм значением.
# 4. Наибольшая доля выживших была в классе 1, можем убедиться в пункте 39.
# 5. Мне очень понравилась группировка и комбинирование pandas и numpy библиотек. Группировка позволяет обрабатывать огромные структуры и быстро создавать новые таблицы
# с необходимыми даннами, а возможность быстро переключиться на numpy позволяет с большой экффективностью вычислять большие данные. Еще понравилось обилие методов, буквально для
# любой задачи есть свой метод, это очнень удобно.