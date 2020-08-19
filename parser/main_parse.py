from parser.avito import list_of_adverts
import sqlite3


def parse_avito(link, table_name, db_name='./database/avito_parsing.db'):
    ads_list = list_of_adverts()
    try:
        ads_list.from_url(link)
        conn = sqlite3.connect(db_name)
        ads_list.to_base(conn, table_name)

    except Exception as e:
        print(e)


def read_db(board_name, table_name, db_name=None):
    if board_name == 'avito':
        db_name = './database/avito_parsing.db'
        try:
            ads_list = list_of_adverts()
            conn = sqlite3.connect(db_name)
            ads_list.from_base(conn, table_name)
            return ads_list

        except Exception as e:
            print(e)

    elif board_name == 'auto.ru':
        print('Not supported')
        return -1
    else:
        print('Wrong board name: ', board_name)
        return -1
