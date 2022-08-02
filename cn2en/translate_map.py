import re

from cn2en import profile

'''Full match string'''
__full_match = [
    {
        'org': '等待任务...',
        'change': 'Waiting for task...',
        'type': 'text'
    },
    {
        'org': '爬虫不自动结束， 等待下一轮任务...',
        'change': 'Spider won\'t end, wait the next round...',
        'type': 'text'
    },
    {
        'org': "暂无可用代理 ...",
        'change': "No available proxy yet...",
        'type': 'text'
    },
    {
        'org': "无任务，爬虫结束",
        'change': "No task, spider end",
        'type': 'text'
    },
    {
        'org': "parser 等待任务...",
        'change': "parser Waiting for task...",
        'type': 'text'
    },
    {
        'org': "暂无可用代理 ...",
        'change': "No available proxy yet...",
        'type': 'text'
    },
]

'''Regex match string'''
__regex_match = [
    # /core/parser_control.py
    {
        'org': re.compile(r"""
( +)入库 等待重试
\1url +(.+?)
\1重试次数 (\d+)?
\1最大允许重试次数 (\d+)"""),
        'change': r"""
\1ImportDB Waiting retry
\1url     \2
\1Retry times \3
\1Maximum retry \4""",
        'type': 'regex'
    },
    # /buffer/item_buffer.py
    {
        'org': re.compile(r"""
                -------------- item 批量入库 --------------
                表名: (.+)
                datas: ([\s\S]+)
                    """),
        'change': r"""
                -------------- item bulk DB save --------------
                table: \1
                datas: \2
                    """,
        'type': 'regex'
    },
    {
        'org': re.compile(r"""
                -------------- item 批量更新 --------------
                表名: (.+)
                datas: ([\s\S]+)
                    """),
        'change': r"""
                -------------- item bulk update --------------
                table: \1
                datas: \2
                    """,
        'type': 'regex'
    },
    # /core/scheduler.py
    {
        'org': re.compile(r"检查到有待做任务 (\d+) 条，不重下发新任务，将接着上回异常终止处继续抓取"),
        'change': r"There has \1 task already, no new task will be issued, continue to crawl from the last exception",
        'type': 'regex'
    },
    {
        'org': re.compile(r'共导出 (\d+) 条数据 到 (\w+), 重复 (\d+) 条'),
        'change': r'Total export \1 rows to \2, repeat \3 rows',
        'type': 'regex'
    },
    {
        'org': re.compile(r'代理池重置的太快了:\) (\d+)'),
        'change': r'Proxy pool reset too fast:) \1',
        'type': 'regex'
    },
    {
        'org': re.compile(r"request已存在  url = (\S+)"),
        'change': r"request already exists url = \1",
        'type': 'regex'
    },
    {
        'org': re.compile(r"正在删除key (\w+)"),
        'change': r'Deleting key \1',
        'type': 'regex'
    },
    {
        'org': re.compile(r"《(\w+)》爬虫结束，耗时 (\w+)"),
        'change': lambda x: profile.translate_spider_cost(x.group(1), x.group(2)),
        'type': 'recall'
    },
    {
        'org': re.compile(r"重置代理池成功: 获取(\d+), 成功添加(\d+), 失效(\d+),  当前代理数(\d+),"),
        'change': r'Reset ProxyPool succeed: fetched \1, success add \2, invalid \3,  now proxy amount \4,',
        'type': 'regex'
    },
    {
        'org': re.compile(r"重置丢失任务完毕，共(\d+)条"),
        'change': r'Reset lost task completed, total \1 rows',
        'type': 'regex'
    },
]

"""Combine full match and regex match"""
maps = __full_match + __regex_match
