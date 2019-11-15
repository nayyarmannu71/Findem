import json
import re

from selenium import webdriver

driver = webdriver.Chrome("D:\MN\chromedriver.exe")
driver.get("https://www.owler.com/company/affordablegaragedoorsllc")
test_data = driver.find_element_by_xpath("//script[contains(.,'__NEXT_DATA__')]").get_attribute('innerText')
try:
    # data = json.loads(test_data.replace("__NEXT_DATA__", "").replace("=", "").strip() + '"}]}}}}')
    x = re.search(r'props":(.*)\n', test_data)
    # with open("mn.json", "w", encoding='utf-8') as fle:
    #     fle.write("{}".format('"' + x.group().replace("__NEXT_DATA__", "").replace("=", "").strip()))
    # data = json.loads('"' + x.group().replace("__NEXT_DATA__", "").replace("=", "").strip() + '"}]}}}')
    data = json.loads('{"' + x.group().replace("__NEXT_DATA__", "").replace("=", "").strip())
    print(data)
except Exception as e:
    print(e)
    import pyperclip
    pyperclip.copy(test_data.replace("__NEXT_DATA__", "").replace("=", "").strip() + '"}]}}}}')
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
with open("data.json", "w") as fle:
    fle.write("{},\n".format(item))
driver.quit()
