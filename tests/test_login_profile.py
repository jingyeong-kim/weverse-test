import os
from core.utils import wait, save_screenshot

class TestLoginProfile:
    @staticmethod
    def get_env_variable(key, default_value=None):
        """
        환경 변수에서 키 값을 가져오고, 설정되지 않았으면 에러 발생.

        Args:
            key (str): 가져올 환경 변수의 키 이름.
            default_value (str, optional): 환경 변수가 설정 되지 않은 경우 사용할 기본값.

        Returns:
            str: 환경 변수에서 가져온 값.
        """
        value = os.getenv(key, default_value)
        if not value:
            raise EnvironmentError(f"환경 변수 '{key}'가 설정 되지 않았습니다.")
        return value

    def test_login_and_go_to_profile(self, driver, home_page, signup_page, login_page, profile_page):
        """
        로그인 후 프로필 페이지로 이동하는 테스트.

        Args:
            driver: Selenium WebDriver 인스턴스.
            home_page: HomePage 인스턴스.
            signup_page: SignUpPage 인스턴스.
            login_page: LoginPage 인스턴스.
            profile_page: ProfilePage 인스턴스.
        """
        email = None
        password = None
        wid = None

        try:
            # 환경 변수에서 이메일 및 패스워드를 가져옴
            email = self.get_env_variable("TEST_EMAIL")
            password = self.get_env_variable("TEST_USER_PASSWORD")

            # 1. 홈 페이지에서 로그인/회원가입 클릭
            home_page.click_sign_in()

            # 2. 회원가입 페이지 - 이메일 입력 및 계속하기 클릭
            signup_page.enter_email(email)
            wait(2)  # 봇 감지를 위해 이메일 입력 후 2초 대기
            signup_page.click_continue()

            # 3. 로그인 페이지 - 비밀번호 입력 후 로그인 클릭
            login_page.enter_password(password)
            wait(4)  # 봇 감지를 위해 비밀번호 입력 후 4초 대기
            login_page.click_login()

            # 4. 홈 페이지 - 프로필 버튼 클릭
            home_page.click_profile_button()

            # 5. 프로필 페이지로 이동 확인 및 wid 값 추출
            profile_page.verify_profile_page()  # 프로필 페이지 로드 확인
            wid = profile_page.extract_wid()    # wid 값 추출
            print("Extracted wid:", wid)

            # 추가적인 검증 로직을 추가할 수 있습니다.
            assert wid is not None, "wid 값을 추출하지 못했습니다."

        except Exception as e:
            # 에러 발생 시 스크린샷 저장
            test_name = os.path.splitext(os.path.basename(__file__))[0]
            save_screenshot(driver, test_name)
            raise e
        finally:
            # 테스트 종료 시 이메일(ID), 비밀번호(PWD), WID를 출력 (비밀번호는 보안을 위해 일부 마스킹)
            masked_password = password[:2] + "****" + password[-2:] if len(password) > 4 else "****"
            print(f"Test completed with email: {email}, password: {masked_password}, wid: {wid}")
