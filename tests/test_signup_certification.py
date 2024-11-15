import os
import time
from core.slack import Slack
from core.utils import generate_random_email, save_screenshot

slack_helper = Slack()


class TestSignUpCertification:
    """
    회원가입 테스트 클래스 - 이메일 인증까지 수행.
    Slack을 통해 인증 URL을 획득하여 회원가입을 완료하는 과정을 테스트
    """

    @staticmethod
    def get_env_variable(key, default_value=None):
        """
        환경 변수에서 키 값 불러옴

        Args:
            key (str): 가져올 환경 변수의 키 이름.
            default_value (str, optional): 환경 변수가 설정되지 않은 경우 사용할 기본값. 기본값 None.

        Returns:
            str: 환경 변수에서 가져온 값.

        Raises:
            EnvironmentError: 환경 변수가 설정되지 않은 경우 발생.
        """
        value = os.getenv(key, default_value)
        if not value:
            raise EnvironmentError(f"환경 변수 '{key}'가 설정되지 않았습니다.")
        return value

    @staticmethod
    def get_slack_verification_url(email, retries=3, wait_time=10):
        """
        Slack에서 인증 URL을 가져오는 메서드. 특정 이메일 주소에 해당하는 인증 링크를 Slack 메시지 찾기

        Args:
            email (str): Slack에서 찾을 이메일 주소.
            retries (int, optional): 재시도 횟수. 기본값은 3회.
            wait_time (int, optional): 각 재시도 사이의 대기 시간 (초). 기본값 10초.

        Returns:
            str: 찾은 인증 URL이 없을 경우 None.
        """
        verification_url = None
        for _ in range(retries):  # 최대 3번(retries) 번 시도
            verification_url = slack_helper.find_verification_url_by_email(email)
            if verification_url:
                break
            time.sleep(wait_time)
        return verification_url

    @staticmethod
    def agree_all_terms(agreement_page):
        """
        이용 약관 전체 동의를 처리하는 공통 메서드.

        Args:
            agreement_page: AgreementPage 인스턴스.
        """
        agreement_page.click_agree_all()
        agreement_page.click_next()

    def test_signup_and_verify_profile(
            self,
            driver,
            home_page,
            signup_page,
            password_page,
            nickname_page,
            agreement_page,
            profile_page,
    ):
        """
        회원 가입 및 이메일 인증 과정을 테스트.

        Steps:
            1. 이메일 생성.
            2. 홈 페이지 - 로그인(sign_in) 클릭.
            3. 이메일 입력 및 회원가입 진행.
            4. 비밀번호 설정.
            5. 닉네임 설정.
            6. 이용 약관 동의.
            7. Slack에서 이메일 인증 URL 가져오기
            8. 인증 URL을 사용하여 이메일 인증 완료
            9. 홈 페이지 - 프로필 버튼 클릭
            10. 프로필 페이지로 이동 확인 및 wid 값 추출

        Args:
            driver: Selenium WebDriver 인스턴스.
            home_page: HomePage 인스턴스.
            signup_page: SignUpPage 인스턴스.
            password_page: PasswordPage 인스턴스.
            nickname_page: NicknamePage 인스턴스.
            agreement_page: AgreementPage 인스턴스.
            profile_page: ProfilePage 인스턴스.
        """
        password = None
        email = None
        wid = None

        try:
            # 환경 변수에서 비밀번호 가져오기
            password = self.get_env_variable("USER_PASSWORD")

            # 1. 이메일 생성
            email = generate_random_email()  # 랜덤 이메일 생성
            print(f"Generated email: {email}")

            # 2.홈 페이지 - 로그인(sign_in) 클릭.
            home_page.click_sign_in()

            # 3. 회원가입 페이지 - 이메일 입력 및 계속하기 클릭
            signup_page.enter_email(email)
            signup_page.click_continue()
            signup_page.click_signup()

            # 4. 비밀번호 설정 페이지
            password_page.enter_password(password)
            password_page.click_next()

            # 5. 닉네임 설정 페이지
            nickname_page.enter_nickname("아보카도")  # 테스트 닉네임으로 "아보카도" 사용
            nickname_page.click_next()

            # 6. 이용 약관 동의 페이지
            self.agree_all_terms(agreement_page)

            # 7. Slack에서 이메일 인증 URL 가져오기
            verification_url = self.get_slack_verification_url(email)
            assert verification_url is not None, "인증 URL을 가져오지 못했습니다."

            # 8. 인증 URL을 사용하여 이메일 인증 완료
            driver.get(verification_url)
            assert "환영합니다!" in driver.page_source, "가입 완료 단계에 도달하지 못했습니다."

            # 9. 홈 페이지 - 프로필 버튼 클릭
            home_page.click_profile_button()

            # 10. 프로필 페이지로 이동 확인 및 wid 값 추출
            profile_page.verify_profile_page()  # 프로필 페이지 로드 확인
            wid = profile_page.extract_wid()  # wid 값 추출
            assert wid is not None, "wid 값을 추출하지 못했습니다."
            print(f"Extracted wid: {wid}")

        except Exception as e:
            # 에러 발생 시 스크린샷 저장
            test_name = os.path.splitext(os.path.basename(__file__))[0]
            save_screenshot(driver, test_name)
            raise e
        finally:
            # 테스트 종료 시 이메일(ID), 비밀번호(PWD), WID를 출력 (비밀번호는 보안을 위해 일부 마스킹)
            masked_password = (
                password[:2] + "****" + password[-2:] if password and len(password) > 4 else "****"
            )
            print(f"Test completed with email: {email}, password: {masked_password}, wid: {wid}")

