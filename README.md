# Итоговый проект по программе Цифровой кафедры «Средства разработки инженерных приложений»

Вьюшин Егор Олегович, БМТ-21-1<br>
Росоленко Софья Кирилловна, БМТ-21-2<br>

Цифровая кафедра. Средства разработки инженерных приложений.

## Прогнозирование механических свойств сплава на основе концентрации легирующего компонента

**Цель**<br>
разработать приложение, способное cпрогнозировать механические свойства сплава на основе концентрации легирующего компонента
и визуализировать их изменения в виде графиков зависимостей свойств от концентраций

**Задачи**
* формирование необходимого для исследования алгоритма
* создание обновляющегося dataframe с измененными в базе данных результатами
* написание программного кода на языке python
* тестирование разработанного алгоритма
*компьютерное моделирование зависимости механических свойств от концентрации второго компонента сплава путем создания модели кубической регрессии
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

### Описание работы программы
В открытой онлайн-таблице Google Sheets находится база данных реальных производственных сплавов сплавов систем медь-никель, медь-алюминий и медь-цинк и их механические свойства. На основе этих данных программа может спрогнозировать механические свойства сплава с новой указанной концентрацией компонентов.<br>
<br>
С помощью модуля `conventer` листы из таблицы Google Sheets считываются программой и конвертируются в csv-файлы, сохраняя их в папке проекта. Запуск этого модуля необходим в случае, если информация в открытой онлайн-таблице Google Sheets была изменена и требуется синхронизировать изменения с локально расположенными csv-файлами, или создать эти файлы, если в папке проекта их еще нет. *(Редактировать таблицу может любой, кто имеет права редактора в ней. Обновлять csv-файлы же может лишь владелец программы)* <br>
Если обновление csv-файлов не требуется, модуль `conventer`, будучи импортированным в `main` и инициализируясь, присваивает переменным соответствующие датафреймы, считанные из csv-файлов.<br>
<br>
На вход программа получает следующие данные:<br>
* Систему, свойства сплава которой требуется спрогнозировать:
```
Системы:
    1 - Система медь-никель (Cu-Ni)
    2 - Система медь-алюминий (Cu-Al)
    3 - Система медь-цинк (Cu-Zn)
Выбранная система: 
```
В случае, если введенного значения нет в предложенном списке, или оно не относится к типу данных `int`, то программа выведет соответствующие предупреждения
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
* Концентрацию второго компонента выбранной системы:
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
Для производственных целей используются сплавы определенных, узких интервалов концентрации компонентов. Например, среди медноникелиевых сплавов наиболее часто используются сплавы и 5-10% Ni, и механические свойства этих сплавов широко известны. Но, например, сплав 60% Cu и 40% Ni не используется в отрасли, поэтому механические свойства такого сплава легче найти экспериментально, чем изучая открытые справочники или научные статьи. Так как в датасете в Google Sheets расположены механические свойства подобных реальных сплавов, для некоторых систем известны механические свойства не для всего интервала концентрации от 0 до 100% (Например, в датасете для медно-цинковых сплавов максимальная концентрация цинка составляет 37%). В случае, если введенная пользователем концентрация второго компонента выбранной системы лежит далеко вне интервала, представленного в датасете, программа в самом конце выдаст вот такое сообщение
```
ВНИМАНИЕ: Указанное значение концентрации лежит далеко от интервала концентраций (0-37%), заданного в базе данных сплавов этой системы.
Прогнозируемые значения некоторых механических свойств могут значительно отличаться от реальных.
```









