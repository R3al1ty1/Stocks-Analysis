import os
import pandas as pd

# Получаем текущую директорию
current_directory = os.path.dirname(os.path.abspath(__file__))

# Путь к папке с файлами CSV
dataset_directory = os.path.join(current_directory, 'dataset')

# Переменные для общей статистики
total_duplicates = 0
total_missing_values = 0

# Переменные для общей описательной статистики
total_descriptive_stats = pd.DataFrame()

# Переменная для корреляционной матрицы
total_correlation_matrix = pd.DataFrame()

# Проход по всем CSV-файлам в датасете
for file_name in os.listdir(dataset_directory):
    if file_name.endswith('.csv'):
        file_path = os.path.join(dataset_directory, file_name)

        # Загрузка данных из CSV-файла
        data = pd.read_csv(file_path)

        # Поиск и удаление дубликатов
        duplicate_rows = data[data.duplicated()]
        if not duplicate_rows.empty:
            print(f"Найдены дубликаты строк в файле {file_name}:\n{duplicate_rows}")
            data = data.drop_duplicates()
            total_duplicates += len(duplicate_rows)
            print("Дубликаты удалены.")

        # Проверка наличия пропущенных значений
        missing_values = data.isnull().sum()
        if missing_values.sum() > 0:
            print(f"Найдены пропущенные значения в файле {file_name}:\n{missing_values}")
            data = data.dropna()
            total_missing_values += missing_values.sum()
            print("Строки с пропущенными значениями удалены.")

        # Сбор описательной статистики для текущего файла
        descriptive_stats = data.describe(include='all')

        # Замена NaN на "-" при выводе
        descriptive_stats = descriptive_stats.applymap(lambda x: '-' if pd.isna(x) else x)

        total_descriptive_stats = pd.concat([total_descriptive_stats, descriptive_stats], axis=1)

        # Добавление корреляционной матрицы
        numeric_data = data.select_dtypes(include=[float, int])  # Выбираем только числовые столбцы
        correlation_matrix = numeric_data.corr()
        total_correlation_matrix = pd.concat([total_correlation_matrix, correlation_matrix], axis=1)

# Вывод общей статистики
print(f"\nОбщее количество дубликатов: {total_duplicates}")
print(f"Общее количество пропущенных значений: {total_missing_values}")
print("\nОбщая описательная статистика:")
print(total_descriptive_stats)

# Вывод корреляционной матрицы
print("\nКорреляционная матрица:")
print(total_correlation_matrix)
