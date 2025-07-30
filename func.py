import hashlib
from urllib.parse import urlparse
import json

def get_md5(text):
    md5 = hashlib.md5()
    md5.update(text.encode('utf-8'))  # 将字符串编码为字节
    return md5.hexdigest()

# parsed = urlparse(url)
# print(parsed.netloc)

def read_config(name):
    with open(name, 'r') as f:
        res = f.read()
    res = json.loads(res)
    return res

# 格式化处理


def get_main_domain(domain):
    """提取主域名，如从 www.bilibili.com 提取 bilibili.com"""
    parts = domain.split('.')
    if len(parts) > 2:
        return '.'.join(parts[-2:])
    return domain

def ensure_valid_output(s, size):
    """确保结果满足要求：
    1. 全部大写
    2. 前N位至少包含一个字母
    """
    # 先转换为大写
    s = s.upper()
    
    # 检查前N位是否至少有一个字母
    first_n = s[:size]
    if not any(c.isalpha() for c in first_n):
        # 如果没有字母，找到第一个字母并确保它在结果中
        for i, c in enumerate(s):
            if c.isalpha():
                # 将这个字母交换到前N位
                swap_pos = min(size-1, i)
                s = s[:swap_pos] + c + s[swap_pos:i] + s[i+1:]
                break
    return s[:size]

import csv
from datetime import datetime
import pyperclip

def log_to_csv(domain, size, result):
    """记录到CSV文件"""
    with open('password_log.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            domain,
            size,
            result
        ])

def main():
    config = read_config('setting.json')
    salt = config.get("salt", "")
    default_password = config.get("default_password", "")

    while True:
        url = input('请输入域名：')
        domain = urlparse(url).netloc
        if not domain:  # 如果netloc为空，尝试直接使用输入的URL
            domain = url.split('//')[-1].split('/')[0]
        domain = get_main_domain(domain)
        if domain:  # 确保最终domain不为空
            print(f"获取到的域名: {domain}")
            break
        print("无效的域名格式，请重新输入")

    # 使用默认密码或输入密码
    passwd = input(f"输入密码(默认'{default_password}'): ") or default_password
    
    # 拼接盐和域名计算MD5
    text = salt + domain
    md5_hash = get_md5(text)
    
    # 生成4/6/8三种长度的密码
    results = {}
    for size in [4, 6, 8]:
        res = ensure_valid_output(md5_hash, size)
        results[size] = passwd + res
    
    # 输出所有密码
    print("\n生成的密码:")
    for size, pwd in results.items():
        print(f"{size}位: {pwd}")
    
    # 将默认size密码复制到剪贴板
    default_size = config.get("default_size", 4)
    pyperclip.copy(results[default_size])
    print(f"\n已复制{default_size}位密码到剪贴板")
    
    # 记录到日志文件
    for size, result in results.items():
        log_to_csv(domain, size, result)



if __name__ == '__main__':
    main()
    input("按任意键退出...")
