import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pyperclip
import sys
import selenium

from bs4 import BeautifulSoup
import requests

from random import randint

import operate_data
def cafe_update(id=operate_data.cafe_id, pwd=operate_data.cafe_pwd, search=operate_data.cafe_info["카페 이름"], cafe_xpath=operate_data.cafe_info["카페 xpath"]):
    x = randint(0, 1)

    # pip install beautifulsoup4, requests, lxml

    url = "https://www.naver.com/"
    res = requests.get(url)

    res.raise_for_status()

    soup = BeautifulSoup(res.text, "html.parser")

    browser = webdriver.Chrome('./chromedriver.exe')
    browser.get('https://www.naver.com/')

    elem_login = browser.find_element_by_xpath('//*[@id="account"]/a')
    elem_login.click()
    time.sleep(0.5)

    elem_id = browser.find_element_by_id('id')
    pyperclip.copy(id)
    elem_id.send_keys(Keys.CONTROL, 'v')
    time.sleep(0.5)

    elem_pwd = browser.find_element_by_id('pw')
    pyperclip.copy(pwd)
    elem_pwd.send_keys(Keys.CONTROL, 'v')
    time.sleep(0.5)

    elem_login_btn = browser.find_element_by_id('log.login')
    elem_login_btn.click()
    time.sleep(0.5)

    if x == 0:

        elem_newsave = browser.find_element_by_id('new.save')
        elem_newsave.click()
        time.sleep(0.5)
        print("등록")

    else:

        elem_newdontsave = browser.find_element_by_id('new.dontsave')
        elem_newdontsave.click()
        time.sleep(0.5)
        print("등록 안함")

    elem_search = browser.find_element_by_id('query')
    elem_search.send_keys(search)
    time.sleep(0.5)

    elem_search_btn = browser.find_element_by_id('search_btn')
    elem_search_btn.click()
    time.sleep(0.5)

    elem_momcafe = browser.find_element_by_xpath(cafe_xpath)
    elem_momcafe.click()
    time.sleep(1.5)

    # 가장 최근 탭으로 이동
    browser.switch_to.window(browser.window_handles[-1])

    # Tip
    # # 현재 탭 닫기
    # browser.close()

    # # 맨 처음 탭으로 변경(0번 탭)
    # browser.switch_to.window(browser.window_handles[0])

    print(browser.window_handles)

    elem_cafeinfo = browser.find_element_by_xpath('//*[@id="member-action-data"]/ul/li[2]/p/a')
    print("처음 카페정보 : ", elem_cafeinfo.is_enabled())

    elem_myact = browser.find_element_by_xpath('//*[@id="cafe-info-data"]/ul/li[3]/p/a')
    print("처음 내 활동 : ", elem_cafeinfo.is_enabled())
    elem_myact.click()
    time.sleep(0.5)

    print("클릭 후 내 활동 : ", elem_cafeinfo.is_enabled())

    print("클릭 후 카페정보 : ", elem_cafeinfo.is_enabled())

    elem_myword = browser.find_element_by_xpath('//*[@id="ia-action-data"]/div[2]/ul/li[2]/span/strong/a')
    elem_myword.click()
    time.sleep(0.5)

    browser.switch_to.frame('cafe_main')

    browser.switch_to.frame('innerNetwork')

    c_url = browser.current_url
    res = requests.get(c_url)

    soup = BeautifulSoup(res.text, "html.parser")

    compare = "compare"

    index = -1

    while index != 15:
        index += 1
        # for idx, tag in enumerate(browser.find_elements_by_tag_name('a')):
        tag = browser.find_elements_by_tag_name('a')[index]
        print(tag.text, tag.get_attribute('href'), tag.get_attribute('xpath'))

        if str(tag.get_attribute('href')) == compare:
            continue

        compare = str(tag.get_attribute('href'))

        if index < 6:
            continue
        elif index > 12:
            continue

        print(index)

        tag.click()

        browser.switch_to.default_content()
        browser.switch_to.frame('cafe_main')
        time.sleep(1.5)

        elem_modified = browser.find_element_by_xpath('//*[@id="app"]/div/div/div[1]/div[1]/a[1]')
        elem_modified.click()
        time.sleep(2)

        browser.switch_to.window(browser.window_handles[-1])

        elem_enroll = browser.find_element_by_xpath('//*[@id="app"]/div/div/section/div/div[1]/div/a')
        # elem_enroll.click()
        elem_enroll.send_keys(Keys.ENTER)
        time.sleep(2)

        browser.close()

        browser.switch_to.window(browser.window_handles[1])

        elem_myword = browser.find_element_by_xpath('//*[@id="ia-action-data"]/div[2]/ul/li[2]/span/strong/a')
        elem_myword.click()
        time.sleep(0.5)

        browser.switch_to.frame('cafe_main')

        browser.switch_to.frame('innerNetwork')

        # compare = str(tag.get_attribute('href'))
        # StaleElementReferenceException
        # tag.get_attribute('href') 가 없어서 나타나는 에러 !!

    print("카페 업데이트가 완료되었습니다.")