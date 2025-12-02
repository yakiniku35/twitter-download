# 快速开始指南

## ⚡ 优化后使用指南

### 1️⃣ 首次使用 - 配置设置

```bash
# 步骤1: 复制配置模板
cp settings.json.template settings.json

# 步骤2: 编辑settings.json，填入你的凭证
# 需要修改的字段:
# - cookie: 你的Twitter cookie (auth_token 和 ct0)
# - user_lst: 要下载的用户名列表
```

### 2️⃣ 运行程序

```bash
# 标准用户下载
python3 main.py

# 按标签下载
python3 tag_down.py

# 纯文本下载
python3 text_down.py
```

### 3️⃣ 检查下载结果

```bash
# 下载的文件在 twitter/ 文件夹下
ls -la twitter/

# 每个用户有独立的文件夹
# 例如: twitter/username/
```

---

## 🔧 主要修复说明

### ✅ 已修复的关键Bug

#### 1. 下载重试死循环 (Critical)
**问题**: 某些情况下程序会无限重试，导致挂起
**修复**: 
- 添加最大重试次数限制 (10次)
- 修复图片格式降级逻辑
- 修复位置: `main.py` 和 `main2.py`

#### 2. 凭证安全问题 (High)
**问题**: settings.json 包含敏感凭证可能被提交到git
**修复**:
- 添加到 .gitignore
- 创建 settings.json.template 模板
- 提醒用户保护凭证

---

## 📁 新增文件说明

| 文件 | 用途 | 是否必需 |
|------|------|---------|
| `utils.py` | 共用工具函数 | 可选(未来使用) |
| `config.py` | 配置管理类 | 可选(未来使用) |
| `api_client.py` | API客户端封装 | 可选(未来使用) |
| `settings.json.template` | 配置模板 | 推荐使用 |
| `CODE_REVIEW.md` | 代码审查报告 | 文档 |
| `OPTIMIZATION_SUMMARY.md` | 优化总结 | 文档 |

**注意**: 新的 .py 模块是为未来重构准备的，当前 main.py 仍使用原有代码，但已修复关键bug。

---

## 🚨 重要提醒

### 保护你的凭证
```bash
# ❌ 不要这样做
git add settings.json
git commit -m "add config"

# ✅ 应该这样
# settings.json 已在 .gitignore 中，不会被提交
git status  # 应该看不到 settings.json

# 如果看到了，立即移除
git rm --cached settings.json
```

### 检查修复是否生效
```bash
# 测试1: 检查语法
python3 -m py_compile main.py main2.py

# 测试2: 运行小批量测试
# 修改 settings.json 只包含1-2个用户
# 然后运行
python3 main.py
```

---

## 📊 性能建议

### 并发设置 (main.py 第16行)
```python
max_concurrent_requests = 8  # 默认值

# 网络好: 可以提高到 15-20
# 网络不稳定: 降低到 3-5
# 频繁失败: 降低到 1-2
```

### 下载模式选择
```json
{
    "has_retweet": false,     // 不包含转推 (推荐，节省API调用)
    "has_video": true,        // 下载视频
    "async_down": true,       // 异步下载 (推荐)
    "down_log": true,         // 避免重复下载 (推荐)
    "autoSync": false         // 自动同步新内容 (谨慎使用)
}
```

---

## ❓ 常见问题

### Q1: "API次数已超限" 错误
**原因**: Twitter API 每日调用次数限制
**解决**: 
- 等待24小时后重试
- 关闭 `has_retweet` 减少API调用
- 使用 `down_log` 避免重复下载

### Q2: 下载失败率很高
**原因**: 网络不稳定或并发过高
**解决**:
- 降低 `max_concurrent_requests` (第16行)
- 检查代理设置
- 检查网络连接

### Q3: 重复下载同样的内容
**原因**: 未启用缓存
**解决**:
```json
{
    "down_log": true  // 启用缓存
}
```

### Q4: 想要重新下载所有内容
**解决**:
```bash
# 删除缓存文件
rm twitter/username/cache_data.log

# 或者关闭缓存
{
    "down_log": false
}
```

---

## 🔄 从旧版本迁移

如果你之前使用过此工具:

```bash
# 1. 备份你的配置
cp settings.json settings.json.backup

# 2. 拉取最新代码
git pull

# 3. 确认.gitignore生效
git status

# 4. 测试运行
python3 main.py
```

---

## 📞 需要帮助?

1. 查看 `CODE_REVIEW.md` - 详细的代码分析
2. 查看 `OPTIMIZATION_SUMMARY.md` - 优化总结
3. 查看原 `README.md` - 原项目说明

---

## ✨ 下一步

推荐阅读:
- `CODE_REVIEW.md` - 了解代码质量和潜在问题
- `OPTIMIZATION_SUMMARY.md` - 了解具体修复了什么

现在可以安全使用程序了! 🎉
