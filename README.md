# Итоговый проект по программе Цифровой кафедры «Средства разработки инженерных приложений»

Вьюшин Егор Олегович, БМТ-21-1<br>
Росоленко Софья Кирилловна, БМТ-21-2<br>

Цифровая кафедра. Средства разработки инженерных приложений.

## Прогнозирование механических свойств сплава на основе концентрации легирующего компонента

**Цель**<br>
Разработать приложение, способное cпрогнозировать механические свойства сплава на основе концентрации легирующего компонента
и визуализировать их изменения в виде графиков зависимостей свойств от концентраций.

**Задачи**
* формирование необходимого для исследования алгоритма
* создание обновляющегося dataframe с измененными в базе данных результатами
* написание программного кода на языке python
* тестирование разработанного алгоритма
* компьютерное моделирование зависимости механических свойств от концентрации второго компонента сплава путем создания модели кубической регрессии
* анализ полученных результатов

**Актуальность**<br>
Наш проект актуален в современную эпоху инженерного материаловедения и позволяет:
* Исследовать взаимосвязи между составом сплавов, технологическими параметрами обработки, их физико-механическими свойствами
* Выбирать материалы для изделий различного назначения
Разработка позволяет ускорить компьютерный анализ физически-механических свойств материалов, и как следствие технологических процессов, а также вносить
обновленные данные по результатам испытаний

**Использованные библиотеки и модули**<br>
* `google.auth`, `httplib2`, `apiclient`, `os.path` – подключение к Google Sheets API, Google Drive API, Google Cloud, авторизация в аккаунте Google и предоставления прав для просмотра и редактирования файла
* `pygsheet` – чтение данных из таблицы Google Sheets и иъ конвертация в `DataFrame`
* `pandas` – запись `DataFrame` в csv-файл в процессе конвертации, чтение из csv-файла в виде `DataFrame` в основной части кода приложения, чтение значений из `DataFrame`, преобразование `DataFrame` в таблицу типа `ndarray`
* `numpy` – работа с созданной таблицей `ndarray`, создание трех моделей кубической регрессии с помощью модуля `numpy.poly1d`
* `matplotlib` – создание графиков уравнений кубической регрессии (зависимость свойств от состава), их вывод на экран и сохранение в виде png-изображения

