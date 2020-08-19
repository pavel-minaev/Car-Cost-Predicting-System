from bs4 import BeautifulSoup
import pandas as pd
import requests

class advert():
    def __init__(self):
        self.snippet_parsed = False
        self.ad_parsed = False

    def snippet_parse(self, snippet):

        self.soup = snippet
        link_a = snippet.find('a', class_='snippet-link')
        tech_spec = snippet.find('div', class_="specific-params").get_text()[1:-2].split(',')

        # todo: сделать assert тесты на распаршенные данные
        self.brand = link_a.get_text().split(',')[0].split(' ')[0]
        self.model = link_a.get_text().split(',')[0][len(self.brand) + 1:]
        self.year = int(link_a.get_text().split(',')[1])
        self.url = 'https://www.avito.ru' + link_a.get('href')
        self.ad_id = int(self.url.split('_')[-1])
        self.price = int(snippet.find('span', class_="snippet-price").get_text()[1:-4].replace(' ', ''))
        self.mileage = int(tech_spec[0][:-3].replace(' ', ''))
        self.engine_volume = tech_spec[1].split(' ')[1]
        self.engine_power = int(tech_spec[1].split(' ')[3].replace('(', ''))
        self.gearbox = tech_spec[1].split(' ')[2]
        self.body_type = tech_spec[2].replace(' ', '')
        self.drive = tech_spec[3].replace(' ', '')
        self.fuel_type = tech_spec[4].replace(' ', '')

        self.snippet_parsed = True

    def advert_parse(self):
        pass

    def export_dictionary(self):
        dic = {}

        if self.snippet_parsed:
            dic['brand'] = [self.brand]
            dic['model'] = [self.model]
            dic['year'] = [self.year]
            dic['url'] = [self.url]
            dic['id'] = [self.ad_id]
            dic['price'] = [self.price]
            dic['mileage'] = [self.mileage]
            dic['engine_volume'] = [self.engine_volume]
            dic['engine_power'] = [self.engine_power]
            dic['gearbox'] = [self.gearbox]
            dic['body_type'] = [self.body_type]
            dic['drive'] = [self.drive]
            dic['fuel_type'] = [self.fuel_type]

        if self.ad_parsed:
            dic['text'] = self.text

        return dic

    def export_tuple(self):

        return (self.ad_id, self.brand, self.model, self.year, self.url, self.price,
                self.mileage, self.engine_volume, self.engine_power, self.gearbox,
                self.body_type, self.drive, self.fuel_type)

    def tuple_parse(self, data):
        self.ad_id = data[0]
        self.brand = data[1]
        self.model = data[2]
        self.year = data[3]
        self.url = data[4]
        self.price = data[5]
        self.mileage = data[6]
        self.engine_volume = data[7]
        self.engine_power = data[8]
        self.gearbox = data[9]
        self.body_type = data[10]
        self.drive = data[11]
        self.fuel_type = data[12]
        self.snippet_parsed = True



class list_of_adverts(list):

    def from_url(self, url):

        total_pages = get_total_pages(url)
        page_part = '&p='

        #         for i in range(1, total_pages+1):
        for i in range(1, 3):
            numbered_page_url = url + page_part + str(i)
            soup = BeautifulSoup(get_html(numbered_page_url), 'lxml')
            soup_list = soup.find_all('div', class_='snippet-horizontal')
            for snippet_soup in soup_list:
                try:
                    ad = advert()
                    ad.snippet_parse(snippet_soup)
                    self.append(ad)
                except:
                    pass
            print('Page {} DONE'.format(i))

    def create_frame(self):

        frame = pd.DataFrame(columns=['brand', 'model', 'gen', 'modification', 'year', 'mileage', 'condition',
                                      'owners', 'vin_masked', 'body_type', 'doors', 'fuel_type', 'engine_volume'
            , 'engine_power'
              'gearbox', 'drive', 'color', 'location', 'seller', 'text',
                                      'price', 'ad_id', 'url'])

        for ad in self:
            if ad.snippet_parsed:
                frame = frame.append(pd.DataFrame.from_dict(ad.export_dictionary()))

        return frame

    def to_base(self, conn, table_name):
        cur = conn.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS {}(
                       ad_id INT PRIMARY KEY,
                       brand TEXT,
                       model TEXT,
                       year INT, 
                       url TEXT,
                       price INT,
                       mileage INT,
                       engine_volume TEXT,
                       engine_power INT,
                       gearbox TEXT,
                       body_type TEXT,
                       drive TEXT,
                       fuel_type TEXT);
                    """.format(table_name))
        conn.commit()

        tuple_list = []
        for ad in self:
            tuple_list.append(ad.export_tuple())
        cur.executemany("INSERT INTO  " + str(table_name) + " VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?);", tuple_list)
        conn.commit()

    def from_base(self, conn, table_name):
        cur = conn.cursor()
        cur.execute("SELECT DISTINCT * FROM {};".format(table_name))
        for line in cur.fetchall():
            ad = advert()
            ad.tuple_parse(line)
            self.append(ad)




def get_html(url):
    return requests.get(url).text


def get_total_pages(url):
    soup = BeautifulSoup(get_html(url), 'lxml')
    soup_tag = soup.find('div', class_="pagination-root-2oCjZ").find_all('span', class_="pagination-item-1WyVp")[-2]
    return int(soup_tag.get_text())
#