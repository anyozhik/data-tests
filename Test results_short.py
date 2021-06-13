# We have made several tests to choose the best product design. In our dataset we have information about orders, their status, profit, type (desktop/mobile) and tests. Our aim is to range all tests and evaluate their effectiveness.

import pandas as pd
import numpy as np

def setparameters():
    pd.set_option("display.max_rows", 200)
    pd.set_option("display.max_columns", 100)
    pd.set_option("display.max_colwidth", 200)
    pd.set_option('display.expand_frame_repr', False)

setparameters()

tests_data=pd.read_csv('tests.csv', sep=';', encoding='cp1251')

def numeric(dataframe):
    dataframe=pd.to_numeric(dataframe, errors='coerce')
    return dataframe

tests_data["Профит"] = numeric(tests_data["Профит"])
tests_data['Стоимость_заказа'] = numeric(tests_data['Стоимость_заказа'])

# Let's make the rating of positiveness using data from column "Статус"
status_dict={'Оплачен':'Позитивный', 'Не оплачен': 'Негативный', 'Забронирован':'Нейтральный', 'Ошибка':'Негативный'}
tests_data['Оценка']=tests_data['Статус'].map(status_dict)
table1=tests_data[['Тест', 'Оценка']].pivot_table(index='Тест', columns='Оценка', aggfunc=len, margins=True)
table2 = table1.div(table1.iloc[:,-1], axis=0 )
print(table2.sort_values(by='Позитивный', ascending=False))

# Now we can find the tests with the highest ARPPU (Profit/number of orders). Note: we use only orders with positive results; the best tests must have raiting of positivness al least 77%
filter_positiv=tests_data['Оценка']=='Позитивный'
filter_mobile=tests_data['Тип устройства']=='mobile'
filter_desktop=tests_data['Тип устройства']=='desktop'
tests_data2=tests_data.loc[filter_positiv & filter_mobile]
tests_data3=tests_data.loc[filter_positiv & filter_desktop]
mobile_groupby=tests_data2.groupby('Тест')['Профит'].agg(['sum', 'count'])
desktop_groupby=tests_data3.groupby('Тест')['Профит'].agg(['sum', 'count'])

# Add a column for calcuting 'ARPPU' for mobile devices to choose the best one (taking into account the raiting of positivensess)
mobile_groupby['ARPPU']=mobile_groupby['sum']/mobile_groupby['count']
print(mobile_groupby.sort_values(by='ARPPU',ascending=False))
print('В категории мобильных устройств лучщий показатель у теста под номером 15 (ARPPU=806.204762), его рейтинг позитивности составляет 78,98%')

# Add a column for calcuting 'ARPPU' for desktop devices to choose the best one (taking into account the raiting of positivensess)
desktop_groupby['ARPPU']=desktop_groupby['sum']/desktop_groupby['count']
print(desktop_groupby.sort_values(by='ARPPU',ascending=False))
print('В категории стационарных компьютеров лучщий показатель у теста под номером 11, однако с учетом рейтинга позитивности лучший результат будет у теста 6 (APRU=800.720385, уровень позитивности 78,97%')

# Let us choose the best test for each price group (taking into account the raiting of positivensess)
price_bins=[0, 10000.01, 25000, 50000, 100000, 300000, 800000]
tests_data['Стоимость заказов по группам']=pd.cut(tests_data['Стоимость_заказа'], bins=price_bins)
test_data4=tests_data.loc[filter_positiv]
test_groupbyvalue=test_data4.groupby(['Тест', 'Стоимость заказов по группам'])['Профит'].agg(['sum', 'count'])
test_groupbyvalue['ARPPU']=test_groupbyvalue['sum']/test_groupbyvalue['count']
print(test_groupbyvalue.sort_values(by=['Стоимость заказов по группам', 'ARPPU'], ascending=False))

print('С учетом данных рейтинга позитивности в ценовом интервале от 0-10000.01 лидирует тест №2 (ARPPU=354.318140), в интервале от 10000.01-25000 - тест №6 (ARPPU=699.288403),\
      в интервале от 25000-50000 - тест №6 (ARPPU=1271.434286),в интервале от 50000-100000 - тест №7 (ARPPU=2087.712000), в интервале от 100000-300000 - тест №6 (ARPPU=4564.04),\
      в интервале от 300000-800000 также тест №6 (ARPPU=1199.00)')






