import re

def extract_all_numbers(s):
    """
    从字符串中提取所有连续的数字。

    参数:
    s -- 输入字符串

    返回:
    一个包含所有连续数字的列表。
    """
    return re.findall(r'\d+', s)