from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class NicknamePage:
    """
    회원 가입 - 닉네임 설정
    """

    def __init__(self, driver):
        """
        NicknamePage 클래스의 생성자.

        Args:
            driver: Selenium WebDriver 인스턴스.
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        # 닉네임 입력 필드 위치
        self.nickname_field = (By.NAME, "nickname")
        # '다음' 버튼 위치
        self.next_button = (By.CSS_SELECTOR, "button[type='submit']")

    def enter_nickname(self, nickname):
        """
        닉네임을 입력.

        Args:
            nickname (str): 설정할 닉네임.
        """
        try:
            nickname_input = self.wait.until(EC.element_to_be_clickable(self.nickname_field))
            nickname_input.click()
            nickname_input.send_keys(nickname)
        except Exception as e:
            raise Exception(f"닉네임 입력 중 오류가 발생했습니다: {str(e)}")

    def click_next(self):
        """
        '다음' 버튼을 클릭 후 다음 단계로 이동.
        """
        try:
            next_btn = self.wait.until(EC.element_to_be_clickable(self.next_button))
            next_btn.click()
        except Exception as e:
            raise Exception(f"'다음' 버튼 클릭 중 오류가 발생했습니다: {str(e)}")
