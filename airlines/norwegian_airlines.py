from crawler_interface import CrawlerInterface
import requests
import requests_html
from requests_html import HTMLSession
from bs4 import BeautifulSoup
import re
import json


class NoCrawler(CrawlerInterface):

    def __init__(self):
        # self.session = requests.Session()
        self.session = HTMLSession()
        self.ssl_verify = False
        self.initial_url = 'https://www.norwegian.com/'
        self.data = {}
        self.flights = {}
        self.response = None

        headers = requests.utils.default_headers()
        headers.update({
                           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'})

        try:
            self.response = self.session.get(self.initial_url, headers=headers)
        except requests.exceptions.RequestException as error:
            print(error)

        with open('urls/doc.json', 'r') as json_file:
            self.data = json.load(json_file)


        self.soup_get = BeautifulSoup(self.response.text, 'html.parser')
        # print(self.soup_get)

        event_argument, event_target, view_state = self.get_data_for_postback()

        form_data = {'__EVENTTARGET': event_target.attrs['id'],
                     '__EVENTARGUMENT': event_argument.attrs['value'],
                     '__VIEWSTATE': view_state.attrs['value'],
                     }

        try:
            self.post_response = requests.post(self.initial_url, data=form_data)
        except requests.exceptions.RequestException as error:
            print(error)
        self.soup_post = BeautifulSoup(self.post_response.text, 'html.parser')
        print(self.soup_post)

    def get_data_for_postback(self):
        event_target = self.soup_get.find('a', attrs={'class': 'HiddenControl postbackfaker'})
        event_argument = self.soup_get.find('input', attrs={'name': 'hdnFlightSelectOutboundStandardLowFare0'})
        view_state = self.soup_get.find('input', attrs={'id': '__VIEWSTATE'})
        return event_argument, event_target, view_state

    def get_data(self):

        flight_1 = {}
        flight_2 = {}

        clean_date = re.split('^\w+\s', self.soup_get.find('td', attrs={'nowrap': 'nowrap'}).text.strip())
        self.flights = {clean_date[1]: {}}

        taxes = self.soup_post.find_all('td', attrs={'class': 'rightcell emphasize'})
        flight_1.update({'taxes': taxes[1].text})
        price = re.split('\$', taxes[1].text)

        counter = 0

        if self.soup_get.find('tr', attrs={'class': 'oddrow rowinfo1 '}):
            flight_1_row_1 = self.soup_get.find('tr', attrs={'class': 'oddrow rowinfo1 '}).contents
            flight_1_row_2 = self.soup_get.find('tr', attrs={'class': 'oddrow rowinfo2'}).contents
        else:
            flight_1_row_1 = self.soup_get.find('tr', attrs={'class': 'oddrow selectedrow rowinfo1 '}).contents
            flight_1_row_2 = self.soup_get.find('tr', attrs={'class': 'oddrow selectedrow rowinfo2'}).contents

        if self.soup_get.find('tr', attrs={'evenrow rowinfo1 '}):
            flight_2_row_1 = self.soup_get.find('tr', attrs={'class': 'evenrow rowinfo1 '}).contents
            flight_2_row_2 = self.soup_get.find('tr', attrs={'class': 'evenrow rowinfo2'}).contents
        else:
            flight_1_row_1 = self.soup_get.find('tr', attrs={'class': 'evenrow selectedrow rowinfo1 '}).contents
            flight_1_row_2 = self.soup_get.find('tr', attrs={'class': 'evenrow selectedrow rowinfo2'}).contents

        for elem in flight_1_row_1:
            if elem.attrs['class'] == ['depdest']:
                flight_1.update({'departureTimeInLocal': elem.text})
            elif elem.attrs['class'] == ['arrdest']:
                flight_1.update({'arrivalTimeInLocal': elem.text})
            elif elem.attrs['class'] == ['fareselect', 'standardlowfare']:
                flight_1.update({'cheapestPrice': '$' + '{:03.2f}'.format(float(elem.text) - float(price[1]))})
            elif elem.attrs['class'] == ['fareselect', 'standardlowfare', 'selectedfare']:
                flight_1.update({'cheapestPrice': '$' + '{:03.2f}'.format(float(elem.text) - float(price[1]))})
                break
        for elem in flight_1_row_2:
            if elem.attrs['class'] == ['depdest']:
                flight_1.update({'departureAirport': elem.text})
            elif elem.attrs['class'] == ['arrdest']:
                flight_1.update({'arrivalAirport': elem.text})
                break
        counter += 1
        self.flights[clean_date[1]].update({str(counter): flight_1})

        flight_2.update({'taxes': taxes[1].text})
        for elem in flight_2_row_1:
            if elem.attrs['class'] == ['depdest']:
                flight_2.update({'departureTimeInLocal': elem.text})
            elif elem.attrs['class'] == ['arrdest']:
                flight_2.update({'arrivalTimeInLocal': elem.text})
            elif elem.attrs['class'] == ['fareselect', 'standardlowfare']:
                flight_2.update({'cheapestPrice': '$' + '{:03.2f}'.format(float(elem.text) - float(price[1]))})
                break
        for elem in flight_2_row_2:
            if elem.attrs['class'] == ['depdest']:
                flight_2.update({'departureAirport': elem.text})
            elif elem.attrs['class'] == ['arrdest']:
                flight_2.update({'arrivalAirport': elem.text})
                break
        counter += 1
        self.flights[clean_date[1]].update({str(counter): flight_2})

        self.write_json()

    def write_json(self):
        with open('collected_data/json_norwegian.json', 'w') as json_file:
            json.dump(self.flights, json_file, indent=3, sort_keys=True)
