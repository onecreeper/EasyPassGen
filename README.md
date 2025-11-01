# EasyPassGen - 智能密码生成器

## 功能说明
- 根据域名和自定义密码生成安全密码
- 同时生成多种长度的密码变体（可配置）
- 支持特殊字符增强密码
- 自动复制默认配置的密码到剪贴板
- 记录密码生成历史到日志文件

## 主要特性

### 1. 特殊字符支持
- 同时生成基础密码和带特殊字符的增强密码
- 支持自定义特殊字符集合
- 可配置特殊字符数量和插入规则（基于哈希/固定位置/随机）

### 2. 灵活的密码长度配置
- 支持自定义密码长度数组，如 `[4, 6, 8, 10, 32]`
- 可以根据需要设置任意长度组合

### 3. 智能复制功能
- 可配置默认复制的密码长度
- 可选择默认复制基础版本或增强版本

## 人工推导密码方法
密码生成算法：
```
基础密码 = 用户密码 + 处理后的MD5(salt + 域名)
增强密码 = 基础密码 + 特殊字符（按规则插入）
```

基础密码推导步骤：
1. 获取配置文件(setting.json)中的salt值
2. 拼接salt和域名（如："saltvalue" + "example.com"）
3. 计算MD5哈希值（32位小写十六进制）
4. 转换为大写
5. 取前N位（根据需要的长度），确保至少包含1个字母
6. 在前面加上用户密码

示例（假设salt="mysalt"，域名="example.com"，用户密码="mypwd"）：
1. 计算MD5("mysaltexample.com") = "1a79a4d60de6718e8e5b326e338ae533"
2. 转换为大写："1A79A4D60DE6718E8E5B326E338AE533"
3. 取前4位并确保包含字母："1A79"
4. 最终4位基础密码："mypwd1A79"

## 配置说明
编辑`setting.json`文件：
```json
{
    "salt": "自定义加密盐值",
    "default_password": "默认密码",
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

### 配置项说明
- **`password_lengths`**: 要生成的密码长度数组
- **`default_copy.length`**: 默认复制的密码长度
- **`default_copy.with_special_chars`**: 是否默认复制带特殊字符的版本
- **`special_chars`**: 可用的特殊字符列表
- **`special_rules.enabled`**: 是否启用特殊字符功能
- **`special_rules.num_special_chars`**: 每个密码中特殊字符的数量
- **`special_rules.position_rule`**: 特殊字符位置规则
  - `hash_based`: 基于域名哈希计算位置（推荐）
  - `fixed`: 固定位置均匀分布
  - `random`: 随机位置

## 使用示例

### 运行程序
```bash
python func.py
```

### 输出示例
```
请输入域名：http://example.com
获取到的域名: example.com
输入密码(默认'passwd'):

生成的密码:
4位: passwdABCD     [增强: passwdA!CD]
6位: passwdABCDEF   [增强: passwdA@CDEF]
8位: passwdABCDEFGH [增强: passwdA#CDEFGH]
10位: passwdABCDEFGHIJ [增强: passwdA#CDEFGHIJ]
32位: passwdABCDEFGHIJKLMNOPQRSTUVWXYZ012345 [增强: passwdA#CDEFGHIJKLMNOPQRSTUVWXYZ012345]

已复制8位增强密码到剪贴板: passwdA#CDEFGH
```

## 日志文件
密码生成记录保存在`password_log.csv`中，包含：
- 生成时间
- 域名
- 密码长度
- 生成的密码
- 版本类型（基础版本/特殊字符版本）

## 注意事项
- 请妥善保管salt值，修改后之前生成的密码将无法匹配
- 建议定期更换salt值增强安全性
- 特殊字符功能可以随时通过配置文件启用或禁用
- 基于哈希的特殊字符位置确保同一域名总是相同的密码模式
