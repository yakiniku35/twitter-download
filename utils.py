"""共用工具函数模块"""
import re
import time
from datetime import datetime
from typing import Tuple


def del_special_char(string: str) -> str:
    """移除特殊字符，只保留中日英文数字和点"""
    return re.sub(r'[^\u4e00-\u9fa5\u0030-\u0039\u0041-\u005a\u0061-\u007a\u3040-\u31FF\.]', '', string)


def stamp2time(msecs_stamp: int) -> str:
    """将毫秒时间戳转换为可读时间格式"""
    time_array = time.localtime(msecs_stamp / 1000)
    return time.strftime("%Y-%m-%d %H-%M", time_array)


def stamp2datetime(msecs_stamp: int) -> str:
    """将毫秒时间戳转换为完整日期时间格式"""
    time_array = time.localtime(msecs_stamp / 1000)
    return time.strftime("%Y-%m-%d %H:%M:%S", time_array)


def time2stamp(timestr: str) -> int:
    """将日期字符串转换为毫秒时间戳"""
    datetime_obj = datetime.strptime(timestr, "%Y-%m-%d")
    return int(time.mktime(datetime_obj.timetuple()) * 1000.0 + datetime_obj.microsecond / 1000.0)


def time_comparison(now: int, start: int, end: int) -> Tuple[bool, bool]:
    """
    比较时间是否在范围内
    
    Args:
        now: 当前时间戳
        start: 开始时间戳
        end: 结束时间戳
    
    Returns:
        (should_download, should_continue): 是否下载，是否继续
    """
    should_download = start <= now <= end
    should_continue = now >= start
    return should_download, should_continue


def quote_url(url: str) -> str:
    """URL编码大括号"""
    return url.replace('{', '%7B').replace('}', '%7D')


def get_highest_video_quality(variants: list) -> str:
    """从视频变体列表中找到最高质量的视频URL"""
    if len(variants) == 1:  # GIF适配
        return variants[0]['url']
    
    max_bitrate = 0
    highest_url = None
    for variant in variants:
        if 'bitrate' in variant:
            bitrate = int(variant['bitrate'])
            if bitrate > max_bitrate:
                max_bitrate = bitrate
                highest_url = variant['url']
    return highest_url


def extract_csrf_token(cookie: str) -> str:
    """从cookie中提取CSRF token"""
    match = re.search(r'ct0=(.*?);', cookie)
    if match:
        return match.group(1)
    raise ValueError("无法从cookie中提取ct0 token")


# API常量
TWITTER_BEARER_TOKEN = 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA'

# 默认时间范围
DEFAULT_START_TIMESTAMP = 655028357000   # 1990-10-04
DEFAULT_END_TIMESTAMP = 2548484357000    # 2050-10-04
