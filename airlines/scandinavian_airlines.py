from crawler_interface import CrawlerInterface
import requests
import pprint
from bs4 import BeautifulSoup
import re
import time


class ScCrawler(CrawlerInterface):

    def __init__(self):
        self.max_retries = 3
        self.ssl_verify = False
        self.url = 'https://classic.flysas.com/en/us/'
        self.url_book = 'https://book.flysas.com'
        self.last_post_url = ''
        self.session = requests.Session()
        self.session.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; ' \
                                             'Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) ' \
                                             'Chrome/69.0.3497.100 Safari/537.36'
        self.session.verify = self.ssl_verify
        self.response = None
        self.post_params = None

        self.run()

    def run(self):
        form_data = {
            '__EVENTTARGET': 'ctl00$FullRegion$MainRegion$ContentRegion$ContentFullRegion$ContentLeftRegion$CEPGroup1$CEPActive$cepNDPRevBookingArea$Searchbtn$ButtonLink',
            'ctl00$FullRegion$TopRegion$_siteHeader$hdnProfilingConsent': '',
            'ctl00$FullRegion$TopRegion$_siteHeader$hdnTermsConsent': '',
            'ctl00$FullRegion$TopRegion$_siteHeader$_ssoLogin$MainFormBorderPanel$uid': '',
            'ctl00$FullRegion$TopRegion$_siteHeader$_ssoLogin$MainFormBorderPanel$pwd': '',
            'ctl00$FullRegion$TopRegion$_siteHeader$_ssoLogin$MainFormBorderPanel$hdnShowModal': '',
            'ctl00$FullRegion$TopRegion$_siteHeader$_ssoLogin$MainFormBorderPanel$hdnIsEb0': '',
            'ctl00$FullRegion$MainRegion$ContentRegion$ContentFullRegion$ContentLeftRegion$CEPGroup1$CEPActive$cepNDPRevBookingArea$ceptravelTypeSelector$TripTypeSelector': 'roundtrip',
            'ctl00$FullRegion$MainRegion$ContentRegion$ContentFullRegion$ContentLeftRegion$CEPGroup1$CEPActive$cepNDPRevBookingArea$predictiveSearch$hiddenIntercont': 'False',
            'ctl00$FullRegion$MainRegion$ContentRegion$ContentFullRegion$ContentLeftRegion$CEPGroup1$CEPActive$cepNDPRevBookingArea$predictiveSearch$hiddenDomestic': 'SE,GB',
            'ctl00$FullRegion$MainRegion$ContentRegion$ContentFullRegion$ContentLeftRegion$CEPGroup1$CEPActive$cepNDPRevBookingArea$predictiveSearch$hiddenFareType"': 'A',
            'ctl00$FullRegion$MainRegion$ContentRegion$ContentFullRegion$ContentLeftRegion$CEPGroup1$CEPActive$cepNDPRevBookingArea$predictiveSearch$txtFrom': 'Stockholm, Sweden - Arlanda (ARN)',
            'ctl00$FullRegion$MainRegion$ContentRegion$ContentFullRegion$ContentLeftRegion$CEPGroup1$CEPActive$cepNDPRevBookingArea$predictiveSearch$hiddenFrom': 'ARN',
            'ctl00$FullRegion$MainRegion$ContentRegion$ContentFullRegion$ContentLeftRegion$CEPGroup1$CEPActive$cepNDPRevBookingArea$predictiveSearch$txtTo': 'London, United Kingdom - Heathrow (LHR)',
            'ctl00$FullRegion$MainRegion$ContentRegion$ContentFullRegion$ContentLeftRegion$CEPGroup1$CEPActive$cepNDPRevBookingArea$predictiveSearch$hiddenTo': 'LHR',
            'ctl00$FullRegion$MainRegion$ContentRegion$ContentFullRegion$ContentLeftRegion$CEPGroup1$CEPActive$cepNDPRevBookingArea$predictiveSearch$txtFromTOJ': '',
            'ctl00$FullRegion$MainRegion$ContentRegion$ContentFullRegion$ContentLeftRegion$CEPGroup1$CEPActive$cepNDPRevBookingArea$predictiveSearch$hiddenFromTOJ': '',
            'ctl00$FullRegion$MainRegion$ContentRegion$ContentFullRegion$ContentLeftRegion$CEPGroup1$CEPActive$cepNDPRevBookingArea$cepCalendar$hiddenOutbound': '2018-11-05',
            'ctl00$FullRegion$MainRegion$ContentRegion$ContentFullRegion$ContentLeftRegion$CEPGroup1$CEPActive$cepNDPRevBookingArea$cepCalendar$hiddenReturn': '2018-11-11',
            'ctl00$FullRegion$MainRegion$ContentRegion$ContentFullRegion$ContentLeftRegion$CEPGroup1$CEPActive$cepNDPRevBookingArea$cepCalendar$hdnSelectedOutboundMonth': '',
            'ctl00$FullRegion$MainRegion$ContentRegion$ContentFullRegion$ContentLeftRegion$CEPGroup1$CEPActive$cepNDPRevBookingArea$cepCalendar$hdnSelectedReturnMonth': '',
            'ctl00$FullRegion$MainRegion$ContentRegion$ContentFullRegion$ContentLeftRegion$CEPGroup1$CEPActive$cepNDPRevBookingArea$cepCalendar$hiddenReturnCalVisible': '',
            'ctl00$FullRegion$MainRegion$ContentRegion$ContentFullRegion$ContentLeftRegion$CEPGroup1$CEPActive$cepNDPRevBookingArea$cepCalendar$hiddenStoreCalDates': 'Sun Sep 30 2018 00:00:00 GMT+0300 (Eastern European Summer Time),Sun Sep 30 2018 00:00:00 GMT+0300 (Eastern European Summer Time),Tue Sep 24 2019 00:00:00 GMT+0300 (Eastern European Summer Time)',
            'ctl00$FullRegion$MainRegion$ContentRegion$ContentFullRegion$ContentLeftRegion$CEPGroup1$CEPActive$cepNDPRevBookingArea$cepCalendar$selectOutbound': '2018-09-01',
            'ctl00$FullRegion$MainRegion$ContentRegion$ContentFullRegion$ContentLeftRegion$CEPGroup1$CEPActive$cepNDPRevBookingArea$cepCalendar$selectReturn': '2018-10-01',
            'ctl00$FullRegion$MainRegion$ContentRegion$ContentFullRegion$ContentLeftRegion$CEPGroup1$CEPActive$cepNDPRevBookingArea$FlexDateSelector': 'Show selected dates',
            'ctl00$FullRegion$MainRegion$ContentRegion$ContentFullRegion$ContentLeftRegion$CEPGroup1$CEPActive$cepNDPRevBookingArea$cepPassengerTypes$passengerTypeAdult': '1',
            'ctl00$FullRegion$MainRegion$ContentRegion$ContentFullRegion$ContentLeftRegion$CEPGroup1$CEPActive$cepNDPRevBookingArea$cepPassengerTypes$passengerTypeChild211': '0',
            'ctl00$FullRegion$MainRegion$ContentRegion$ContentFullRegion$ContentLeftRegion$CEPGroup1$CEPActive$cepNDPRevBookingArea$cepPassengerTypes$passengerTypeInfant': '0',
            'ctl00$FullRegion$MainRegion$ContentRegion$ContentFullRegion$ContentLeftRegion$CEPGroup1$CEPActive$cepNDPRevBookingArea$cepNdpFareTypeSelector$ddlFareTypeSelector': 'A',
            'ctl00$FullRegion$MainRegion$ContentRegion$ContentFullRegion$ContentLeftRegion$CEPGroup1$CEPActive$cepNDPRevBookingArea$hdnsetDefaultValue': 'true',
            'ctl00$FullRegion$MainRegion$ContentRegion$ContentFullRegion$ContentLeftRegion$CEPGroup1$CEPActive$cepNDPRevBookingArea$hdncalendarDropdown': 'true',
        }

        try:
            self.response = self.session.get(self.url)
            self.post_params = self.get_post_inputs(self.response.text)
            self.post_params.update(form_data)

            time.sleep(0.3)
            self.response = self.session.post(self.url, data=self.post_params)
            time.sleep(1)
        except requests.exceptions.RequestException as error:
            print(error)
        self.post_params = self.get_post_inputs(self.response.text)
        self.post_params['__EVENTTARGET'] = 'btnSubmitAmadeus'
        match = re.search('(?P<post_url>https://book\.flysas\.com/[^\']+)', self.response.text)
        self.last_post_url = match.group('post_url').replace(' ', '%20')

        try:
            self.response = self.session.post(self.last_post_url, data=self.post_params)
            self.check_js_validation()
        except requests.exceptions.RequestException as error:
            print(error)
        print(self.response.text)

        self.soup = BeautifulSoup(self.response.text, 'html.parser')
        print(pprint.pprint(self.soup))

    def check_js_validation(self):
        retries = 1
        while self.response.text.find('suspiciousActivity') and retries < self.max_retries:
            self.confirm_js(self.last_post_url)
            headers = {'Referer': self.last_post_url}
            self.response = self.session.post(self.last_post_url, headers=headers, data=self.post_params)
            retries += 1

    def confirm_js(self, referer):
        match = re.search('(?P<js_url>/sk\d+\.js)', self.response.text)
        self.response = self.session.get(''.join([self.url_book, match.group('js_url')]))
        print(self.response.text)
        match = re.search('path:"(?P<post_url>[^"]+)', self.response.text)
        js_url = match.group('post_url')
        match = re.search('ajax_header:"(?P<ajax_header>[^"]+)', self.response.text)
        ajax_headers = {'X-Distil-Ajax': match.group('ajax_header'),
                        "Referer": referer, 'Content-Type': 'text/plain;charset=UTF-8'}
        js_params = {
            'p': '{"proof":"2f6:1538248690529:LkOygXhHDF4BmxJzias6","fp2":{"userAgent":"Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/69.0.3497.100Safari/537.36","language":"en-US","screen":{"width":1536,"height":864,"availHeight":834,"availWidth":1536,"pixelDepth":24,"innerWidth":1536,"innerHeight":732,"outerWidth":1536,"outerHeight":834,"devicePixelRatio":1.25},"timezone":3,"indexedDb":true,"addBehavior":false,"openDatabase":true,"cpuClass":"unknown","platform":"Win32","doNotTrack":"1","plugins":"ChromePDFPlugin::PortableDocumentFormat::application/x-google-chrome-pdf~pdf;ChromePDFViewer::::application/pdf~pdf;NativeClient::::application/x-nacl~,application/x-pnacl~","canvas":{"winding":"yes","towebp":true,"blending":true,"img":"b643d8fcaa9007173be066b61e9f8bb742f4a035"},"webGL":{"img":"bd6549c125f67b18985a8c509803f4b883ff810c","extensions":"ANGLE_instanced_arrays;EXT_blend_minmax;EXT_color_buffer_half_float;EXT_frag_depth;EXT_shader_texture_lod;EXT_texture_filter_anisotropic;WEBKIT_EXT_texture_filter_anisotropic;EXT_sRGB;OES_element_index_uint;OES_standard_derivatives;OES_texture_float;OES_texture_float_linear;OES_texture_half_float;OES_texture_half_float_linear;OES_vertex_array_object;WEBGL_color_buffer_float;WEBGL_compressed_texture_s3tc;WEBKIT_WEBGL_compressed_texture_s3tc;WEBGL_compressed_texture_s3tc_srgb;WEBGL_debug_renderer_info;WEBGL_debug_shaders;WEBGL_depth_texture;WEBKIT_WEBGL_depth_texture;WEBGL_draw_buffers;WEBGL_lose_context;WEBKIT_WEBGL_lose_context","aliasedlinewidthrange":"[1,1]","aliasedpointsizerange":"[1,1024]","alphabits":8,"antialiasing":"yes","bluebits":8,"depthbits":24,"greenbits":8,"maxanisotropy":16,"maxcombinedtextureimageunits":32,"maxcubemaptexturesize":16384,"maxfragmentuniformvectors":1024,"maxrenderbuffersize":16384,"maxtextureimageunits":16,"maxtexturesize":16384,"maxvaryingvectors":30,"maxvertexattribs":16,"maxvertextextureimageunits":16,"maxvertexuniformvectors":4096,"maxviewportdims":"[16384,16384]","redbits":8,"renderer":"WebKitWebGL","shadinglanguageversion":"WebGLGLSLES1.0(OpenGLESGLSLES1.0Chromium)","stencilbits":0,"vendor":"WebKit","version":"WebGL1.0(OpenGLES2.0Chromium)","vertexshaderhighfloatprecision":23,"vertexshaderhighfloatprecisionrangeMin":127,"vertexshaderhighfloatprecisionrangeMax":127,"vertexshadermediumfloatprecision":23,"vertexshadermediumfloatprecisionrangeMin":127,"vertexshadermediumfloatprecisionrangeMax":127,"vertexshaderlowfloatprecision":23,"vertexshaderlowfloatprecisionrangeMin":127,"vertexshaderlowfloatprecisionrangeMax":127,"fragmentshaderhighfloatprecision":23,"fragmentshaderhighfloatprecisionrangeMin":127,"fragmentshaderhighfloatprecisionrangeMax":127,"fragmentshadermediumfloatprecision":23,"fragmentshadermediumfloatprecisionrangeMin":127,"fragmentshadermediumfloatprecisionrangeMax":127,"fragmentshaderlowfloatprecision":23,"fragmentshaderlowfloatprecisionrangeMin":127,"fragmentshaderlowfloatprecisionrangeMax":127,"vertexshaderhighintprecision":0,"vertexshaderhighintprecisionrangeMin":31,"vertexshaderhighintprecisionrangeMax":30,"vertexshadermediumintprecision":0,"vertexshadermediumintprecisionrangeMin":31,"vertexshadermediumintprecisionrangeMax":30,"vertexshaderlowintprecision":0,"vertexshaderlowintprecisionrangeMin":31,"vertexshaderlowintprecisionrangeMax":30,"fragmentshaderhighintprecision":0,"fragmentshaderhighintprecisionrangeMin":31,"fragmentshaderhighintprecisionrangeMax":30,"fragmentshadermediumintprecision":0,"fragmentshadermediumintprecisionrangeMin":31,"fragmentshadermediumintprecisionrangeMax":30,"fragmentshaderlowintprecision":0,"fragmentshaderlowintprecisionrangeMin":31,"fragmentshaderlowintprecisionrangeMax":30},"touch":{"maxTouchPoints":0,"touchEvent":false,"touchStart":false},"video":{"ogg":"probably","h264":"probably","webm":"probably"},"audio":{"ogg":"probably","mp3":"probably","wav":"probably","m4a":"maybe"},"vendor":"GoogleInc.","product":"Gecko","productSub":"20030107","browser":{"ie":false,"chrome":true,"webdriver":false},"window":{"historyLength":5,"hardwareConcurrency":4,"iframe":false},"fonts":"Calibri;Century;Haettenschweiler;Marlett;Pristina;ZWAdobeF"},"cookies":1,"setTimeout":0,"setInterval":0,"appName":"Netscape","platform":"Win32","syslang":"en-US","userlang":"en-US","cpu":"","productSub":"20030107","plugins":{"0":"ChromePDFPlugin","1":"ChromePDFViewer","2":"NativeClient"},"mimeTypes":{"0":"application/pdf","1":"PortableDocumentFormatapplication/x-google-chrome-pdf","2":"NativeClientExecutableapplication/x-nacl","3":"PortableNativeClientExecutableapplication/x-pnacl"},"screen":{"width":1536,"height":864,"colorDepth":24},"fonts":{"0":"Calibri","1":"Cambria","2":"Constantia","3":"LucidaBright","4":"Georgia","5":"SegoeUI","6":"Candara","7":"TrebuchetMS","8":"Verdana","9":"Consolas","10":"LucidaConsole","11":"LucidaSansTypewriter","12":"CourierNew","13":"Courier"}}'}
        time.sleep(1)
        self.response = self.session.post(''.join([self.url_book, js_url]),
                                          headers=ajax_headers, data=js_params)

    def get_post_inputs(self, text):
        soup = BeautifulSoup(text, 'html.parser')
        inputs = soup.find_all('input', attrs={'type': 'hidden'})
        return dict([(p.attrs['name'], p.attrs.get('value', '')) for p in inputs])

    def get_data(self):
        pass
        # flight_info = {}
        # direct_flight = ['departureAirport', 'arrivalAirport', 'departureTimeInLocal', 'arrivalTimeInLocal',
        #                  'cheapestPrice', 'taxes']
        # have_connection = ['departureAirport', 'arrivalAirport', 'connectionAirport', 'departureTimeInLocal',
        #                    'arrivalTimeInLocal', 'cheapestPrice', 'taxes']


