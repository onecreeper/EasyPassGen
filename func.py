import hashlib
from urllib.parse import urlparse
import json
import csv
from datetime import datetime
import pyperclip
import random

def get_md5(text):
    md5 = hashlib.md5()
    md5.update(text.encode('utf-8'))  # 将字符串编码为字节
    return md5.hexdigest()

def read_config(name):
    with open(name, 'r') as f:
        res = f.read()
    res = json.loads(res)
    return res

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

def add_special_chars(password, special_chars, num_special_chars, position_rule, domain=""):
    """为密码添加特殊字符"""
    if not special_chars or num_special_chars <= 0:
        return password
    
    # 选择要插入的特殊字符
    selected_chars = random.choices(special_chars, k=num_special_chars)
    
    if position_rule == "hash_based":
        # 基于域名哈希计算位置
        hash_obj = get_md5(domain + "special")
        positions = []
        for i in range(num_special_chars):
            # 使用哈希的不同部分计算位置
            pos = int(hash_obj[i*4:(i+1)*4], 16) % len(password)
            positions.append(pos)
    elif position_rule == "fixed":
        # 固定位置：均匀分布
        step = len(password) // (num_special_chars + 1)
        positions = [step * (i + 1) for i in range(num_special_chars)]
    else:  # random
        # 随机位置
        positions = random.sample(range(len(password)), num_special_chars)
    
    # 按位置排序，确保从后往前插入（避免位置偏移）
    positions.sort(reverse=True)
    
    # 插入特殊字符
    password_list = list(password)
    for i, pos in enumerate(positions):
        password_list.insert(pos, selected_chars[i])
    
    return ''.join(password_list)

def log_to_csv(domain, size, result, is_special=False):
    """记录到CSV文件"""
    with open('password_log.csv', 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            domain,
            size,
            result,
            "特殊字符版本" if is_special else "基础版本"
        ])

def main():
    try:
        config = read_config('setting.json')
    except FileNotFoundError:
        print("配置文件 setting.json 不存在，请参考 setting.json.example 创建配置文件")
        return
    
    salt = config.get("salt", "")
    default_password = config.get("default_password", "")
    password_lengths = config.get("password_lengths", [4, 6, 8])
    default_copy = config.get("default_copy", {"length": 8, "with_special_chars": True})
    special_chars = config.get("special_chars", "!@#$%^&*")
    special_rules = config.get("special_rules", {"enabled": True, "num_special_chars": 1, "position_rule": "hash_based"})

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
    
    # 生成指定长度的密码（基础版本和特殊字符版本）
    results = {}
    special_results = {}
    
    for size in password_lengths:
        # 生成基础密码
        res = ensure_valid_output(md5_hash, size)
        base_password = passwd + res
        results[size] = base_password
        
        # 生成带特殊字符的密码
        if special_rules.get("enabled", True) and special_chars:
            special_password = add_special_chars(
                base_password,
                special_chars,
                special_rules.get("num_special_chars", 1),
                special_rules.get("position_rule", "hash_based"),
                domain
            )
            special_results[size] = special_password
    
    # 输出所有密码
    print("\n生成的密码:")
    for size in password_lengths:
        base_pwd = results[size]
        if size in special_results:
            special_pwd = special_results[size]
            print(f"{size}位: {base_pwd:<15} [增强: {special_pwd}]")
        else:
            print(f"{size}位: {base_pwd}")
    
    # 复制默认配置的密码到剪贴板
    copy_length = default_copy.get("length", 8)
    copy_special = default_copy.get("with_special_chars", True)
    
    if copy_length in password_lengths:
        if copy_special and copy_length in special_results:
            password_to_copy = special_results[copy_length]
            print(f"\n已复制{copy_length}位增强密码到剪贴板: {password_to_copy}")
        else:
            password_to_copy = results[copy_length]
            print(f"\n已复制{copy_length}位基础密码到剪贴板: {password_to_copy}")
        
        pyperclip.copy(password_to_copy)
    else:
        print(f"\n错误：配置的默认复制长度 {copy_length} 不在密码长度列表中")
    
    # 记录到日志文件
    for size, result in results.items():
        log_to_csv(domain, size, result, False)
    
    for size, result in special_results.items():
        log_to_csv(domain, size, result, True)

if __name__ == '__main__':
    main()
    input("按任意键退出...")
