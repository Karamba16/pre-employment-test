import argparse
import csv
from tabulate import tabulate

def Reader(files,colomns_needed):
    data={}
    for path in files:
        try:
            with open(path, mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    # Извлекаем значения, предполагая столбцы 'Country' и 'GDP'
                    new_row = [row[colomns_needed[i]] for i in range(len(colomns_needed))]
                    try:
                        data[new_row[0]].append(int(new_row[1]))
                    except:
                        data[new_row[0]]=[int(new_row[1])]
        except FileNotFoundError:
            print(f"Ошибка: Файл {path} не найден.")
    return data

#сортирует данные
def Sort_data(data):
    for key, value in data.items():
        data[key]=round(sum(value)/len(value),2)
    sort_data=dict(sorted(data.items(), key=lambda item: item[1],reverse=True))
    #print(sort_data)
    return sort_data

#показывает итоговую таблицу в командную строку
def Data_Show(data,column):
    table = [[k, round(v,2)] for k, v in data.items()]
    print(tabulate(table, headers=column, tablefmt="grid",floatfmt=".2f"))
    return table

#сохраняет данные в файл .csv с названием, которое в --report
def File_Save (data,name,headers):
    if(name):
        try:
            with open(str(name)+".csv", 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(headers)
                writer.writerows(data)
            print("Файл "+ str(name)+".csv  создан")
        except PermissionError:
            print("Файл с таким названием открыт и не может быть перезаписан." \
            " Данные сохранятся в файле output.csv . ")
            with open("output.csv", 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(headers)
                writer.writerows(data)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--files', nargs='+',dest="files", help='Список путей к файлам')
    parser.add_argument('--report', dest="name", help='Название нового файла с результатом')
    args = parser.parse_args()

    needed=["country","gdp"] # в последствии можно будет изменить
    File_Save(Data_Show(Sort_data(Reader(args.files,needed)),needed),args.name,needed)



if __name__ == "__main__":
    main()