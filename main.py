import os
import pandas as pd
import matplotlib.pyplot as plt

# Получаем текущую директорию
current_directory = os.path.dirname(os.path.abspath(__file__))

# Путь к папке с файлами CSV
dataset_directory = os.path.join(current_directory, 'dataset')

# Словарь для соответствия символа компании и её названия
company_names = {
    'T': 'AT&T',
    'EA': 'Electronic Arts',
    'OMC': 'Omnicom Group',
    'EBAY': 'eBay',
    'HAS': 'Hasbro',
    'MCD': 'McDonald\'s',
    'COST': 'Costco',
    'KO': 'Coca-Cola',
    'HSY': 'The Hershey Company',
    'MRO': 'Marathon Oil',
    'WMB': 'Williams Companies',
    'OXY': 'Occidental Petroleum',
    'AXP': 'American Express',
    'BAC': 'Bank of America',
    'C': 'Citigroup',
    'PFE': 'Pfizer',
    'CAH': 'Cardinal Health',
    'SYK': 'Stryker',
    'LMT': 'Lockheed Martin',
    'DOV': 'Dover Corporation',
    'NSC': 'Norfolk Southern',
    'MSFT': 'Microsoft',
    'AAPL': 'Apple',
    'IBM': 'IBM',
    'ECL': 'Ecolab',
    'PKG': 'Packaging Corporation of America',
    'VMC': 'Vulcan Materials',
    'PLD': 'Prologis',
    'EQR': 'Equity Residential',
    'WY': 'Weyerhaeuser',
    'FE': 'FirstEnergy',
    'NI': 'NiSource',
    'CNP': 'CenterPoint Energy'
}

# Словарь для соответствия сектора и компаний в нём
sectors = {
    'Communication Services': ['T', 'EA', 'OMC'],
    'Consumer Discretionary': ['EBAY', 'HAS', 'MCD'],
    'Consumer Staples': ['COST', 'KO', 'HSY'],
    'Energy': ['MRO', 'WMB', 'OXY'],
    'Financials': ['AXP', 'BAC', 'C'],
    'Health Care': ['PFE', 'CAH', 'SYK'],
    'Industrials': ['LMT', 'DOV', 'NSC'],
    'Information Technology': ['MSFT', 'AAPL', 'IBM'],
    'Materials': ['ECL', 'PKG', 'VMC'],
    'Real Estate': ['PLD', 'EQR', 'WY'],
    'Utilities': ['FE', 'NI', 'CNP']
}

sectorsRU = {
'Communication Services': 'Коммуникационные сервисы',
    'Consumer Discretionary': 'Потребительская деятельность',
    'Consumer Staples': 'Товары народного потребления',
    'Energy': 'Энергетика',
    'Financials': 'Финансы',
    'Health Care': 'Здравоохранение',
    'Industrials': 'Промышленность',
    'Information Technology': 'Информационные технологии',
    'Materials': 'Материалы',
    'Real Estate': 'Недвижимость',
    'Utilities': 'Коммунальные услуги'
}

# Построение графика для каждого сектора
plt.figure(figsize=(12, 8))

# Создание общего DataFrame для хранения средних значений процентного изменения
average_df = pd.DataFrame()

for sector, companies in sectors.items():
    sector_prices = []

    for company_symbol in companies:
        file_path = os.path.join(dataset_directory, f'{company_symbol}.csv')
        df = pd.read_csv(file_path, parse_dates=['Date'], dayfirst=True)
        df = df[df['Date'] >= '2000-01-01']

        # Вычисление процентного изменения от начальной цены
        initial_price = df['Close'].iloc[0]
        df['Percent Change'] = ((df['Close'] - initial_price) / initial_price) * 100

        # Добавление процентного изменения к списку для сектора
        sector_prices.append(df[['Date', 'Percent Change']])

    # Объединение данных компаний в секторе на основе столбца 'Date'
    sector_data = pd.DataFrame({'Date': df['Date']})
    for i, company_symbol in enumerate(companies):
        sector_prices[i] = sector_prices[i].set_index('Date')
        sector_data = pd.merge(sector_data, sector_prices[i], left_on='Date', right_index=True, how='left')
        sector_data = sector_data.rename(columns={'Percent Change': company_symbol})

    # Рассчет среднего значения процентного изменения для компаний в секторе
    sector_data['Average'] = sector_data.iloc[:, 1:].mean(axis=1)

    # Построение графика среднего процентного изменения и названия сектора в легенде
    plt.plot(sector_data['Date'], sector_data['Average'], label=f'{sectorsRU[sector]}')

    # Добавление данных в общий DataFrame
    average_df = pd.concat([average_df, sector_data[['Date', 'Average']]], axis=1)

# Настройки графика
plt.title('Среднее процентное изменение цен на закрытие по секторам')
plt.xlabel('Дата')
plt.ylabel('Среднее процентное изменение от начальной цены')
plt.legend()
plt.show()

# Промежутки времени
time_intervals = [
    ('2007-01-01', '2008-12-31', 'С 2007 по конец 2008'),
    ('2019-01-01', '2020-12-31', 'С 2019 по конец 2020'),
    ('2021-01-01', '2022-12-31', 'С 2021 по конец 2022')
]

