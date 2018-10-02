import logging
from crawler_interface import CrawlerInterface
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from datetime import datetime


class SasCrawler(CrawlerInterface):

    def __init__(self):
        self.logger = logging.getLogger(str(self.__class__))
        self.url = 'https://classic.flysas.com/'
        self.flight = {
            'from': 'ARN',
            'to': 'LHR',
            'date_from': '2018-11-05',
            'date_to': '2018-11-11',
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
        opts.headless = True
        self.browser = Firefox(options=opts)

        self.run()

    def run(self):
        self.load_search_form()
        self.fill_search_form()
        self.submit_search_form()
        self.browser.close()

    def load_search_form(self):
        self.browser.get(self.url)
        # select language
        self.browser.find_element_by_xpath('//*[@id="lstMarkets"]/tbody/tr[8]/td[3]').click()

    def fill_search_form(self):
        # flight from
        elem = self.browser.find_element_by_name(
            'ctl00$FullRegion$MainRegion$ContentRegion$ContentFullRegion$ContentLeftRegion$CEPGroup1$CEPActive$cepNDPRevBookingArea$predictiveSearch$txtFrom')
        elem.send_keys(self.flight['from'])
        self.browser.implicitly_wait(1.5)
        self.browser.find_element_by_css_selector('#resultFrom .selected').click()

        # flight to
        elem = self.browser.find_element_by_name(
            'ctl00$FullRegion$MainRegion$ContentRegion$ContentFullRegion$ContentLeftRegion$CEPGroup1$CEPActive$cepNDPRevBookingArea$predictiveSearch$txtTo')
        elem.send_keys(self.flight['to'])
        self.browser.implicitly_wait(1.5)
        self.browser.find_element_by_css_selector('#resultTo .selected').click()

        # from (field)
        elem = self.browser.find_element_by_class_name('flOutDate')
        elem.click()

        self.find_outward_date()

        # return (field)
        elem = self.browser.find_element_by_class_name('flInDate')
        elem.click()

        self.find_return_date()

    def find_outward_date(self):
        # from (datepicker)
        datetime_object = self.get_datepicker_date()
        date_from = datetime.strptime(self.flight['date_from'], '%Y-%m-%d')
        while datetime_object.month != date_from.month:
            self.browser.find_element_by_class_name('ui-datepicker-month-link').click()
            datetime_object = self.get_datepicker_date()
        for el in self.browser.find_elements_by_css_selector('.ui-datepicker-calendar td'):
            if el.text.strip() == str(date_from.day):
                el.click()
                break

    def find_return_date(self):
        # return (datepicker)
        datetime_object = self.get_datepicker_date()
        date_to = datetime.strptime(self.flight['date_to'], '%Y-%m-%d')
        while datetime_object.month != date_to.month:
            self.browser.find_element_by_class_name('ui-datepicker-month-link').click()
            datetime_object = self.get_datepicker_date()
        for el in self.browser.find_elements_by_css_selector('.ui-datepicker-calendar td'):
            if el.text.strip() == str(date_to.day):
                el.click()
                break

    def submit_search_form(self):
        # submit form
        elem = self.browser.find_element_by_id(
            'ctl00_FullRegion_MainRegion_ContentRegion_ContentFullRegion_ContentLeftRegion_CEPGroup1_CEPActive_cepNDPRevBookingArea_Searchbtn_ButtonLink')
        elem.click()

    def get_datepicker_date(self):
        cur_day = int(self.browser.find_element_by_class_name('ui-state-active').text)
        cur_month = self.browser.find_element_by_class_name('ui-datepicker-month').text
        cur_year = int(self.browser.find_element_by_class_name('ui-datepicker-year').text)
        return datetime.strptime('{year} {month} {day}'.format(year=cur_year, month=cur_month, day=cur_day),
                                 '%Y %B %d')

    def get_data(self):
        pass
