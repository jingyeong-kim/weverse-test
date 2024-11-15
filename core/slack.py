import os
import re
import logging
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Slack:
    """
    특정 이메일이 포함된 슬랙 메시지에서 인증URL 검색
    """

    def __init__(self):
        self.token = os.getenv("SLACK_API_TOKEN")
        self.channel_id = os.getenv("SLACK_CHANNEL_ID")

        if not self.token or not self.channel_id:
            raise ValueError("SLACK_API_TOKEN 또는 SLACK_CHANNEL_ID 환경 변수가 설정되지 않았습니다.")

        self.client = WebClient(token=self.token)

    def find_verification_url_by_email(self, email):
        """
        주어진 이메일이 포함된 Slack 메시지에서 인증 URL 찾기

        Args:
            email (str): 검색할 이메일 주소.

        Returns:
            str or None: 찾은 인증 URL을 반환. URL을 찾지 못한 경우 None을 반환.
        """
        try:
            # 슬랙에서 최근 20개 메시지 가져오기
            result = self.client.conversations_history(channel=self.channel_id, limit=20)

            # 메시지 리스트에서 이메일이 포함된 메시지 검색
            for message in result.get('messages', []):
                # 메시지에 이메일이 포함되어 있는지 확인
                if email in message.get('text', ''):
                    # 이메일이 포함된 경우, 해당 메시지에서 URL을 검색
                    match = re.search(r'(https://[^\s]+)', message['text'])
                    if match:
                        logger.info(f"인증 URL을 찾았습니다!: {match.group(1)}")
                        return match.group(1)

        except SlackApiError as e:
            logger.error(f"Slack API에서 메시지를 가져오는 중 오류가 발생했습니다: {e.response.get('error', '알 수 없는 오류')}")

        # URL을 찾지 못한 경우 None 반환
        logger.info("인증 URL을 찾지 못했습니다.")
        return None
