from bs4 import BeautifulSoup
import requests
import time
import csv
import os

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.5304.122 Safari/537.36',
    'accept': '*/*'
}

categories_lst = ['https://www.aurigininc.com/c/{0}/Hedge-Funds/{1}/1/All/1',
                  'https://www.aurigininc.com/c/{0}/Private-Equity-Funds/{1}/2/All/1',
                  'https://www.aurigininc.com/c/{0}/Venture-Capital-Funds/{1}/3/All/1',
                  'https://www.aurigininc.com/c/{0}/Investment-Management-Firms/{1}/4/All/1',
                  'https://www.aurigininc.com/c/{0}/Investment-Banking-Firms/{1}/5/All/1',
                  'https://www.aurigininc.com/c/{0}/Law-Firms/{1}/6/All/1',
                  'https://www.aurigininc.com/c/{0}/Accounting-Firms/{1}/7/All/1',
                  'https://www.aurigininc.com/c/{0}/Financial-Services-Companies/{1}/8/All/1',
                  'https://www.aurigininc.com/c/{0}/Banks/{1}/9/All/1'
                  ]

def get_countries_lst():
    url = 'https://www.aurigininc.com/c'

    r = requests.get(url=url, headers=headers)
    if r.status_code == 200:
        soup = BeautifulSoup(r.text, 'lxml')

        all_li = soup.find('ul', class_='cols3 countrylist country_cols clearfix').find_all('li')
        count = 0
        for li in all_li:
            try:
                link = 'https://www.aurigininc.com' + li.find('a').get('href')

                with open('countries.txt', 'a', encoding='utf-8') as file:
                    file.write(f'{link}\n')

                count += 1
            except:
                continue

def read_countries():
    countries = []
    with open('countries.txt', 'r', encoding='utf-8') as file:
        for line in file.readlines():
            countries.append(line)

    return countries

def create_csv(filename):
    file_path = f'data/{filename}.csv'
    isExist = os.path.exists(file_path)

    if not isExist:
        with open(file_path, 'w', encoding='utf-8', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                'Investment Banking Name', 'Country'
            ])
        return True
    else:
        return False

def create_folder():
    isExist = os.path.exists('data')

    if not isExist:
        os.makedirs('data')
        print('The folder was created!')

def get_category_request(category, filename):
    countries = read_countries()
    length = len(countries)

    total_count = 0
    for i, country in enumerate(countries):
        country_name = country.split('/')[-2].strip()
        country_short_name = country.split('/')[-1].strip()

        link = category.format(country_name, country_short_name).strip()
        r = requests.get(url=link, headers=headers)

        if i % 20 == 0:
            time.sleep(1)

        count = 0
        while True:
            soup = BeautifulSoup(r.text, 'lxml')
            all_li = soup.find('ul', class_='cols3 countrylist country_cols clearfix').find_all('li')

            for li in all_li:
                try:
                    firm_name = li.find('a').text.strip()

                    with open(f'data/{filename}.csv', 'a', encoding='utf-8', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow([
                            firm_name, country_name
                        ])
                    count += 1
                except:
                    continue
            try:
                next_page = 'https://www.aurigininc.com' + soup.find('a', class_='pagination_links c_next').get('href')
                r = requests.get(url=next_page)
            except:
                break

        print(f'{i + 1}/{length} - {country_name} - {count}')
        total_count += count

    print(f'Scraped {total_count} firms!\n')

def process_starting(category):
    category_name = category.split('/')[-5]
    filename = category_name.replace('-', '_')

    return category_name, filename

def main():
    hedge_funds = categories_lst[0]
    private_equity_funds = categories_lst[1]
    venture_capital_funds = categories_lst[2]
    investment_management_firms = categories_lst[3]
    investment_banking_firms = categories_lst[4]
    law_firms = categories_lst[5]
    accounting_firms = categories_lst[6]
    financial_services_companies = categories_lst[7]
    banks = categories_lst[8]

    while True:
        input_text = input(
            'Choose the category to scrape. Text only the digit!\n'
            'To stop the code text [q]\n'
            '- [1] Hedge Fund\n'
            '- [2] Private Equity Fund\n'
            '- [3] Venture Capital Fund\n'
            '- [4] Investment Management Firm\n'
            '- [5] Investment Banking Firm\n'
            '- [6] Law Firm\n'
            '- [7] Accounting Firm\n'
            '- [8] Financial Services Companies\n'
            '- [9] Banks\n'
            'Your choice: '
        )

        try:
            if input_text == 'q':
                print('You ended the running!\n')
                break
            elif int(input_text) == 1:
                choice = hedge_funds
            elif int(input_text) == 2:
                choice = private_equity_funds
            elif int(input_text) == 3:
                choice = venture_capital_funds
            elif int(input_text) == 4:
                choice = investment_management_firms
            elif int(input_text) == 5:
                choice = investment_banking_firms
            elif int(input_text) == 6:
                choice = law_firms
            elif int(input_text) == 7:
                choice = accounting_firms
            elif int(input_text) == 8:
                choice = financial_services_companies
            elif int(input_text) == 9:
                choice = banks
            else:
                print('Incorrect choice!\n')
        except:
            print('Incorrect symbol!\n')

        try:
            category_name, filename = process_starting(category=choice)
            print(f'Starting with {category_name} category.')

            create_folder()
            running = create_csv(filename)
            if running:
                get_category_request(choice, filename)
            else:
                print('This category was already scraped!\n')
        except:
            continue

if __name__ == '__main__':
    main()