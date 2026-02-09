import argparse
import csv
from tabulate import tabulate

#Настраиваю возможные команды при записи файла
parser = argparse.ArgumentParser(description="Обработка данных")
parser.add_argument("--files", dest="pathes",nargs='+',help="Пути к файлам,которые надо обработать")
parser.add_argument("--report", dest="name", help="Название итогового отчета")

args = parser.parse_args()

cols_to_remove = ["country","gdp"]
data={}

for file in args.pathes:
    try:
            with open(file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:

                    new_row = [row[i] for i in cols_to_remove]
                    if(new_row[0] in data):
                        data[new_row[0]].append(int(new_row[1]))
                    else:
                        data[new_row[0]]=[int(new_row[1])]
    except FileNotFoundError:
        print(f"Файл не найден: {file}")
        continue


for key,value in data.items():
    number_value=(len(value))
    data[key]=round(sum(value)/number_value,2)

#Сортировка по gdp
dict(sorted(data.items(), key=lambda item: item[1]))

table = [[k, v] for k, v in data.items()]


try:
    name=args.name+".xlsx" # разделил, поскольку при записи в csv(через запятую) 
                           # выдает в 1 клетке а не в 2, если открыть в excel
    name2=args.name+".csv"
except TypeError:
    name="economic_result.xlsx"
    name2="economic_result.csv"

with open(name2, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file,delimiter=',')
        writer.writerow(cols_to_remove)
        writer.writerows(table)


print(tabulate(table, headers=table[0], tablefmt="grid"))