## Использование программы
1. Скачать `main.py`, `conventer.py`.
2. Скачать файлы `Cu-Ni Mechanical properties.csv`, `Cu-Al Mechanical properties.csv`, `Cu-Zn Mechanical properties.csv`. Поместить все в одну папку проекта.
3. Запустить `main.py`
Для более подробного описания см. [ниже](#описание-работы-программы)

### Описание работы программы
В открытой онлайн-таблице [Mechanical properties of alloys](https://docs.google.com/spreadsheets/d/1rwr_pypXogXQWyv67b8-2ck14h6mwW8ACusTRwfIlVg/edit?usp=sharing) в Google Sheets находится база данных реальных производственных сплавов сплавов систем медь-никель, медь-алюминий и медь-цинк и их механические свойства, взятые из открытых [источников](#источники). На основе этих данных программа может спрогнозировать механические свойства сплава с новой указанной концентрацией компонентов.<br>
<br>
С помощью модуля `conventer` листы из таблицы [Mechanical properties of alloys](https://docs.google.com/spreadsheets/d/1rwr_pypXogXQWyv67b8-2ck14h6mwW8ACusTRwfIlVg/edit?usp=sharing) считываются программой и конвертируются в csv-файлы, сохраняя их в папке проекта. Запуск этого модуля необходим в случае, если информация в открытой онлайн-таблице [Mechanical properties of alloys](https://docs.google.com/spreadsheets/d/1rwr_pypXogXQWyv67b8-2ck14h6mwW8ACusTRwfIlVg/edit?usp=sharing) была изменена и требуется синхронизировать изменения с локально расположенными csv-файлами, или создать эти файлы, если в папке проекта их еще нет. *Редактировать таблицу может любой, кто имеет права редактора в ней. Обновлять и создавать csv-файлы может лишь владелец программы. Поэтому вместе с conventer.py и main.py необходимо также скачать приложенные csv-файлы, не меняя названия, иначе программе неоткуда будет брать значения.* <br>
Если обновление csv-файлов не требуется, модуль `conventer`, будучи импортированным в `main` и инициализируясь, присваивает переменным соответствующие датафреймы, считанные из csv-файлов, поэтому готовые csv-файлы уже должны быть загружены локально.<br>
<br>
На вход программа получает следующие данные:<br>
1. Систему, свойства сплава которой требуется спрогнозировать:
```
Системы:
    1 - Система медь-никель (Cu-Ni)
    2 - Система медь-алюминий (Cu-Al)
    3 - Система медь-цинк (Cu-Zn)
Выбранная система: 
```
В случае, если введенного значения нет в предложенном списке, или оно не относится к типу данных `int`, то программа выведет соответствующие предупреждения:
```
Системы:
    1 - Система медь-никель (Cu-Ni)
    2 - Система медь-алюминий (Cu-Al)
    3 - Система медь-цинк (Cu-Zn)
Выбранная система: 4

Наша база данных сплавов не настолько богатая, и системы 4 пока нет в списке.
```
```
Системы:
    1 - Система медь-никель (Cu-Ni)
    2 - Система медь-алюминий (Cu-Al)
    3 - Система медь-цинк (Cu-Zn)
Выбранная система: ээ.. мне, пожалуйста, медь с цинком

Неверный формат ввода.
```
2. Концентрацию второго компонента выбранной системы:
```
Концентрация второго компонента выбранной системы:
```
В случае, если введеное значение концентрации не принадлежит отрезку [0, 100] или не относится к типу данных `int`, то программа выведет соответствующие предупреждения:
```
Концентрация второго компонента выбранной системы: 100500
Концентрация второго (легирующего) компонента должна находится в пределах от 0 до 100%
```
```
Концентрация второго компонента выбранной системы: сорок шесть с половиной процентов
Неверный формат ввода.
```
Также на основе выбранной системы и указанной концентрации программа создаст название сплава в соответствии с принятым форматом и запишет его в виде строки в переменную `alloy_name`:
```
alloy_name = f'{alloy_dict[user_system][0][:2]}-{int(user_concentration // 1)},' \
             f'{int(user_concentration % 1)}%{alloy_dict[user_system][0][3:-2]}'
```
Далее программа с помощью модуля `numpy.poly1d` создает три модели кубической регрессии для каждого из механических свойств (твердости, прочность и пластичности), т. е. функцию вида ``y = a0 + a1*x + a2*x**2 + a3*x**3``, и подбирает такие коэффициента `a0`, `a1`, `a2`, `a3`, чтобы отклонение любого спрогнозированного и экспериментального значения было минимальным. Подробнее см. [Регрессионный анализ](https://habr.com/ru/articles/690414 "Регрессионный анализ на Хабре") и [Метод наименьших квадратов](https://habr.com/ru/articles/672540 "МНК на Хабре").
```
hardness_model = np.poly1d(np.polyfit(concentration, hardness, 3))
toughness_model = np.poly1d(np.polyfit(concentration, toughness, 3))
plasticity_model = np.poly1d(np.polyfit(concentration, plasticity, 3))
```
С помощью `matplotlib` строятся графики рассчитанных функций с указанными на ними пользовательскими значениями концентрации и спрогронизрованными значениями механических свойств.
```
polyline = np.linspace(1, max_concentration + 10, 500)
fig, axs = plt.subplots(1, 3, figsize=(14, 6))
axs[0].scatter(user_concentration, hardness_model(user_concentration), c='blue', label='Прогонзируемые')
axs[0].plot(polyline, hardness_model(polyline), c='red')
axs[0].scatter(concentration, hardness, c='red', label='Исходные')
axs[0].set_title(f'Твердость, {user_alloy.columns[1]}') # Для разных систем твердость измеряется в разных ед. изм.
```
*Аналогично для трех графиков*<br>
<br>
После окончания работы программа выводит графики зависимости свойств от концентраций<br>
<br>
![image](https://github.com/alphori/AlloyProperties/assets/137003036/e23e54cb-881b-4552-a992-d7bac0dcccff)<br>
<br>
В тоже время в консоли программа выводит датасет выбранной системы:
```
 Механические свойства сплавов системы Cu-Ni:
    Second component concentration   HV  Tensile Strength N/mm^2, MPa   Elongation, %  
0                               2   75                           220                15  
1                               6   80                           250                18  
2                              10   95                           300                30 
3                              25  100                           290                33
4                              30  120                           350                35
5                              44  160                           420                38
6                              99  120                           190                 3
```
И спрогнозированные свойства сплава с указанной концентрацией:
```
Механические свойства сплава Cu-33,0%Ni
Твердость: 128.2 HRB
Предел прочности: 361.7 МПа
Пластичность: 36.9%
```
Иногда после этого программа может выдать сообщение следующего содержания:
```
ВНИМАНИЕ: Указанное значение концентрации лежит далеко от интервала концентраций (0-37%), заданного в базе данных сплавов этой системы.
Прогнозируемые значения некоторых механических свойств могут значительно отличаться от реальных.
```
Связано это с тем, что указанная концентрация сплава слишком сильно отличается от тех концентраций, которые представлены в датасете.
> *Краткая теоретическая справка:*<br>
> <br>
> Для производственных целей чаще всего используются сплавы определенных, узких интервалов концентрации компонентов. Например, среди медноникелиевых сплавов наиболее часто используются сплавы и 5-10% Ni, и механические свойства этих сплавов широко известны. Но, например, сплав 60% Cu и 40% Ni не используется в отрасли, поэтому механические свойства такого сплава легче найти экспериментально, чем изучая открытые справочники или научные статьи. Так как в датасете [Mechanical properties of alloys](https://docs.google.com/spreadsheets/d/1rwr_pypXogXQWyv67b8-2ck14h6mwW8ACusTRwfIlVg/edit?usp=sharing) расположены механические свойства подобных реальных сплавов, взятые из открытых источников, для некоторых систем известны механические свойства не для всего интервала концентрации от 0 до 100% (Например, в датасете для медно-цинковых сплавов максимальная концентрация цинка составляет 37%). В случае, если введенная пользователем концентрация второго компонента выбранной системы лежит далеко вне интервала, представленного в датасете, модель не сможет корректно спрогнозировать значения свойств ввиду отсутствия достаточного количества данных, и в конце работы выдаст следующее сообщение.<br>

После закрытия окна с графиками, программа предложит сохранить их в качестве png-изображения в папку с проектом.
```
Сохранить текущие графики в виде png-изображения?
1 - Да, сохранить
0 - Нет, не сохранять
```
Если пользователь соглашается, то в папке с проектом появляется png-изображение графиков с названием, записанным в `alloy_name`, и программа завершает работу.<br>
<br>
### Варианты доработки программы
* Название таблицы и листов строго определены. То есть, если изменить их, программа даст сбой и откажется работать. В качестве улучшения программы, следует прописать такой код, который выполнялся бы независимо от названий листов и самой таблицы.
* Аналогично строго определены порядок и название столбцов. То есть, если в систему добавить еще один столбец с другим механическим свойством, программа не будет его обрабатывать, а если удалить существующий, программа выдаст ошибку. В качестве улучшения, следует автоматизировать процесс чтения столбцов и построения модели и графика для каждого из них, независимо от порядка и названия.
* Возможность обновления локальных csv-файлов доступна только владельцу программы, чей аккаунт зарегистрирован как Owner в настройках приложения AlloyProperties в Google Cloud. Один из вариантов улучшения программы - предоставления функционала `conventer.py` всем пользователем, чьим аккаунтам выданы права чтения или редактирования таблицы [Mechanical properties of alloys](https://docs.google.com/spreadsheets/d/1rwr_pypXogXQWyv67b8-2ck14h6mwW8ACusTRwfIlVg/edit?usp=sharing)

### Источники
1. [Copper-Nickel Alloys: Properties, Processing, Applications](https://www.copper.org/applications/marine/cuni/properties/DKI_booklet.html#1.4)
2. [Guide to Nickel Aluminium Bronze for Engineers](https://copper.org/applications/marine/nickel_al_bronze/pub-222-nickel-al-bronze-guide-engineers.pdf)
3. [Mechanical behavior of Al–Cu binary alloy system/ Cu particulates reinforced metal-metal composites](https://www.sciencedirect.com/science/article/pii/S2590123019300465)
4. [https://nickelinstitute.org/media/1771/propertiesofsomemetalsandalloys_297_.pdf](https://nickelinstitute.org/media/1771/propertiesofsomemetalsandalloys_297_.pdf)
5. [NumPy documantation](https://numpy.org/doc/stable/reference/generated/numpy.poly1d.html)
6. [Как выполнить полиномиальную регрессию в Python](https://www.codecamp.ru/blog/polynomial-regression-python/)
