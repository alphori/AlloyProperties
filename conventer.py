import pygsheets as gs
import pandas as pd

# Считывает информацию с листов Google Sheets и перезаписывет соответствующие csv-файлы, только если запущен напрямую.
# При импорте этого модуля в main.py, просто создает датафреймы из csv-файлов

if __name__ == '__main__':
    # Чтение листов Google Sheets
    gc = gs.authorize()
    sheet = gc.open('Mechanical properties of alloys')
    wks1_cuni = sheet.worksheet('title', 'Cu-Ni')
    wks2_cual = sheet.worksheet('title', 'Cu-Al')
    wks3_cuzn = sheet.worksheet('title', 'Cu-Zn')

    # Конвертация создание dataframe-a и его конвертация в CSV файл
    cuni = wks1_cuni.get_as_df()
    cuni.to_csv('Cu-Ni Mechanical Properties.csv', ',', index=False)
    fec = wks2_cual.get_as_df()
    fec.to_csv('Cu-Al Mechanical Properties.csv', ',', index=False)
    pbsn = wks3_cuzn.get_as_df()
    pbsn.to_csv('Cu-Zn Mechanical Properties.csv', ',', index=False)

cuni = pd.read_csv('Cu-Ni Mechanical Properties.csv')
cual = pd.read_csv('Cu-Al Mechanical Properties.csv')
cuzn = pd.read_csv('Cu-Zn Mechanical Properties.csv')
