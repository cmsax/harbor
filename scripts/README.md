# 微博备份脚本

可以保存这些内容：

- 文本
- 赞、转发、评论
- 日期、来自
- 图片、视频

## 依赖

- [chromedriver](https://sites.google.com/a/chromium.org/chromedriver/getting-started)

## 用法

Powershell:

```powershell
$env:WEIBO_USERNAME = [USERNAME]; $env:PASSWORD = [PASSWORD]; python3 weibo_bot.py
```

Bash:

```bash
WEIBO_USERNAME='[USERNAME]' WEIBO_PASSWORD='[PASSWORD]' python3 weibo_bot.py
```
