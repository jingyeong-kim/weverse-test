from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    """
    로그인 페이지
    """

    def __init__(self, driver):
        """
        LoginPage 클래스의 생성자.

        Args:
            driver: Selenium WebDriver 인스턴스.
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)
        # 이메일 입력 필드 위치
        self.email_field = (By.NAME, "userEmail")
        # 비밀번호 입력 필드 위치
        self.password_field = (By.NAME, "password")
        # 로그인 버튼 위치
        self.login_button = (By.CSS_SELECTOR, ".sc-cedf9b36-1")

    def enter_email(self, email):
        """
        이메일 입력 필드에 이메일 주소를 입력.

        Args:
            email (str): 입력할 이메일 주소.
        """
        try:
            email_input = self.wait.until(EC.visibility_of_element_located(self.email_field))
            email_input.click()  # 필드 클릭 후 이메일 입력
            email_input.send_keys(email)
        except Exception as e:
            raise Exception(f"이메일 입력 중 오류가 발생했습니다: {str(e)}")

    def enter_password(self, password):
        """
        비밀번호 입력 필드에 비밀번호를 입력.

        Args:
            password (str): 입력할 비밀번호.
        """
        try:
            password_input = self.wait.until(EC.visibility_of_element_located(self.password_field))
            password_input.click()
            password_input.send_keys(password)
        except Exception as e:
            raise Exception(f"비밀번호 입력 중 오류가 발생했습니다: {str(e)}")

    def click_login(self):
        """
        '로그인' 버튼, 로그인 요청을 전송.
        """
        try:
            login_btn = self.wait.until(EC.element_to_be_clickable(self.login_button))
            login_btn.click()
        except Exception as e:
            raise Exception(f"'로그인' 버튼 클릭 중 오류가 발생했습니다: {str(e)}")
