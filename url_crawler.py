from crawler_interface import CrawlerInterface
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver import ActionChains
from datetime import datetime
import logging
import json


class UrlCrawler(CrawlerInterface):

    def __init__(self):
        self.urls = []
        self.url = 'https://www.norwegian.com/en/ipc/availability/avaday?A_City=RIX&AdultCount=1&ChildCount=0&' \
                   'CurrencyCode=EUR&D_City=OSL&D_Day=01&D_Month=201811&D_SelectedDay=01&IncludeTransit=true&' \
                   'InfantCount=0&R_Day=02&R_Month=201810&TripType=1&mode=ab'

        logname = '{0}.log'.format(datetime.strftime(datetime.now(), '%Y-%m-%d_%H%M%S'))

        # set up logging to file
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(levelname)-8s %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S',
                            filename='log_files/' + logname,
                            filemode='w')

        opts = Options()
        opts.headless = False
        self.browser = Firefox(options=opts)

    def get_data(self):
        self.browser.get(self.url)
        self.browser.implicitly_wait(10)
        self.browser.find_element_by_xpath(
            '//*[@id="ctl00_MainContent_ipcAvaDay_upnlSearchBar"]/div/table/tbody/tr[2]/td[3]/span/label').click()
        # self.browser.find_element_by_name('ctl00$MainContent$ipcAvaDay$ipcAvaDaySearchBar$txtDepartureDate').click()

        calendar = self.browser.find_element_by_xpath('//*[@id="ui-datepicker-div"]/table/tbody')


        # for tr in calendar:
        #     for td in tr
        #     self.urls.append(self.browser.current_url)

        # with open('urls.json', 'w') as json_file:
        #     # self.html = self.browser.page_source
        #     json.dump(self.urls, json_file)

    # def from_first_till_last_day(self):
    #     first_day = self.browser.find_element_by_xpath('//span[contains(.,"01"]')
    #     # day = self.browser.find_elements_by_css_selector('.text-center day')
    #     last_day = self.browser.find_element_by_xpath('//span[contains(.,"30"]')
    #     for el in self.browser.find_element_by_xpath(
    #             '//*[@id="outboundDate"]/div/div/div[1]/div/div[1]/div/table/tbody'):
    #         el.click()
