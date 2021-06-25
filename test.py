import requests
import datetime
from bs4 import BeautifulSoup

"""
1)  На бесконечной в обе стороны белой полоске размеченной в клеточку находятся два робота. 
    Ровно одна из клеток на полоске - чёрная, и она находится между роботами. Вам необходимо 
    одинаково запрограммировать обоих роботов так, чтоб они встретились. Программа состоит из 
    нескольких строк, каждая из которых содержит ровно одну команду. Допустимые команды: 
    1) ML - сделать шаг на клетку влево и перейти к следующей строке программы; 
    2) MR - сделать шаг на клетку вправо и перейти к следующей строке программы; 
    3) IF FLAG - проверить, находимся ли мы на чёрной клетке. Если да,
       перейти к следующей строке программы, иначе, перейти к послеследующей строке программы; 
    4) GOTO N - перейти к N-й строке программы; На выполнение каждой из команд, 
       кроме GOTO у робота уходит 1 секунда. GOTO выполняется мгновенно.
       
Решение:
    1)ML
    2)IF FLAG
    3)GOTO5
    4)GOTO1
    5)ML
    6)ML
    7)GOTO 5
    

2) При входе в Музей лжи стоят три вазы, на одной из которых написано «Черные», на второй — «Белые»,
   на третьей — «Черные и белые». В одной из них лежат черные шары, в другой — белые, 
   в оставшейся — и черные, и белые. Все надписи заведомо ложны.
   Как определить содержимое каждой вазы, достав только один шар?
   
Решение:
    Взять шар из вазы «Черные и белые». Зная, что все надписи заведомо ложны, получаем,
    что в «Черные и белые» лежат либо белые, либо черные шары.
    Если шар что мы достали черный, то в «Черные» лежат белые, а в «Белые» лежат черные и белые.
    Если шар что мы достали белые, то в «Черные» лежат черные и белые, а в «Белые» лежат черные.

    
3) Напишите на любом языке программирования следующую задачу:
1. Вытащить из апи Центробанка (пример http://www.cbr.ru/scripts/XML_daily_eng.asp?date_req=11/11/2020)
   данные по переводу различных валют в рубли за последние 90 дней.
2. Результатом работы программы:  
 - нужно указать значение максимального курса валюты, название этой валюты и дату этого максимального значения.
 - нужно указать значение минимального курса валюты, название этой валюты и дату этого минимального значения.
 - нужно указать среднее значение курса рубля за весь период по всем валютам.

Решение:
    Представлено в коде ниже...
"""
class valute_stat_for_days:
    max_val = 0
    max_name = ""
    max_date = ""
    min_val = 1000
    min_name = ""
    min_date = ""
    val_avg = {}
    val_count = {}
    date_t = datetime.date.today()
    delta_day = datetime.timedelta(days=1)

    """Просмотр указанных дней"""
    def __init__(self,days_for: int):
        self.date_t -= datetime.timedelta(days=days_for)
        for i in range(days_for):
            day, month = self.correct_day_month()
            url = f"http://www.cbr.ru/scripts/XML_daily.asp?date_req={day}/{month}/{self.date_t.year}"
            page = requests.get(url).text
            soup = BeautifulSoup(page, 'lxml')
            self.check_max(soup)
            self.check_min(soup)
            self.get_val_data(soup)
            self.date_t += self.delta_day
        self.get_avg()

    def correct_day_month(self):
        if self.date_t.day < 10:
            day = "0" + str(self.date_t.day)
        else:
            day = str(self.date_t.day)
        if self.date_t.month < 10:
            month = "0" + str(self.date_t.month)
        else:
            month = str(self.date_t.month)
        return day, month

    def get_val_data(self, soup: BeautifulSoup):
        for valute in soup.find_all('valute'):
            name = valute.find('name').text
            val = float(valute.find('value').text.replace(',','.')) / float(valute.find('nominal').text)
            if name in self.val_avg.keys():
                self.val_avg[name] += val
                self.val_count[name] += 1
            else:
                self.val_avg.update({name : val})
                self.val_count.update({name: 1})

    def get_avg(self):
        for val in self.val_avg.keys():
            self.val_avg[val] /= self.val_count[val]

    def check_max(self, soup: BeautifulSoup):
        for valute in soup.find_all('valute'):
            val = float(valute.find('value').text.replace(',','.')) / float(valute.find('nominal').text)
            if val > self.max_val:
                self.max_val = val
                self.max_name = valute.find('name').text
                self.max_date = self.date_t

    def check_min(self, soup: BeautifulSoup):
        for valute in soup.find_all('valute'):
            val = float(valute.find('value').text.replace(',','.')) / float(valute.find('nominal').text)
            if val < self.min_val:
                self.min_val = val
                self.min_name = valute.find('name').text
                self.min_date = self.date_t

    def print_max(self):
        print("Valute maximum:")
        print(f"Name: {self.max_name}")
        print(f"Val: {self.max_val}")
        print(f"Date: {self.max_date}")
        print()

    def print_min(self):
        print("Valute minimum:")
        print(f"Name: {self.min_name}")
        print(f"Val: {self.min_val}")
        print(f"Date: {self.min_date}")
        print()

    def print_avg(self):
        print("Average valute:")
        for val in self.val_avg.keys():
            print(f"Name: {val}")
            print(f"Val: {self.val_avg[val]}")
            print()

    def print_all(self):
        self.print_max()
        self.print_min()
        self.print_avg()

"""valute_stat_for_days принимает количество дней для просмотра(дней до сегоднешнего дня)"""
if __name__ == '__main__':
    val = valute_stat_for_days(90)
    val.print_all()
