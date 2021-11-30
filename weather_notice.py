import datetime
from notice import Messenger
m = Messenger(
    token="你的token",
    secret="你的secret"
)
m.send_md(f"天气预报-{datetime.datetime.today()}", "![weather](https://v2d.wttr.in/Shenzhen.png)")
