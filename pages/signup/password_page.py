from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class PasswordPage:
    """
    회원 가입 - 비밀번호 설정 페이지
    """

    def __init__(self, driver):
        """
        PasswordPage 클래스의 생성자.

        Args:
            driver: Selenium WebDriver 인스턴스.
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        # 새 비밀번호 입력 필드
        self.new_password_field = (By.NAME, "newPassword")
        # 비밀번호 확인 입력 필드
        self.confirm_password_field = (By.NAME, "confirmPassword")
        # '다음' 버튼 위치
        self.next_button = (By.CSS_SELECTOR, "button[type='submit']")

    def enter_password(self, password):
        """
        비밀번호와 비밀번호 확인을 입력.

        Args:
            password (str): 설정할 비밀번호.
        """
        try:
            new_password_input = self.wait.until(EC.element_to_be_clickable(self.new_password_field))
            new_password_input.click()
            new_password_input.send_keys(password)

            confirm_password_input = self.wait.until(EC.presence_of_element_located(self.confirm_password_field))
            confirm_password_input.click()
            confirm_password_input.send_keys(password)

        except Exception as e:
            raise Exception(f"비밀 번호 입력 중 오류가 발생 했습니다: {str(e)}")

    def click_next(self):
        """
        '다음' 버튼을 클릭 후 다음 단계 이동
        """
        try:
            next_btn = self.wait.until(EC.element_to_be_clickable(self.next_button))
            next_btn.click()
        except Exception as e:
            raise Exception(f"'다음' 버튼 클릭 중 오류가 발생 했습니다: {str(e)}")
