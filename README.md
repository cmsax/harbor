# Harbor

微博个人账户备份，可以保存这些内容：

- 文本
- 赞、转发、评论
- 日期、来自
- 图片、视频

## 简单使用

直接运行 `scripts` 文件夹下的脚本。

Powershell:

```powershell
$env:WEIBO_USERNAME = [USERNAME]; $env:PASSWORD = [PASSWORD]; python3 weibo_bot.py
```

Bash:

```bash
WEIBO_USERNAME='[USERNAME]' WEIBO_PASSWORD='[PASSWORD]' python3 weibo_bot.py
```

## 进阶使用

通过 pip 安装：`pip install weibo-harbor`

### 依赖

- Python 3.7 and up
- [chromedriver](https://sites.google.com/a/chromium.org/chromedriver/getting-started)

### 安装

使用 python setup-tools 安装和运行.

```
$ python3 -m venv env
$ python3 -m pip install -r requirements.txt
$ python3 setup.py install
$ env/bin/harbor
```

### 运行

Powershell:

```powershell
$env:WEIBO_USERNAME = [USERNAME]; $env:PASSWORD = [PASSWORD]; harbor
```

Bash:

```bash
WEIBO_USERNAME='[USERNAME]' WEIBO_PASSWORD='[PASSWORD]' harbor
```

## 开发

```bash
python3 -m venv env
. env/bin/activate
pip install -e .
```

## 测试

```bash
python3 setup.py nosetests
```

更新了 `setup.py` 中的依赖后，请运行 `pip-compile` 来刷新 `requirements.txt` 文件.

## 欢迎贡献代码

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
