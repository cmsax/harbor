# Script to backup weibo

A project for backuping own weibo content, including:

- fulltext
- reposts
- comments
- likes
- meta info
- original images
- videos

## Requirements

- [chromedriver](https://sites.google.com/a/chromium.org/chromedriver/getting-started) should be installed

## Usage

Powershell:

```powershell
$env:WEIBO_USERNAME = [USERNAME]; $env:PASSWORD = [PASSWORD]; python3 weibo_bot.py
```

Bash:

```bash
WEIBO_USERNAME='[USERNAME]' WEIBO_PASSWORD='[PASSWORD]' python3 weibo_bot.py
```
