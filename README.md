# Feapder 爬虫代码样品
## 说明
* main_integration.py 是爬虫集成启动模式
* main_schedule.py + launch.sh 是爬虫调度模式需要的文件


## 中文 console 转英文
在启动文件夹里开启以下代码可用把常见中文 console 转成英文输出，log 不会翻译.
```
from loguru import logger
logger.remove()
logger.add(sys.stderr, format=cn2en.formatter)
```