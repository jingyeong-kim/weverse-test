import pytest
from dotenv import load_dotenv
from core.driver import Driver
from pages.home_page import HomePage
from pages.signup.login_page import LoginPage
from pages.signup.signup_page import SignUpPage
from pages.signup.password_page import PasswordPage
from pages.signup.nickname_page import NicknamePage
from pages.signup.agreement_page import AgreementPage
from pages.profile_page import ProfilePage

# .env 파일을 로드
load_dotenv()

@pytest.fixture(scope="function")
def driver():
    driver_instance = Driver.get_driver()
    yield driver_instance
    driver_instance.quit()

# 페이지 객체 픽스처 정의
@pytest.fixture
def home_page(driver):
    return HomePage(driver)

@pytest.fixture
def signup_page(driver):
    return SignUpPage(driver)

@pytest.fixture
def password_page(driver):
    return PasswordPage(driver)

@pytest.fixture
def nickname_page(driver):
    return NicknamePage(driver)

@pytest.fixture
def agreement_page(driver):
    return AgreementPage(driver)

@pytest.fixture
def profile_page(driver):
    return ProfilePage(driver)

@pytest.fixture
def login_page(driver):
    return LoginPage(driver)

