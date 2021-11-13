# Python实用宝典
# 2021/11/13
import json
import hashlib
import base64
import hmac
import os
import time
import requests
from urllib.parse import quote_plus


class Messenger:
    def __init__(self, token=os.getenv("DD_ACCESS_TOKEN"), secret=os.getenv("DD_SECRET")):
        self.__token = token
        self.timestamp = str(round(time.time() * 1000))
        secret = secret
        secret_enc = secret.encode('utf-8')
        string_to_sign = '{}\n{}'.format(self.timestamp, secret)
        string_to_sign_enc = string_to_sign.encode('utf-8')
        hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
        self.sign = quote_plus(base64.b64encode(hmac_code))
        self.URL = "https://oapi.dingtalk.com/robot/send"

    def send_text(self, content):
        data = {"msgtype": "text", "text": {"content": content}}
        params = {'access_token': self.__token, "sign": self.sign, "timestamp": self.timestamp}
        headers = {'Content-Type': 'application/json'}
        return requests.post(
            url=self.URL,
            data=json.dumps(data),
            params=params,
            headers=headers
        )

    def send_md(self, title, content):
        data = {"msgtype": "markdown", "markdown": {"title": title, "text": content}}
        params = {'access_token': self.__token, "sign": self.sign, "timestamp": self.timestamp}
        headers = {'Content-Type': 'application/json'}
        return requests.post(
            url=self.URL,
            data=json.dumps(data),
            params=params,
            headers=headers
        )


if __name__ == "__main__":
    markdown_text = "\n".join(open("md_test.md", encoding="utf-8").readlines())
    m = Messenger(
        token="你的token",
        secret="你的secret"
    )
    m.send_text("测试一下，今天天气不错")
    m.send_md("测试Markdown", markdown_text)