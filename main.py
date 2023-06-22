import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from conventer import cuni, cual, cuzn

alloy_dict = {
    1: ['Cu-Ni:\n', cuni],
    2: ['Cu-Al:\n', cual],
    3: ['Cu-Zn:\n', cuzn],
}

# Ввод данных и обработка исключений
while True:
    try:
        user_system = int(input('Системы:\n'
                                '    1 - Система медь-никель (Cu-Ni)\n'
                                '    2 - Система медь-алюминий (Cu-Al)\n'
                                '    3 - Система медь-цинк (Cu-Zn)\n'
                                'Выбранная система: '))
        user_alloy = alloy_dict[user_system][1]
    except KeyError:
        print(f'\nНаша база данных сплавов не настолько богатая, и системы {user_system} пока нет в списке.')
    except ValueError:
        print(f'\nНеверный формат ввода.')
    else:
        break

max_concentration = user_alloy.iloc[-1]['Second component concentration']
while True:
    try:
        user_concentration = float(input('Концентрация второго компонента выбранной системы: '))
    except ValueError:
        print('Неверный формат ввода.')
    else:
        if user_concentration < 0 or user_concentration > 100:
            print('Концентрация второго (легирующего) компонента должна находится в пределах от 0 до 100%')
            continue
        else:
            break

# Название слпава в принятом формате в виде строки
alloy_name = f'{alloy_dict[user_system][0][:2]}-{int(user_concentration // 1)},' \
             f'{int(user_concentration % 1)}%{alloy_dict[user_system][0][3:-2]}'

# Преобразование daraframe в ndarray для регрессионного анализа
np_table = user_alloy.to_numpy()
concentration = np_table[:, 0]
hardness = np_table[:, 1]
toughness = np_table[:, 2]
plasticity = np_table[:, 3]

# Три модели кубической регрессии степени для твердости, прочности и пластичности
hardness_model = np.poly1d(np.polyfit(concentration, hardness, 3))
toughness_model = np.poly1d(np.polyfit(concentration, toughness, 3))
plasticity_model = np.poly1d(np.polyfit(concentration, plasticity, 3))

# Построение трех соответствующих графиков зависимости свойств от концентрации, с точками исходных (красные)
# и прогнозируемых (синие) данных
polyline = np.linspace(1, max_concentration + 10, 500)
fig, axs = plt.subplots(1, 3, figsize=(14, 6))
axs[0].scatter(user_concentration, hardness_model(user_concentration), c='blue', label='Прогонзируемые')
axs[0].plot(polyline, hardness_model(polyline), c='red')
axs[0].scatter(concentration, hardness, c='red', label='Исходные')
axs[0].set_title(f'Твердость, {user_alloy.columns[1]}') # Для разных систем твердость измеряется в разных ед. изм.

axs[1].plot(polyline, toughness_model(polyline), c='red')
axs[1].scatter(user_concentration, toughness_model(user_concentration), c='blue')
axs[1].scatter(concentration, toughness, c='red')
axs[1].set_title('Предел прочности, МПА')

axs[2].plot(polyline, plasticity_model(polyline), c='red')
axs[2].scatter(user_concentration, plasticity_model(user_concentration), c='blue')
axs[2].scatter(concentration, plasticity, c='red')
axs[2].set_title('Пластичность, %')
axs[0].legend()

for i, j in zip([user_concentration], [round(hardness_model(user_concentration), 1)]):
    axs[0].annotate('(%s, %s)' % (i, j), xy=(i, j), textcoords='offset points', xytext=(0, 10), ha='center')

for i, j in zip([user_concentration], [round(toughness_model(user_concentration), 1)]):
    axs[1].annotate('(%s, %s)' % (i, j), xy=(i, j), textcoords='offset points', xytext=(0, 10), ha='center')

for i, j in zip([user_concentration], [round(plasticity_model(user_concentration), 1)]):
    axs[2].annotate('(%s, %s)' % (i, j), xy=(i, j), textcoords='offset points', xytext=(0, 10), ha='center')

# Вывод данных
pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', None)
print('\n\n', 'Механические свойства сплавов системы', *alloy_dict[user_system], '\n\n')

print(f'Механические свойства сплава '
      f'{alloy_name}\n'
      f'Твердость: {round(hardness_model(user_concentration), 1)} HRB\n'
      f'Предел прочности: {round(toughness_model(user_concentration), 1)} МПа\n'
      f'Пластичность: {round(plasticity_model(user_concentration), 1)}%\n')

if user_concentration > max_concentration + 10:
    print(f'ВНИМАНИЕ: Указанное значение концентрации лежит далеко от интервала концентраций (0-{max_concentration}%), '
          f'заданного в базе данных сплавов этой системы.'
          f'\nПрогнозируемые значения некоторых механических свойств могут значительно отличаться от реальных.')

fig1 = plt.gcf()
plt.show()

if input('Сохранить текущие графики в виде png-изображения?\n'
         '1 - Да, сохранить\n'
         '0 - Нет, не сохранять\n') == '1':
    fig1.savefig(alloy_name, dpi=100)
    print('Изображение сохранено в папке проекта.')
