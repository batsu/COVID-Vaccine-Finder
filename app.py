from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep, strftime
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from datetime import date
from datetime import time
from datetime import datetime
from fake_useragent import UserAgent
import json

def run_app():
    chrome_options = Options()
    chrome_options.add_experimental_option("prefs", {
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing_for_trusted_sources_enabled": False,
            "safebrowsing.enabled": False
    })
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-extensions")
    ua = UserAgent()
    userAgent = ua.random
    print(userAgent)
    #chrome_options.add_argument("--user-agent='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36'")
    chrome_options.add_argument(f'--user-agent={userAgent}')
    driver = webdriver.Chrome(options=chrome_options, executable_path='/mnt/c/chromedriver/chromedriver')
    link = "https://www.ruhealth.org/covid-19-vaccine"

    now = datetime.now()
    time_formatted = (now.strftime("%m-%d-%Y %I:%M:%S %p"))
    ##db["date_time"] = time_formatted
    appointments = {"appointments": []
                    }
    

    driver.get(link)
    #try:
    #    driver.implicitly_wait(5)
    #    driver.find_element_by_xpath('//*[@id="auto-modal"]/div/div/div[2]/div/p[3]/button').click()
    #except:
    #    pass

    # Date '//*[@id="block-civic-content"]/article/div/div/div[2]/section/div/div/div[1]/div[2]/div/div[4]/table/tbody/tr/td[1]' need txt
    # Location '//*[@id="block-civic-content"]/article/div/div/div[2]/section/div/div/div[1]/div[2]/div/div[4]/table/tbody/tr/td[3]' need txt
    # Image src for full appt '//*[@id="block-civic-content"]/article/div/div/div[2]/section/div/div/div[1]/div[2]/div/div[4]/table/tbody/tr/td[4]/a/img'
    # appts start at index tr[4]

    # xpath = '//*[@id="block-civic-content"]/article/div/div/div[2]/section/div/div/div[1]/div[2]/div/div[4]/table/tbody/tr' had to switch to a div[2]


    #appt_check = driver.find_elements_by_xpath('//*[@id="block-civic-content"]/article/div/div/div[2]/section/div/div/div[1]/div[2]/div/div[4]/table/tbody/tr/td[4]/a/img')

    #if table_length == len(appt_check):
        #list_appts = []
        #print("There are no appointments available as of", time_formatted)

    tablelength = driver.find_elements_by_xpath('//*[@id="dnn_ctr2947_HtmlModule_lblContent"]/table[2]/tbody/tr')

    if tablelength == []:
        tablelength = driver.find_elements_by_xpath('//*[@id="dnn_ctr2947_HtmlModule_lblContent"]/table[2]/tbody/tr')

    if tablelength == []:
        print("Cannot find table of appointments!")
        sleep(30)
        run_app()

    all_tr = []

    for i, x in enumerate(tablelength, 1):
        xpath = ('//*[@id="dnn_ctr2947_HtmlModule_lblContent"]/table[2]/tbody/tr[%s]/td[4]/center/span/img' % i)
        a = driver.find_elements_by_xpath(xpath)
        xpath = ('//*[@id="dnn_ctr2947_HtmlModule_lblContent"]/table[2]/tbody/tr[%s]/td[4]/center/span/small/img' % i)
        b = driver.find_elements_by_xpath(xpath)
        xpath = ('//*[@id="dnn_ctr2947_HtmlModule_lblContent"]/table[2]/tbody/tr[%s]/td[1]/span/small' % i)
        c = driver.find_elements_by_xpath(xpath)
        xpath = ('//*[@id="dnn_ctr2947_HtmlModule_lblContent"]/table[2]/tbody/tr[%s]/td[4]/center/span/small' % i)
        d = driver.find_elements_by_xpath(xpath)
        d_check = False
        for x in d:
            if "coming" in x.text.lower():
                d_check = True
                break
                
        if a == [] and b == [] and c != [] and d_check == False:
            all_tr.append(i)
    
    data = {
        "last_check": time_formatted
            }

    available = []

    for i, tr in enumerate(all_tr, 0):
        appointments["appointments"].append({"id":i})
        appointments["appointments"][i]["available"] = True

        driver.execute_script("arguments[0].scrollIntoView();", x)
        driver.implicitly_wait(10)
        
        appointments["appointments"][i]["date"] = driver.find_element_by_xpath('//*[@id="dnn_ctr2947_HtmlModule_lblContent"]/table[2]/tbody/tr[%s]/td[1]/span/small' % tr).text
        appointments["appointments"][i]["location"] = driver.find_element_by_xpath('//*[@id="dnn_ctr2947_HtmlModule_lblContent"]/table[2]/tbody/tr[%s]/td[3]/span/small' % tr).text
        


    with open("last_check.json", "w") as write_file:
        json.dump(data, write_file)

    with open("data_file.json", "w") as write_file:
        json.dump(appointments, write_file)

    driver.quit()
    sleep(15)
    print("Starting over!")
    run_app()













