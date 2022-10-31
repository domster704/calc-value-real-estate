import undetected_chromedriver
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
import time
from flask import request
from flask_restful import Resource


class DomofondParserApi(Resource):

    def post(self):
        args = request.json
        address = args['address']
        rooms = args['rooms']
        segment = args['segment']
        floors = args['floors']
        wall_material = args['wall_material']
        correct_address = str(address).split(',')[1]

        parser = DomofondParser()
        result = parser.parse(correct_address, rooms, segment, floors, wall_material)
        return result


class DomofondParser(object):

    def __init__(self):
        self.rooms = {
            1: 'One',
            2: 'Two',
            3: 'Three',
            4: 'Four'
        }

        self.segment = {
            'Новостройка': 'New',
            'Вторичка': 'Resale'
        }

        self.wall_material = {
            'Кирпич': 'Brick',
            'Панель': 'Panel',
            'Монолит': 'Monolithic'
        }

    def parse(self, address, rooms, segment, floors, wall_material):
        url = self.get_url(address, rooms, segment, floors, wall_material)
        print(url)
        ua = UserAgent()
        options = undetected_chromedriver.ChromeOptions()
        options.add_argument(f'user-agent={ua.random}')
        options.add_argument('--disable-blink-features=AutomationControlled')

        driver = undetected_chromedriver.Chrome(options=options)

        try:
            driver.get(url)
            card_list = driver.find_element(By.CLASS_NAME, 'search-results__itemCardList___RdWje')
            cards = card_list.find_elements(By.CLASS_NAME, 'long-item-card__item___ubItG')[:5]

            for card in cards:
                href = card.get_attribute("href")
                driver.tab_new(href)

            incorrect_offers = []
            index = len(cards)
            for _ in cards:
                tab = driver.window_handles[index]
                driver.switch_to.window(tab)
                index -= 1

                information = driver.find_elements(By.CLASS_NAME, 'detail-information__wrapper___FRRqm')[0]
                line = information.text.splitlines()
                link = driver.current_url
                line.append(f'Ссылка:{link}')
                incorrect_offer = {}
                for item in line:
                    incorrect_form = item.partition(':')[2]
                    value = incorrect_form.replace(' ', '')
                    incorrect_offer[item.partition(':')[0]] = value
                incorrect_offers.append(incorrect_offer)
            offers = []
            for item in incorrect_offers:
                offer = {
                    'rooms': item['Комнаты'],
                    'segment': item['Тип объекта'],
                    'floors': item['Этаж'],
                    'wall_material': item['Материал здания'],
                    'square': item['Площадь'][:len(item['Площадь']) - 2],
                    'price': item['Цена'][:len(item['Цена']) - 1],
                    'm_price': item['Цена за м²'][:len(item['Цена за м²']) - 1],
                    'url': item['Ссылка']
                }
                offers.append(offer)
            return offers

        except Exception as ex:
            print(ex)
        finally:
            driver.close()
            driver.quit()

    def get_url(self, address, index_rooms, index_segment, index_floors, index_wall_material):
        url = f'https://www.domofond.ru/prodazha-kvartiry-moskva-c3584?Rooms={self.rooms[index_rooms]}&ApartmentSaleType={self.segment[index_segment]}' \
              f'&NumberOfFloorsFrom={index_floors}' \
              f'&ApartmentStyles={self.wall_material[index_wall_material]}&SortOrder=Newest'
        return url
