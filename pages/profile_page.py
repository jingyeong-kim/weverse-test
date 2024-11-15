import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time
from selenium.common.exceptions import WebDriverException

BASE_URL = os.getenv("BASE_URL", "https://weverse.io")
API_HOST = os.getenv("API_HOST", "https://global.apis.naver.com")

class ProfilePage:

    def __init__(self, driver):
        """
        ProfilePage 클래스의 생성자

        Args:
            driver: Selenium WebDriver 인스턴스.
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)  # 대기 시간 10초로 설정
        # 프로필 버튼
        self.profile_button = (By.XPATH, "//button[@type='button' and contains(@class, 'HeaderView_profile_button')]")
        # wid 취득을 위한 API_ENDPOINT를 완성
        self.api_endpoint = f"{API_HOST}/weverse/wevweb/users/v1.0/users/me"

    def verify_profile_page(self):
        """
        프로필 페이지가 정상적으로 로드(예상된URL 경로, 프로필 버튼 노출)되었는지 확인.
        """
        try:
            self.wait.until(lambda d: d.execute_script('return document.readyState') == 'complete')

            self.wait.until(EC.url_contains(f"{BASE_URL}/more"))

            self.wait.until(EC.visibility_of_element_located(self.profile_button))
        except Exception as e:
            # 페이지 로드 확인 중 오류 발생
            raise Exception(f"프로필 페이지 로딩 확인 중 오류가 발생했습니다: {str(e)}")

    def extract_wid(self):
        """
        네트워크 트래픽에서 WID 값을 추출.

        - 네트워크 트래픽을 활성화, 특정 요청을 통해 WID 값을 추출.

        Returns:
            str: 추출된 WID 값.

        Raises:
            Exception: WID 값을 찾을 수 없는 경우 예외 발생.
        """
        # Chrome DevTools Protocol
        self.driver.execute_cdp_cmd('Network.enable', {})

        # 네트워크 요청이 충분히 발생 하도록 대기
        time.sleep(5)

        logs = self.driver.get_log('performance')

        for log in logs:
            # 성능 로그 메시지를 파싱
            log_message = json.loads(log['message'])
            message = log_message['message']

            # 'Network.responseReceived' 메시지를 찾기 위한 조건
            if message['method'] == 'Network.responseReceived':
                response_url = message['params']['response']['url']

                #특정 API URL에 대한 응답인지 확인
                if self.api_endpoint in response_url:
                    request_id = message['params']['requestId']
                    try:
                        # 응답 본문을 요청
                        response_data = self.driver.execute_cdp_cmd('Network.getResponseBody', {'requestId': request_id})

                        # 응답 데이터 JSON으로 파싱하고 'wid' 값 추출
                        response_body = json.loads(response_data['body'])
                        if "wid" in response_body:
                            return response_body["wid"]

                    except WebDriverException as e:
                        # 'No resource with given identifier found' 오류는 무시
                        if "No resource with given identifier found" in str(e):
                            pass
                        else:
                            # 그 외의 오류가 발생한 경우 출력
                            print(f"Error getting response body for requestId {request_id}: {str(e)}")

        # WID 값을 찾을 수 없는 경우 예외를 발생
        raise Exception("wid 값을 찾을 수 없습니다.")
