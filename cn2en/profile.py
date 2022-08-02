level_colors = {
    'DEBUG': 'blue',
    'INFO': 'blink',
    'SUCCESS': 'green',
    'WARNING': 'yellow',
    'ERROR': 'red',
    'CRITICAL': 'reverse',
    None: ''}


def translate_spider_cost(spider_name, cn_time_str):
    """
    翻译字符串 -《abc》爬虫结束，耗时 2小时9分10秒
    Convert Chinese time to English time.
    """
    return f'《{spider_name}》finished, spent {cn_time_str.replace("天", "D").replace("小时", "H").replace("分", "m").replace("秒", "s")}'
