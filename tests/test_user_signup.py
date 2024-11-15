import os
from pages.home_page import HomePage
from pages.signup.signup_page import SignUpPage
from pages.signup.password_page import PasswordPage
from pages.signup.nickname_page import NicknamePage
from pages.signup.agreement_page import AgreementPage
from core.utils import generate_random_email, save_screenshot


class TestUserSignUp:
    """
    회원 가입 테스트 수행 (미인증)
    """

    @staticmethod
    def get_env_variable(key, default_value=None):
        """
        환경 변수에서 키 값을 불러옴.

        Args:
            key (str): 가져올 환경 변수의 키 이름.
            default_value (str, optional): 환경 변수가 설정 되지 않은 경우 사용할 기본값. 기본값은 None.

        Returns:
            str: 환경 변수에서 가져온 값.

        Raises:
            EnvironmentError: 환경 변수가 설정되지 않은 경우 발생.
        """
        value = os.getenv(key, default_value)
        if not value:
            raise EnvironmentError(f"환경 변수 '{key}'가 설정되지 않았습니다.")
        return value

    def test_signup_and_verify_profile(self, driver):
        """
        회원 가입(미인증).

        Args:
            driver: Selenium WebDriver 인스턴스.

        Steps:
            1. 이메일 생성.
            2. 홈 페이지 - 로그인(sign_in) 클릭.
            3. 이메일 입력 및 회원가입 진행.
            4. 비밀번호 설정.
            5. 닉네임 설정.
            6. 이용 약관 동의.
            7. 이메일 인증 화면 확인.
        """
        email = None
        password = None

        try:
            # 환경 변수에서 패스워드 가져오기
            password = self.get_env_variable("TEST_USER_PASSWORD")

            # 1. 이메일 생성
            email = generate_random_email()

            # 2. 홈 페이지 - 로그인(sign_in) 클릭
            home_page = HomePage(driver)
            home_page.click_sign_in()

            # 3. 회원가입 페이지 - 이메일 입력 및 계속하기 클릭
            signup_page = SignUpPage(driver)
            signup_page.enter_email(email)
            signup_page.click_continue()
            signup_page.click_signup()

            # 4. 비밀번호 설정 페이지
            password_page = PasswordPage(driver)
            password_page.enter_password(password)
            password_page.click_next()

            # 5. 닉네임 설정 페이지
            nickname_page = NicknamePage(driver)
            nickname_page.enter_nickname("아보카도")  # 테스트 닉네임으로 "아보카도" 사용
            nickname_page.click_next()

            # 6. 이용 약관 동의 페이지
            agreement_page = AgreementPage(driver)
            agreement_page.click_agree_all()  # 이용 약관 전체 동의
            agreement_page.click_next()

            # 7. 이메일 인증 화면 확인 - 회원가입의 마지막 단계 확인
            assert "이제 이메일을 인증해주세요!" in driver.page_source, "이메일 인증 안내 화면에 도달하지 못했습니다."

        except Exception as e:
            # 에러 발생 시 스크린샷을 저장하여 디버깅 정보를 제공
            test_name = os.path.splitext(os.path.basename(__file__))[0]  # 현재 파일명에서 확장자 제거
            save_screenshot(driver, test_name)
            raise e
        finally:
            # 테스트 종료 시 이메일(ID)과 비밀번호(PWD)를 출력 (비밀번호는 보안을 위해 일부 마스킹)
            masked_password = password[:2] + "****" + password[-2:] if len(password) > 4 else "****"
            print(f"Test completed with email: {email}, password: {masked_password}")
