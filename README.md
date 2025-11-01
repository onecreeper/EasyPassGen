# <img src="img/ico.png" alt="EasyPassGen" width="64" height="64"> EasyPassGen - 智能密码生成器


一个基于域名和自定义密码的智能密码生成器，支持特殊字符增强。

## ✨ 特性

- 🔐 **安全密码生成** - 基于MD5哈希和自定义盐值
- 🎯 **多长度支持** - 可配置密码长度数组 `[4, 6, 8, 10, 32]`
- ⚡ **特殊字符增强** - 同时生成基础密码和增强密码
- 📋 **自动复制** - 智能复制到剪贴板
- 📝 **日志记录** - 完整的密码生成历史
- 🎨 **跨平台** - Windows exe + macOS app，带精美图标

## 🚀 快速开始

### Windows用户
1. 下载 windows发布包
2. 解压后双击 `EasyPassGen.exe`
3. 按提示输入域名生成密码

### 开发者
```bash
git clone https://github.com/onecreeper/EasyPassGen.git
cd EasyPassGen
python func.py
```

## 📖 使用示例

```bash
请输入域名：https://github.com
获取到的域名: github.com
输入密码(默认'passwd'):

生成的密码:
4位: passwdF1A2     [增强: passwdF!A2]
6位: passwdF1A2B3   [增强: passwdF@A2B3]
8位: passwdF1A2B3C4 [增强: passwdF#A2B3C4]
10位: passwdF1A2B3C4D5 [增强: passwdF#A2B3C4D5]
32位: passwdF1A2B3C4D5E6F7G8H9I0J1K2L3M4N5O6P7Q8R9S0T1U2V [增强: passwdF#A2B3C4D5E6F7G8H9I0J1K2L3M4N5O6P7Q8R9S0T1U2V]

已复制8位增强密码到剪贴板: passwdF#A2B3C4
```

## ⚙️ 配置选项

编辑 `setting.json` 自定义行为：

```json
{
    "salt": "your_secret_salt",
    "default_password": "passwd",
    "password_lengths": [4, 6, 8, 10, 32],
    "default_copy": {
        "length": 8,
        "with_special_chars": true
    },
    "special_chars": "!@#$%^&*",
    "special_rules": {
        "enabled": true,
        "num_special_chars": 1,
        "position_rule": "hash_based"
    }
}
```

### 配置说明
- **`password_lengths`** - 密码长度数组
- **`default_copy`** - 默认复制设置
- **`special_chars`** - 特殊字符集合
- **`position_rule`** - 插入规则：`hash_based` | `fixed` | `random`

## 🔒 算法说明

```
基础密码 = 用户密码 + 处理后的MD5(salt + 域名)
增强密码 = 基础密码 + 特殊字符（按规则插入）
```

### 推导步骤
1. 获取配置中的salt值
2. 拼接salt和域名
3. 计算MD5哈希
4. 转换为大写并确保包含字母
5. 根据配置插入特殊字符

## 📁 项目结构

```
EasyPassGen/
├── func.py                    # 主程序
├── setting.json              # 配置文件
├── img/                     # 图标资源
├── EasyPassGen_Windows_Final.zip  # Windows发布包
└── README.md                # 说明文档
```


## 🚨 注意事项

- 🔑 请妥善保管salt值，修改后密码将无法匹配
- 🛡️ 建议定期更换salt值增强安全性
- 📋 macOS需要授予剪贴板访问权限
- 🦠 某些杀毒软件可能误报，请添加信任

## 📄 许可证

本项目采用 [MIT License](LICENSE) 开源协议。

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

<div align="center">
  Made with ❤️ by onecreeper
</div>
