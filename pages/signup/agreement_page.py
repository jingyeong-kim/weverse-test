from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class AgreementPage:
    """
    회원 가입 과정 - 약관 동의 페이지
    """

    def __init__(self, driver):
        """
        AgreementPage 클래스의 생성자.

        Args:
            driver: Selenium WebDriver 인스턴스.
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        # 이용 약관 전체 동의 체크박스 위치
        self.agree_checkbox = (By.CSS_SELECTOR, "input[type='checkbox']")
        # '다음' 버튼 위치
        self.next_button = (By.CSS_SELECTOR, "button[type='submit']")

    def click_agree_all(self):
        """
        이용 약관 전체 동의 체크박스를 클릭.
        """
        try:
            agree_all_checkbox = self.wait.until(EC.element_to_be_clickable(self.agree_checkbox))
            agree_all_checkbox.click()
        except Exception as e:
            raise Exception(f"이용 약관 동의 체크박스 클릭 중 오류가 발생했습니다: {str(e)}")

    def click_next(self):
        """
        '다음' 버튼을 클릭 후 다음 단계로 이동.
        """
        try:
            next_btn = self.wait.until(EC.element_to_be_clickable(self.next_button))
            next_btn.click()
        except Exception as e:
            raise Exception(f"'다음' 버튼 클릭 중 오류가 발생했습니다: {str(e)}")
