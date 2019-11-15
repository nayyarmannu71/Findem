from selenium import webdriver
import re
import json


class ParseOwler:
    def __init__(self):
        self.driver = None

    def open_browser(self):
        self.driver = webdriver.Chrome("chromedriver.exe")
        self.driver.get("https://owler.com")
        cookies = {'domain': 'owler.com', 'httpOnly': True, 'name': '__cfduid', 'path': '/', 'secure': False,
                   'value': 'dcedcfe11a8960df8ac680062636309d31573801367'}
        self.driver.add_cookie(cookies)

    def close_browser(self):
        self.driver.quit()

    def open_page(self, url):
        self.driver.get(url)

    def parse_data(self):
        if '404' in self.driver.title:
            pass
        else:
            test_data = self.driver.find_element_by_xpath("//script[contains(.,'__NEXT_DATA__')]").get_attribute(
                'innerText')
            try:
                x = re.search(r'props":(.*)\n', test_data)
                data = json.loads('{"' + x.group().replace("__NEXT_DATA__", "").replace("=", "").strip())
                initialState = data['props']['pageProps']['initialState']
                item = dict({
                    "companyName": initialState['companyName'],
                    "description": initialState['description'],
                    "domainName": initialState['domainName'],
                    "logo": initialState['logo'],
                    "founded": initialState['founded'],
                    "revenue": initialState['revenue'],
                    "employeeCount": initialState['employeeCount'],
                    "completenessScore": initialState['completenessScore'],
                    "followers": initialState['followers'],
                    "links": initialState['links']
                })
                item["address"] = dict({
                    "city": initialState['city'],
                    "state": initialState['state'],
                    "country": initialState['country']
                })
                if 'firstName' in initialState['ceoDetail']:
                    item["ceoDetail"] = dict({
                        "name": initialState['ceoDetail']['firstName'] + " " + initialState['ceoDetail']['lastName'],
                        "ceoRating": "%d out of 100" % initialState['ceoDetail']['ceoRating'],
                        "ceoPic": initialState['ceoDetail']['ceoPic']
                    })
                top_competitors = []

                for competitor in initialState['cg']:
                    top_competitors.append(competitor['companyBasicInfo']['shortName'])
                item["top_competitors"] = top_competitors
                with open("data.json", "a", encoding="utf-8") as fle:
                    fle.write("{},\n".format(item))
            except Exception as e:
                print(e)


urls = []
with open("owler.results_old.csv", "r") as fle:
    for line in fle.readlines():
        line = line.replace(".", "").replace(",", "").replace("&", "").strip()
        line = line.replace(" ", "").strip()
        urls.append(line)

# objs = list()
# for i in range(3):
#     objs.append(ParseOwler())
# object_length = len(objs)
# url_chunks = [urls[x:x+20] for x in range(0, len(urls), 5)]

# for url in url_chunks:
#     for obj in objs:
#         obj.open_browser()
#         for u in url:
#             obj.open_page("https://www.owler.com/company/" + u)
# #             obj.parse_data()
#         obj.close_browser()


obj = ParseOwler()
obj.open_browser()
for url in urls:
    obj.open_page("https://www.owler.com/company/" + url)
    obj.parse_data()
obj.close_browser()
