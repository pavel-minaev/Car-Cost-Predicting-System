from parser.main_parse import parse_avito, read_db
def main():
    # url = 'https://www.avito.ru/moskva/avtomobili?radius=1000&q=volvo'
    # parse_avito(url, table_name='volvo_ads')

    ads_list = read_db('avito',table_name='volvo_ads')
    data_frame = ads_list.create_frame()
    print(data_frame)

if __name__ == '__main__':
    main()