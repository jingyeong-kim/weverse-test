from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class HomePage:
    """
    메인 홈 페이지
    """

    def __init__(self, driver):
        """
        HomePage 클래스의 생성자.

        Args:
            driver: Selenium WebDriver 인스턴스.
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)
        # 로그인 버튼 위치 (XPath)
        self.sign_in_button = (By.XPATH, "//button[contains(text(), 'Sign in')]")
        # 프로필 버튼 위치 (XPath)
        self.profile_button = (By.XPATH, "//button[@type='button' and contains(@class, 'HeaderView_profile_button')]")

    def click_sign_in(self):
        """
        로그인 버튼 클릭..
        """
        try:
            self.wait.until(EC.visibility_of_element_located(self.sign_in_button))

            self.wait.until(EC.element_to_be_clickable(self.sign_in_button)).click()
        except Exception as e:
            raise Exception(f"로그인 버튼 클릭 중 오류가 발생했습니다: {str(e)}")

    def click_profile_button(self):
        """
        프로필 버튼을 클릭.
        """
        try:
            self.wait.until(EC.visibility_of_element_located(self.profile_button))

            self.wait.until(EC.element_to_be_clickable(self.profile_button)).click()
        except Exception as e:
            raise Exception(f"프로필 버튼 클릭 중 오류가 발생했습니다: {str(e)}")
