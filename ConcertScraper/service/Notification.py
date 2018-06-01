import logging
import requests

log = logging.getLogger(__name__)


class Notification:

    @staticmethod
    def sendSlackMsg(SLACK_WEBHOOK_URL, content):
        payload = "{'text': '" + content + "'}"
        response = requests.request("POST", SLACK_WEBHOOK_URL, data=payload, headers={
            'content-type': "application/x-www-form-urlencoded",
        })
        return response

    @staticmethod
    def sendLineMsg(CHANEL_ACCESS_TOKEN, LINE_USER_ID_LIST, content):
        payload = {
            "to": LINE_USER_ID_LIST,
            "messages": [
                {
                    "type": "text",
                    "text": content
                }
            ]
        }
        response = requests.request("POST", "https://api.line.me/v2/bot/message/multicast", json=payload, headers={
            'content-type': "application/json",
            'Authorization': "Bearer {}".format(CHANEL_ACCESS_TOKEN)
        })
        return response

    @staticmethod
    def createMsgFromResult(result):
        result["title"] = Notification.cleanSpaceAndCarriageReturn(str(result["title"]))
        result["detail"] = Notification.cleanSpaceAndCarriageReturn(str(result["detail"]))
        result["contact"] = Notification.cleanSpaceAndCarriageReturn(str(result["contact"]))
        return "Source: {}\nItem id: {}\n\nTitle: {}\n\nDetail: {}\n\nPrice: {}\nContact: {}\nLink: {}\nCreated Date: {}".format(
            result["source"], result["id"], result["title"], result["detail"], result["price"], result["contact"],
            result["link"], result["created_date"])

    @staticmethod
    def cleanSpaceAndCarriageReturn(word):
        return ' '.join(word.split())
