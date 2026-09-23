#!/usr/bin/env python3
"""
DNSHE域名续期脚本 - 简化版
"""

import requests
import os
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def send_github_notification(subject, body):
    """使用GitHub Actions输出通知"""
    print(f"::notice::{subject}")
    print(f"::notice::{body}")
    logger.info(f"GitHub通知: {subject}")

def renew_subdomain(subdomain_id):
    """续期子域名"""
    api_key = os.getenv('DNSHE_API_KEY')
    api_secret = os.getenv('DNSHE_API_SECRET')
    
    url = "https://api005.dnshe.com/index.php"
    params = {
        'm': 'domain_hub',
        'endpoint': 'subdomains',
        'action': 'renew'
    }
    
    headers = {
        'X-API-Key': api_key,
        'X-API-Secret': api_secret,
        'Content-Type': 'application/json'
    }
    
    data = {'subdomain_id': subdomain_id}
    
    try:
        response = requests.post(url, params=params, json=data, headers=headers, timeout=30)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logger.error(f"续期失败: {str(e)}")
        raise

def main():
    """主函数"""
    subdomain_ids = [int(x.strip()) for x in os.getenv('DNSHE_SUBDOMAIN_IDS', '').split(',') if x.strip()]
    
    if not subdomain_ids:
        logger.error("未配置子域名ID")
        send_github_notification("DNSHE续期失败", "未配置子域名ID")
        return False
    
    success_count = 0
    failure_count = 0
    results = []
    
    for subdomain_id in subdomain_ids:
        try:
            logger.info(f"正在续期子域名ID: {subdomain_id}")
            result = renew_subdomain(subdomain_id)
            
            if result.get('success'):
                success_count += 1
                results.append(f"✓ 子域名ID {subdomain_id} 续期成功")
                logger.info(f"续期成功: {result.get('message', '无消息')}")
            else:
                failure_count += 1
                results.append(f"✗ 子域名ID {subdomain_id} 续期失败: {result.get('message', '未知错误')}")
                logger.error(f"续期失败: {result.get('message', '未知错误')}")
                
        except Exception as e:
            failure_count += 1
            results.append(f"✗ 子域名ID {subdomain_id} 续期异常: {str(e)}")
            logger.error(f"续期异常: {str(e)}")
    
    # 生成报告
    report = f"""DNSHE域名续期报告
=====================
成功: {success_count} 个
失败: {failure_count} 个
总计: {len(subdomain_ids)} 个

详细结果:
{chr(10).join(results)}
"""
    
    logger.info(f"续期完成: 成功 {success_count} 个, 失败 {failure_count} 个")
    
    # 发送GitHub通知
    if failure_count > 0:
        subject = f"⚠️ DNSHE续期报告 - 有 {failure_count} 个失败"
        send_github_notification(subject, report)
    else:
        subject = f"✅ DNSHE续期报告 - 全部成功 ({success_count} 个)"
        send_github_notification(subject, report)
    
    return failure_count == 0

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)