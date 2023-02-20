# -*- coding: utf-8 -*-
import re
from datetime import datetime

import scrapy
from scrapy import Selector
from Google_Events.cities import cities


class GoogleEventsSpider(scrapy.Spider):
    name = 'google_events'

    request_url = ''

    headers = {
        'authority': 'www.google.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'cache-control': 'max-age=0',
        #'cookie': 'HSID=AqAHxzD8xFOPmZEA0; SSID=AgzCvPWgmyDoZwo1f; APISID=QDJLA0oF1SScsuUW/A2ze7VAaDlNE_vXQE; SAPISID=uMJbFdeKLbSmEJzj/A3RQrsThJBIe5OC6r; __Secure-1PAPISID=uMJbFdeKLbSmEJzj/A3RQrsThJBIe5OC6r; __Secure-3PAPISID=uMJbFdeKLbSmEJzj/A3RQrsThJBIe5OC6r; __Secure-ENID=8.SE=lx5Jzz1n4t57tlcaMKpqwBAGMbse37Gcw4pH2w0ntL0142B7mdwov0Hf6rBX5mFsJtQN10oqD_T4bZOozsHGB3Jfnyh4XNuqFpqlvPzmXXTzyhxDIVQPLsLYPxeMohYuc9aLMTk6xdoxT2-fnIjFqQCn9LHlhAeDtnndS7NWeIAHr7PpZGKfVuUTHJLwmPEXU6GdqTT_pq93l-mBQahZKzb5viNNr12kbQ8atdFB3oMEGZxRJ-Fgnzx2inBSy0KlW9wprIU6M-bCYTa2UIho9h02QA83pCdoJhykxw; SID=SgjHVq_6iT0rbg1iPFlipReNu_ITg7azugWDlRBGaiTYsVsye-qmwtES64xyiYbJIxrPjA.; __Secure-1PSID=SgjHVq_6iT0rbg1iPFlipReNu_ITg7azugWDlRBGaiTYsVsyCKDihImjSDgpsnPL3D-DPg.; __Secure-3PSID=SgjHVq_6iT0rbg1iPFlipReNu_ITg7azugWDlRBGaiTYsVsy7ddRmgNZH3fFWtGH2gy4pg.; OTZ=6872144_36_36__36_; SEARCH_SAMESITE=CgQIt5cB; 1P_JAR=2023-01-28-05; NID=511=Lg7xdbhyucn6AM67yHOpAyRlh2PiP688zSu6WzuPSE9KYTaOuXthSOKo2znVjhivNcB6F1fulRD5yWaFzPH29cUq5aSMgX5Jg8pdz3j1ZWNoUDP7GsgWfdAxWLJ5P_DxugrGw_ZernJwvMF1dWm2jZxPV0LyK06-E_-C9JD-9ifzIMIScsao9rn5zqdX7yoguOfxzhHphgE_633hkmEPBUHsfmm-OMk2cs1ZYRoL60j4uP-Si4KCc6K88DGusdS6IMMtGMsgfJhub82ELyg6qhKYIV1vOrNZgSHkirEdbOHw2YsTTR95RZT9TwOF5M7zKDq8WcZMMruLA_NHw90; AEC=ARSKqsIhjSpZewypKXjonkVCQJJG1X7C46IIVP_d4xCPpb1WUgoJJozGUA; SIDCC=AFvIBn8FfElKJ_Qv6z01lLY9xqB2Vl8dboa71VRWTTpzvYCqfoGKDkJp32SP5a861ES0n5IKk0Q; __Secure-1PSIDCC=AFvIBn_JXB5d_kx3EcykLfERZvpDgJ0EU8hT1em-rDgDwjSKqH8MrJCE74mLNIMkE6J6sIHpyHA; __Secure-3PSIDCC=AFvIBn_ZjNddcQ6OnmE0WFOKTPNmsIOnBJIHbn3Vrcmen_IFxWjdvrFPGRgBeAiklhN6xTe7qRuU; 1P_JAR=2023-01-28-06; AEC=ARSKqsKzIJHeuLfSSyeTzidrAGwY3vFNbg30X3eq_z_u9zJS5vgUCa4gX7o; NID=511=giNgB--UX1XQA2bdbTcANYrO-f4Dw5ikZznnwv5RalFOMytwZ2_GOcLr0Qd9vxfAdyNXD09QkI4Y32A1LjlniD11NMORldbv9Xad2TFlXYR86qVSmXX5SfN4x7_CFZEyVYQjQh-pVJwLIrksH5_xK23we918rxDOdPh5M85Sus4; SIDCC=AFvIBn-KYjXrrSSJMROkS7DF7VCIBohy1XXpPxzN1M-TrHg7Un6sCNSPQdvCZpKy8iY-TPL4v7k; __Secure-1PSIDCC=AFvIBn_K0WNiBiteQZfZlHw-Fd-GTbqavmOdy8Dq6G-nJE2sIIsz1GvnE70oM9lyzUTT16i5sKY; __Secure-3PSIDCC=AFvIBn_R7GcQahp_G1dO6vtXtOYkpcGqnywXf43hAb356eIEFF133DncI_e3SNVlXWNJIGACxzHq',
        'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
        'sec-ch-ua-arch': '"x86"',
        'sec-ch-ua-bitness': '"64"',
        'sec-ch-ua-full-version': '"109.0.5414.120"',
        'sec-ch-ua-full-version-list': '"Not_A Brand";v="99.0.0.0", "Google Chrome";v="109.0.5414.120", "Chromium";v="109.0.5414.120"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-model': '""',
        'sec-ch-ua-platform': '"Windows"',
        'sec-ch-ua-platform-version': '"10.0.0"',
        'sec-ch-ua-wow64': '?0',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        #'x-client-data': 'CI62yQEIo7bJAQjEtskBCKmdygEIrvbKAQiWocsBCJv2zAEI8oDNAQjygs0BCMKGzQEI9YjNAQjwic0BCPeLzQEIj4zNAQinjM0BCNeMzQEI0uGsAgimhK0C'
    }
    filters = ['today', 'tomorrow', 'week', 'weekend', 'next_week', 'month', 'next_month']
    custom_settings = {
        'FEED_URI': f'output/google_events_{datetime.today().strftime("%Y-%m-%d")}.csv',
        'FEED_FORMAT': 'csv',
        'FEED_EXPORT_ENCODING': 'utf-8-sig',
    }

    def base_url(self, city):
        base_url = f'https://www.google.com/search?ei=0SvaY92lJMiXkwXOjYjACA&rciv=evn&yv=3&nfpr=0&chips=date:{{}}&q' \
                f'=events+in+{city}&start={{}}&asearch=evn_af&cs=1&async=_id:Q5Vznb,_pms:hts,_fmt:pc'
        self.request_url = base_url

    def start_requests(self):
        for city in cities:
            for search_filter in self.filters:
                pagination_data = {'search_filter': search_filter,
                                'start_index': 0}
                self.base_url(city)
                yield scrapy.Request(url=self.request_url.format(search_filter, 0), callback=self.parse,
                                    headers=self.headers, meta={'pagination': pagination_data})

    def parse(self, response):
        pagination = response.meta['pagination']
        data_list = response.xpath("//div[@jsname='qlMead']")
        for data in data_list:
            try:
                am_pm_match = ''
                dates = []
                times = []
                item = dict()
                dates_string = data.xpath(".//div[@class='Gkoz3']/text()").get('').strip()
                am_pm_match_list = re.findall("\s?(am|pm)", dates_string)
                if am_pm_match_list and len(am_pm_match_list) == 1:
                    am_pm_match = am_pm_match_list[0]
                if re.search('–', dates_string):
                    for dt in dates_string.split('–'):
                        time_match = re.search(r'(\d{1,2}):(\d{2})\s*([ap]m)?(\s*GMT-5)?', dt, re.IGNORECASE)
                        if time_match:
                            time = time_match.group(0)
                            times.append(time)
                        else:
                            time = ''
                        date = dt.replace(time, '')
                        date_match = re.search(r'(\d{1,2})\s+(\w{3})', date, re.IGNORECASE)
                        if date_match:
                            date = date_match.group(0)
                            dates.append(date)
                else:
                    time_match = re.search(r'(\d{1,2}):(\d{2})\s*([ap]m)?(\s*GMT-5)?', dates_string, re.IGNORECASE)
                    if time_match:
                        time = time_match.group(0)
                        times.append(time)
                    else:
                        time = ''
                    date = dates_string.replace(time, '')
                    date_match = re.search(r'(\d{1,2})\s+(\w{3})', date, re.IGNORECASE)
                    if date_match:
                        date = date_match.group(0)
                        dates.append(date)
                item['Name'] = data.xpath(".//div[@class='dEuIWb']/text()").get('').strip()
                item['Date'] = ','.join([item for item in dates])
                item['Time'] = ','.join(
                    [element + (am_pm_match if am_pm_match not in element else "") + (
                        " GMT-5" if "GMT-5" not in element else "") for element in times])
                venue = data.css('div.ov85De span.n3VjZe::text').get('').strip()
                if not ('USA' or 'United States' or 'united states' or 'usa') in venue:
                    item['Venue'] = venue
                    item['Address'] = data.css('div.ov85De span.U6txu::text').get('').strip()
                else:
                    item['Venue'] = ''
                    item['Address'] = venue
                item['Tickets Buying Urls'] = ' | '.join(
                    url.css('::attr(href)').get('') for url in data.css('div.MwDRlf a.SKIyM'))
                item['Filter'] = pagination.get('search_filter', '')
                yield item
            except Exception as ex:
                print(ex)
        current_start = pagination.get('start_index', 0)
        max_start = 140
        next_start = int(current_start) + 10
        if next_start <= max_start:
            pagination['start_index'] = next_start
            yield scrapy.Request(url=self.request_url.format(pagination.get('search_filter', ''), next_start),
                                 callback=self.parse, headers=self.headers, meta={'pagination': pagination})
