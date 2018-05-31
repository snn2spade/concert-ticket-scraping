import logging
import requests

log = logging.getLogger(__name__)


class SlackNotification:

    @staticmethod
    def sendMsg(SLACK_WEBHOOK_URL, content):
        payload = "{'text': '" + content + "'}"
        response = requests.request("POST", SLACK_WEBHOOK_URL, data=payload, headers={
            'content-type': "application/x-www-form-urlencoded",
        })
        return response
