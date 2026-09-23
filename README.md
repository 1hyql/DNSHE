# DNSHE域名续期

最简单的DNSHE域名续期方案，支持自动执行和通知。

## 快速开始

### 1. 配置GitHub Secrets

在GitHub仓库中设置以下Secrets：

```
DNSHE_API_KEY=your_api_key_here
DNSHE_API_SECRET=your_api_secret_here
DNSHE_SUBDOMAIN_IDS=3,5,7
```

### 2. 文件
- `renewal.py` - 主脚本
- `.github/workflows/renewal.yml` - Actions配置
- `.gitignore` - 忽略文件

### 3. 启用自动执行

脚本会每月1号凌晨2点自动运行，也可以手动触发。

## 通知方式

### 1. GitHub Actions通知（默认）
- 在Actions页面显示结果
- 成功/失败状态清晰可见

### 2. Slack通知（可选）
- 配置Webhook后发送失败通知
- 实时提醒

## 配置说明

- `DNSHE_SUBDOMAIN_IDS`: 要续期的子域名ID，用逗号分隔
- 邮件配置已移除，改用更安全的GitHub通知
