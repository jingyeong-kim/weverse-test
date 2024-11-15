from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class SignUpPage:
    """
    회원가입 페이지
    """

    def __init__(self, driver):
        """
        SignUpPage 클래스의 생성자.

        Args:
            driver: Selenium WebDriver 인스턴스.
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)
        # 이메일 입력 필드
        self.email_field = (By.XPATH, "//input[@name='userEmail']")
        # "이메일로 계속하기" 버튼
        self.continue_button = (By.XPATH, "//button[.//span[text()='이메일로 계속하기']]")
        # "가입하기" 버튼
        self.signup_button = (By.XPATH, "//button[.//span[text()='가입하기']]")

    def enter_email(self, email):
        """
        이메일을 입력.

        Args:
            email (str): 입력할 이메일 주소.
        """
        try:
            self.wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')

            email_input = self.wait.until(EC.presence_of_element_located(self.email_field))
            self.scroll_into_view(email_input)

            self.driver.execute_script("arguments[0].click();", email_input)
            email_input.send_keys(email)
        except Exception as e:
            raise Exception(f"이메일 입력 중 오류가 발생했습니다: {str(e)}")

    def click_continue(self):
        """
        "이메일로 계속하기" 버튼을 클릭.
        """
        self._click_button(self.continue_button, "이메일로 계속하기")

    def click_signup(self):
        """
        "가입하기" 버튼을 클릭.
        """
        self._click_button(self.signup_button, "가입하기")

    def scroll_into_view(self, element):
        """
        페이지 내 특정 요소를 화면 중앙으로 스크롤.

        Args:
            element: 스크롤하려는 웹 요소.
        """
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)

    def _click_button(self, button_locator, button_name):
        """
        버튼을 클릭 하는 공통 메서드.

        - 버튼이 클릭 가능할 때까지 대기한 후 JavaScript로 강제 클릭.

        Args:
            button_locator: 클릭할 버튼의 위치
            button_name (str): 클릭 하는 버튼의 이름
        """
        try:
            button = self.wait.until(EC.element_to_be_clickable(button_locator))

            self.scroll_into_view(button)

            self.driver.execute_script("arguments[0].click();", button)
        except Exception as e:
            raise Exception(f"JavaScript로 '{button_name}' 버튼 클릭 실패: {str(e)}")
