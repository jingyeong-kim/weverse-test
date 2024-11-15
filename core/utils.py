import uuid
import time
import os
from datetime import datetime

def generate_random_email(domain="benx.com"):
    """
    랜덤한 이메일 주소를 생성하는 함수.

    Args:
        domain (str): 이메일 주소의 도메인 부분. 기본값은 "benx.com"

    Returns:
        str: 랜덤하게 생성된 이메일 주소를 반환.
    """
    # UUID4를 사용하여 고유한 랜덤한 문자열을 생성하고 앞 8자를 사용
    return f"{uuid.uuid4().hex[:8]}@{domain}"


def wait(seconds=1):
    """
    지정된 시간 동안 실행을 멈추는 대기 함수.

    Args:
        seconds (int): 대기할 시간(초)을 지정. 기본값은 1초.

    Returns:
        None
    """
    time.sleep(seconds)


def save_screenshot(driver, test_name):
    """
    에러 발생 시 스크린샷을 저장하는 함수 (디버깅 용도).

    Args:
        driver: Selenium WebDriver 인스턴스.
        test_name (str): 테스트 이름을 파일명에 포함하여 스크린샷 파일명을 고유하게 만듭니다.

    Returns:
        None
    """
    # 스크린샷을 저장할 디렉토리 경로 설정
    screenshots_dir = "screenshots"
    if not os.path.exists(screenshots_dir):
        os.makedirs(screenshots_dir)  # 스크린샷 폴더가 없으면 생성

    # 타임스탬프를 이용해 고유한 파일 이름 생성
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot_name = f"{test_name}_{timestamp}.png"
    screenshot_path = os.path.join(screenshots_dir, screenshot_name)

    # 스크린샷 저장 및 저장 위치 출력
    driver.save_screenshot(screenshot_path)
    print(f"Screenshot saved to {screenshot_path}")