# Построение графиков для каждого промежутка времени
for start_date, end_date, title in time_intervals:
    plt.figure(figsize=(12, 8))

    # Создание общего DataFrame для хранения средних значений процентного изменения
    average_df = pd.DataFrame()

    for sector, companies in sectors.items():
        sector_prices = []

        for company_symbol in companies:
            file_path = os.path.join(dataset_directory, f'{company_symbol}.csv')
            df = pd.read_csv(file_path, parse_dates=['Date'], dayfirst=True)
            df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]

            # Вычисление процентного изменения от начальной цены
            initial_price = df['Close'].iloc[0]
            df['Percent Change'] = ((df['Close'] - initial_price) / initial_price) * 100

            # Добавление процентного изменения к списку для сектора
            sector_prices.append(df[['Date', 'Percent Change']])

        # Объединение данных компаний в секторе на основе столбца 'Date'
        sector_data = pd.DataFrame({'Date': df['Date']})
        for i, company_symbol in enumerate(companies):
            sector_prices[i] = sector_prices[i].set_index('Date')
            sector_data = pd.merge(sector_data, sector_prices[i], left_on='Date', right_index=True, how='left')
            sector_data = sector_data.rename(columns={'Percent Change': company_symbol})

        # Рассчет среднего значения процентного изменения для компаний в секторе
        sector_data['Average'] = sector_data.iloc[:, 1:].mean(axis=1)

        # Построение графика среднего процентного изменения и названия сектора в легенде
        plt.plot(sector_data['Date'], sector_data['Average'], label=f'{sectorsRU[sector]}')

        # Добавление данных в общий DataFrame
        average_df = pd.concat([average_df, sector_data[['Date', 'Average']]], axis=1)

    # Настройки графика
    plt.title(f'Среднее процентное изменение цен на закрытие по секторам ({title})')
    plt.xlabel('Дата')
    plt.ylabel('Среднее процентное изменение от начальной цены')
    plt.legend()
    plt.show()

total_volume_df = pd.DataFrame()

for sector, companies in sectors.items():
    sector_volumes = []

    for company_symbol in companies:
        file_path = os.path.join(dataset_directory, f'{company_symbol}.csv')
        df = pd.read_csv(file_path, parse_dates=['Date'], dayfirst=True)

        # Добавление объема продаж к списку для сектора
        sector_volumes.append(df[['Date', 'Volume']])

    # Объединение данных компаний в секторе на основе столбца 'Date'
    sector_data = pd.DataFrame({'Date': df['Date']})
    for i, company_symbol in enumerate(companies):
        sector_volumes[i] = sector_volumes[i].set_index('Date')
        sector_data = pd.merge(sector_data, sector_volumes[i], left_on='Date', right_index=True, how='left')
        sector_data = sector_data.rename(columns={'Volume': company_symbol})

    # Рассчет суммарного объема продаж для компаний в секторе
    sector_data['Total Volume'] = sector_data.iloc[:, 1:].sum(axis=1)

    # Построение bar chart для суммарного объема продаж и названия сектора в легенде
    plt.bar(sectorsRU[sector], sector_data['Total Volume'].sum() / 1e6, label=f'{sectorsRU[sector]}')  # Делим на 1 миллион для удобства

    # Добавление данных в общий DataFrame
    total_volume_df = pd.concat([total_volume_df, sector_data[['Date', 'Total Volume']]], axis=1)

# Настройки графика
plt.title('Объем продаж акций по секторам за все время (в миллионах)')
plt.ylabel('Объем продаж')
plt.xticks(rotation=45, ha="right", fontsize=8)  # Поворот подписей секторов на 45 градусов и уменьшение размера шрифта
plt.legend()
plt.tight_layout()  # Автоматическая коррекция расположения подписей
plt.show()

average_daily_volume_df = pd.DataFrame()

for sector, companies in sectors.items():
    sector_volumes = []

    for company_symbol in companies:
        file_path = os.path.join(dataset_directory, f'{company_symbol}.csv')
        df = pd.read_csv(file_path, parse_dates=['Date'], dayfirst=True)

        # Добавление объема продаж в день к списку для сектора
        df['Daily Volume'] = df['Volume'] / df['Date'].nunique()  # Рассчет среднего объема продаж в день
        sector_volumes.append(df[['Date', 'Daily Volume']])

    # Объединение данных компаний в секторе на основе столбца 'Date'
    sector_data = pd.concat(sector_volumes, axis=0, ignore_index=True)  # Используем pd.concat
    sector_data = sector_data.groupby('Date').mean().reset_index()

    # Рассчет среднего объема продаж в день для компаний в секторе
    sector_data['Average Daily Volume'] = sector_data['Daily Volume']

    # Добавление данных в общий DataFrame
    if average_daily_volume_df.empty:
        average_daily_volume_df = sector_data[['Date', 'Average Daily Volume']]
    else:
        average_daily_volume_df = average_daily_volume_df.merge(sector_data[['Date', 'Average Daily Volume']], on='Date', how='outer', suffixes=('', f'{sectorsRU[sector]}'))

# Convert the 'Date' column to datetime
average_daily_volume_df['Date'] = pd.to_datetime(average_daily_volume_df['Date'])

# Remove duplicate dates
average_daily_volume_df = average_daily_volume_df.groupby('Date').mean().reset_index()

# Plot the pie chart
plt.figure(figsize=(8, 8))
labels = sectorsRU.values()
plt.pie(average_daily_volume_df.iloc[:, 1:].mean(), labels=labels, autopct='%1.1f%%', startangle=140)
plt.title('Распределение среднего объема продаж в день по секторам')
plt.tight_layout()
plt.show()