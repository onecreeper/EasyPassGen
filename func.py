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


def main():
    domain = input('请输入域名：')
    domain = urlparse(domain).netloc
    passwd = input("输入密码：")
    config = read_config('setting.json')
    text = config.get("salt") + passwd + domain
    passout = get_md5(text)
    print(passout) 



if __name__ == '__main__':
    main()