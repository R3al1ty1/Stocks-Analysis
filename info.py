import os
import pandas as pd
from tabulate import tabulate

# Получаем текущую директорию
current_directory = os.path.dirname(os.path.abspath(__file__))

# Путь к папке с файлами CSV
dataset_directory = os.path.join(current_directory, 'dataset')

# Списки для хранения общей информации
columns_info = []

# Читаем все файлы в папке "dataset"
for filename in os.listdir(dataset_directory):
    if filename.endswith(".csv"):
        file_path = os.path.join(dataset_directory, filename)

        # Читаем файл и получаем информацию
        data = pd.read_csv(file_path)

        # Получаем информацию о колонках
        columns_info.extend([(column, data[column].dtype, data[column].count(), len(data)) for column in data.columns])

# Создаем таблицу
table_data = pd.DataFrame(columns_info, columns=["Column Name", "Data Type", "Non-Null Count", "Total Count"])

# Группируем данные по колонкам и выводим общую статистику
table_summary = table_data.groupby("Column Name").agg({
    "Data Type": "first",
    "Non-Null Count": "sum",
    "Total Count": "sum"
}).reset_index()

# Выводим таблицу
print(tabulate(table_summary, headers="keys", tablefmt="grid", showindex=False))
