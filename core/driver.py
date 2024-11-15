import os
from selenium import webdriver

class Driver:
    """
    Selenium WebDriver 설정 및 특정 URL로 이동하는 드라이버를 생성
    """

    BASE_URL = os.getenv("BASE_URL", "https://weverse.io")
    HEADLESS = os.getenv("HEADLESS", "False").lower() in ("true", "1", "yes")  # 기본값은 False

    @staticmethod
    def get_driver():
        """
        Selenium WebDriver를 생성 및  기본 설정을 적용

        Returns:
            WebDriver: 설정이 완료된 Chrome WebDriver 인스턴스를 반환합니다.
        """

        chrome_options = webdriver.ChromeOptions()

        # SSL 관련 오류 우회
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument('--ignore-ssl-errors')

        # 자동화 제어 관련 기능 비활성화
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')

        # 브라우저의 로깅 기능 활성화
        chrome_options.add_argument("--enable-logging")
        chrome_options.add_argument("--v=1")
        chrome_options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})

        # 헤드리스 모드 설정
        if Driver.HEADLESS:
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920x1080")

        driver = webdriver.Chrome(options=chrome_options)

        # 브라우저 창을 최대화 (헤드리스 모드가 아닐 경우)
        if not Driver.HEADLESS:
            driver.maximize_window()

        # 기본 URL로 이동
        driver.get(Driver.BASE_URL)

        return driver
