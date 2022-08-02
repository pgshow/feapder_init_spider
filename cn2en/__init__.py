# -*- coding: utf-8 -*-
"""
Translate Chinese logs to English.
"""
import re
import sys

from loguru import logger
from cn2en import translate_map
from cn2en import profile


def get_match_rule(message: str):
    """Get which rule match this message"""
    for pair in translate_map.maps:
        if pair['type'] == 'text':
            # 普通文本，完全匹配
            if pair['org'] == message:
                return pair
        elif pair['type'] == 'regex':
            # 正则表达式
            if re.match(pair['org'], message):
                return pair
        elif pair['type'] == 'recall':
            # 回调函数替换
            if re.match(pair['org'], message):
                return pair


def _replace_message(message: str):
    """Obfuscate sensitive information."""
    match_rule = get_match_rule(message)

    if not match_rule:
        return message

    if match_rule['type'] == 'text':
        # 完全替换
        return match_rule['change']
    elif match_rule['type'] == 'regex':
        # 正则表达式替换
        return re.sub(match_rule['org'], match_rule['change'], message)
    elif match_rule['type'] == 'recall':
        # 回调函数替换
        return re.sub(match_rule['org'], match_rule['change'], message)


def _replace_color(format_string, record):
    """Replace <color> to color name"""
    color = profile.level_colors[record["level"].name]
    finial_string = format_string.replace('<color>', f'<{color}>')
    finial_string = finial_string.replace('</color>', f'</{color}>')
    return finial_string


def formatter(record):
    record["message"] = _replace_message(record["message"])
    msg = '<g>{time:MM-DD HH:mm:ss}</g> | <color>{level: <8}</color> | <c>{name}</c>:<c>{function}</c>:<c>{line}</c> - <color>{message}</color>\n{exception}'
    final_msg = _replace_color(msg, record)
    return final_msg


if __name__ == '__main__':
    import json
    url = 'http://asdfasdf asdfasd.com/89?67=f&jf=asdf asdf'
    logger.remove()
    logger.add(sys.stderr, format=formatter)

    spider_name = 'abc'
    spand_time = '2小时9分10秒'

    logger.debug("《%s》爬虫结束，耗时 %s" % (spider_name, spand_time))