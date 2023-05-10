from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import quote_plus
from urllib.request import urlopen
import os
import time

def save_images(images, save_path):
    for index, image in enumerate(images):
        src = image.get_attribute('src')
        t = urlopen(src).read()
        file = open(os.path.join(save_path, str(index + 1) + ".jpg"), "wb")
        file.write(t)
        print("img save " + save_path + str(index + 1) + ".jpg")
 

def create_folder_if_not_exists(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error: Creating directory. ' + directory)


def make_url(search_term):
    # 네이버 이미지 검색
    base_url = 'https://search.naver.com/search.naver?where=image&section=image&query='
    # CCL 상업적 이용 가능 옵션
    end_url = '&res_fr=0&res_to=0&sm=tab_opt&color=&ccl=2' \
              '&nso=so%3Ar%2Ca%3Aall%2Cp%3Aall&recent=0&datetype=0&startdate=0&enddate=0&gif=0&optStr=&nso_open=1'
    return base_url + quote_plus(search_term) + end_url


def crawl_images(search_term):
    # URL 생성
    url = make_url(search_term)

    # 브라우저 자동 꺼짐 방지하기
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)

    # 불필요한 에러 메세지 안보이게 하기
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])

    # 크롬드라이버매니저를 통해서 최신 크롬드라이버를 자동으로 설치하고,
    # service 객체를 만들어 변수에 저장.
    service = Service(executable_path=ChromeDriverManager().install())

    # 크롬 열고, 화면 최대화
    browser = webdriver.Chrome(service=service, options=chrome_options)
    browser.maximize_window()
 
    # chrome 브라우저 열기
    browser = webdriver.Chrome('C:/Users/82103/Downloads/chromedriver_win32/chromedriver.exe')
    browser.maximize_window()
    browser.get(url)
    browser.implicitly_wait(3); # 브라우저를 오픈할 때 시간간격을 준다.

    before_h = browser.execute_script("return window.scrollY")

    # 무한스크롤
    while True:
        #맨 아래로 스크롤 내리기
        browser.find_element(By.CSS_SELECTOR, "body.wrap-new.api_animation.tabsch.tabsch_image").send_keys(Keys.END)
        # 스크롤 사이 페이지 로딩 시간
        time.sleep(10)
        # 스크롤 후 높이
        after_h = browser.execute_script("return window.scrollY")

        if after_h == before_h:
            break
        before_h = after_h

    images = browser.find_elements(By.CLASS_NAME, "_image")

    # 이미지 긁어오기
    print(images)
    # 저장 경로 설정
    save_path = "dataset/crawling_naver/" + search_term + "/"
    create_folder_if_not_exists(save_path)
 
    # 이미지 저장
    save_images(images, save_path)
 
    # 마무리
    print(search_term + " 저장 성공")
    browser.close()
 
 
if __name__ == '__main__':
    crawl_images(input('원하는 검색어: '))