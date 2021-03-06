import requests
from bs4 import BeautifulSoup
import json
import csv

# url = 'https://health-diet.ru/table_calorie/?utm_source=leftMenu&utm_medium=table_calorie'
#
#
headers = {
    'accept': '*/*',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'
}
# req = requests.get(url, headers=headers)
# src = req.text
# print(src)
#
# with open('index.html', 'w') as file:  # Запишем код страницы в файл
#     file.write(src)

# with open('index.html') as file:    # Открыли и сохранили файл в переменную
#     src = file.read()
#
# soup = BeautifulSoup(src, 'lxml')
# all_products_hrefs = soup.find_all(class_='mzr-tc-group-item-href')
#
# all_categories_dict = {}
# for item in all_products_hrefs:
#     item_text = item.text
#     item_href = 'https://health-diet.ru' + item.get('href')
#
#     all_categories_dict[item_text] = item_href
#
# with open('all_categories_dict.json', 'w') as file:                       # Сохраняем наши ссылки в json
#     json.dump(all_categories_dict, file, indent=4, ensure_ascii=False)    # indent=4 - чтобы не в строку, ensure_ascii=False - чтобы понимал кодировку кирилицы


with open('all_categories_dict.json') as file:
    all_categories = json.load(file)                                        # Сохраняем в переменную

iteration_count = int(len(all_categories))-1
count = 0
print(f'Всего итераций: {iteration_count}')

for categories_name, categories_href in all_categories.items():

    rep = [',', ' ', '-', "'"]                        #Создадим словарь с символами которые хотим заменить на "_"
    for item in rep:                             #бежим по словарю
        if item in categories_name:              #условие если символ есть в categories_name то
            categories_name = categories_name.replace(item, '_')         #то меняем символ на "_"

    req = requests.get(url=categories_href, headers=headers)
    src = req.text

    with open(f'data/{count}_{categories_name}.html', 'w') as file:    #Сохраним наши ссылки в html в директорию data и номер станицы будет в имени
        file.write(src)

    with open(f'data/{count}_{categories_name}.html') as file:    #Откроем код страницы и сохраним в переменную
        src = file.read()

    soup = BeautifulSoup(src, 'lxml')

    #Проверка страницы на наличие таблицы с продуктами
    alert_block = soup.find(class_='uk-alert-danger')
    if alert_block is not  None:
        continue

    #Собираем заголовки таблицы
    table_head = soup.find(class_='mzr-tc-group-table').find('tr').find_all('th')

    product = table_head[0].text
    calories = table_head[1].text
    proteins = table_head[2].text
    fats = table_head[3].text
    carbohydrates = table_head[4].text

    with open(f'data/{count}_{categories_name}.csv', 'w', encoding='utf-8') as file:  #Сохраняем нашу таблицу в csv
        writer = csv.writer(file)
        writer.writerow(
            (
                product,
                calories,
                proteins,
                fats,
                carbohydrates
            )
        )

    # Собираем данные продуктов
    product_data = soup.find(class_='mzr-tc-group-table').find('tbody').find_all('tr')

    product_info = []
    for item in product_data:
        product_tds = item.find_all('td')

        title = product_tds[0].find('a').text
        calories = product_tds[1].text
        proteins = product_tds[2].text
        fats = product_tds[3].text
        carbohydrates = product_tds[4].text

        product_info.append(
            {
                'Title': title,
                'Calories': calories,
                'Proteins': proteins,
                'Fats': fats,
                'Carbohydrates': carbohydrates
            }
        )

        with open(f'data/{count}_{categories_name}.csv', 'a', encoding='utf-8') as file:  # дозаписываем нашу таблицу в csv
            writer = csv.writer(file)
            writer.writerow(
                (
                    title,
                    calories,
                    proteins,
                    fats,
                    carbohydrates
                )
            )

    with open(f'data/{count}_{categories_name}.json', 'a', encoding='utf-8') as file:
        json.dump(product_info, file, indent=4, ensure_ascii=False)

    count += 1
    print(f'# Итерация {count}. {categories_name} записан...')
    iteration_count = iteration_count - 1

    if iteration_count == 0:
        print('Работа завершена')
        break

    print(f'Осталось итераций: {iteration_count}')


