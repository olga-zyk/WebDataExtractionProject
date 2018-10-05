from crawler_interface import CrawlerInterface
import logging
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver import ActionChains
from datetime import datetime
import re
import json


class NorSelen(CrawlerInterface):

    def __init__(self):
        self.logger = logging.getLogger(str(self.__class__))
        self.logger.setLevel(logging.INFO)
        self.url = 'https://www.norwegian.com/'
        self.new_url = {}

        self.flight = {
            'from': 'OSL',
            'to': 'RIX',
            'year': '2018',
            'month': 'November',
            'firstDay': '01',
            'lastDay': '30'
        }

        logname = '{0}_{1}-{2}.log'.format(datetime.strftime(datetime.now(), '%Y-%m-%d_%H%M%S'),
                                           self.flight['from'], self.flight['to'])
        # set up logging to file
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(levelname)-8s %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S',
                            filename='log_files/' + logname,
                            filemode='w')

        opts = Options()
        opts.headless = False
        self.browser = Firefox(options=opts)

        self.run()

    def run(self):
        self.load_search_form()
        self.fill_search_form()
        self.submit_the_form()
        self.get_new_url()
        self.browser.close()

    def get_new_url(self):
        # save current page url
        self.new_url.update({'0': self.browser.current_url})

        with open('first_page_url/nor_airlines_url.json', 'w') as json_file:
            json.dump(self.new_url, json_file)

    def load_search_form(self):
        self.browser.get(self.url)
        self.browser.implicitly_wait(5)
        # close notification about cookies
        self.browser.find_element_by_xpath('/html/body/main/div[4]/div/div/div[2]/button').click()
        # select language
        self.browser.find_element_by_xpath('/html/body/main/article/ul/li[13]/a/div').click()

    def fill_search_form(self):
        # flight from
        elem = self.browser.find_element_by_id('airport-select-origin')
        elem.clear()
        elem.send_keys(self.flight['from'])
        self.browser.find_element_by_id('airport-select-origin').click()
        self.browser.implicitly_wait(6)
        self.browser.find_element_by_xpath('//*[@id="OSL"]/button').click()

        # flight to
        elem = self.browser.find_element_by_id('airport-select-destination')
        elem.send_keys(self.flight['to'])
        self.browser.implicitly_wait(6)
        self.browser.find_element_by_xpath('//*[@id="RIX"]/button').click()

        # select one-way flight
        elem = self.browser.find_element_by_xpath('//*[@id="tripType"]/span[2]/label/span[2]')
        ActionChains(self.browser).move_to_element(elem).click().perform()

        # open datepicker
        self.browser.find_element_by_class_name('calendar__input').click()
        # switch to the datepicker
        self.browser.find_element_by_name('availabilityOutboundDate')
        # set month
        self.set_datepicker_month()
        # move to table
        t_body = self.browser.find_element_by_xpath('//*[@id="outboundDate"]/div/div/div[1]/div/div[1]/div/table/tbody')
        ActionChains(self.browser).move_to_element(t_body).perform()
        tds_in_tbody = self.browser.find_elements_by_css_selector('td')
        # choose date
        for el in tds_in_tbody:
            if el.text == '01':
                el.click()
                break

    def submit_the_form(self):
        # Submit the form
        try:
            self.browser.find_element_by_xpath('//*[@id="searchButton"]').click()
        except Exception as error:
            print(error)

    def set_datepicker_month(self):
        if re.search('(^[A-Za-z]+[^\s])',
                     self.browser.find_elements_by_css_selector('.ui-datepicker-content')[0].text) != self.flight['month']:
            self.browser.find_element_by_xpath(
                '//*[@id="outboundDate"]/div/div/div[1]/div/div[1]/div/div/button[3]').click()

    def get_data(self):
        pass
