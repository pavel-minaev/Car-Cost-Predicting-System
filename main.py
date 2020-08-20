from parser.main_parse import parse_avito, read_db
def main():
    # url = 'https://www.avito.ru/moskva/avtomobili?radius=1000&q=volvo'
    # table_name = 'volvo_ads_full'
    url = 'https://www.avito.ru/moskva/avtomobili?radius=1000&q=mazda'
    table_name = 'mazda_ads_full2'
    csv_name = 'mazda2.csv'

    parse_avito(url, table_name, './database/' + csv_name)
    # ads_list = read_db('avito',table_name)
    # ads_list.to_csv('./database/' + csv_name)

    # data_frame = ads_list.create_frame()
    # print(data_frame)


if __name__ == '__main__':
    main()