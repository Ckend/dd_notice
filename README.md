# 钉钉通知机器人

支持 Text 和 Markdown.

教程原文：[教你用Python开发钉钉通知机器人](https://pythondict.com/life-intelligent/tools/10%e5%88%86%e9%92%9f%e6%95%99%e4%bd%a0%e7%94%a8python%e5%bc%80%e5%8f%91%e9%92%89%e9%92%89%e9%80%9a%e7%9f%a5%e6%9c%ba%e5%99%a8%e4%ba%ba/)

在项目协同工作或自动化流程完成时，我们需要用一定的手段通知自己或他人。比如说，当服务器CPU使用率达到90%，发送告警信息给多名项目成员、或是股票自动化交易成交时发送通知给自己等应用场景。通知的手段有很多，使用邮件、Telegram都可以实现，但是它们都有各自的缺点。

邮件通知的方式存在滞后性，而且容易覆盖掉一些重要的邮件，整理起来非常繁琐。Telegram 非常好用，几个步骤就能创建一个机器人，可惜在国内无法使用，需要添加代理才能使用。

不过，前几天发现钉钉的机器人其实和Telegram的相差无几，用起来也相当舒服，因此今天给大家带来一个开发钉钉通知机器人的教程，非常简单，门槛极低，任何人都能用，每个人都能学会。

## **1.准备**

开始之前，你要确保Python和pip已经成功安装在电脑上，如果没有，请访问这篇文章：[超详细Python安装指南](https://pythondict.com/python-tutorials/how-to-install-python/) 进行安装。

**(可选1)** 如果你用Python的目的是[数据分析](https://pythondict.com/python-data-analyze/)，可以直接安装Anaconda：[Python数据分析与挖掘好帮手—Anaconda](https://pythondict.com/life-intelligent/tools/python-data-analysis-with-anaconda/)，它内置了Python和pip.

**(可选2)** 此外，推荐大家用VSCode编辑器来编写小型Python项目：[Python 编程的最好搭档—VSCode 详细指南](https://pythondict.com/life-intelligent/tools/python-best-partner-vscode/)

Python 环境准备完成后，我们就可以来创建一个钉钉机器人了。

1.1 打开钉钉软件，选择 "**我**", 再点击右上角+号，选择建场景群

![](https://pythondict-1252734158.file.myqcloud.com/home/www/pythondict/wp-content/uploads/2021/11/2021111309503268.png)

1.2 这里可以选择任意一种群，我选择了培训群

![](https://pythondict-1252734158.file.myqcloud.com/home/www/pythondict/wp-content/uploads/2021/11/2021111309512812.png)

1.3 群新建好后，点击右上角的齿轮—**群设置**，点击智能群助手。这里你也可以修改群的名字，点击名字右边的铅笔就能修改群名。

![](https://pythondict-1252734158.file.myqcloud.com/home/www/pythondict/wp-content/uploads/2021/11/2021111309510146.png)

1.4 点击添加机器人

![](https://pythondict-1252734158.file.myqcloud.com/home/www/pythondict/wp-content/uploads/2021/11/2021111309523282.png)

1.5 点击右上角的+号

![](https://pythondict-1252734158.file.myqcloud.com/home/www/pythondict/wp-content/uploads/2021/11/2021111309540138.png)

1.6 选择自定义机器人，它能让我们通过Webhook接入自定义服务

![](https://pythondict-1252734158.file.myqcloud.com/home/www/pythondict/wp-content/uploads/2021/11/2021111309551169.png)

1.7 然后输入机器人名字，安全设置选择加签，这一字符串你需要拷贝下来，发通知的时候就是我们的**SECRET KEY**.

![](https://pythondict-1252734158.file.myqcloud.com/home/www/pythondict/wp-content/uploads/2021/11/2021111309552564.png)

1.8 点击完成后，会弹出创建成功的框框，请把这串webhook的链接拷贝下来，并将access_token参数复制下来，这一串 access_token 我们发送消息的时候也需要用到。

![](https://pythondict-1252734158.file.myqcloud.com/home/www/pythondict/wp-content/uploads/2021/11/2021111309571677.png)

机器人创建完毕后，会在群聊中出现，然后我们就可以开始编写通知代码了。

![](https://pythondict-1252734158.file.myqcloud.com/home/www/pythondict/wp-content/uploads/2021/11/2021111310002121.png)

## 2.Python 钉钉机器人通知代码

我们通过往 **https://oapi.dingtalk.com/robot/send** 地址发送 POST 请求的方式就能够利用钉钉自定义机器人发送消息。钉钉机器人支持两种消息内容：

1. 纯文本信息
2. Markdown信息

简单来讲，如果你的消息只有文本内容，就用第一种。如果你的消息内含图片和自定义格式，就用第二种。

纯文本消息，你的内容需要包含以下3种参数，并带2个内容体：

参数列表：

1. access_token: 创建成功后返回的webhook链接里就有这个参数。
2. sign: 就是我们选择加签安全设置中返回的SECRET.
3. timestamp: 当前时间戳。

内容体包含：

1. msgtype: 消息内容 text/markdown
2. text: 文本内容

代码如下，非常简单：

```python
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
        self.timestamp = str(round(time.time() \* 1000))
        self.URL = "https://oapi.dingtalk.com/robot/send"
        self.headers = {'Content-Type': 'application/json'}
        secret = secret
        secret_enc = secret.encode('utf-8')
        string_to_sign = '{}\n{}'.format(self.timestamp, secret)
        string_to_sign_enc = string_to_sign.encode('utf-8')
        hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
        self.sign = quote_plus(base64.b64encode(hmac_code))
        self.params = {'access_token': token, "sign": self.sign}

    def send_text(self, content):
        """
        发送文本
        @param content: str, 文本内容
        """
        data = {"msgtype": "text", "text": {"content": content}}
        self.params["timestamp"] = self.timestamp
        return requests.post(
            url=self.URL,
            data=json.dumps(data),
            params=self.params,
            headers=self.headers
        )
```

使用的时候，请注意token和secret你既可以通过环境变量配置(DD_ACCESS_TOKEN和DD_SECRET)，也可以直接传入给Messenger：

```python
if __name__ == "__main__":
    m = Messenger(
        token="你的token",
        secret="你的secret"
    )
    m.send_text("测试一下，今天天气不错")
```

然后运行这个脚本，就能获取消息通知：

![](https://pythondict-1252734158.file.myqcloud.com/home/www/pythondict/wp-content/uploads/2021/11/2021111310343744.png)

如果你只需要文本通知，那么到这里就已经实现了，如果你还需要发送图文消息或更多自定义内容体，请看下一节内容。

## 3.钉钉机器人支持Markdown

为了支持发送图片消息和自定义的文字格式，我们需要配置更多的参数：

```python
    def send_md(self, title, content):
        """
        发送Markdown文本
        @param title: str, 标题
        @param content: str, 文本内容
        """
        data = {"msgtype": "markdown", "markdown": {"title": title, "text": content}}
        self.params["timestamp"] = self.timestamp
        return requests.post(
            url=self.URL,
            data=json.dumps(data),
            params=self.params,
            headers=self.headers
        )
```

msgtype改为markdown，并配置markdown的参数，包括：

1. title: 标题
2. content: markdown内容

这样，就能支持发送markdown消息了，我们试一下：

```python
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
        self.timestamp = str(round(time.time() \* 1000))
        self.URL = "https://oapi.dingtalk.com/robot/send"
        self.headers = {'Content-Type': 'application/json'}
        secret = secret
        secret_enc = secret.encode('utf-8')
        string_to_sign = '{}\n{}'.format(self.timestamp, secret)
        string_to_sign_enc = string_to_sign.encode('utf-8')
        hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
        self.sign = quote_plus(base64.b64encode(hmac_code))
        self.params = {'access_token': token, "sign": self.sign}

    def send_text(self, content):
        """
        发送文本
        @param content: str, 文本内容
        """
        data = {"msgtype": "text", "text": {"content": content}}
        self.params["timestamp"] = self.timestamp
        return requests.post(
            url=self.URL,
            data=json.dumps(data),
            params=self.params,
            headers=self.headers
        )

    def send_md(self, title, content):
        """
        发送Markdown文本
        @param title: str, 标题
        @param content: str, 文本内容
        """
        data = {"msgtype": "markdown", "markdown": {"title": title, "text": content}}
        self.params["timestamp"] = self.timestamp
        return requests.post(
            url=self.URL,
            data=json.dumps(data),
            params=self.params,
            headers=self.headers
        )

if __name__ == "__main__":
    markdown_text = "\n".join(open("md_test.md", encoding="utf-8").readlines())
    m = Messenger(
        token="你的token",
        secret="你的secret"
    )
    m.send_text("测试一下，今天天气不错")
    m.send_md("测试Markdown", markdown_text)

```
效果如下：

![](https://pythondict-1252734158.file.myqcloud.com/home/www/pythondict/wp-content/uploads/2021/11/2021111310421995.png)

效果还是不错的，速度也非常快，一运行脚本，马上就能收到通知消息。大家可以在Python实用宝典公众号后台回复 **钉钉** 下载本文源代码，也可以在 https://github.com/Ckend/dd_notice 中找到源代码。

欢迎关注Python实用宝典公众号。